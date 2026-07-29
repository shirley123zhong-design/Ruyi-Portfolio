### Data Science exam
### pip install -r requirements.txt
  #pandas
  #numpy
  #matplotlib
  #seaborn
  #scikit-learn
  #scipy
  #dmba
### use pip list to verify, which packages we have installed
#%%
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.model_selection import train_test_split, KFold, cross_val_predict, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, LogisticRegression, LogisticRegressionCV
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error, mean_squared_error, silhouette_score, classification_report, confusion_matrix
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.impute import KNNImputer
from dmba import plotDecisionTree, classificationSummary


# load in the dataset 
# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent

# Build path to data/exam.csv
data_path = BASE_DIR / "data" / "exam.csv"

# Load the dataset
df = pd.read_csv(data_path)

df 
# to check if data is loaded correctly
pd.set_option('display.max_columns', None)  # to display all columns
df.columns

# Display the dataset in a table with rows and columns
print(df.head(10))
print(f"\nDataset shape: {df.shape[0]} rows, {df.shape[1]} columns")


#%%
# --------------------------------------------------------
# Checking the data
# --------------------------------------------------------

def check_data(df: pd.DataFrame) -> None:
    """
    Check dataset quality:
    - Missing values
    - Duplicated rows
    - Duplicated dates (if exists)
    - Negative numeric values
    """


    print("=== DATA QUALITY REPORT ===\n")


    # Missing values
    print("Missing values per column:")
    print(df.isnull().sum())
    print("\nTotal missing values:", df.isnull().sum().sum())


    # Duplicate rows
    print("\nDuplicated rows:", df.duplicated().sum())


    # Negative numeric values check
    numeric_cols = [
        col for col in df.columns
        if df[col].dtype.kind in "iufc"  # int, uint, float, complex
    ]


    if numeric_cols:
        neg_counts = {col: (df[col] < 0).sum()
                      for col in numeric_cols if col in df.columns}


        print("\nNegative values per numeric column:")
        print(neg_counts)


    print("\n=== END OF REPORT ===")

check_data(df)
# to call the function on our dataset
df.describe() # to get summary statistics for numeric columns
df.dtypes # to check data types of each column

#outliers check
df.hist(bins=60, figsize=(30,20))

