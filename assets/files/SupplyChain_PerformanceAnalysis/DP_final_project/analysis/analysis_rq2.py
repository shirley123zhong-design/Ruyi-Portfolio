# analysis_rq.py
import plotly.express as px
import pandas as pd

# -------------------------------------------------
# Correlation calculation
# -------------------------------------------------
def compute_correlation(df_corr: pd.DataFrame) -> float:
    """
    Pearson correlation between lead time and order quantity
    """
    return df_corr["supplier_lead_time_days"].corr(
        df_corr["order_quantity"]
    )


# -------------------------------------------------
# Visualizations
# -------------------------------------------------
def scatter_leadtime_vs_order(df_corr: pd.DataFrame):
    fig = px.scatter(
        df_corr,
        x="supplier_lead_time_days",
        y="order_quantity",
        color="supplier_id",
        title="Supplier Lead Time vs Order Quantity",
        labels={
            "supplier_lead_time_days": "Supplier Lead Time (Days)",
            "order_quantity": "Order Quantity",
        },
        # trendline="ols",  # <- remove this
    )
    fig.update_layout(template="plotly_white")
    return fig


def bar_avg_order_by_supplier(df_summary: pd.DataFrame):
    fig = px.bar(
        df_summary,
        x="supplier_id",
        y="avg_order_qty",
        title="Average Order Quantity by Supplier",
        labels={"avg_order_qty": "Average Order Quantity"},
        text=df_summary["avg_order_qty"].round(1),
    )
    fig.update_layout(template="plotly_white")
    return fig


def bar_avg_cost_by_supplier(df_summary: pd.DataFrame):
    fig = px.bar(
        df_summary,
        x="supplier_id",
        y="avg_unit_cost",
        title="Average Unit Cost by Supplier",
        labels={"avg_unit_cost": "Average Unit Cost"},
        text=df_summary["avg_unit_cost"].round(2),
    )
    fig.update_layout(template="plotly_white")
    return fig


def heatmap_supplier_metrics(df_summary: pd.DataFrame):
    heat_df = df_summary.set_index("supplier_id")[
        ["avg_lead_time", "avg_order_qty", "avg_unit_cost"]
    ]

    fig = px.imshow(
        heat_df,
        text_auto=".2f",
        color_continuous_scale="Blues",
        title="Supplier Metrics Heatmap",
    )
    fig.update_layout(template="plotly_white")
    return fig













