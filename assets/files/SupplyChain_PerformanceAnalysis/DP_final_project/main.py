import pandas as pd
import dash
from dash import dcc, html, Input, Output
from dash import dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np

###  modules
import analysis.data_modeling as dm 
import analysis.analysis_rq1 as vis_rq1
import analysis.analysis_rq2 as vis_rq2
import analysis.analysis_rq3 as vis_rq3
import analysis.analysis_rq4 as vis_rq4
# load in the cleaned dataset
df_clean = dm.load_clean_data(run_check=False)

# CAll RQ1, lists and dicts
(warehouse_list,sku_list,warehouse_sku_dict,sku_warehouse_dict,sku_daily_demand_dict,wh_sku_lead_dict,wh_sku_reorder_dict,) = dm.rq1_lists_and_maps(df_clean)
warehouse_turnover_df, sku_turnover_df = vis_rq1.build_turnover_tables(df_clean)
# title and information
title_rq1 = "RQ1: Inventory Turnover and Reorder Point Alignment"
text_rq1 = [
    "This section analyzes ",
    html.Br(),
    "(1) inventory turnover per warehouse, ",
    html.Br(),
    "(2) Inventory Turnover per Warehouse (SKU-specific view) ",
    html.Br(),
    "(3) Safety Stock Status Table (Warehouse × SKU)",
    html.Br(),
    "(4) reorder gap Alignment Ratio vs Lead-Time Demand (Heatmap) ",]

# Figure 1a: Inventory turnover per warehouse (bar)
fig_rq1= vis_rq1.make_warehouse_turnover_fig(df_clean)
rq1_plot_id = "rq1-turnover-warehouse"
# Figure 1b: Inventory turnover per SKU warehouse (bar) with input function
# for rq1, drop down
_, sku_options, _, _, _, _, _  = dm.rq1_lists_and_maps(df_clean)
default_sku = sku_options[0] if sku_options else None
fig_rq1b = vis_rq1.make_sku_turnover_fig(sku_turnover_df, default_sku)
rq1b_plot_id = "rq1-turnover-sku"
#Figure 1c: stock level table
safety_status_df = vis_rq1.build_safety_stock_status_table(
    df_clean,
    sku_daily_demand_dict,
    wh_sku_lead_dict,
    wh_sku_reorder_dict,
    aligned_low=0.9,
    aligned_high=1.1,
)

rq1_table_id = "rq1-safety-status-table"
rq1_wh_filter_id = "rq1-warehouse-filter"
rq1_sku_filter_id = "rq1-sku-filter"
# Figure 1d: Heatmap / Matrix – Reorder Gap vs Lead-time Demand (binned)
fig_rq1c = vis_rq1.make_safety_stock_binned_heatmap_fig(df_clean,sku_daily_demand_dict,wh_sku_lead_dict,wh_sku_reorder_dict)
rq1c_plot_id = "rq1-safety-stock-heatmap"

#CALL RQ2
df = dm.load_clean_data()
df_corr = dm.leadtime_order_dataset(df)
supplier_df = dm.supplier_summary(df)

# Correlation
corr_value = vis_rq2.compute_correlation(df_corr)

# Figures
fig_scatter = vis_rq2.scatter_leadtime_vs_order(df_corr)
fig_bar_qty = vis_rq2.bar_avg_order_by_supplier(supplier_df)
fig_bar_cost = vis_rq2.bar_avg_cost_by_supplier(supplier_df)
fig_heatmap = vis_rq2.heatmap_supplier_metrics(supplier_df)

#CALL RQ3
title_rq3 = "RQ3: Forecast Accuracy (MAPE) and Promotion Effects"
text_rq3 =[
    "This section analyzes: ",
    html.Br(),
    "(3.1) general forecasting accuracy (MAPE), ",
    html.Br(),
    "(3.2) forecast accuracy per sku per warehouse(comparing to the general one),",
    html.Br(),
    "(3.3) how promotion affects sales value and profit.",
    html.Br(),
    "(3.4) the promotion impact per sku.",]
rq3_line_id = "rq3-line-forecast"
rq3_heatmap_id = "rq3-mape-heatmap"
rq3_promo_table_id = "rq3-promo-summary-table"
rq3_promo_bar_id = "rq3-promo-overall-bar"
rq3_sku_filter_id = "rq3-sku-filter"
rq3_wh_filter_id = "rq3-wh-filter"
rq3_sku_impact_fig_id = "rq3-sku-impact-fig"
# RQ3.1: Line chart of forecast vs actual over time
mape_overall = vis_rq3.rq3_general_mape(df_clean)
rq3_monthly_df = vis_rq3.dm.monthly_aggregation(df_clean)
fig_rq3_1 = vis_rq3.rq3_general_accuracy_fig(rq3_monthly_df)