# -------------------------------------------------------
# Cleaning the data
# -------------------------------------------------------

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare dataset WITHOUT removing or imputing:
    - Standardize column names (lowercase, underscore)
    - Convert numeric columns to numeric types
    - Enforce non-negative numeric values (but do not drop)
    """
    df = df.copy()


    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^0-9a-zA-Z]+", "_", regex=True)
    )


    # Convert numeric-like columns
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                # leave column unchanged if conversion fails
                pass


    return df
df_cleaned = clean_data(df)

# Missing data - avg_order_value
# 285 missing, we simply use median imputation
median_avg = df_cleaned["avg_order_value"].median()
df_cleaned["avg_order_value"].fillna(median_avg, inplace=True)
missing_after = df_cleaned["avg_order_value"].isna().sum()
print("Missing AFTER imputation:", missing_after)

zero_total_rows = (df_cleaned['total_spent'] == 0) & (df_cleaned['total_orders'] == 0)
condition_impossible = (
    (df_cleaned['avg_order_value'] > 0) |
    (df_cleaned['median_order_value'] > 0) |
    (df_cleaned['max_order_value'] > 0) |
    (df_cleaned['discount_rate_mean'] > 0) |
    (df_cleaned['pct_orders_discounted'] > 0)
)
corrupted_rows = df_cleaned[zero_total_rows & condition_impossible]
print("Number of corrupted rows:", corrupted_rows.shape[0])
### there are 2352 rows with total_orders = 0 and total_orders =0 while average_order_value and such are not 0
### one third of data invalid and they have high correlation with other data columns
### we try to impute missing data
# first to convert 0 to NaN
df_cleaned.loc[zero_total_rows, ['total_spent', 'total_orders']] = np.nan
### simple math imputation will not work as we missing both values(total_spent = total_orders * avg_order_value)
### so mean-impute, median-impute also did not make sense
### introduce ML to predcit the missing values
### Supervised Continuous Regression （random forest regression）
# - Takes other known features
# - Learns the mapping to total_spent
# - Predicts total_spent for missing rows
# - calculate total_orders by total_orders_pred = total_spent_pred / avg_order_value

# Rows with correct values (for training)
mask_train = df_cleaned["total_spent"].notna() & df_cleaned["total_orders"].notna()
# Rows with missing/corrupted values
mask_predict = df_cleaned["total_spent"].isna() & df_cleaned["total_orders"].isna()
#features that still exist even when total_spent is missing.
features = [
    "avg_order_value",
    "median_order_value",
    "max_order_value",
    "discount_rate_mean",
    "pct_orders_discounted",
    "orders_last_1m",
    "orders_last_3m",
    "loyalty_points",
    "loyalty_tier_encoded",
    "recency_days",
    "website_sessions_3m",
    "app_sessions_3m"
]
#Train Random Forest Regression
X_all = df_cleaned.loc[mask_train, features]
y_all = df_cleaned.loc[mask_train, "total_spent"]

#80%training data 20%test data
# cross-validation
X_train, X_test, y_train, y_test = train_test_split(
    X_all, y_all, test_size=0.2, random_state=42
)
print(f"Train size: {X_train.shape[0]}")
print(f"Test size : {X_test.shape[0]}")
# Random forest wtih Out-of-bag error
rf_oob = RandomForestRegressor(
    n_estimators=300,
    oob_score=True,
    bootstrap=True,
    random_state=42,
    n_jobs=-1
)

rf_oob.fit(X_train, y_train)

oob_r2 = rf_oob.oob_score_
y_test_pred_oob = rf_oob.predict(X_test)

test_r2_oob = r2_score(y_test, y_test_pred_oob)
test_mae_oob = mean_absolute_error(y_test, y_test_pred_oob)
test_rmse_oob = np.sqrt(mean_squared_error(y_test, y_test_pred_oob))

# cross-validation appoach
rf_cv = RandomForestRegressor(
    n_estimators=300,
    oob_score=False,
    bootstrap=True,
    random_state=42,
    n_jobs=-1
)

cv = KFold(n_splits=5, shuffle=True, random_state=42)

y_train_pred_cv = cross_val_predict(
    rf_cv, X_train, y_train, cv=cv, n_jobs=-1
)

cv_r2 = r2_score(y_train, y_train_pred_cv)
cv_mae = mean_absolute_error(y_train, y_train_pred_cv)
cv_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred_cv))

rf_cv.fit(X_train, y_train)
y_test_pred_cv = rf_cv.predict(X_test)

test_r2_cv = r2_score(y_test, y_test_pred_cv)
test_mae_cv = mean_absolute_error(y_test, y_test_pred_cv)
test_rmse_cv = np.sqrt(mean_squared_error(y_test, y_test_pred_cv))

# evaluation comparasion to choose one appoarch (cross validation or OOB)
# Interpretation:R² > 0.8 → very good; R² > 0.9 → excellent; R² > 0.95 → outstanding

print("\n=== Comparison Summary (TEST set) ===")
print(f"OOB -> R²={test_r2_oob:.4f}, MAE={test_mae_oob:.2f}, RMSE={test_rmse_oob:.2f}")
print(f"CV  -> R²={test_r2_cv:.4f}, MAE={test_mae_cv:.2f}, RMSE={test_rmse_cv:.2f}")

best_approach = "OOB" if test_r2_oob >= test_r2_cv else "CV"
print(f"Chosen approach for imputation: {best_approach}")

final_model = RandomForestRegressor(
    n_estimators=300,
    oob_score=(best_approach == "OOB"),
    bootstrap=True,
    random_state=42,
    n_jobs=-1
)
final_model.fit(X_all, y_all)

if best_approach == "OOB":
    print(f"Final model OOB R² (all non-missing): {final_model.oob_score_:.4f}")

# Predict the missing total_spend
# Compute total_orders from predicted total_spent
X_missing = df_cleaned.loc[mask_predict, features]
rf_spent_pred = final_model.predict(X_missing)

avg = df_cleaned.loc[mask_predict, "avg_order_value"].replace(0, np.nan)
rf_orders_pred = (
    (rf_spent_pred / avg)
    .round()
    .fillna(1)
    .astype(int)
    .clip(lower=1)
)
# create new column with new values
df_cleaned["RF_total_spent"] = df_cleaned["total_spent"]
df_cleaned["RF_total_orders"] = df_cleaned["total_orders"]
df_cleaned.loc[mask_predict, "RF_total_spent"] = rf_spent_pred
df_cleaned.loc[mask_predict, "RF_total_orders"] = rf_orders_pred

print("\nTotal rows imputed (RF):", mask_predict.sum())

# check result
df_compare = df_cleaned.loc[mask_predict, [
    "customer_id",
    "total_spent",
    "RF_total_spent",
    "total_orders",
    "RF_total_orders",
    "avg_order_value",
    "median_order_value",
    "max_order_value"
]]

df_compare.head(20)
print("Before Imputation (zeros only):")
print(df_cleaned.loc[mask_predict, ["total_spent", "total_orders"]].describe())

print("\nAfter Imputation (clean values):")
print(df_cleaned["RF_total_spent"].describe())
print(df_cleaned["RF_total_orders"].describe())

# count rows were imputed
print("Total rows fixed:", mask_predict.sum())
# visual inspection
plt.figure(figsize=(10,5))
df_cleaned["total_spent"].hist(alpha=0.5, label="Original", bins=50)
df_cleaned["RF_total_spent"].hist(alpha=0.5, label="Cleaned", bins=50)
plt.legend()
plt.title("Total Spent: Before vs After Imputation")
plt.show()

#Random forest gives a more prediction values instead of realistic historical values
# therefore, KNN was used to impute data
# --- KNN IMPUTATION FOR CLEAN ANALYSIS COLUMNS ---
# Choose predictors for KNN distance (no leakage like future_3m_spend)
knn_cols = features + ["total_spent", "total_orders"]
df_knn = df_cleaned[knn_cols].copy()

# Scale before KNN
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_knn)

# KNN impute on scaled matrix
knn = KNNImputer(n_neighbors=5, weights="distance")
X_imputed = knn.fit_transform(X_scaled)
# Unscale back to original units
X_imputed = scaler.inverse_transform(X_imputed)

df_knn_imp = pd.DataFrame(X_imputed, columns=knn_cols, index=df_cleaned.index)

# Create clean columns:
df_cleaned["total_spent_clean"] = df_cleaned["total_spent"]
df_cleaned["total_orders_clean"] = df_cleaned["total_orders"]

# Fill only missing rows (corrupted rows)
df_cleaned.loc[mask_predict, "total_orders_clean"] = (
    df_knn_imp.loc[mask_predict, "total_orders"]
    .round()
    .clip(lower=1)
    .astype(int)
)
# fill in total spend
df_cleaned.loc[mask_predict, "total_spent_clean"] = (
    df_cleaned.loc[mask_predict, "total_orders_clean"] *
    df_cleaned.loc[mask_predict, "avg_order_value"]
        .replace(0, median_avg)
        .fillna(median_avg)
).clip(lower=0)

# visualize KNN
plt.figure(figsize=(10,5))

df_cleaned.loc[mask_train, "total_spent"].hist(
    bins=50, alpha=0.5, density=True, label="Observed"
)

df_cleaned.loc[mask_predict, "total_spent_clean"].hist(
    bins=50, alpha=0.5, density=True, label="KNN Imputed"
)

plt.legend()
plt.title("Observed vs KNN-Imputed Total Spent (Density)")
plt.show()

print("=== RF totals (imputed rows only) ===")
print(df_cleaned.loc[mask_predict, ["RF_total_spent", "RF_total_orders"]].describe())

print("\n=== KNN clean totals (imputed rows only) ===")
print(df_cleaned.loc[mask_predict, ["total_spent_clean", "total_orders_clean"]].describe())

print("\n=== Observed totals (train rows only) ===")
print(df_cleaned.loc[mask_train, ["total_spent", "total_orders"]].describe())


# missing data in satisfaction score
median_satisfaction = df_cleaned['satisfaction_score'].median()
df_cleaned['satisfaction_score'].fillna(median_satisfaction, inplace=True)
df_cleaned['satisfaction_score'].describe()

# for missing data - interactions(email_open_rate, email_click_rate)
#first, lets convert those 2 columns to object dtype
df_cleaned['email_open_rate'] = df_cleaned['email_open_rate'].astype('object')
df_cleaned['email_click_rate'] = df_cleaned['email_click_rate'].astype('object')
# we want to fill some missing data in interactions via email with new value NR 
mask_nr = (
    df_cleaned["email_open_rate"].isnull() &
    df_cleaned["email_click_rate"].isnull() &
    (df_cleaned["email_opt_in"] == 0)
)

df_cleaned.loc[mask_nr, ["email_open_rate", "email_click_rate"]] = "NR"

# Make numeric versions for modeling (keep original 'NR' columns for reporting/PCA text logic)
df_cleaned["email_open_rate_num"] = pd.to_numeric(df_cleaned["email_open_rate"], errors="coerce")
df_cleaned["email_click_rate_num"] = pd.to_numeric(df_cleaned["email_click_rate"], errors="coerce")

# If 'NR' means "not relevant because opted out", treat as 0 engagement:
mask_optout = (df_cleaned["email_opt_in"] == 0)
df_cleaned.loc[mask_optout, ["email_open_rate_num", "email_click_rate_num"]] = 0.0

# For any remaining missing values (e.g., opted-in but missing), impute safely:
df_cleaned["email_open_rate_num"] = df_cleaned["email_open_rate_num"].fillna(df_cleaned["email_open_rate_num"].median())
df_cleaned["email_click_rate_num"] = df_cleaned["email_click_rate_num"].fillna(df_cleaned["email_click_rate_num"].median())

# customers with zero orders should have returns_rate = 0
df_cleaned["returns_rate"] = pd.to_numeric(df_cleaned["returns_rate"], errors="coerce")

df_cleaned["returns_rate"] = np.where(
    df_cleaned["total_orders"] == 0,
    0.0,
    df_cleaned["returns_rate"]
)
# if any NaNs remain (e.g., weird missingness), set to 0 as a conservative default
df_cleaned["returns_rate"] = df_cleaned["returns_rate"].fillna(0.0)

df_cleaned.isnull().sum()  # to check missing values after cleaning
df_cleaned.dtypes  # to check data types after cleaning
df_cleaned.describe()  # to get summary statistics after cleaning

df_cleaned['future_3m_spend'].describe()  
# to deal with outliers we gonna replace them with 75% tile value
# and for that we need another mask
mask = df_cleaned['future_3m_spend']> 46.267500
df_cleaned.loc[mask, 'future_3m_spend'] = 46.267500
df_cleaned['future_3m_spend'].describe()
print(df_cleaned['future_3m_spend'].head(30))
# now we fill in the missing values with new mean value of the column
mask = ((df_cleaned['future_3m_spend'].isnull()))
df_cleaned.loc[mask, 'future_3m_spend'] =  17.634899
df_cleaned['future_3m_spend'].describe()
print(df_cleaned['future_3m_spend'].head(30))

#%%
### PART 3: correlation heatmap - not including 

# 1. Compute correlation matrix for numeric columns only
corr_df = df_cleaned.select_dtypes(include=[np.number]).corr()

# 2. Plot heatmap
plt.figure(figsize=(14, 12))
sns.heatmap(
    corr_df,
    cmap="coolwarm",
    center=0,
    square=True,
    linewidths=0.5
)

plt.title("Correlation Heatmap", fontsize=16)
plt.tight_layout()
plt.show()

# 3.drop variables for PCA
# 3.1 drop duplicated function variables
# PCA can handle correlation, but when variables are near-duplicates, they dominate PCs and reduce interpretability.
# 3.2 drop Predictive / model outputs, Raw corrupted totals, Future information (leakage)
# 3.3 drop categorical and boomlean variables
# PCA is designed for continuous numeric variables, not categorical or boolean variables.
# so we also drop categorical and boomlean variables
cols_to_drop = [
    # identifiers / non-numeric
    "customer_id",
    "region",
    "gender",

    # loyalty redundancy
    "loyalty_tier_encoded",

    # spend & order duplicates
    "total_spent",
    "total_orders",
    "total_spent_clean",
    "total_orders_clean",
    "RF_total_spent",
    "RF_total_orders",

    # order value redundancy
    "median_order_value",
    "max_order_value",

    # time redundancy
    "days_since_first_order",

    # frequency redundancy
    "orders_last_1m",

    # returns redundancy
    "returns_count",

    # category redundancy
    "category_diversity",

    # targets (no leakage into PCA)
    "future_3m_spend",
    "churn_90d"
]

df_pca_ready = df_cleaned.drop(columns=cols_to_drop, errors="ignore")

### PCA analysis

def run_pca(df, cols, pca_name):

    # 1. Select & clean
    X = df[cols].copy()
    X = X.replace(["NR", "NA", "N/A", "", " "], np.nan)
    X = X.apply(pd.to_numeric, errors="coerce")
    X = X.fillna(X.median())

    # 2. Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3. PCA
    pca = PCA()
    X_pca = pca.fit_transform(X_scaled)

    # 4. Explained variance
    explained = pd.DataFrame({
        "PC": [f"PC{i}" for i in range(1, len(pca.explained_variance_)+1)],
        "Eigenvalue": pca.explained_variance_,
        "Variance_Ratio": pca.explained_variance_ratio_,
        "Cumulative": np.cumsum(pca.explained_variance_ratio_)
    })

    print(f"\n=== {pca_name} – Explained Variance ===")
    print(explained)

    # 5. Scree / cumulative plot
    plt.figure(figsize=(8,4))
    plt.plot(explained["PC"], explained["Cumulative"], marker="o")
    plt.axhline(0.8, linestyle="--", color="gray", label="80% variance")
    plt.title(f"{pca_name} – Cumulative Explained Variance")
    plt.xlabel("Principal Component")
    plt.ylabel("Cumulative Variance Explained")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 6. Loadings
    loadings = pd.DataFrame(
        pca.components_.T,
        index=cols,
        columns=explained["PC"]
    )

    print(f"\nTop contributors to {pca_name} PC1:")
    print(loadings["PC1"].sort_values(key=abs, ascending=False))

    print(f"\nTop contributors to {pca_name} PC2:")
    print(loadings["PC2"].sort_values(key=abs, ascending=False))

    return X_pca, explained, loadings

#################################################################
# PCA#0 – ALL VARIABLES PCA (drop NR rows + auto-cap components)
df_subset = df_pca_ready.copy()
# Drop rows where email rates are 'NR'
df_subset_noNR = df_subset[
    (df_subset["email_open_rate"] != "NR") &
    (df_subset["email_click_rate"] != "NR")
].copy()

# Keep only numeric columns for "all variables PCA"
# (this avoids IDs / region / gender etc. if any still exist)
X_all = df_subset_noNR.select_dtypes(include=[np.number]).copy()

# handle missing values (match your run_pca logic)
X_all = X_all.fillna(X_all.median())

# Standardize
scaler_all = StandardScaler()
X_all_scaled = scaler_all.fit_transform(X_all)

# Auto-cap n_components
max_possible = min(X_all_scaled.shape[0], X_all_scaled.shape[1])
n_comp = min(18, max_possible)   # keeps your "18" target but won't crash if smaller

pcs_all = PCA(n_components=n_comp)
X_all_pca = pcs_all.fit_transform(X_all_scaled)

pcsAllSummary_df = pd.DataFrame({
    "Eigenvalue": pcs_all.explained_variance_,
    "Proportion of Variance": pcs_all.explained_variance_ratio_,
    "Cumulative proportion": np.cumsum(pcs_all.explained_variance_ratio_)
}).round(4)

pcsAllSummary_df.index = [f"PC{i}" for i in range(1, len(pcsAllSummary_df) + 1)]

pcsAllComponents_df = pd.DataFrame(
    pcs_all.components_.T,
    columns=pcsAllSummary_df.index,
    index=X_all.columns
)

print("\n=== ALL VARIABLES PCA – Explained Variance ===")
print(pcsAllSummary_df)

print("\n=== ALL VARIABLES PCA – Loadings (Components) ===")
print(pcsAllComponents_df)

# PCA#1, Customer Spend Behavior
pca_spend_cols = [
    "avg_order_value",
    "discount_rate_mean",
    "orders_last_3m",
    "distinct_products",
    "recency_days"
]

X_spend_pca, spend_explained, spend_loadings = run_pca(
    df_pca_ready,
    pca_spend_cols,
    "Customer Spend Behaviour PCA"
)

# Which original variables contribute most to the pattern captured by PC1,PC2 and PC3?
# I only check PC1-PC3, because these demenions explain most of variances
df_pca_ready["spend_PC1"] = X_spend_pca[:, 0]
df_pca_ready["spend_PC2"] = X_spend_pca[:, 1]
df_pca_ready["spend_PC3"] = X_spend_pca[:, 2]

# PCA#2, Interaction / Engagement
pca_engagement_cols = [
    "website_sessions_3m",
    "app_sessions_3m",
    "email_open_rate",
    "email_click_rate",
    "loyalty_points"
]

X_eng_pca, eng_explained, eng_loadings = run_pca(
    df_pca_ready,
    pca_engagement_cols,
    "Customer Interaction / Engagement PCA"
)

# run and save the PC scores for further analysis
df_pca_ready["engagement_PC1"] = X_eng_pca[:, 0]
df_pca_ready["engagement_PC2"] = X_eng_pca[:, 1]
df_pca_ready["engagement_PC3"] = X_eng_pca[:, 2]

# PCA#3, Service & Experience
pca_experience_cols = [
    "returns_rate",
    "complaint_count",
    "satisfaction_score",
    "avg_delivery_days",
    "on_time_rate"
]

X_exp_pca, exp_explained, exp_loadings = run_pca(
    df_pca_ready,
    pca_experience_cols,
    "Service & Experience PCA"
)

df_pca_ready["experience_PC1"] = X_exp_pca[:, 0]
df_pca_ready["experience_PC2"] = X_exp_pca[:, 1]
df_pca_ready["experience_PC3"] = X_exp_pca[:, 2]

# PCA#4, Product Preference
pca_category_cols = [
    "category_share_electronics",
    "category_share_grocery",
    "category_share_home"
]

X_cat_pca, cat_explained, cat_loadings = run_pca(
    df_pca_ready,
    pca_category_cols,
    "Product Preference PCA"
)

df_pca_ready["category_PC1"] = X_cat_pca[:, 0]
df_pca_ready["category_PC2"] = X_cat_pca[:, 1]
df_pca_ready["category_PC3"] = X_cat_pca[:, 2]

###################################################################
# Clustering - customer segmentation - PCA input
# Build clustering feature matrix (PCA scores)
cluster_cols = [
    "spend_PC1", "spend_PC2", "spend_PC3",
    "engagement_PC1", "engagement_PC2",
    "experience_PC1", "experience_PC2",
    "category_PC1"
]
cluster_cols = [c for c in cluster_cols if c in df_pca_ready.columns]

X_cluster = df_pca_ready[cluster_cols].copy()
# Safety: ensure numeric + no missing (important for kmeans/ward)
X_cluster = X_cluster.apply(pd.to_numeric, errors="coerce")
X_cluster = X_cluster.fillna(X_cluster.median())

print("Missing values in clustering inputs (after fix):")
print(X_cluster.isnull().sum())

# K-means: choose K using Elbow + Silhouette
inertia = []
sil_scores = []
K_range = range(2, 9)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_cluster)
    inertia.append(km.inertia_)
    sil_scores.append(silhouette_score(X_cluster, labels))

# Plot Elbow + Silhouette
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(K_range, inertia, marker="o")
plt.title("Elbow Method (K-means)")
plt.xlabel("Number of clusters")
plt.ylabel("Inertia")
# elbow result: 
# Big drop from K = 2 → 3 
# Moderate drop from 3 → 4 
# After K = 4, the curve becomes almost linear and flat
plt.subplot(1, 2, 2)
plt.plot(K_range, sil_scores, marker="o")
plt.title("Silhouette Score (K-means)")
plt.xlabel("Number of clusters")
plt.ylabel("Silhouette score")

plt.tight_layout()
plt.show()
# Silhouette Score result: 
# Highest silhouette at K = 2 (~0.20) 
# Sharp drop after K = 3–4
# Scores flatten after K ≥ 6

# Decision: k = 4
k = 4
kmeans_final = KMeans(n_clusters=k, random_state=42, n_init=10)
df_pca_ready["cluster_kmeans"] = kmeans_final.fit_predict(X_cluster)
df_pca_ready["cluster_kmeans"] = df_pca_ready["cluster_kmeans"] + 1
print("\nK-means cluster sizes:")
print(df_pca_ready["cluster_kmeans"].value_counts())

# Visualize K-means clusters in PCA space (Spend PC1 vs Engagement PC1)
plt.figure(figsize=(7, 6))
plt.scatter(
    df_pca_ready["spend_PC1"],
    df_pca_ready["engagement_PC1"],
    c=df_pca_ready["cluster_kmeans"],  # uses 1–4 labels
    s=10,
    alpha=0.8
)
plt.title("K-means Clusters in PCA Space")
plt.xlabel("Spend PC1")
plt.ylabel("Engagement PC1")
plt.tight_layout()
plt.show()

# Hierarchical clustering (Ward) for comparison/validation
Z = linkage(X_cluster, method="ward")

plt.figure(figsize=(10, 5))
dendrogram(Z, truncate_mode="lastp", p=20)
plt.title("Hierarchical Clustering Dendrogram (Ward linkage)")
plt.xlabel("Cluster")
plt.ylabel("Distance")
plt.tight_layout()
plt.show()

df_pca_ready["cluster_hierarchical"] = fcluster(Z, t=k, criterion="maxclust")

print("\nHierarchical cluster sizes:")
print(df_pca_ready["cluster_hierarchical"].value_counts())

# Compare cluster assignments + silhouette
print("\nCrosstab (K-means vs Hierarchical):")
print(pd.crosstab(df_pca_ready["cluster_kmeans"], df_pca_ready["cluster_hierarchical"]))

sil_kmeans = silhouette_score(X_cluster, df_pca_ready["cluster_kmeans"])
sil_hier = silhouette_score(X_cluster, df_pca_ready["cluster_hierarchical"])

print(f"\nSilhouette score (K-means): {sil_kmeans:.3f}")
print(f"Silhouette score (Hierarchical): {sil_hier:.3f}")

# Visual comparison in PCA space (Spend PC1 vs Engagement PC1)
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.scatter(
    df_pca_ready["spend_PC1"],
    df_pca_ready["engagement_PC1"],
    c=df_pca_ready["cluster_kmeans"],
    s=10
)
plt.title("K-means Clusters")
plt.xlabel("Spend PC1")
plt.ylabel("Engagement PC1")

plt.subplot(1, 2, 2)
plt.scatter(
    df_pca_ready["spend_PC1"],
    df_pca_ready["engagement_PC1"],
    c=df_pca_ready["cluster_hierarchical"],
    s=10
)
plt.title("Hierarchical Clusters")
plt.xlabel("Spend PC1")
plt.ylabel("Engagement PC1")

plt.tight_layout()
plt.show()

# Cluster Profiling 
#    Use original business variables for interpretation
df_pca_ready["cluster"] = df_pca_ready["cluster_kmeans"]  

profile_cols = [
    # Spend
    "avg_order_value", "orders_last_3m", "discount_rate_mean", "recency_days",
    "total_spent_clean", "total_orders_clean",
    # KNN predicted values added for description but not for influence structure

    # Engagement
    "website_sessions_3m", "app_sessions_3m",
    "email_open_rate", "email_click_rate", "loyalty_points",

    # Service & experience
    "satisfaction_score", "complaint_count",
    "returns_rate", "avg_delivery_days", "on_time_rate",

    # Product preference
    "category_share_electronics",
    "category_share_grocery",
    "category_share_home"
]
profile_cols = [c for c in profile_cols if c in df_pca_ready.columns]
profile_cols = [c for c in profile_cols if c not in ["RF_total_spent", "RF_total_orders"]]
# Work on a clean numeric copy for profiling
profile_df = df_pca_ready[["cluster"] + profile_cols].copy()

# Common text tokens -> NaN
profile_df[profile_cols] = profile_df[profile_cols].replace(
    ["NR", "NA", "N/A", "", " ", "None", "null", "NULL"], np.nan
)

# Handle percent strings like "12%" and comma decimals like "12,3"
for c in profile_cols:
    if profile_df[c].dtype == "object":
        profile_df[c] = (
            profile_df[c]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
    profile_df[c] = pd.to_numeric(profile_df[c], errors="coerce")

# Now mean works safely (and numeric_only prevents object aggregation)
cluster_profile = (
    profile_df
    .groupby("cluster")
    .mean(numeric_only=True)
    .round(2)
)

print("\n=== Cluster Profile (Mean Values) ===")
print(cluster_profile)

# Standardized profile (z-scores)
cluster_profile_z = (cluster_profile - cluster_profile.mean()) / cluster_profile.std()
print("\n=== Cluster Profile (Z-scores) ===")
print(cluster_profile_z.round(2))

#%%
#################################################
#below models use original features.
#################################################

### REGRESSION ###

y_target = df_cleaned["future_3m_spend"]

# ONE shared split (indices) to ensure fair model comparison
train_idx, test_idx = train_test_split(
    df_cleaned.index, test_size=0.2, random_state=42
)

y_train = y_target.loc[train_idx]
y_test = y_target.loc[test_idx]

## Linear Regression ##
core_features = [
    "loyalty_tier_encoded",
    "loyalty_points",
    "orders_last_3m",
    "recency_days",
    "discount_rate_mean",
]

x_core = df_cleaned[core_features].copy()
X_train_core = x_core.loc[train_idx]
X_test_core = x_core.loc[test_idx]

linreg_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LinearRegression())
])

linreg_pipe.fit(X_train_core, y_train)
y_pred_lr = linreg_pipe.predict(X_test_core)

r2_lr = r2_score(y_test, y_pred_lr)
rmse_lr = root_mean_squared_error(y_test, y_pred_lr)

print("Linear Regression R²:", r2_lr)
print("Linear Regression RMSE:", rmse_lr)

linreg_coef = linreg_pipe.named_steps["model"].coef_
coef_df = pd.DataFrame({
    "Feature": core_features,
    "Coefficient": linreg_coef
}).sort_values(by="Coefficient", key=abs, ascending=False)

print("\nLinear Regression Coefficients:")
print(coef_df)

## Lasso Regression ##
lasso_features = [
    "loyalty_tier_encoded",
    "loyalty_points",
    "orders_last_3m",
    "recency_days",
    "discount_rate_mean",
    "email_open_rate_num",
    "email_click_rate_num",
    "satisfaction_score",
    "returns_rate",
    "on_time_rate",
    "category_diversity",
]
lasso_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),  # <- handles NaNs
    ("scaler", StandardScaler()),
    ("model", LassoCV(cv=5, random_state=42, max_iter=10000))
])
x_lasso = df_cleaned[lasso_features].copy()
X_train_lasso = x_lasso.loc[train_idx]
X_test_lasso = x_lasso.loc[test_idx]

lasso_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LassoCV(cv=5, random_state=42)) # If convergence warnings occur, add max_iter=10000
])

lasso_pipe.fit(X_train_lasso, y_train)
y_pred_lasso = lasso_pipe.predict(X_test_lasso)

r2_lasso = r2_score(y_test, y_pred_lasso)
rmse_lasso = root_mean_squared_error(y_test, y_pred_lasso)

print("\nLasso Regression R²:", r2_lasso)
print("Lasso Regression RMSE:", rmse_lasso)

lasso_model = lasso_pipe.named_steps["model"]
lasso_coef = pd.DataFrame({
    "feature": lasso_features,
    "coefficient": lasso_model.coef_
})

lasso_nonzero = lasso_coef[lasso_coef["coefficient"] != 0].copy()
lasso_nonzero = lasso_nonzero.sort_values(by="coefficient", key=abs, ascending=False)

print("\nLasso Regression Coefficients (non-zero):")
print(lasso_nonzero)

print("\nChosen alpha (LassoCV):", lasso_model.alpha_)
print("Number of non-zero predictors:", (lasso_model.coef_ != 0).sum())

## PCA + Linear regression comparison ##
X_pca_base = df_cleaned[lasso_features].copy()
X_train_pca_base = X_pca_base.loc[train_idx]
X_test_pca_base = X_pca_base.loc[test_idx]

pca_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("pca", PCA(n_components=0.8)),  # keep 80% variance
    ("model", LinearRegression())
])

pca_pipe.fit(X_train_pca_base, y_train)
y_pred_pca = pca_pipe.predict(X_test_pca_base)

r2_pca = r2_score(y_test, y_pred_pca)
rmse_pca = root_mean_squared_error(y_test, y_pred_pca)

print("\nPCA Regression R²:", r2_pca)
print("PCA Regression RMSE:", rmse_pca)
print("Number of PCA components:", pca_pipe.named_steps["pca"].n_components_)

# Final comparison
comparison = pd.DataFrame({
    "Model": ["Linear Regression", "Lasso Regression", "PCA Regression"],
    "R2": [r2_lr, r2_lasso, r2_pca],
    "RMSE": [rmse_lr, rmse_lasso, rmse_pca]
})

print("\nModel Comparison:")
print(comparison)

# Actual vs. predicted all models scatter plot
plt.figure(figsize=(7, 7))

plt.scatter(y_test, y_pred_lr, alpha=0.5, label="Linear Regression")
plt.scatter(y_test, y_pred_lasso, alpha=0.5, label="Lasso Regression")
plt.scatter(y_test, y_pred_pca, alpha=0.5, label="PCA Regression")

# 45-degree reference line
min_val = min(y_test.min(), y_pred_lasso.min(), y_pred_pca.min())
max_val = max(y_test.max(), y_pred_lasso.max(), y_pred_pca.max())
plt.plot([min_val, max_val], [min_val, max_val], 'k--', label="Perfect prediction")

plt.xlabel("Actual future 3-month spend")
plt.ylabel("Predicted future 3-month spend")
plt.title("Actual vs Predicted Future Spend (Test Set)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

#%%
################################################
### CLASSIFICATION ###

df_tree = df_cleaned[['age', 'region', 'gender',
       'email_opt_in', 'loyalty_points', 'loyalty_tier_encoded',
       'avg_order_value', 'pct_orders_discounted',
       'recency_days', 'days_since_first_order', 'orders_last_3m',
       'distinct_products', 'category_diversity',
       'returns_rate', 'complaint_count', 'satisfaction_score',
       'email_open_rate', 'email_click_rate', 'website_sessions_3m',
       'app_sessions_3m', 'avg_delivery_days', 'on_time_rate',
       'churn_90d']]
df_tree_noNR = df_tree[(df_tree['email_open_rate'] != 'NR') & (df_tree['email_click_rate'] != 'NR')]
df_tree_noNR['region'] = df_tree_noNR['region'].astype('category')
new_categories = {1: 'North', 2: 'East', 3: 'South', 4: 'West'}
df_tree_noNR.region.cat.rename_categories(new_categories)
df_tree_noNR = pd.get_dummies(df_tree_noNR, columns=['region'], prefix='region', drop_first=True)

df_tree_noNR['gender'] = df_tree_noNR['gender'].astype('category')
new_categories = {1: 'F', 2: 'M', 3: 'O'}
df_tree_noNR.gender.cat.rename_categories(new_categories)
df_tree_noNR = pd.get_dummies(df_tree_noNR, columns=['gender'], prefix='gender', drop_first=True)

X = df_tree_noNR.drop(columns=["churn_90d"])
Y = df_tree_noNR["churn_90d"]

train_X, test_X, train_Y, test_Y = train_test_split(X,Y, test_size=0.2, random_state=1)

fullClassTree = DecisionTreeClassifier(max_depth=1, random_state=1)
fullClassTree.fit(train_X, train_Y)

plot_tree(fullClassTree, feature_names=train_X.columns, filled=True)

plt.tight_layout()
plt.show()

classificationSummary(train_Y, fullClassTree.predict(train_X))
classificationSummary(test_Y, fullClassTree.predict(test_X))

treeClassifier = DecisionTreeClassifier(random_state=1)
scores = cross_val_score(treeClassifier, train_X, train_Y, cv=5)
print('Accuracy scores of each fold: ', [f'{acc:3f}' for acc in scores])

print(df_tree_noNR.columns)

## Logistic Regression ##
df_logreg = df_cleaned[['age', 'region', 'gender',
       'email_opt_in', 'loyalty_points', 'loyalty_tier_encoded',
       'avg_order_value', 'pct_orders_discounted',
       'recency_days', 'days_since_first_order', 'orders_last_3m',
       'distinct_products', 'category_diversity',
       'returns_rate', 'complaint_count', 'satisfaction_score',
       'email_open_rate', 'email_click_rate', 'website_sessions_3m',
       'app_sessions_3m', 'avg_delivery_days', 'on_time_rate']]
df_logreg_noNR = df_logreg[(df_logreg['email_open_rate'] != 'NR') & (df_logreg['email_click_rate'] != 'NR')]

df_logreg_noNR['region'] = df_logreg_noNR['region'].astype('category')
new_categories = {1: 'North', 2: 'East', 3: 'South', 4: 'West'}
df_logreg_noNR.region.cat.rename_categories(new_categories)
df_logreg_noNR = pd.get_dummies(df_logreg_noNR, columns=['region'], prefix='region', drop_first=True)

df_logreg_noNR['gender'] = df_logreg_noNR['gender'].astype('category')
new_categories = {1: 'F', 2: 'M', 3: 'O'}
df_logreg_noNR.gender.cat.rename_categories(new_categories)
df_logreg_noNR = pd.get_dummies(df_logreg_noNR, columns=['gender'], prefix='gender', drop_first=True)

df_logreg_noNR = df_logreg_noNR.apply(pd.to_numeric, errors='coerce')
df_logreg_noNR = df_logreg_noNR.dropna()

X = df_logreg_noNR.drop(columns=['region_North'])
Y = df_logreg_noNR['region_North']

train_X, test_X, train_Y, test_Y = train_test_split(X,Y, test_size=0.2, random_state=1)

logit_reg = LogisticRegression(penalty="l2", C=1e42, solver = 'liblinear')
logit_reg.fit(train_X,train_Y) 

print('intercept ', logit_reg.intercept_[0])
print(pd.DataFrame({'coeff': logit_reg.coef_[0]}, index=X.columns))

classificationSummary(train_Y, logit_reg.predict(train_X))
classificationSummary(test_Y, logit_reg.predict(test_X))

pred_train = logit_reg.predict(train_X)
pred_test = logit_reg.predict(test_X)

print("TRAIN RESULTS")
print(classification_report(train_Y, pred_train))

print("TEST RESULTS")
print(classification_report(test_Y, pred_test))

#################################################
# KNN - predict customer satisfaction score
# Define target
target = "satisfaction_score"

#    Choose predictors (avoid direct leakage; use drivers of experience/engagement)
#    Keep mostly numeric features to avoid heavy encoding work.
knn_features = [
    # Service & experience
    "avg_delivery_days",
    "on_time_rate",
    "returns_rate",
    "complaint_count",

    # Engagement
    "website_sessions_3m",
    "app_sessions_3m",
    "loyalty_points",
    "email_opt_in",  

    # Spend / relationship signals (not the teammate's total_amount target)
    "orders_last_3m",
    "recency_days",
    "discount_rate_mean",
    "pct_orders_discounted",

    # Product preference (can help explain satisfaction patterns)
    "category_share_electronics",
    "category_share_grocery",
    "category_share_home"
]

# Keep only columns that exist (safe if your dataset changes)
knn_features = [c for c in knn_features if c in df_cleaned.columns]

#Prepare X/y
X_knn = df_cleaned[knn_features].copy()
y_knn = df_cleaned[target].copy()

# Ensure numeric (handles 'NR'/'NA' etc. if they appear), boolean is fine
X_knn = X_knn.replace(["NR", "NA", "N/A", "", " "], np.nan)
X_knn = X_knn.apply(pd.to_numeric, errors="coerce")
X_knn = X_knn.fillna(X_knn.median())

y_knn = pd.to_numeric(y_knn, errors="coerce")
y_knn = y_knn.fillna(y_knn.median())

# Train/Validation pool + Final Test set
X_trainval, X_test, y_trainval, y_test = train_test_split(
    X_knn, y_knn, test_size=0.2, random_state=42
)

# Pipeline: scale -> KNN regression
#    (Scaling is important for KNN because it uses distance)
knn_model = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("knn", KNeighborsRegressor(n_neighbors=7, weights="distance"))
])


# 5-fold Cross-Validation on TRAIN/VAL (validation step)
cv = KFold(n_splits=5, shuffle=True, random_state=42)
# out-of-fold predictions for train/val set
y_oof = cross_val_predict(knn_model, X_trainval, y_trainval, cv=cv)

cv_r2 = r2_score(y_trainval, y_oof)
cv_mae = mean_absolute_error(y_trainval, y_oof)
cv_rmse = np.sqrt(mean_squared_error(y_trainval, y_oof))

print("\n=== KNN Regression: 5-Fold CV on Train/Validation ===")
print("Target:", target)
print("Predictors used:", knn_features)
print(f"CV R²   : {cv_r2:.4f}")
print(f"CV MAE  : {cv_mae:.4f}")
print(f"CV RMSE : {cv_rmse:.4f}")

#Fit final model on FULL Train/Val, then evaluate on TEST
knn_model.fit(X_trainval, y_trainval)

y_pred_test = knn_model.predict(X_test)

test_r2 = r2_score(y_test, y_pred_test)
test_mae = mean_absolute_error(y_test, y_pred_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))

print("\n=== Final Evaluation on Held-out Test Set ===")
print(f"Test R²   : {test_r2:.4f}")
print(f"Test MAE  : {test_mae:.4f}")
print(f"Test RMSE : {test_rmse:.4f}")

# Predicted vs Actual plot (Test set)
plt.figure(figsize=(6, 6))

plt.scatter(y_test, y_pred_test, alpha=0.6)
plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    linestyle="--"
)

plt.xlabel("Actual Satisfaction Score")
plt.ylabel("Predicted Satisfaction Score")
plt.title("KNN Regression: Predicted vs Actual (Test Set)")

plt.tight_layout()
plt.show()

#%%
########################################################
# FINAL CSV EXPORT FOR POWER BI (one row per customer_id) - without new imputation
########################################################
# export all columns
df_pca_ready.to_csv(
    "customer_analytics_dashboard.csv",
    index=False
)
import os
print("CSV saved in:", os.getcwd())

# Base key (NEVER drop this)
base = df_cleaned[["customer_id"]].copy()
base["customer_id"] = pd.to_numeric(base["customer_id"], errors="coerce").astype(int)

# PCA (PC1–PC3) linked to customer_id (choose numeric features, exclude ID and chosen targets)
exclude = {"customer_id", "future_3m_spend", "churn_90d"}
pca_features = [
    c for c in df_cleaned.columns
    if c not in exclude and pd.api.types.is_numeric_dtype(df_cleaned[c])
]

X_pca = df_cleaned[pca_features].copy()
X_pca = X_pca.apply(pd.to_numeric, errors="coerce")
X_pca = X_pca.fillna(X_pca.median())

pca_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("pca", PCA(n_components=3, random_state=42))
])

pcs = pca_pipe.fit_transform(X_pca)

pca_scores = pd.DataFrame({
    "customer_id": base["customer_id"].values,
    "PC1": pcs[:, 0],
    "PC2": pcs[:, 1],
    "PC3": pcs[:, 2],
})

# Hierarchical clustering on PC1–PC3 (Ward), linked to customer_id
Z = linkage(pca_scores[["PC1", "PC2", "PC3"]].values, method="ward")
k = 4  # keep your chosen k
cluster_h = fcluster(Z, t=k, criterion="maxclust")

clusters = pd.DataFrame({
    "customer_id": base["customer_id"].values,
    "cluster_hierarchical": cluster_h
})

# Regression outputs (Lasso): OOF preds + residuals + full-fit preds
y = pd.to_numeric(df_cleaned["future_3m_spend"], errors="coerce").fillna(df_cleaned["future_3m_spend"].median())

lasso_features = [
    "loyalty_tier_encoded","loyalty_points","orders_last_3m","recency_days","discount_rate_mean",
    "email_open_rate_num","email_click_rate_num","satisfaction_score","returns_rate","on_time_rate",
    "category_diversity",
]
lasso_features = [c for c in lasso_features if c in df_cleaned.columns]

X_lasso = df_cleaned[lasso_features].copy()
X_lasso = X_lasso.apply(pd.to_numeric, errors="coerce").fillna(df_cleaned[lasso_features].median())

# Use the already trained LassoCV model.
best_alpha = lasso_model.alpha_

lasso_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", Lasso(alpha=best_alpha, max_iter=50000, random_state=42))
])

cv = KFold(n_splits=5, shuffle=True, random_state=42)

# Out-of-fold predictions
y_pred_oof = cross_val_predict(
    lasso_pipe,
    X_lasso,
    y,
    cv=cv,
    n_jobs=-1
)

# Fit on all data
lasso_pipe.fit(X_lasso, y)
y_pred_full = lasso_pipe.predict(X_lasso)

reg_out = pd.DataFrame({
    "customer_id": df_cleaned["customer_id"].astype(int).values,
    "lasso_alpha": best_alpha,
    "lasso_pred_oof": y_pred_oof,
    "lasso_residual_oof": y - y_pred_oof,
    "lasso_pred_fullfit": y_pred_full,
    "lasso_residual_fullfit": y - y_pred_full,
})

# Classification outputs (churn): probability + predicted class (OOF + fullfit)
cls_num = [
    "loyalty_points","loyalty_tier_encoded","avg_order_value","pct_orders_discounted",
    "recency_days","orders_last_3m","returns_rate","complaint_count","satisfaction_score",
    "website_sessions_3m","app_sessions_3m","avg_delivery_days","on_time_rate",
    "email_open_rate_num","email_click_rate_num"
]
cls_cat = [c for c in ["region", "gender"] if c in df_cleaned.columns]
cls_num = [c for c in cls_num if c in df_cleaned.columns]

X_cls = df_cleaned[cls_num + cls_cat].copy()
for c in cls_num:
    X_cls[c] = pd.to_numeric(X_cls[c], errors="coerce")
X_cls[cls_num] = X_cls[cls_num].fillna(X_cls[cls_num].median())

y_cls = pd.to_numeric(df_cleaned["churn_90d"], errors="coerce").fillna(0).astype(int)

pre = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), cls_num),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cls_cat),
    ],
    remainder="drop"
)

cls_pipe = Pipeline([
    ("pre", pre),
    ("model", LogisticRegression(max_iter=2000, solver="liblinear"))
])

proba_oof = cross_val_predict(cls_pipe, X_cls, y_cls, cv=cv, method="predict_proba", n_jobs=-1)[:, 1]
pred_oof = (proba_oof >= 0.5).astype(int)

cls_pipe.fit(X_cls, y_cls)
proba_full = cls_pipe.predict_proba(X_cls)[:, 1]
pred_full = (proba_full >= 0.5).astype(int)

cls_out = pd.DataFrame({
    "customer_id": base["customer_id"].values,
    "churn_proba_oof": proba_oof,
    "churn_pred_oof": pred_oof,
    "churn_proba_fullfit": proba_full,
    "churn_pred_fullfit": pred_full,
})

# Core KPI columns to include for Power BI
core_cols = [
    "customer_id","age","region","gender","tenure_months","email_opt_in",
    "loyalty_tier_encoded","loyalty_points",
    "total_orders_clean","total_spent_clean",
    "total_orders","total_spent",
    "RF_total_orders","RF_total_spent", 
    "avg_order_value","pct_orders_discounted","discount_rate_mean",
    "recency_days","orders_last_3m","distinct_products","category_diversity",
    "returns_rate","complaint_count","satisfaction_score",
    "website_sessions_3m","app_sessions_3m",
    "avg_delivery_days","on_time_rate",
    "churn_90d"
]
core_cols = [c for c in core_cols if c in df_cleaned.columns]

dashboard = df_cleaned[core_cols].copy()
dashboard["customer_id"] = pd.to_numeric(dashboard["customer_id"], errors="coerce").astype(int)

## FINAL DASHBOARD ##
# Merge everything (one row per customer_id)
dashboard_final = (
    dashboard
    .merge(pca_scores, on="customer_id", how="left", validate="one_to_one")
    .merge(clusters, on="customer_id", how="left", validate="one_to_one")
    .merge(reg_out, on="customer_id", how="left", validate="one_to_one")
    .merge(cls_out, on="customer_id", how="left", validate="one_to_one")
)

# Sanity checks
assert dashboard_final["customer_id"].is_unique, "customer_id is not unique after merges!"
assert dashboard_final.shape[0] == df_cleaned.shape[0], "Row count changed after merges!"
print("Rows:", dashboard_final.shape[0])
print("Missing PC1:", dashboard_final["PC1"].isna().sum())
print("Missing cluster:", dashboard_final["cluster_hierarchical"].isna().sum())
print("Missing lasso_pred_oof:", dashboard_final["lasso_pred_oof"].isna().sum())
print("Missing churn_proba_oof:", dashboard_final["churn_proba_oof"].isna().sum())

# Export for Power BI
dashboard_final.to_csv("powerbi_customer_dashboard.csv", index=False)
print("✅ Exported: powerbi_customer_dashboard.csv")


########################################################
# ONE MASTER CSV EXPORT FOR POWER BI
# Includes:
# - ALL original df_cleaned columns
# - Global PCA (PC1–PC3)
# - Grouped PCA scores (spend / engagement / experience / category: PC1–PC3)
# - Clustering: K-means + Hierarchical (Ward)
# - Regression outputs (Lasso): 5 cols
# - Classification outputs (Churn logistic): 4 cols
# - KNN prediction for satisfaction_score (OOF + fullfit)
########################################################
# -----------------------------
# 0) BASE = ALL COLUMNS in df_cleaned (already cleaned + imputed)
# -----------------------------
base = df_cleaned.copy()
base["customer_id"] = pd.to_numeric(base["customer_id"], errors="coerce").astype(int)

# Shared CV
cv = KFold(n_splits=5, shuffle=True, random_state=42)

# Utility: safe numeric matrix (median fill)
def _numeric_matrix(df, cols):
    cols = [c for c in cols if c in df.columns]
    X = df[cols].copy()
    X = X.replace(["NR", "NA", "N/A", "", " "], np.nan)
    X = X.apply(pd.to_numeric, errors="coerce")
    X = X.fillna(X.median(numeric_only=True))
    return X

# Utility: run PCA -> return PC1..PC3 with a prefix, keyed by customer_id
def _pca_scores(df, cols, prefix, n_components=3):
    cols = [c for c in cols if c in df.columns]
    out = pd.DataFrame({"customer_id": df["customer_id"].values})

    if len(cols) == 0:
        # still return columns (as NaN) so downstream code doesn't break
        out[f"{prefix}_PC1"] = np.nan
        out[f"{prefix}_PC2"] = np.nan
        out[f"{prefix}_PC3"] = np.nan
        return out

    X = _numeric_matrix(df, cols)
    n_comp = min(n_components, X.shape[1])

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("pca", PCA(n_components=n_comp, random_state=42))
    ])

    pcs = pipe.fit_transform(X)

    out[f"{prefix}_PC1"] = pcs[:, 0] if pcs.shape[1] > 0 else np.nan
    out[f"{prefix}_PC2"] = pcs[:, 1] if pcs.shape[1] > 1 else np.nan
    out[f"{prefix}_PC3"] = pcs[:, 2] if pcs.shape[1] > 2 else np.nan
    return out

# -----------------------------
# 1) GLOBAL PCA (PC1–PC3)
# -----------------------------
exclude = {"customer_id", "future_3m_spend", "churn_90d"}
global_pca_features = [
    c for c in base.columns
    if c not in exclude and pd.api.types.is_numeric_dtype(base[c])
]

X_global = base[global_pca_features].copy()
X_global = X_global.apply(pd.to_numeric, errors="coerce")
X_global = X_global.fillna(X_global.median(numeric_only=True))

global_pca_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("pca", PCA(n_components=3, random_state=42))
])
global_pcs = global_pca_pipe.fit_transform(X_global)

pca_global = pd.DataFrame({
    "customer_id": base["customer_id"].values,
    "PC1": global_pcs[:, 0],
    "PC2": global_pcs[:, 1],
    "PC3": global_pcs[:, 2],
})

# -----------------------------
# 2) GROUPED PCA (PC1–PC3 each)
#    Use your cleaned/imputed columns (prefer *_num)
# -----------------------------
pca_spend_cols = ["avg_order_value", "discount_rate_mean", "orders_last_3m", "distinct_products", "recency_days"]

pca_engagement_cols = [
    "website_sessions_3m", "app_sessions_3m",
    "email_open_rate_num", "email_click_rate_num",
    "loyalty_points"
]

pca_experience_cols = ["returns_rate", "complaint_count", "satisfaction_score", "avg_delivery_days", "on_time_rate"]

# category shares (some datasets have only 3; some have 4)
pca_category_cols = [
    "category_share_electronics",
    "category_share_grocery",
    "category_share_home",
    "category_share_apparel",
]

pca_spend = _pca_scores(base, pca_spend_cols, prefix="spend")
pca_eng  = _pca_scores(base, pca_engagement_cols, prefix="engagement")
pca_exp  = _pca_scores(base, pca_experience_cols, prefix="experience")
pca_cat  = _pca_scores(base, pca_category_cols, prefix="category")

# -----------------------------
# 3) CLUSTERING (K-means + Hierarchical)
#    Cluster on grouped PCA space
# -----------------------------
tmp_for_cluster = (
    base[["customer_id"]]
    .merge(pca_spend, on="customer_id", how="left")
    .merge(pca_eng,   on="customer_id", how="left")
    .merge(pca_exp,   on="customer_id", how="left")
    .merge(pca_cat,   on="customer_id", how="left")
)

cluster_cols = [c for c in tmp_for_cluster.columns if c.endswith("_PC1") or c.endswith("_PC2") or c.endswith("_PC3")]
X_cluster = tmp_for_cluster[cluster_cols].copy()
X_cluster = X_cluster.apply(pd.to_numeric, errors="coerce")
X_cluster = X_cluster.fillna(X_cluster.median(numeric_only=True))

k = 4  # chosen k

# K-means
km = KMeans(n_clusters=k, random_state=42, n_init=10)
cluster_kmeans = km.fit_predict(X_cluster) + 1

# Hierarchical (Ward)
Z = linkage(X_cluster.values, method="ward")
cluster_hier = fcluster(Z, t=k, criterion="maxclust")

cluster_out = pd.DataFrame({
    "customer_id": base["customer_id"].values,
    "cluster_kmeans": cluster_kmeans,
    "cluster_hierarchical": cluster_hier
})

# -----------------------------
# 4) REGRESSION (Lasso) outputs: 5 columns
# -----------------------------
y_reg = pd.to_numeric(base["future_3m_spend"], errors="coerce")
y_reg = y_reg.fillna(y_reg.median())

lasso_features = [
    "loyalty_tier_encoded","loyalty_points","orders_last_3m","recency_days","discount_rate_mean",
    "email_open_rate_num","email_click_rate_num","satisfaction_score","returns_rate","on_time_rate",
    "category_diversity",
]
lasso_features = [c for c in lasso_features if c in base.columns]

X_lasso = _numeric_matrix(base, lasso_features)

# self-contained alpha selection
lasso_cv_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LassoCV(cv=5, random_state=42, max_iter=50000))
])
lasso_cv_pipe.fit(X_lasso, y_reg)
best_alpha = float(lasso_cv_pipe.named_steps["model"].alpha_)

lasso_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", Lasso(alpha=best_alpha, max_iter=50000, random_state=42))
])

lasso_pred_oof = cross_val_predict(lasso_pipe, X_lasso, y_reg, cv=cv, n_jobs=-1)
lasso_pipe.fit(X_lasso, y_reg)
lasso_pred_full = lasso_pipe.predict(X_lasso)

reg_out = pd.DataFrame({
    "customer_id": base["customer_id"].values,
    "lasso_alpha": best_alpha,
    "lasso_pred_oof": lasso_pred_oof,
    "lasso_residual_oof": y_reg - lasso_pred_oof,
    "lasso_pred_fullfit": lasso_pred_full,
    "lasso_residual_fullfit": y_reg - lasso_pred_full,
})

# -----------------------------
# 5) CLASSIFICATION (churn logistic) outputs: 4 columns
# -----------------------------
cls_num = [
    "loyalty_points","loyalty_tier_encoded","avg_order_value","pct_orders_discounted",
    "recency_days","orders_last_3m","returns_rate","complaint_count","satisfaction_score",
    "website_sessions_3m","app_sessions_3m","avg_delivery_days","on_time_rate",
    "email_open_rate_num","email_click_rate_num"
]
cls_cat = [c for c in ["region", "gender"] if c in base.columns]
cls_num = [c for c in cls_num if c in base.columns]

X_cls = base[cls_num + cls_cat].copy()
for c in cls_num:
    X_cls[c] = pd.to_numeric(X_cls[c], errors="coerce")
X_cls[cls_num] = X_cls[cls_num].fillna(base[cls_num].median(numeric_only=True))

y_cls = pd.to_numeric(base["churn_90d"], errors="coerce").fillna(0).astype(int)

pre = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), cls_num),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cls_cat),
    ],
    remainder="drop"
)

cls_pipe = Pipeline([
    ("pre", pre),
    ("model", LogisticRegression(max_iter=2000, solver="liblinear"))
])

churn_proba_oof = cross_val_predict(cls_pipe, X_cls, y_cls, cv=cv, method="predict_proba", n_jobs=-1)[:, 1]
churn_pred_oof = (churn_proba_oof >= 0.5).astype(int)

cls_pipe.fit(X_cls, y_cls)
churn_proba_full = cls_pipe.predict_proba(X_cls)[:, 1]
churn_pred_full = (churn_proba_full >= 0.5).astype(int)

cls_out = pd.DataFrame({
    "customer_id": base["customer_id"].values,
    "churn_proba_oof": churn_proba_oof,
    "churn_pred_oof": churn_pred_oof,
    "churn_proba_fullfit": churn_proba_full,
    "churn_pred_fullfit": churn_pred_full,
})

# -----------------------------
# 6) KNN prediction for satisfaction_score (adds 2 cols)
# -----------------------------
target = "satisfaction_score"
knn_features = [
    # experience drivers
    "avg_delivery_days","on_time_rate","returns_rate","complaint_count",
    # engagement
    "website_sessions_3m","app_sessions_3m","loyalty_points","email_opt_in",
    # spend/relationship
    "orders_last_3m","recency_days","discount_rate_mean","pct_orders_discounted",
    # category preference (if exists)
    "category_share_electronics","category_share_grocery","category_share_home","category_share_apparel",
]
knn_features = [c for c in knn_features if c in base.columns]

X_knn = _numeric_matrix(base, knn_features)
y_knn = pd.to_numeric(base[target], errors="coerce")
y_knn = y_knn.fillna(y_knn.median())

knn_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsRegressor(n_neighbors=7, weights="distance"))
])

satis_pred_oof = cross_val_predict(knn_pipe, X_knn, y_knn, cv=cv, n_jobs=-1)
knn_pipe.fit(X_knn, y_knn)
satis_pred_full = knn_pipe.predict(X_knn)

knn_out = pd.DataFrame({
    "customer_id": base["customer_id"].values,
    "satisfaction_pred_knn_oof": satis_pred_oof,
    "satisfaction_pred_knn_fullfit": satis_pred_full,
})

# -----------------------------
# 7) FINAL MERGE (one row per customer_id)
#    Base columns remain "after cleaned/imputed"
# -----------------------------
dashboard_all = (
    base
    .merge(pca_global, on="customer_id", how="left", validate="one_to_one")
    .merge(pca_spend,  on="customer_id", how="left", validate="one_to_one")
    .merge(pca_eng,    on="customer_id", how="left", validate="one_to_one")
    .merge(pca_exp,    on="customer_id", how="left", validate="one_to_one")
    .merge(pca_cat,    on="customer_id", how="left", validate="one_to_one")
    .merge(cluster_out,on="customer_id", how="left", validate="one_to_one")
    .merge(reg_out,    on="customer_id", how="left", validate="one_to_one")
    .merge(cls_out,    on="customer_id", how="left", validate="one_to_one")
    .merge(knn_out,    on="customer_id", how="left", validate="one_to_one")
)

# Sanity checks
assert dashboard_all["customer_id"].is_unique, "customer_id is not unique after merges!"
assert dashboard_all.shape[0] == base.shape[0], "Row count changed after merges!"

print("Rows:", dashboard_all.shape[0])
print("Cols:", dashboard_all.shape[1])

dashboard_all.to_csv("powerbi__dashboard_ALL.csv", index=False)
print("✅ Exported: powerbi__dashboard_ALL.csv")

