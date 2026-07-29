import pandas as pd
import plotly.express as px

# RQ4: Regional profitability differences with KPIs
def get_rq4_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build SKU+Region KPIs used for RQ4 visuals.

    Expected columns in df (cleaned, lowercase):
    - sku_id, region, unit_price, unit_cost, units_sold
    - inventory_level, stockout_flag, supplier_lead_time_days
    """
    d = df.copy()

    # Row-level computations
    d["profit_per_unit"] = d["unit_price"] - d["unit_cost"]
    d["total_profit"] = d["profit_per_unit"] * d["units_sold"]
    d["sales_value"] = d["unit_price"] * d["units_sold"]

    # Aggregate to SKU+Region level
    kpis = (
        d.groupby(["sku_id", "region"], as_index=False)
        .agg(
            total_profit=("total_profit", "sum"),
            total_units_sold=("units_sold", "sum"),
            avg_unit_price=("unit_price", "mean"),
            avg_unit_cost=("unit_cost", "mean"),
            avg_inventory=("inventory_level", "mean"),
            stockout_rate=("stockout_flag", "mean"),  # if bool 0-1: the average boolean value gives the stockout rate
            avg_lead_time=("supplier_lead_time_days", "mean"),
            sales_value=("sales_value", "sum"),
        )
    )

    # Profit margin (avoid division by zero)
    kpis["profit_margin"] = kpis["total_profit"] / kpis["sales_value"].replace(0, pd.NA)
    kpis["profit_margin"] = kpis["profit_margin"].fillna(0)

    # Profit per average inventory unit
    kpis["profit_per_inventory_unit"] = kpis["total_profit"] / kpis["avg_inventory"].replace(0, pd.NA)
    kpis["profit_per_inventory_unit"] = kpis["profit_per_inventory_unit"].fillna(0)

    return kpis

# Clustered bar chart of SKU profit by region
def plot_clustered_sku_profit_by_region(
    kpis: pd.DataFrame,
    top_n: int = 10
):
    """
    Clustered bar chart of top N SKUs by total profit, split by region.
    """
    # Get top N SKUs by total profit
    top_skus = (
        kpis.groupby("sku_id")["total_profit"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .index
    )

    d = kpis[kpis["sku_id"].isin(top_skus)].copy()

    fig = px.bar(
        d,
        x="sku_id",
        y="total_profit",
        color="region",
        barmode="group",
        labels={
            "sku_id": "SKU",
            "total_profit": "Total Profit",
            "region": "Region",
        },
        title=f"Top {top_n} SKU Profit Comparison by Region",
        height=600,
        width=900,
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig  

# Stacked bar chart of SKU profit by region
def plot_stacked_sku_profit_by_region(kpis: pd.DataFrame):
    """
      Stacked bar chart: Each bar represents a region, stacked by SKU contribution.
    """
    fig = px.bar(
        kpis,
        x="region", 
        y="total_profit",
        color="sku_id",
        barmode="stack",
        labels={
            "total_profit": "Total Profit",
            "sku_id": "SKU",
            "region": "Region",
        },
        title="Stacked SKU Profit by Region",
        height=600,
        width=900,
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig

# Scatter plot that links SKU profitability to inventory efficiency/stockout rate
def plot_scatter_stockouts_vs_margin(kpis: pd.DataFrame):
    """
    Scatter: Stockout rate vs profit margin (size by total profit, color by region).
    """
    fig = px.scatter(
        kpis,
        x="stockout_rate",
        y="profit_margin",
        color="region",
        size="total_profit",
        hover_data=["sku_id", "total_units_sold", "avg_inventory", "avg_lead_time", "profit_per_inventory_unit"],
        title="Stockout Rate vs Profit Margin",
        labels={
            "stockout_rate": "Stockout Rate",
            "profit_margin": "Profit Margin",
            "region": "Region",
            "total_profit": "Total Profit",
        },
        height=600,
        width=900,
    )
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=60, b=20))

    return fig