# RQ3.2: MAPE per SKU and Warehouse (heatmap / matrix)
rq3_mape_dict = vis_rq3.rq3_mape_by_sku_warehouse(vis_rq3.dm.selected_data)

rq3_mape_df = pd.DataFrame(
    [
        {"sku_id": sku, "warehouse_id": wh, "MAPE": metrics["MAPE"], "Skipped": metrics["Skipped"]}
        for (sku, wh), metrics in rq3_mape_dict.items()
    ]
)
rq3_mape_df["MAPE"] = pd.to_numeric(rq3_mape_df["MAPE"], errors="coerce")
rq3_mape_df = rq3_mape_df.dropna(subset=["MAPE"])
rq3_mape_df["sku_id"] = rq3_mape_df["sku_id"].astype(str)
rq3_mape_df["warehouse_id"] = rq3_mape_df["warehouse_id"].astype(str)
if rq3_mape_df.empty:
    fig_rq3_2 = px.imshow([[np.nan]], title="MAPE% by SKU and Warehouse (No valid data)")
    rq3_mape_pivot = pd.DataFrame()
else:
    fig_rq3_2, rq3_mape_pivot = vis_rq3.rq3_mape_heatmap_fig(rq3_mape_df)

# RQ3.3: Promotion effect (overall)
df_clean = vis_rq3.dm.add_sales_profit(df_clean)
rq3_summary = vis_rq3.rq3_promotion_overall_summary(df_clean)
fig_rq3_3 = vis_rq3.rq3_promo_overall_bar_fig(rq3_summary)

# RQ3.4: Promotion impact (per top 10 SKU)
grouped, pivoted = vis_rq3.dm.promotion_analysis(df_clean)
pivoted.columns = pd.MultiIndex.from_tuples(
    [(m, int(f)) for (m, f) in pivoted.columns]
)
rq3_sku_impact = vis_rq3.rq3_promo_impact(pivoted)
fig_rq3_4 = vis_rq3.rq3_promotion_by_sku_fig(rq3_sku_impact, top_n=10)

# CALL RQ4 VISUALIZATIONS
title_rq4 = "RQ4: Regional profitability differences"
text_rq4 = (
"How do SKU-level profits vary across regions, "
"and what factors help explain regional differences?"
)
# Data preparation and KPI calculations
df_rq4_kpis = vis_rq4.get_rq4_kpis(df_clean)
# Clustered bar chart of SKU profit by region
fig_rq4_clustered = vis_rq4.plot_clustered_sku_profit_by_region(df_rq4_kpis, top_n=10) # top 10 SKUs
rq4_clustered_plot_id = "sku-profit-region-clustered"
# Stacked bar chart of SKU profit by region
fig_rq4_stacked = vis_rq4.plot_stacked_sku_profit_by_region(df_rq4_kpis)
rq4_stacked_plot_id = "sku-profit-region-stacked"
# Scatter plot of Stockout Rate vs Profit Margin by Region
fig_rq4_scatter = vis_rq4.plot_scatter_stockouts_vs_margin(df_rq4_kpis)
rq4_scatter_plot_id = "stockout-vs-margin-scatter"

# Placeholder for more research questions
# Repeat the same pattern for RQ2, RQ3, etc.
# UNCOMMENT AND MODIFY THE FOLLOWING LINES FOR EACH ADDITIONAL RQ
# Replace 'X' with the respective research question number
#title_rqX = "RQx : YOUR TITLE HERE"
#text_rqX = "YOUR THOROUGH EXPLANATION HERE"
#fig_rX = YOUR CODE
#rqX_plot_id = "genre-plot"


# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        # Dashboard Title
        html.H1(title_rq1, className="text-center my-4"),
        html.H4("Ruyi Zhong",className="text-center text-muted mb-4"),
        html.P(text_rq1, className="text-center lead"),
        # Research Question 1
        # RQ1 - inventory turnover per warehouse
        dbc.Row(
            dbc.Col(dcc.Graph(id=rq1_plot_id, figure=fig_rq1), width=12),
        className="mb-5"
        ),
        html.Hr(className="my-4"),
        # RQ1 - SKU dropdown + inventory turnover per warehouse per sku
        dbc.Row(dbc.Col([
                    html.Label("Select SKU for SKU-specific turnover:"),
                    dcc.Dropdown(
                        id="sku-dropdown",
                        options=[{"label": s, "value": s} for s in sku_options],
                        value=default_sku,
                        clearable=False,
                    ),],
                width=4),
            className="mb-2"),
        dbc.Row(dbc.Col(dcc.Graph(id=rq1b_plot_id, figure=fig_rq1b), width=12),className="mb-5"),
        html.Hr(className="my-4"),
        # RQ1 - stock level table
        dbc.Row(
            [dbc.Col([
                html.Label("Filter by Warehouse (optional):"),
                dcc.Dropdown(
                    id=rq1_wh_filter_id,
                    options=[{"label": w, "value": str(w)} for w in warehouse_list],
                    value=None,
                    placeholder="All warehouses",
                    clearable=True,
                ),],
            width=4,),
            dbc.Col([
                    html.Label("Filter by SKU (optional):"),
                    dcc.Dropdown(
                        id=rq1_sku_filter_id,
                        options=[{"label": s, "value": str(s)} for s in sku_options],
                        value=None,
                        placeholder="All SKUs",
                        clearable=True,
                    ),],
                    width=4,),
            ],
            className="mb-2",),
        dbc.Row(dbc.Col(
                dash_table.DataTable(
                    id=rq1_table_id,
                    columns=[{"name": c, "id": c} for c in safety_status_df.columns],
                    data=safety_status_df.to_dict("records"),

                    page_size=15,
                    sort_action="native",
                    filter_action="native",

                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left", "padding": "6px", "minWidth": "120px"},
                    style_header={"fontWeight": "bold"},
                ),
                width=12,),
            className="mb-5",),
        html.Hr(className="my-4"),
        # RQ1 - heatmap
        dbc.Row(dbc.Col(dcc.Graph(id=rq1c_plot_id, figure=fig_rq1c), width=12),className="mb-5"),
        html.Hr(className="my-5"),
        
        #Research Question 2
        #Supplier Lead Time & Order Analysis
        html.H1("RQ2: Supplier Lead Time & Order Analysis", className="text-center my-4"),
        html.P(
            "RQ2: Is there a correlation between the supplier lead time and the quantity of units ordered, "
            "and how does the average order size and cost differ among the top suppliers? ",
            className="text-center lead",
        ),

        html.H4(
            f"Correlation (Lead Time vs Order Quantity): {corr_value:.3f}",
            className="text-center text-primary",
        ),

        dbc.Row(dbc.Col(dcc.Graph(figure=fig_scatter), width=12)),
        dbc.Row(dbc.Col(dcc.Graph(figure=fig_bar_qty), width=12)),
        dbc.Row(dbc.Col(dcc.Graph(figure=fig_bar_cost), width=12)),
        dbc.Row(dbc.Col(dcc.Graph(figure=fig_heatmap), width=12)),

        html.Hr(className="my-5"),

        # Research Question 3
        html.H1(title_rq3, className="text-center my-4"),
        html.P(text_rq3, className="text-center lead"),

        # RQ3.1 Forecast vs Actual (monthly)
        dbc.Row(
            dbc.Col(
                dcc.Graph(id=rq3_line_id, figure=fig_rq3_1),
                width=12
            ),
            className="mb-4"
        ),

        # RQ3.2 MAPE Heatmap
        dbc.Row(
            dbc.Col(
                dcc.Graph(id=rq3_heatmap_id, figure=fig_rq3_2),
                width=12
            ),
            className="mb-4"
        ),

        html.Hr(className="my-4"),

        # RQ3.3 Promotion overall summary (table + bar chart)
        dbc.Row(
            [
                dbc.Col(
                    dash_table.DataTable(
                        id=rq3_promo_table_id,
                        columns=[{"name": c, "id": c} for c in rq3_summary.reset_index().rename(columns={"index": "Period"}).columns],
                        data=rq3_summary.reset_index().rename(columns={"index": "Period"}).to_dict("records"),
                        style_table={"overflowX": "auto"},
                        style_cell={"textAlign": "left", "padding": "6px", "minWidth": "120px"},
                        style_header={"fontWeight": "bold"},
                    ),
                    width=5
                ),
                dbc.Col(
                    dcc.Graph(id=rq3_promo_bar_id, figure=fig_rq3_3),
                    width=7
                ),
            ],
            className="mb-5"
        ),

        html.Hr(className="my-4"),

        # RQ3.4 Promotion impact by SKU (Top N) with filters
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Filter SKU (optional):"),
                        dcc.Dropdown(
                            id=rq3_sku_filter_id,
                            options=[{"label": str(s), "value": str(s)} for s in sku_options],
                            value=None,
                            placeholder="All SKUs",
                            clearable=True,
                        ),
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        html.Label("Filter Warehouse (optional):"),
                        dcc.Dropdown(
                            id=rq3_wh_filter_id,
                            options=[{"label": str(w), "value": str(w)} for w in warehouse_list],
                            value=None,
                            placeholder="All Warehouses",
                            clearable=True,
                        ),
                    ],
                    width=4
                ),
            ],
            className="mb-2"
        ),

        dbc.Row(
            dbc.Col(
                dcc.Graph(id="rq3-sku-impact-fig", figure=fig_rq3_4),
                width=12
            ),
            className="mb-5"
        ),
        # Research Question 4

        html.H1(title_rq4, className="text-center my-4"),
        html.P(text_rq4, className="text-center lead"),

        # Clustered bar chart – Top SKUs profit by region
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id=rq4_clustered_plot_id,
                    figure=fig_rq4_clustered
                ),
                width=12
            ),
            className="mb-4"
        ),

        # Stacked bar chart – SKU profit composition by region
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id=rq4_stacked_plot_id,
                    figure=fig_rq4_stacked
                ),
                width=12
            ),
            className="mb-4"
        ),

        # Scatter – Stockout rate vs profit margin
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id=rq4_scatter_plot_id,
                    figure=fig_rq4_scatter
                ),
                width=12
            ),
            className="mb-5"
        ),

            ],
    fluid=True,)




