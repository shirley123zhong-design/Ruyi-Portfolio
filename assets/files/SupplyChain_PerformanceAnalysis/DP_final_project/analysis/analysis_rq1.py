import pandas as pd
from analysis import data_modeling as dm
import plotly.express as px

#analysis Q1:For each warehouse, what is the inventory turnover, and how well do SKUs’ inventory levels and reorder points align with their actual demand? 
# inventory turnover = total_sold / avg_inventory
# inventory turnover per warehouse - bar chart
def warehouse_inventory_turnover(df_clean): 
    """ return dictionary {warehouse_id: inventory_turnover} """ 
    daily_inventory_warehouse = df_clean.groupby(["warehouse_id", "date"])["inventory_level"].sum() 
    avg_inventory_per_wh = daily_inventory_warehouse.groupby("warehouse_id").mean() 
    total_sold=df_clean.groupby("warehouse_id")["units_sold"].sum() 
    turnover_warehouse=total_sold/avg_inventory_per_wh 
    return turnover_warehouse.to_dict()

# inventory turnover per warehouse - bar chart   
def sku_inventory_turnover(df_clean):
    """
    return dictionary
    {(warehouse_id, sku_id): inventory_turnover}
    """
    daily_inventory_sku = df_clean.groupby(["warehouse_id", "sku_id", "date"])["inventory_level"].sum()
    avg_inventory_sku = daily_inventory_sku.groupby(["warehouse_id", "sku_id"]).mean()
    total_sold_sku = df_clean.groupby(["warehouse_id", "sku_id"])["units_sold"].sum()
    turnover_sku = total_sold_sku / avg_inventory_sku
    return turnover_sku.to_dict()

def build_turnover_tables(df_clean):
    """
    Return 2 dataframes:
    1) warehouse_turnover_df: columns [warehouse_id, inventory_turnover]
    2) sku_turnover_df: columns [warehouse_id, sku_id, inventory_turnover]
    """
    warehouse_list, sku_list, _, _, _ , _, _ = dm.rq1_lists_and_maps(df_clean)
    warehouse_turnover = warehouse_inventory_turnover(df_clean)
    sku_turnover = sku_inventory_turnover(df_clean)

    warehouse_turnover_df = (pd.DataFrame.from_dict(
        warehouse_turnover,
        orient="index", # Use dictionary keys as row labels (index), not as columns
        columns=["inventory_turnover"]).reset_index() #take the index and turn into a normal column
    .rename(columns={"index": "warehouse_id"}))

    # column-warehouse_id rank in order as warehouse list
    warehouse_turnover_df["warehouse_id"] = pd.Categorical(
        warehouse_turnover_df["warehouse_id"].astype(str), categories=warehouse_list, ordered=True
    )
    # rank based on warehouse list
    warehouse_turnover_df = warehouse_turnover_df.sort_values("warehouse_id")

    sku_df = (pd.DataFrame.from_dict(
        sku_turnover, 
        orient="index", 
        columns=["inventory_turnover"]).reset_index())

    sku_df[["warehouse_id", "sku_id"]] = pd.DataFrame(sku_df["index"].tolist(), index=sku_df.index)
    # drop the index column
    sku_turnover_df = sku_df.drop(columns=["index"])
    # rank based on sku_list
    # convert the dataframe column into string first
    sku_turnover_df["sku_id"] = pd.Categorical(
        sku_turnover_df["sku_id"].astype(str),
        categories=[str(x) for x in sku_list],
        ordered=True)

    sku_turnover_df = sku_turnover_df.sort_values(
        ["sku_id", "inventory_turnover", "warehouse_id"],
        ascending=[True, False, True])
    return warehouse_turnover_df, sku_turnover_df

#SKU Inventory level - reorder and demand
# Actual demand = average daily units sold per SKU - sku_daily_demand_dict
# reoder point(ROP)= lead time demand + safety stock
# lead-time demand = average daily demand x lead time = avg_daily_demand × supplier_lead_time_days
# for each SKU,
# If inventory ≈ lead-time demand → aligned
# If inventory < lead-time demand → stockout risk
# If inventory > lead-time demand → overstock
def add_sku_demand_group(df_clean): 
    """ 
    Adds 'sku_demand_group' based on average daily demand per SKU. 
    Uses quantiles to split SKUs into Low-demand/Medium-demand/high-demand. 
    return dataframe with 2 columns, sku_id and demand group""" 
    df = df_clean.copy() 
    df["sku_id"] = df["sku_id"].astype(str)
    sku_avg_demand = df.groupby("sku_id")["units_sold"].mean() 
    q1 = sku_avg_demand.quantile(1/3) 
    q2 = sku_avg_demand.quantile(2/3) 
    def label(x): 
        if x <= q1: 
            return "Low-demand" 
        elif x <= q2: 
            return "Medium-demand" 
        else:
            return "high-demand" 
    sku_group = sku_avg_demand.apply(label)
    sku_demand_group = sku_group.reset_index(name="sku_demand_group") 
    return sku_demand_group

