# loads library and read csv files
import pandas as pd 
from pathlib import Path # path helps to build file paths 

# find the folder DP_final_project
def get_base_dir() -> Path:
    """
    Robust base dir resolver.
    Works when running as a script AND in notebooks/interactive sessions.
    """
    try:
        return Path(__file__).resolve().parent.parent
    except NameError:
        # __file__ not defined (e.g., Jupyter). Use current working directory.
        return Path.cwd()
#__file__ eqal to the full path of the script
#.resolve() convert path into an absolute path
#.parent moves one folder up

# build Path to the CSV file
# BASE_DIR = DP_final_project
def get_csv_path() -> Path:
    base_dir = get_base_dir()
    return base_dir / "data" / "supply_chain_dataset.csv"

# ------------------------------------------------------------
# 1. DATA CLEANING
# ------------------------------------------------------------
def check_data(df: pd.DataFrame) -> None:
    """
    Check dataset quality:
    - Missing values
    - Duplicated rows
    - Duplicated dates (if exists)
    - Negative numeric values
    """

    print("=== DATA QUALITY REPORT ===\n")
    print("Missing values per column:")
    print(df.isnull().sum())
    print("\nTotal missing values:", df.isnull().sum().sum())
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

# -------------------------------------------------------
# 2) CLEAN FUNCTION — formatting + type conversion only
# -------------------------------------------------------

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare dataset WITHOUT removing or imputing:
    - Standardize column names (lowercase, underscore)
    - Convert Date column to datetime
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
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )
    # Convert date to datetime
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Convert numeric-like columns
    for col in df.columns:
        if df[col].dtype == "object":
            try:
             df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
            # leave column unchanged if conversion fails
                pass
    return df

def load_clean_data(run_check: bool = False, csv_path: Path | None = None):
    csv_path = csv_path or get_csv_path()
    df = pd.read_csv(csv_path)
    if run_check:
        check_data(df)
    df_clean = clean_data(df)
    if df_clean is None:
        raise ValueError("clean_data() returned None — check return statement")
    return df_clean

df_clean = load_clean_data()

# data modelling
# RQ1-INVENTORY
def rq1_lists_and_maps(df_clean):
    """
    lists and mapping dictionaries for rq1
    warehouse_list,
    sku_list,
    warehouse_sku_dict,
    sku_warehouse_dict,
    sku_daily_demand_dict,
    wh_sku_lead_dict,
    wh_sku_reorder_dict
    """
    df = df_clean.copy()
    df["sku_id"] = df["sku_id"].astype(str)
    df["warehouse_id"] = df["warehouse_id"].astype(str)
    # extract number from an ID string for further list ordering
    def extract_number(text):
        """
        Extract digits from a string and convert them to an integer.
        """
        digits = []
        for char in text:
            if char.isdigit():
                digits.append(char)
        return int("".join(digits))
    
    warehouse_list = sorted(
        df["warehouse_id"].unique().tolist(),
        key=extract_number)
    sku_list = sorted(
        df["sku_id"].unique().tolist(),
        key=extract_number)
    warehouse_sku_dict = {}
    sku_warehouse_dict = {}
    sku_demand = {}
    wh_sku_lead_dict = {}
    wh_sku_reorder_dict = {}
    for _, row in df_clean.iterrows():
        wh = row["warehouse_id"]
        sku = row["sku_id"]
        units = row["units_sold"]
        # warehouse -> SKUs
        if wh not in warehouse_sku_dict:
            warehouse_sku_dict[wh] = []
        if sku not in warehouse_sku_dict[wh]:
            warehouse_sku_dict[wh].append(sku)
        # SKU -> warehouses
        if sku not in sku_warehouse_dict:
            sku_warehouse_dict[sku] = []
        if wh not in sku_warehouse_dict[sku]:
            sku_warehouse_dict[sku].append(wh)
        # SKU daily demand
        if sku not in sku_demand:
            sku_demand[sku] = []
        sku_demand[sku].append(units)
        # (warehouse,sku) -> lead time/reorder point
        pair = (wh, sku)#use tuples as key, cus it is immutale
        if pair not in wh_sku_lead_dict:
            wh_sku_lead_dict[pair] = row["supplier_lead_time_days"]
        if pair not in wh_sku_reorder_dict:
            wh_sku_reorder_dict[pair] = row["reorder_point"]
    # convert SKU demand list → average
    sku_daily_demand_dict = {}
    for sku in sku_demand:
        sku_daily_demand_dict[sku] = sum(sku_demand[sku]) / len(sku_demand[sku])

    return (
    warehouse_list,
    sku_list,
    warehouse_sku_dict,
    sku_warehouse_dict,
    sku_daily_demand_dict,
    wh_sku_lead_dict,
    wh_sku_reorder_dict, 
    )

