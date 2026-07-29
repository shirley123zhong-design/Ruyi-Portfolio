import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np
import analysis.data_modeling as dm 
#---------------------- -------------------------------------------------
# What is the forecasting accuracy (MAPE) across SKUs and warehouses, and how do promotions affect sales value and profitability? 
# --------------------------------------------------------
# STEP 3.1: calculating general MAPE using lists because we are comparing sequences of values
# --------------------------------------------------------
def rq3_general_mape(selected_data):
    selected_data_records = selected_data.to_dict("records") if hasattr(selected_data, "to_dict") else selected_data
    results = dm.mape_func(selected_data_records)
    # extract only valid MAPE values
    valid_mape_values = [m[2] for m in results if m[2] is not None]
    general_mape = sum(valid_mape_values) / len(valid_mape_values)
    return general_mape

### VISUALISATION line chart
def rq3_general_accuracy_fig(monthly_df: pd.DataFrame):
    """
    Line chart (monthly sums): forecast vs actual.
    Returns Plotly figure (fig, monthly_df).
    """
    fig = px.line(
        monthly_df,
        x="date",
        y=["demand_forecast", "units_sold"],
        markers=True,
        labels={"value": "Quantity", "date": "Month", "variable": "Series"},
        title="Forecast vs Actual Over Time"
    )
    return fig


###--------------------------------------------------------
### STEP 3.1.2: calculating MAPE using a list of dictionaries to group SKUs and warehouses
###--------------------------------------------------------

def rq3_mape_by_sku_warehouse(selected_data):
    results = {}
    grouped = {}   # new plain dictionaries

    # group rows by sku_id and warehouse_id
    for row in selected_data:
        key = (row["sku_id"], row["warehouse_id"])
        if key not in grouped:
            grouped[key] = []      # initialise list manually
        grouped[key].append(row)

    # calculating MAPE for each group
    for key, rows in grouped.items():
        actual = np.array([r["units_sold"] for r in rows])
        forecast = np.array([r["demand_forecast"] for r in rows])

        mask = actual != 0
        skipped = (~mask).sum()

        if mask.sum() == 0:
            results[key] = {"MAPE": None, "Skipped": skipped}
        else:
            mape_value = (np.abs((actual[mask] - forecast[mask]) / actual[mask])).mean() * 100
            results[key] = {"MAPE": mape_value, "Skipped": skipped}

    return results

### VISUALISATION heatmap/matrix
def rq3_mape_heatmap_fig(mape_df: pd.DataFrame):
    """
    Heatmap: warehouse_id x sku_id, values = MAPE%.
    """
    pivot_df = mape_df.pivot_table(
        index="warehouse_id",
        columns="sku_id",
        values="MAPE",
        aggfunc="mean"
    )
    fig = px.imshow(
        pivot_df,
        aspect="auto",
        title="MAPE% by SKU and Warehouse",
        labels={"x": "SKU", "y": "Warehouse", "color": "MAPE%"},
    )
    return fig, pivot_df

###--------------------------------------------------------
# STEP 3.2: analyzing promotions' effect on sales value and profitability
# --------------------------------------------------------
### for that we havee 3 parameters: units sold, sales value and profit
# units sold is already in the dataset as units_sold
# sales value = units_sold * unit_price
# profit = sales value - (units_sold * unit_cost)
# then we devided the dataset into 2 parts: promotion period and no promotion period 
def rq3_promotion_overall_summary(df_clean: pd.DataFrame) -> pd.DataFrame:
    """
    Mean performance during promotion vs no promotion periods.
    Performance is measured by units_sold, sales_value and profit.
    Returns a 2-row dataframe (index: Promotion, No Promotion).
    """
    promo = df_clean[df_clean["promotion_flag"] == True]
    no_promo = df_clean[df_clean["promotion_flag"] == False]

    summary = pd.DataFrame({
        "Units_Sold": [promo["units_sold"].mean(), no_promo["units_sold"].mean()],
        "Sales_Value": [promo["sales_value"].mean(), no_promo["sales_value"].mean()],
        "Profit": [promo["profit"].mean(), no_promo["profit"].mean()],
    }, index=["Promotion", "No Promotion"])

    return summary

# VISUALISATION bar chart

