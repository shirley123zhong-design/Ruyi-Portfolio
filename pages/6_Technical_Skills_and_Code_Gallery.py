import streamlit as st
import os
import sys
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_PROJECT_ROOT)
os.chdir(_PROJECT_ROOT)  # ensure relative asset paths work no matter where streamlit was launched from
from theme import apply_theme, hero, eyebrow, badge_row

st.set_page_config(page_title="Technical Skills & Code Gallery | Shirley Zhong", page_icon="🛠️", layout="wide")
apply_theme()

st.page_link("app.py", label="← Back to home")

# -----------------------------------------------------------------------
# PAGE HEADER
# -----------------------------------------------------------------------

hero(
    icon="🛠️",
    title="Technical Skills & Code Gallery",
    subtitle=(
        "Technical tools are only useful when they help answer business questions. This page summarizes "
        "the tools, formulas, measures, transformations, and analytical methods I have applied across my "
        "portfolio projects — how data is cleaned, calculated, modelled, visualized, and translated "
        "into business decisions."
    ),
    tags=[
        "Excel", "Power Query", "Power BI", "DAX", "SQL", "Python", "R", "Streamlit",
        "Dash", "Data Cleaning", "ETL", "KPI Design", "Forecasting", "Regression",
        "Mediation", "Moderation", "Machine Learning", "Dashboard Storytelling",
    ],
    flow="Business question → Data preparation → Calculation logic → Analysis method → "
         "Dashboard / model → Interpretation → Recommendation",
)

# -----------------------------------------------------------------------
# ASSET / DOWNLOAD PATH BASE
# -----------------------------------------------------------------------

IMG_DIR = "assets/img"
DOC_DIR = "assets/files"


def show_image(filename, caption=""):
    path = os.path.join(IMG_DIR, filename)
    with st.container(border=True):
        if os.path.exists(path):
            st.image(path, caption=caption, use_container_width=True)
        else:
            st.caption(f"Screenshot placeholder — add `{path}` to your repo to display it here.")