#  RQ2
def supplier_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates metrics per supplier:
    - Avg lead time
    - Avg order quantity
    - Avg unit cost
    - Total orders
    """
    summary = (
        df.groupby("supplier_id")
        .agg(
            avg_lead_time=("supplier_lead_time_days", "mean"),
            avg_order_qty=("order_quantity", "mean"),
            avg_unit_cost=("unit_cost", "mean"),
            total_orders=("order_quantity", "count"),
        )
        .reset_index()
    )
    return summary


# -------------------------------------------------
# Correlation-ready dataset
# -------------------------------------------------
def leadtime_order_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Dataset for correlation analysis
    """
    return df[
        [
            "supplier_id",
            "supplier_lead_time_days",
            "order_quantity",
            "unit_cost",
        ]
    ].dropna()

### RQ3 FORECASTS AND PROMOTION ANALYSIS 
# Count monthly totals
### RQ3 FORECASTS AND PROMOTION ANALYSIS 
# Count monthly totals
def monthly_aggregation(df_clean: pd.DataFrame) -> pd.DataFrame:
    monthly_df = (
        df_clean.groupby(df_clean["date"].dt.to_period("M"))
        .agg({"units_sold": "sum", "demand_forecast": "sum"})
        .reset_index()
    )
    monthly_df["date"] = monthly_df["date"].dt.to_timestamp()
    return monthly_df
monthly_df = monthly_aggregation(df_clean)
# Prepare zipped data for SKU + warehouse
def prepare_selected_data(df_clean: pd.DataFrame):
    actual_units_sold_list = df_clean["units_sold"].tolist()
    forecast_units_list = df_clean["demand_forecast"].tolist()
    sku_id_list = df_clean["sku_id"].tolist()
    warehouse_id_list = df_clean["warehouse_id"].tolist()

    selected_data = [
        {"sku_id": s, "warehouse_id": w, "units_sold": u, "demand_forecast": f}
        for s, w, u, f in zip(sku_id_list, warehouse_id_list, actual_units_sold_list, forecast_units_list)
    ]
    return selected_data
prepare_selected_data(df_clean)
selected_data = prepare_selected_data(df_clean)
# MAPE function
def mape_func(selected_data):
    results = []
    for item in selected_data:
        sku_id = item["sku_id"]
        warehouse_id = item["warehouse_id"]
        units_sold = item["units_sold"]
        demand_forecast = item["demand_forecast"]

        if units_sold == 0:
            mape = None
            skipped = True
        else:
            mape = abs(units_sold - demand_forecast) / units_sold * 100
            skipped = False

        results.append((sku_id, warehouse_id, mape, skipped))
    return results
mape_func(selected_data)
results = mape_func(selected_data)
print(results[:5])
# MAPE by SKU per warehouse
def mape_by_sku_warehouse_df(selected_data, results):
    vis_df = pd.DataFrame(results, columns=["sku_id", "warehouse_id", "MAPE", "Skipped"])
    vis_df = vis_df.drop(columns=["Skipped"])
    return vis_df