def rq3_promo_overall_bar_fig(summary_df: pd.DataFrame):
    """
    Shows performance during promotion vs no promotion periods.
    """
    long_df = summary_df.reset_index().melt(
        id_vars="index",
        var_name="Metric",
        value_name="Value"
    ).rename(columns={"index": "Period"}
             )
    fig = px.bar(
        long_df,
        x="Metric",
        y="Value",
        color="Period",
        barmode="group",
        title="Performance During Promotion vs No Promotion (Mean Values)",
    )
    return fig

#---------------------------------------------------------
# STEP 3.2.1: grouped analysis by sku_id 
#---------------------------------------------------------
def rq3_promo_impact(pivoted):
    # rename columns
    pivoted.columns = [f"{m}_{'Promo' if f==1 else 'NoPromo'}" for m, f in pivoted.columns]
    pivoted = pivoted.reset_index()
    
    # calculate impacts
    pivoted["Units_Sold_Impact_%"] = (pivoted["units_sold_Promo"] - pivoted["units_sold_NoPromo"]) / pivoted["units_sold_NoPromo"] * 100
    pivoted["Sales_Value_Impact_%"] = (pivoted["sales_value_Promo"] - pivoted["sales_value_NoPromo"]) / pivoted["sales_value_NoPromo"] * 100
    pivoted["Profit_Impact_%"] = (pivoted["profit_Promo"] - pivoted["profit_NoPromo"]) / pivoted["profit_NoPromo"] * 100
    
    return pivoted.round(2)

# VISUALISATION bar chart for promotion impact by SKU

def rq3_promotion_by_sku_fig(sku_impact_df: pd.DataFrame, top_n: int = 10):
    """
    Bar chart: top N SKUs by promotion impact on profit.
    """
    df = sku_impact_df.copy()
    df["abs_profit_impact"] = df["Profit_Impact_%"].abs()
    df = df.sort_values("abs_profit_impact", ascending=False).head(top_n) # and we chose top 10 just above

    long_df = df.melt(
        id_vars=["sku_id"],
        value_vars=["Units_Sold_Impact_%", "Sales_Value_Impact_%", "Profit_Impact_%"],
        var_name="Metric",
        value_name="Impact_%"
    )

    fig = px.bar(
        long_df,
        x="sku_id",
        y="Impact_%",
        color="Metric",
        barmode="group",
        title=f"Top {top_n} SKUs by Promotion Impact",
    )
    fig.update_layout(xaxis_title="SKU", yaxis_title="Impact (%)")
    return fig

# local test
if __name__ == "__main__":

    print("Running RQ3 standalone tests...")

    # Prepare data
    df_clean = dm.df_clean
    selected_data = dm.prepare_selected_data(df_clean)

    # Test RQ3.1: General MAPE
    general_mape = rq3_general_mape(selected_data)
    print("General MAPE:", round(general_mape, 2) if general_mape is not None else "No valid MAPE")

    # Test RQ3.1 Visualization
    monthly_df = dm.monthly_aggregation(df_clean)
    fig1 = rq3_general_accuracy_fig(monthly_df)
    fig1.show()

    # Test RQ3.2: MAPE by SKU & Warehouse
    mape_dict = rq3_mape_by_sku_warehouse(selected_data)
    mape_df = pd.DataFrame(
        [{"sku_id": k[0], "warehouse_id": k[1], "MAPE": v["MAPE"]} for k, v in mape_dict.items()]
    ).dropna()

    fig2, _ = rq3_mape_heatmap_fig(mape_df)
    fig2.show()

    # Test RQ3.3: Promotion summary
    df_clean = dm.add_sales_profit(df_clean)
    promo_summary = rq3_promotion_overall_summary(df_clean)
    print("\nPromotion summary:")
    print(promo_summary)

    fig3 = rq3_promo_overall_bar_fig(promo_summary)
    fig3.show()

    # Test RQ3.4: Promotion impact by SKU
    grouped, pivoted = dm.promotion_analysis(df_clean)
    pivoted.columns = pd.MultiIndex.from_tuples([(m, int(f)) for (m, f) in pivoted.columns])

    sku_impact = rq3_promo_impact(pivoted)
    print("\nPromotion impact (head):")
    print(sku_impact.head())

    fig4 = rq3_promotion_by_sku_fig(sku_impact, top_n=10)
    fig4.show()

    print("RQ3 tests completed.")