# measure whether reorder points match lead-time demand, turn dictionaries into dataframe
# reoder point(ROP)= lead time demand + safety stock
def build_safety_stock_table(df_clean, sku_daily_demand_dict,wh_sku_lead_dict,wh_sku_reorder_dict): 
    """
    Build a table to check whether reorder point (ROP) matches lead-time demand, and compute implied safety stock
    convert existed dictionaries into dataframe columns and also create column by using mapping and integration
    Return 9 columns:
    warehouse_id, sku_id,pair,reorder_point,lead_time_days,avg_daily_demand, lead_time_demand, safety_stock, alignment_ratio """ 
    df = df_clean.copy() 
    df["warehouse_id"] = df["warehouse_id"].astype(str)
    df["sku_id"] = df["sku_id"].astype(str)

    # warehouse-sku pairs from the dataset. still 2 columns in dataframe
    safety_stock_table= df[["warehouse_id", "sku_id"]].drop_duplicates().copy()

    # build tuple key for dict lookup， dataframe column"pair"
    safety_stock_table["pair"] = list(zip( safety_stock_table["warehouse_id"], safety_stock_table["sku_id"]))

    # lookup reorder point + lead time from dicts, dataframe column"reorder_point", "lead_time_days"
    safety_stock_table["reorder_point"] = safety_stock_table["pair"].map(wh_sku_reorder_dict)
    safety_stock_table["lead_time_days"] = safety_stock_table["pair"].map(wh_sku_lead_dict)

    # lookup avg daily demand from dict (sku-only) dataframe column"avg_daily_demand"
    safety_stock_table["avg_daily_demand"] = safety_stock_table["sku_id"].map(sku_daily_demand_dict)

    # derived metrics, dataframe column"lead_time_demand","safety_stock","alignment_ratio"
    safety_stock_table["lead_time_demand"] = safety_stock_table["avg_daily_demand"] * safety_stock_table["lead_time_days"]
    safety_stock_table["safety_stock"] = safety_stock_table["reorder_point"] - safety_stock_table["lead_time_demand"]
    safety_stock_table["alignment_ratio"] = safety_stock_table["reorder_point"] / safety_stock_table["lead_time_demand"]

    return  safety_stock_table

# merge table build_safety_stock_table and add_sku_demand_group
def build_safety_stock_merged_df(df_clean,sku_daily_demand_dict,wh_sku_lead_dict,wh_sku_reorder_dict):
    """
    merge table build_safety_stock_table and add_sku_demand_group.
    Returns a dataframe with build_safety_stock_table as main table
    """
    base = build_safety_stock_table(
        df_clean,
        sku_daily_demand_dict=sku_daily_demand_dict,
        wh_sku_lead_dict=wh_sku_lead_dict,
        wh_sku_reorder_dict=wh_sku_reorder_dict,
    )

    demand_group = add_sku_demand_group(df_clean)

    # Ensure consistent types for merge
    base["sku_id"] = base["sku_id"].astype(str)
    demand_group["sku_id"] = demand_group["sku_id"].astype(str)

    merged = base.merge(demand_group, on="sku_id", how="left")
    return merged

#For each demand group and for each lead-time-demand bin,what is the average alignment ratio?
def build_safety_stock_binned_heat_table(df_clean,sku_daily_demand_dict,wh_sku_lead_dict,wh_sku_reorder_dict):
    """
    Returns heat matrix dataframe for px.imshow:
    index = sku_demand_group
    columns = lead_time_demand bins
    values = mean(alignment_ratio)
    """

    reorder_df = build_safety_stock_merged_df(df_clean,sku_daily_demand_dict,wh_sku_lead_dict,wh_sku_reorder_dict)
    # clean in case we have missing value after merge
    value_col="alignment_ratio"
    reorder_df = reorder_df.dropna(subset=["lead_time_demand", "sku_demand_group", value_col]).copy()
    
    # create bin group column
    # assigns each row to a quantile-based bin based on lead_time_demand
    reorder_df["leadtime_bin"] = pd.qcut(reorder_df["lead_time_demand"], q=5, duplicates="drop")

    # heat matrix
    heat = reorder_df.pivot_table(
            index="sku_demand_group",
            columns="leadtime_bin",
            values=value_col, # what number goes into the heatmap
            aggfunc="mean") # how to combine many numbers into one.
    # Force row order
    heat = heat.reindex(["Low-demand", "Medium-demand", "high-demand"])
    # Sort columns (bins) left to right
    heat = heat.reindex(sorted(heat.columns), axis=1)
    #rename
    heat.columns = [f"{c.left:.1f}–{c.right:.1f}" for c in heat.columns]
    return heat