def download_button_for(filename, label):
    path = os.path.join(DOC_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            st.download_button(label, data=f, file_name=filename)
    else:
        st.caption(f"Add `{path}` to enable this download.")


def download_bankdata_case():
    # Case 2 is stored directly under assets, not assets/files.
    path = os.path.join(_PROJECT_ROOT, "assets", "Bankdata_benchmark.zip")
    if os.path.isfile(path):
        with open(path, "rb") as f:
            st.download_button(
                "Download Bankdata Case 2 (ZIP)", data=f,
                file_name="Bankdata_benchmark.zip", mime="application/zip",
                key="bankdata_case2_download",
            )
    else:
        st.caption("Add `assets/Bankdata_benchmark.zip` to enable the case download.")


def bullet_list(items):
    st.markdown("\n".join(f"- {i}" for i in items))


def render_grouped(groups):
    """Render {group_name: {'why': str, 'items': [str, ...]}} with a why-line per group."""
    for group, data in groups.items():
        st.markdown(f"**{group}**")
        st.caption(data["why"])
        bullet_list(data["items"])
        st.markdown("")


def tool_badges(tools):
    badge_row(tools)


def logic_map(steps):
    """Render a compact horizontal flow: [Step] → [Step] → [Step] ...
    steps: list of (title, subtitle) tuples."""
    cards = ""
    for i, (title, subtitle) in enumerate(steps):
        if i > 0:
            cards += (
                '<div style="display:flex;align-items:center;color:#141414;'
                'font-size:1.3rem;padding:0 6px;">&rarr;</div>'
            )
        cards += (
            '<div style="flex:1 1 160px;min-width:150px;background:#F7F8F4;border:1px solid #E3E2DF;'
            'border-left:3px solid #141414;border-radius:4px;padding:12px 14px;'
            'transition:box-shadow 0.15s ease;">'
            f'<p style="font-weight:700;font-size:0.9rem;margin:0 0 4px 0;color:#141414;">{title}</p>'
            f'<p style="font-size:0.8rem;color:#777;margin:0;line-height:1.3;">{subtitle}</p>'
            '</div>'
        )
    st.markdown(
        f'<div style="display:flex;flex-wrap:wrap;align-items:stretch;gap:2px;margin:10px 0 16px 0;">{cards}</div>',
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------
# SECTION DATA
# -----------------------------------------------------------------------

TOOLS = [
    ("Excel", "Data cleaning, modelling, regression, sensitivity analysis, forecasting, "
              "financial analysis, and quick business calculations.",
     "Best when: the analysis is ad-hoc, needs to stay flexible for someone else to edit, or doesn't justify writing code."),
    ("Power Query", "ETL workflows, repeated data cleaning, merging files, transforming fields, "
                    "fixing data structure, and preparing reports.",
     "Best when: the same cleaning/merge steps will need to run again on the next batch of data."),
    ("Power BI", "Dashboard development, KPI reporting, scenario analysis, slicers, dynamic "
                "parameters, DAX measures, and management reporting.",
     "Best when: the audience needs to explore or filter the result themselves, not just read one static number."),
    ("SQL", "Database querying, filtering, joins, aggregation, internal control testing, "
           "customer analysis, and business rule validation.",
     "Best when: the data lives in a real database — too large or too relational to browse manually."),
    ("Python", "Flexible analytics, data validation, KPI calculation, machine learning, "
              "clustering, forecasting, visualization, and dashboard apps.",
     "Best when: the task needs automation, prediction, or something a spreadsheet can't do natively."),
    ("R", "Statistical testing, survey analysis, CFA, reliability checks, regression, "
         "mediation, moderation, and diagnostics.",
     "Best when: the question needs to be tested statistically — is this real, why, and under what condition — not just visualized."),
    ("Streamlit / Dash", "Interactive web apps, portfolio communication, business dashboards, "
                        "and presenting analysis in a user-friendly way.",
     "Best when: the analysis needs to be shared as a live, interactive tool rather than a static file."),
]

POWERBI_MEASURES = {
    "Basic KPI measures": {
        "why": "Use when the audience needs the core numbers first, before any comparison or drill-down.",
        "items": [
            "Total sales", "Total cost", "Total reimbursement", "Average reimbursement per trip",
            "Number of transactions", "Number of customers", "Number of orders", "Average sales",
            "Average cost", "Profit", "Profit margin",
        ],
    },
    "Comparison measures": {
        "why": "Use when a number alone doesn't mean much without a benchmark — budget, prior period, or scenario.",
        "items": [
            "Actual vs forecast", "Actual vs budget", "Current cost vs scenario cost",
            "Year-over-year change", "Month-over-month change", "Difference from baseline",
            "Percentage difference", "Ranking by category, customer, office, supplier, or product",
        ],
    },
    "Scenario analysis": {
        "why": "Use when the audience needs to test a decision before making it, not just see one fixed result.",
        "items": [
            "Dynamic flat-rate reimbursement parameter", "What-if rate comparison",
            "Selected date forecasting", "Selected category filtering",
            "Cost impact by office / employee / role",
        ],
    },
    "Dashboard logic": {
        "why": "Use when the same report has to serve different people — a quick summary and a detailed drill-down.",
        "items": [
            "KPI cards", "Slicers and filters", "Tooltip pages", "Drill-down views",
            "Conditional formatting", "Trend charts", "Matrix tables", "Segmentation views",
            "Manager-friendly summary pages",
        ],
    },
}

DAX_EXAMPLES = """Total Cost = SUM(Cost)

Average Cost = AVERAGE(Cost)

Profit = SUM(Sales) - SUM(Cost)

Profit Margin = DIVIDE([Profit], SUM(Sales))

Cost Difference = [Scenario Cost] - [Actual Cost]

Percentage Change = DIVIDE([Current Value] - [Previous Value], [Previous Value])"""

PQ_OPERATIONS = {
    "Data import": {
        "why": "Use when the data lives in multiple files, folders, or external sources that need to become one table.",
        "items": [
            "Import CSV files", "Import Excel files", "Combine files from folders",
            "Connect to external data sources", "Use API / CSV fallback when live connection has issues",
        ],
    },
    "Data cleaning": {
        "why": "Use when the data can't be trusted yet — duplicates, blanks, or inconsistent formatting would break any analysis built on top.",
        "items": [
            "Remove duplicate rows", "Remove errors", "Replace null values", "Replace \"NA\" with zero",
            "Fill missing product IDs", "Remove irrelevant columns", "Rename columns",
            "Change data types", "Standardize text formatting", "Trim and clean text fields",
        ],
    },
    "Data transformation": {
        "why": "Use when the data is clean but not yet shaped for the analysis — wrong grain, wrong structure, missing fields.",
        "items": [
            "Split concatenated columns", "Merge columns", "Unpivot / pivot data",
            "Group by product, date, customer, office, or category", "Create conditional columns",
            "Create calculated columns", "Extract date, month, year, and weekday",
            "Merge sales data with external weather data", "Append multiple files into one table",
        ],
    },
    "Reporting preparation": {
        "why": "Use when the same cleaning/transform steps will need to run again on the next batch of data.",
        "items": [
            "Create daily sales tables", "Create bi-weekly order forecast tables",
            "Prepare data for Power BI dashboards", "Build repeatable cleaning workflows",
            "Reduce manual copy-paste reporting work",
        ],
    },
}

COFFEEGO_CASE = {
    "title": "CoffeeGo daily sales — ETL, merge & forecast pipeline",
    "question": "How do you turn scattered daily sales exports, a product reference file, and a live "
                "weather feed into one clean table that's ready for forecasting?",
    "tools": ["Power Query", "Merge Queries", "Web API import", "Custom columns", "Append Queries"],
    "flow": [
        ("Daily CSV exports", "scattered files, two bi-weekly periods"),
        ("Merge ProductList", "adds product name & category"),
        ("Merge weather API", "adds temperature & conditions by date"),
        ("Add custom column", "calculated field on the merged table"),
        ("Clean & output", "forecast-ready table, one-click refresh"),
    ],
    "outcome": "Zero manual copy-paste — re-running it on the next two weeks of files is a one-click refresh.",
}

SQL_TECHNIQUES = {
    "Basic querying": {
        "why": "Use to pull and sort the specific rows and columns a question needs, not the whole table.",
        "items": ["SELECT", "WHERE", "ORDER BY", "LIMIT", "DISTINCT"],
    },
    "Aggregation": {
        "why": "Use when the question is about a total, average, or count — not the individual rows.",
        "items": ["COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY", "HAVING"],
    },
    "Business filters": {
        "why": "Use to apply a business rule (date range, threshold, category) directly in the query, not after the fact in Excel.",
        "items": [
            "Date filtering", "Amount thresholds", "Vendor/category filtering",
            "Country/customer filtering", "Transaction value filtering",
        ],
    },
    "Joins and relationships": {
        "why": "Use when the answer needs information that's split across more than one table.",
        "items": [
            "INNER JOIN", "LEFT JOIN", "Joining customer, invoice, product, order, and transaction tables",
            "Relational database thinking",
        ],
    },
    "Business rule testing": {
        "why": "Use when the goal is finding exceptions to a rule, not describing the data as a whole.",
        "items": [
            "Identify transactions above spending limits", "Identify monthly or yearly overspending",
            "Identify prohibited transaction categories", "Identify possible split transactions",
            "Identify travel-related exceptions", "Rank risk levels using CASE logic",
        ],
    },
    "Advanced logic": {
        "why": "Use when a rule has more than one condition, or needs its own calculated field to test.",
        "items": [
            "Subqueries", "CASE WHEN", "Calculated fields", "Percentage change",
            "Date difference", "Risk ranking",
        ],
    },
}

SQL_EXAMPLES = """-- Question 1: Show all transactions sorted by amount, most expensive first.
-- Display year, month, cardholder name, and the amount.
SELECT year, Month, FullName, Amount
FROM pcards
ORDER BY Amount DESC;

-- Question 2: Narrow to the 2014 calendar year.
-- Sort by month, then by amount (highest first) within each month.
SELECT year, Month, FullName, Amount
FROM pcards
WHERE YEAR = 2014
ORDER BY Month, Amount DESC, FullName;

-- Question 3: Narrow further — 2014 AND amount over $3,000.
-- Same sort logic, now applied to a much smaller, higher-risk set of rows.
SELECT year, Month, FullName, Amount, Vendor
FROM pcards
WHERE YEAR = 2014 AND Amount > 3000
ORDER BY Month, Amount DESC, FullName;

-- Question 4: Narrow to a specific pattern — vendor name contains "Amazon",
-- still 2014 and over $3,000. Sorted ascending to surface the borderline cases first.
SELECT Vendor, FullName, Amount, year, Month
FROM pcards
WHERE YEAR = 2014 AND Amount > 3000 AND Vendor LIKE '%Amazon%'
ORDER BY Amount ASC;"""

PYTHON_CASE = {
    "title": "Customer analytics — from messy data to segments and predictions",
    "question": "With 6,000 customers and over 5,000 missing or invalid data points, which customers are "
                "worth targeting, why are some more likely to churn, and what will they spend next?",
    "tools": ["Random Forest", "KNN Imputation", "PCA", "K-means Clustering", "Logistic Regression",
              "Decision Tree", "Lasso Regression"],
    "process": "Excel/Power BI can chart and filter, but can't reconstruct missing values or compare "
               "five prediction methods to see which one actually fits.",
    "methods": [
        ("Random Forest", "reconstructed 2,352 corrupted \"total spent\" values from a customer's other "
                          "behaviour, since spending patterns are non-linear and a simple average would guess wrong"),
        ("KNN Imputation", "filled missing satisfaction/engagement scores conservatively — based on similar "
                          "customers — so exploratory analysis wasn't distorted by an aggressive guess"),
        ("PCA (Principal Component Analysis)", "compressed dozens of correlated product-preference and "
                          "spending variables into a handful of components before clustering or regression"),
        ("K-means & Hierarchical Clustering", "grouped customers into behavioural segments, cross-checked "
                          "two different ways to make sure the segments were real, not a modelling artifact"),
        ("Decision Tree & Logistic Regression", "explained which features actually drive churn risk and "
                          "predicted which region a customer is likely to belong to, in a form a manager can read"),
        ("Lasso & PCA Regression", "predicted future customer spend while controlling for the multicollinearity "
                          "that a simple linear model would have gotten wrong"),
    ],
    "outcome": "Rather than picking one model upfront, several were run and compared on the same data — "
               "then the segments, predictions, and risk scores were brought into Power BI so a "
               "non-technical manager could act on them without touching Python at all.",
}

PYTHON_METHODS = {
    "Data preparation": {
        "why": "Use before any analysis — untrusted or messy data will quietly break every result built on top of it.",
        "items": [
            "pandas DataFrames", "Data type checks", "Missing value checks", "Duplicate checks",
            "Logical consistency checks", "Standardizing column names", "Transforming date fields",
            "Creating calculated KPI columns",
        ],
    },
    "Data structures": {
        "why": "Use to organize how the code represents the data, before any calculation happens.",
        "items": [
            "Lists for ordered categories", "Dictionaries for lookup relationships",
            "Tuple keys for warehouse\u2013SKU combinations",
            "DataFrames for structured analysis and visualization",
        ],
    },
    "Analysis methods": {
        "why": "Use once the data is clean, to summarize or compare it at a group or category level.",
        "items": [
            "Groupby aggregation", "Inventory turnover calculation", "Reorder point comparison",
            "Forecast accuracy calculation", "Promotion effect analysis", "Profitability analysis",
            "Customer segmentation preparation",
        ],
    },
    "Visualization": {
        "why": "Use when the audience needs to see a pattern, not read a table of numbers.",
        "items": ["Plotly charts", "Heatmaps", "Bar charts", "Scatter plots", "Interactive Dash dashboards"],
    },
    "Machine learning / modelling": {
        "why": "Use when the question is predicting or classifying something the data doesn't state directly.",
        "items": [
            "Random Forest", "KNN imputation", "Linear Regression", "Lasso Regression", "PCA Regression",
            "Decision Tree", "Logistic Regression", "KNN Regression", "K-means clustering",
            "Hierarchical clustering", "Model comparison", "Cross-validation",
        ],
    },
}

R_CASE = {
    "title": "Employee burnout research — from survey data to a tested mechanism",
    "question": "What actually drives burnout in a hybrid, AI-enabled workplace — and do manager support "
                "and autonomy genuinely buffer it, or does that just sound true?",
    "tools": ["Cronbach's Alpha", "CFA", "Regression", "Mediation", "Moderation"],
    "process": "Not just \"is there a relationship\" — is the survey measuring what it claims, why does "
               "the effect exist, and under what conditions does it change.",
    "methods": [
        ("Cronbach's Alpha (reliability screening)", "checked whether the burnout, stress, manager-support, "
                    "and autonomy survey items were internally consistent before trusting them at all — "
                    "all five constructs cleared the 0.70 threshold"),
        ("Confirmatory Factor Analysis (CFA)", "validated that each survey item actually measured its "
                    "intended construct; five weaker items were removed, leaving an excellent-fitting "
                    "measurement model (CFI/TLI = 1.00, RMSEA = .000)"),
        ("Baseline & Extended Regression", "tested whether deadline pressure and work hours predict "
                    "burnout on their own, then whether adding stress, manager support, and autonomy "
                    "explains more of it"),
        ("Mediation Analysis", "tested whether stress is the mechanism connecting deadline pressure to "
                    "burnout — not just whether the two are correlated, but whether one explains the other"),
        ("Moderation Analysis", "tested whether manager support or autonomy weakens the deadline-pressure-"
                    "to-burnout relationship — i.e. does support actually buffer the effect, or only "
                    "reduce burnout on its own"),
    ],
    "outcome": "Deadline pressure turned out to affect burnout mainly through stress (a mediation effect), "
               "while manager support and autonomy reduced burnout directly but didn't significantly "
               "buffer the deadline-pressure effect specifically — a distinction a simple correlation "
               "would have missed entirely.",
}

STATS_METHODS = {
    "Data quality and measurement": {
        "why": "Use before testing any relationship — a shaky measurement makes every later result unreliable.",
        "items": [
            "Missing value checks", "Descriptive statistics", "Skewness and kurtosis review",
            "Cronbach's alpha", "Confirmatory Factor Analysis", "Omega reliability",
            "Construct score creation",
        ],
    },
    "Relationship testing": {
        "why": "Use once measurement is validated, to check whether two things are actually related and how strongly.",
        "items": [
            "Correlation matrix", "OLS regression", "Baseline model", "Extended model",
            "Control variables", "VIF / multicollinearity check", "Residual diagnostics",
        ],
    },
    "Mechanism and condition testing": {
        "why": "Use when a plain relationship isn't enough — the question is why it happens, or when it changes.",
        "items": [
            "Mediation analysis", "Moderation analysis", "Interaction terms", "Simple slopes",
            "Bootstrap confidence intervals", "Model comparison",
        ],
    },
    "Qualitative research support": {
        "why": "Use when numbers alone can't explain the human reasoning behind a pattern.",
        "items": [
            "Semi-structured interviews", "Focus groups", "Diary data", "Qualitative coding",
            "Mixed-method integration",
        ],
    },
}

KPI_GROUPS = {
    "Financial & Accounting Performance": {
        "why": "Use when the audience needs to know if the business itself is healthy — profitability, efficiency, capital structure.",
        "items": [
            "Revenue = Price \u00d7 Quantity",
            "Profit = Revenue - Cost",
            "Profit Margin = Profit / Revenue",
            "Return on Equity = Net Income / Shareholders\u2019 Equity",
            "Asset Turnover = Sales / Total Assets",
            "Financial Leverage = Total Assets / Shareholders\u2019 Equity",
            "DuPont ROE = Profit Margin \u00d7 Asset Turnover \u00d7 Financial Leverage",
        ],
    },
    "Operational & Workforce Diagnostics": {
        "why": "Use to find where in the operation or the workforce a problem is concentrated.",
        "items": [
            "Inventory Turnover = Units Sold / Average Inventory",
            "Lead Time Demand = Average Daily Demand \u00d7 Supplier Lead Time",
            "Reorder Gap = Reorder Point - Lead Time Demand",
            "Stockout Rate = Stockout Days / Total Days",
            "Promotion Lift = (Promotion Sales - Non-Promotion Sales) / Non-Promotion Sales",
            "Burnout Score = Average retained burnout items",
            "Stress Score = Average retained stress items",
            "Manager Support Score = Average retained manager support items",
            "Autonomy Score = Average retained autonomy items",
        ],
    },
    "Relationship & Driver Analysis": {
        "why": "Use when correlation isn't enough — the question is what's actually causing the effect, and under what condition.",
        "items": [
            "Indirect Effect = a-path \u00d7 b-path   (mediation \u2014 is this the mechanism?)",
            "Interaction Effect = X \u00d7 Moderator   (moderation \u2014 does this condition change the effect?)",
        ],
    },
    "Trend-Based Forecasting": {
        "why": "Use for a straightforward projection when the pattern is simple and doesn't need a trained model.",
        "items": [
            "Forecast Error = Actual - Forecast",
            "Absolute Error = |Actual - Forecast|",
            "Percentage Error = (Actual - Forecast) / Actual",
            "MAPE = Average(|Actual - Forecast| / Actual)",
            "Bias = Average(Forecast Error)",
            "Sales Forecast = Intercept + Slope \u00d7 Forecast Temperature",
        ],
    },
    "Classification & Risk Scoring": {
        "why": "Use to sort individuals into a category or risk level based on their characteristics.",
        "items": [
            "Churn Risk = Probability of customer inactivity / loss",
            "Classification Accuracy = Correct Predictions / Total Predictions",
        ],
    },
    "Model-Based Forecasting": {
        "why": "Use when the outcome depends on many interacting variables that a simple trend line can't capture.",
        "items": [
            "Future Spend Prediction = Predicted customer spending in next period",
            "RMSE = Root Mean Squared Error",
            "MAE = Mean Absolute Error",
            "R\u00b2 = Explained Variation / Total Variation",
        ],
    },
}


# -----------------------------------------------------------------------
# TABS
# -----------------------------------------------------------------------

tab_a, tab_b, tab_c, tab_d, tab_e, tab_f, tab_g = st.tabs(
    [
        "A · Business Tools",
        "B · Power BI",
        "C · Power Query / ETL",
        "D · SQL",
        "E · Python",
        "F · Statistics",
        "G · KPIs & Formulas",
    ]
)

# --- A · Business Tools ---
with tab_a:
    eyebrow("Section A")
    st.subheader("Business Tools")
    st.caption("These are the main tools I use to structure, analyse, visualize, and communicate business data.")
    show_image("Tools_overview.png", "Workspace overview: Excel, Power BI, SQL, Python, and Streamlit side by side")
    st.markdown("---")
    for name, desc, when in TOOLS:
        st.markdown(f"**{name}**  \n{desc}")
        st.caption(when)

# --- B · Power BI ---
with tab_b:
    eyebrow("Section B")
    st.subheader("Power BI Measures & Dashboard Logic")
    st.caption("Power BI is useful when business users need to explore results, compare scenarios, and "
               "understand performance through interactive dashboards.")
    show_image("PowerBI_dashboard_overview.png", "Power BI dashboard with KPI cards, slicers, and a scenario/what-if parameter")
    st.markdown("---")
    with st.expander("View measures and dashboard logic"):
        render_grouped(POWERBI_MEASURES)
    with st.expander("DAX / measure examples"):
        st.code(DAX_EXAMPLES, language="dax")

# --- C · Power Query / ETL ---
with tab_c:
    eyebrow("Section C")
    st.subheader("Power Query / ETL Operations")
    st.caption("Turning messy, repeated manual reporting into a structured, reusable workflow.")

    show_image(
        "CoffeeGo_PowerQuery_AppliedSteps.png",
        "CoffeeGo daily sales pipeline — full Applied Steps sequence",
    )

    st.markdown(f"**Typical case: {COFFEEGO_CASE['title']}**")
    st.markdown(COFFEEGO_CASE["question"])
    tool_badges(COFFEEGO_CASE["tools"])
    logic_map(COFFEEGO_CASE["flow"])
    st.markdown(f"**Outcome:** {COFFEEGO_CASE['outcome']}")

    st.markdown("---")

    with st.expander("View full Power Query operations reference"):
        render_grouped(PQ_OPERATIONS)
    st.markdown("> Not just cleaning data once — building a process reusable every time new data arrives.")

# --- D · SQL ---
with tab_d:
    eyebrow("Section D")
    st.subheader("SQL Query Logic")
    st.caption("Narrowing a big database down to a specific, auditable answer — not building one big table.")
    logic_map([
        ("Large database", "e.g. a full year of P-card transactions"),
        ("Overall picture", "totals, trends, rankings across everyone"),
        ("Narrow the question", "add filters: year \u2192 amount \u2192 vendor pattern"),
        ("Audit-ready exceptions", "a short, specific list worth a closer look"),
    ])

    st.markdown("**Step 1 — map the schema first**")
    st.caption("Keys and relationships before any query — otherwise you're guessing at column names, not asking a real question.")
    show_image("SQL_database_ERD.png", "ER diagram — how customers, orders, products, deliveries, returns & interactions connect")

    st.markdown("**Step 2 — turn a question into a query series**")
    show_image("SQL_query_results.png", "P-card audit — each query adds one filter, narrowing all transactions down to the flagged exceptions")
    st.markdown("---")
    with st.expander("View SQL techniques"):
        render_grouped(SQL_TECHNIQUES)
    with st.expander("SQL examples — a question series, not a single query"):
        st.caption("Each query below builds on the one before it by adding another filter.")
        st.code(SQL_EXAMPLES, language="sql")
    st.markdown(
        "> The skill isn't writing a query — it's knowing which question narrows thousands of rows "
        "down to the handful that need a decision."
    )

# --- E · Python ---
with tab_e:
    eyebrow("Section E")
    st.subheader("Python Analytics Methods")
    st.caption("Where spreadsheets and dashboards stop being enough — messy data, or a question that needs a model, not a filter.")

    logic_map([
        ("Too complex for a spreadsheet", "missing data, correlated variables, non-linear behaviour"),
        ("Clean & prepare", "pandas — impute, validate, engineer features"),
        ("Match method to question", "prediction, segmentation, or classification need different tools"),
        ("Compare models", "run several, keep what actually explains the data"),
        ("Hand off the result", "segments/predictions feed into Power BI or Streamlit for the business user"),
    ])

    st.markdown(f"**Case: {PYTHON_CASE['title']}**")
    st.markdown(PYTHON_CASE["question"])
    tool_badges(PYTHON_CASE["tools"])
    st.markdown(f"\n{PYTHON_CASE['process']}")

    with st.expander("Which method, and why"):
        for method, reason in PYTHON_CASE["methods"]:
            st.markdown(f"**{method}** — {reason}")
        st.markdown(f"\n**Outcome**  \n{PYTHON_CASE['outcome']}")

    show_image("Python_notebook_chart.png", "K-means clusters in PCA space — customer segments after reducing correlated variables to 2 components")
    st.markdown("---")

    with st.expander("View full Python methods reference"):
        render_grouped(PYTHON_METHODS)

    st.markdown("---")
    st.markdown("**Case: Bankdata — bank size, regression and robustness**")
    tool_badges(["Python", "Regression", "Interaction terms", "Sensitivity analysis"])
    with st.expander("View the Bankdata technical workflow"):
        st.markdown(
            "**Prepare in Excel / Power Query** — structure financial data, calculate KPIs, "
            "attach group and sample flags, and distinguish bank-year observations from bank-level values."
        )
        st.markdown(
            "**Model in Python** — test affiliation with bank size as a control, then add "
            "affiliation-by-size interactions to test moderation. Compare the relevant sample "
            "specifications rather than selecting only the most significant model."
        )
        st.markdown(
            "**Report** — keep coefficients, uncertainty, model fit, sample definitions, and "
            "business interpretation together. Treat the models as association analysis."
        )
        st.caption("Method summary; no reconstructed code is presented as the original analysis script.")
        st.page_link("pages/5_Research_Based_Problem_Solving.py", label="Read the Bankdata research case →")
        download_bankdata_case()

# --- F · Statistics ---
with tab_f:
    eyebrow("Section F")
    st.subheader("Statistical & Research Methods")
    st.caption("Not just \"what happened\" — is the relationship real, why does it happen, and does it hold under different conditions.")

    logic_map([
        ("Survey / raw data", "multi-item scales for each construct"),
        ("Check reliability", "Cronbach's alpha \u2014 are the items even consistent?"),
        ("Validate measurement", "CFA \u2014 do items measure what they claim to?"),
        ("Test the relationship", "baseline \u2192 extended regression"),
        ("Test why & when", "mediation (mechanism) + moderation (condition)"),
        ("Recommend", "translate into a management decision"),
    ])

    st.markdown(f"**Case: {R_CASE['title']}**")
    st.markdown(R_CASE["question"])
    tool_badges(R_CASE["tools"])
    st.markdown(f"\n{R_CASE['process']}")

    with st.expander("Which method, and why"):
        for method, reason in R_CASE["methods"]:
            st.markdown(f"**{method}** — {reason}")
        st.markdown(f"\n**Outcome**  \n{R_CASE['outcome']}")

    show_image("R_output_regression.png", "R output for the burnout study — reliability, CFA fit, or mediation/moderation results")
    st.markdown("---")

    with st.expander("View full statistical & research methods reference"):
        render_grouped(STATS_METHODS)

    st.markdown("---")
    st.markdown("**Bankdata — matching the test to the question**")
    with st.expander("View financial benchmarking methods and their purpose"):
        st.markdown("""
| Method | Purpose in Case 2 |
| --- | --- |
| Group medians | Describe typical KPI levels while limiting the influence of extreme values. |
| Kruskal–Wallis | Test rank-based distributional differences across the three groups; it is not automatically a test of medians. |
| Effect size | Describe the magnitude of group differences alongside statistical significance. |
| Dunn's post-hoc comparisons | Identify relevant pairwise differences after an appropriate overall test, accounting for multiple comparisons. |
| Bank-level / mortgage sensitivity checks | Assess whether the observation unit or sample composition changes the interpretation. |
| Size-adjusted regression | Examine affiliation differences while accounting for bank size. |
| Affiliation × size interactions | Test whether the association changes with bank size. |
""")
        st.caption("Operational mediation is a future research proposal, not a completed test in Case 2.")

# --- G · KPIs & Formulas ---
with tab_g:
    eyebrow("Section G")
    st.subheader("Business Formulas and KPIs")
    st.caption("Formulas grouped by the business function they serve — financial performance, operational "
               "diagnostics, root-cause analysis, and forecasting (trend-based or model-based).")
    for group, data in KPI_GROUPS.items():
        with st.expander(group):
            st.caption(data["why"])
            for formula in data["items"]:
                st.markdown(f"`{formula}`")

st.markdown("---")
eyebrow("One more thing")
st.caption(
    "Full code, notebooks, and query files for the projects referenced above are available on the "
    "**Downloads** page and in the linked GitHub repository."
)