vis_df = mape_by_sku_warehouse_df(selected_data, results)
print(vis_df.head())
# Pivot table for warehouse vs SKU
def pivot_mape(vis_df):
    pivot_df = vis_df.pivot_table(
        index="warehouse_id",
        columns="sku_id",
        values="MAPE",
        aggfunc="mean"
    )
    return pivot_df
pivot_df = pivot_mape(vis_df)
print(pivot_df.head())
# Add sales value and profit
def add_sales_profit(df_clean: pd.DataFrame) -> pd.DataFrame:
    df_clean["sales_value"] = df_clean["units_sold"] * df_clean["unit_price"]
    df_clean["profit"] = df_clean["units_sold"] * (df_clean["unit_price"] - df_clean["unit_cost"])
    return df_clean
add_sales_profit(df_clean)
df_clean = add_sales_profit(df_clean)
print(df_clean.head())
# Promotion impact analysis
def promotion_analysis(df_clean: pd.DataFrame):
    grouped = (
        df_clean.groupby(["sku_id", "promotion_flag"])
        .agg({"units_sold": "mean", "sales_value": "mean", "profit": "mean"})
        .reset_index()
    )
    pivoted = grouped.pivot_table(
        index="sku_id",
        columns="promotion_flag",
        values=["units_sold", "sales_value", "profit"]
    )
    return grouped, pivoted
promotion_analysis(df_clean)
grouped, pivoted = promotion_analysis(df_clean)
print(grouped.head())
print(pivoted.head())

#rq4-lists and maps
# LISTS AND DICTS FOR RQ4
from typing import Any, Dict, List, Tuple

## First I build the lists
def build_rq4_lists(df: pd.DataFrame) -> Dict[str, List[Any]]:
    """
    Build row-aligned lists for RQ4.
    Lists preserve order, enabling row-wise KPI calculations.
    """
    lists = {
        "unit_price": df["unit_price"].tolist(),
        "unit_cost": df["unit_cost"].tolist(),
        "units_sold": df["units_sold"].tolist(),
        "inventory_level": df["inventory_level"].tolist(),
        "stockout_flag": df["stockout_flag"].tolist(),
        "supplier_lead_time_days": df["supplier_lead_time_days"].tolist(),
        "region": df["region"].tolist(),
        "sku_id": df["sku_id"].tolist(),
    }
    return lists

# Then I build KPIs using the lists
def compute_row_kpis_from_lists(lists: Dict[str, List[Any]]) -> Dict[str, List[float]]:
    """
    Compute row-level KPIs using parallel lists (row-aligned).
    """
    unit_price = lists["unit_price"]
    unit_cost = lists["unit_cost"]
    units_sold = lists["units_sold"]
    inventory_level = lists["inventory_level"]

    profit = []
    margin = []
    profit_per_inventory_unit = []

    for i in range(len(units_sold)):
        ppu = unit_price[i] - unit_cost[i]
        p = ppu * units_sold[i]
        profit.append(p)

        m = (ppu / unit_price[i]) if unit_price[i] else 0.0
        margin.append(m)

        eff = (p / inventory_level[i]) if inventory_level[i] else 0.0
        profit_per_inventory_unit.append(eff)

    return {
        "profit": profit,
        "profit_margin": margin,
        "profit_per_inventory_unit": profit_per_inventory_unit,
    }