## visualization - overall turnover

def make_warehouse_turnover_fig(df_clean):
    """
    Plot inventory turnover per warehouse (all SKUs) from dataframe
    """
    warehouse_turnover_df, _ = build_turnover_tables(df_clean)
    fig = px.bar(
        warehouse_turnover_df,
        x="warehouse_id",
        y="inventory_turnover",
        title="Inventory Turnover per Warehouse (All SKUs)"
    )
    return fig

def make_sku_turnover_fig(sku_turnover_df, selected_sku):
    """
    Plot inventory turnover per warehouse for a selected SKU from dataframe.
    """
    selected_sku = str(selected_sku)

    df = sku_turnover_df[sku_turnover_df["sku_id"] == selected_sku]

    fig = px.bar(
        df,
        x="warehouse_id",
        y="inventory_turnover",
        title=f"Inventory Turnover per Warehouse ({selected_sku})"
    )
    return fig

# Heatmap: Alignment Ratio vs Lead-time Demand (by SKU demand group)
# alignment_ratio< 1 = stockout risk
# alignment_ratio≈ 1 = aligned
# alignment_ratio> 1 = overstock risk
def build_safety_stock_status_table(
    df_clean,
    sku_daily_demand_dict,
    wh_sku_lead_dict,
    wh_sku_reorder_dict,
    aligned_low=0.9,
    aligned_high=1.1
):
    # Build merged base dataframe
    merged = build_safety_stock_merged_df(df_clean,sku_daily_demand_dict,wh_sku_lead_dict,wh_sku_reorder_dict)

    # Create status column using explicit loop
    status_list = []

    for _, row in merged.iterrows():
        ratio = row["alignment_ratio"]

        if ratio < aligned_low:
            status = "outstock"
        elif ratio > aligned_high:
            status = "overstock"
        else:
            status = "aligned"

        status_list.append(status)

    merged["status"] = status_list

    # Select and order columns
    cols = [
        "warehouse_id", "sku_id", "sku_demand_group",
        "reorder_point", "lead_time_days", "avg_daily_demand",
        "lead_time_demand", "safety_stock", "alignment_ratio",
        "status"
    ]
    numeric_cols = [
    "avg_daily_demand",
    "lead_time_demand",
    "safety_stock",
    "alignment_ratio",]

    return merged[cols]

def make_safety_stock_binned_heatmap_fig(df_clean,sku_daily_demand_dict,wh_sku_lead_dict,wh_sku_reorder_dict):
    """
    Plot build_safety_stock_binned_heat_table
    """
    heat = build_safety_stock_binned_heat_table(df_clean,sku_daily_demand_dict,wh_sku_lead_dict,wh_sku_reorder_dict)

    fig = px.imshow(
        heat,
        aspect="auto",
        title="ROP Alignment Ratio vs Lead-time Demand (Binned)",
        labels={
            "x": "expected demand during the supplier lead time",
            "y": "SKU Demand Group",
            "color": "Alignment Ratio"
        
        },
        color_continuous_scale="RdBu",
        zmin=0.5,
        zmax=1.5
    )
    return fig


# run test
if __name__ == "__main__":
    df_clean = dm.load_clean_data()

    # Build tables
    (warehouse_list,sku_list,warehouse_sku_dict,sku_warehouse_dict,sku_daily_demand_dict,wh_sku_lead_dict,wh_sku_reorder_dict) = dm.rq1_lists_and_maps(df_clean)
    warehouse_turnover_df, sku_turnover_df = build_turnover_tables(df_clean)
    # FIGURE 1: Warehouse turnover (all SKUs)
    fig1 = make_warehouse_turnover_fig(df_clean)
    fig1.show()

    # FIGURE 2: SKU turnover (pick one SKU that exists)
    selected_sku = sku_turnover_df["sku_id"].iloc[0]
    fig2 = make_sku_turnover_fig(sku_turnover_df, selected_sku)
    fig2.show()

    # TABLE 3: Safety stock status table (aligned / overstock / outstock)
    safety_status_df = build_safety_stock_status_table(df_clean,sku_daily_demand_dict,wh_sku_lead_dict,wh_sku_reorder_dict)
    print("\nSafety stock status table (sample):")
    print(safety_status_df.head())

    # FIGURE 4: Safety stock heatmap
    fig3 = make_safety_stock_binned_heatmap_fig(df_clean,sku_daily_demand_dict,wh_sku_lead_dict,wh_sku_reorder_dict)
    fig3.show()