### You can create callbacks here if needed for interactivity
### For example, if you want to update plots based on user input
### You can define your callbacks below
### It is optional. Bonus points if you implement interactivity!!!

# Callback for SKU-specific plot
@app.callback(
    Output(rq1b_plot_id, "figure"),
    Input("sku-dropdown", "value")
)
def update_sku_plot(selected_sku):
    return vis_rq1.make_sku_turnover_fig(sku_turnover_df, selected_sku)
@app.callback(
    Output(rq1_table_id, "data"),
    Input(rq1_wh_filter_id, "value"),
    Input(rq1_sku_filter_id, "value"),
)
def update_status_table(selected_wh, selected_sku):
    df = safety_status_df

    if selected_wh:
        df = df[df["warehouse_id"].astype(str) == str(selected_wh)]

    if selected_sku:
        df = df[df["sku_id"].astype(str) == str(selected_sku)]

    return df.to_dict("records")

@app.callback(
    Output("rq3-sku-impact-fig", "figure"),
    Input("rq3-sku-filter", "value"),
    Input("rq3-wh-filter", "value"),
)
def update_rq3_promo_impact(selected_sku, selected_wh):

    df = df_clean.copy()

    if selected_sku:
        df = df[df["sku_id"].astype(str) == str(selected_sku)]
    if selected_wh:
        df = df[df["warehouse_id"].astype(str) == str(selected_wh)]

    # If nothing left after filtering, return an empty figure (so you see a reaction)
    if df.empty:
        return px.bar(title="No data for selected filters")

    # Make sure sales_value / profit exist
    if "sales_value" not in df.columns:
        df["sales_value"] = df["units_sold"] * df["unit_price"]
    if "profit" not in df.columns:
        df["profit"] = df["units_sold"] * (df["unit_price"] - df["unit_cost"])

    grouped, pivoted = vis_rq3.dm.promotion_analysis(df)

    if pivoted.empty:
        return px.bar(title="No promo/non-promo data for selected filters")

    # Convert True/False -> 1/0 to match rq3_promo_impact logic
    pivoted.columns = pd.MultiIndex.from_tuples([(m, int(f)) for (m, f) in pivoted.columns])

    # If promo or no-promo is missing after filtering, impacts can't be computed
    required = {
        ("units_sold", 0), ("units_sold", 1),
        ("sales_value", 0), ("sales_value", 1),
        ("profit", 0), ("profit", 1),
    }
    if not required.issubset(set(pivoted.columns)):
        return px.bar(title="Need both Promotion and No Promotion rows")

    impact_df = vis_rq3.rq3_promo_impact(pivoted)
    return vis_rq3.rq3_promotion_by_sku_fig(impact_df, top_n=10)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)


###
### To see the results of your work, run this file (main.py)
### Then open your web browser and go to the website:
### Dash is running on http://127.0.0.1:8050/
###

### All the best of success with your final project!!!