# Now I create grouping dictionaries for region and SKU
def build_rq4_group_dicts(
    lists: Dict[str, List[Any]],
    row_kpis: Dict[str, List[float]]
) -> Tuple[Dict[str, Dict[str, float]], Dict[str, Dict[str, float]]]:
    """
    Build grouping dictionaries:
    - region_kpis: KPIs grouped by region
    - sku_kpis: KPIs grouped by SKU
    """
    regions = lists["region"]
    skus = lists["sku_id"]
    stockout = lists["stockout_flag"]
    lead = lists["supplier_lead_time_days"]

    profit = row_kpis["profit"]
    margin = row_kpis["profit_margin"]
    eff = row_kpis["profit_per_inventory_unit"]

    region_kpis: Dict[str, Dict[str, float]] = {}
    sku_kpis: Dict[str, Dict[str, float]] = {}

    def _init_bucket() -> Dict[str, float]:
        return {
            "total_profit": 0.0,
            "sum_margin": 0.0,
            "sum_efficiency": 0.0,
            "stockout_count": 0.0,
            "sum_lead_time": 0.0,
            "n": 0.0
        }

    for i in range(len(profit)):
        r = regions[i]
        s = skus[i]

        region_kpis.setdefault(r, _init_bucket())
        sku_kpis.setdefault(s, _init_bucket())

        for bucket in (region_kpis[r], sku_kpis[s]):
            bucket["total_profit"] += profit[i]
            bucket["sum_margin"] += margin[i]
            bucket["sum_efficiency"] += eff[i]
            bucket["stockout_count"] += 1.0 if stockout[i] else 0.0
            bucket["sum_lead_time"] += float(lead[i])
            bucket["n"] += 1.0

    # Convert sums to averages and rates for 
    for d in (region_kpis, sku_kpis):
        for key, b in d.items():
            n = b["n"] if b["n"] else 1.0
            b["avg_margin"] = b["sum_margin"] / n
            b["avg_efficiency"] = b["sum_efficiency"] / n
            b["stockout_rate"] = b["stockout_count"] / n
            b["avg_lead_time"] = b["sum_lead_time"] / n

            # Drop raw sums to keep dict clean
            del b["sum_margin"], b["sum_efficiency"], b["sum_lead_time"]

    return region_kpis, sku_kpis

# Multi-dimensional structure with nested dicts
def build_rq4_nested_dict(
    lists: Dict[str, List[Any]],
    row_kpis: Dict[str, List[float]]
) -> Dict[str, Dict[str, Dict[str, float]]]:
    """
    Nested dictionary:
    outer key = sku_id
    inner key = region
    values = aggregated KPIs
    """
    skus = lists["sku_id"]
    regions = lists["region"]
    stockout = lists["stockout_flag"]
    lead = lists["supplier_lead_time_days"]

    profit = row_kpis["profit"]
    margin = row_kpis["profit_margin"]
    eff = row_kpis["profit_per_inventory_unit"]

    nested: Dict[str, Dict[str, Dict[str, float]]] = {}

    def _init_bucket() -> Dict[str, float]:
        return {"total_profit": 0.0, "sum_margin": 0.0, "sum_efficiency": 0.0,
                "stockout_count": 0.0, "sum_lead_time": 0.0, "n": 0.0}

    for i in range(len(profit)):
        s, r = skus[i], regions[i]
        nested.setdefault(s, {})
        nested[s].setdefault(r, _init_bucket())

        b = nested[s][r]
        b["total_profit"] += profit[i]
        b["sum_margin"] += margin[i]
        b["sum_efficiency"] += eff[i]
        b["stockout_count"] += 1.0 if stockout[i] else 0.0
        b["sum_lead_time"] += float(lead[i])
        b["n"] += 1.0


    for s in nested:
        for r in nested[s]:
            b = nested[s][r]
            n = b["n"] if b["n"] else 1.0
            b["avg_margin"] = b["sum_margin"] / n
            b["avg_efficiency"] = b["sum_efficiency"] / n
            b["stockout_rate"] = b["stockout_count"] / n
            b["avg_lead_time"] = b["sum_lead_time"] / n
            del b["sum_margin"], b["sum_efficiency"], b["sum_lead_time"]

    return nested

# Finally, I build lists of dictionaries for plotting and visualization
def nested_to_records(nested: Dict[str, Dict[str, Dict[str, float]]]) -> List[Dict[str, Any]]:
    """
    Convert nested dict into list-of-dicts (tidy records) for easy plotting.
    """
    records: List[Dict[str, Any]] = []
    for sku, region_map in nested.items():
        for region, kpi in region_map.items():
            records.append({
                "sku_id": sku,
                "region": region,
                **kpi
            })
    return records