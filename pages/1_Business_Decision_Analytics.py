import streamlit as st
import os
import sys
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_PROJECT_ROOT)
os.chdir(_PROJECT_ROOT)  # ensure relative asset paths work no matter where streamlit was launched from
from theme import apply_theme, hero, case_card_html, eyebrow

st.set_page_config(page_title="Business Decision Analytics | Shirley Zhong", page_icon="📊", layout="wide")
apply_theme()

st.page_link("app.py", label="← Back to home")

# -----------------------------------------------------------------------
# PAGE HEADER
# -----------------------------------------------------------------------

hero(
    icon="📊",
    title="Business Decision Analytics",
    subtitle=(
        "I use data to support practical business decisions across forecasting, cost evaluation, "
        "customer insight, and operational performance. These cases show how I turn unclear business "
        "questions into structured analysis, clear dashboards, and recommendations that managers can act on."
    ),
    tags=[
        "Forecasting & Planning", "Cost & Policy Decisions", "Customer Segmentation",
        "Churn & Risk Prediction", "Operational Performance", "Dashboard Storytelling",
    ],
    flow="Business question → Data preparation → Analysis method → Decision insight → Recommendation",
)

# -----------------------------------------------------------------------
# PATHS
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


# -----------------------------------------------------------------------
# CASE DATA
# -----------------------------------------------------------------------

BANKDATA = {
    "title": "Bankdata — Forecast Accuracy & Cost Planning",
    "question": "Which cost/activity forecasts can management trust before budgeting, and where should forecast logic be adjusted?",
    "tools": ["Excel", "Power BI", "MAPE", "Bias analysis", "Forecast comparison"],
    "metric": "14 cost/activity categories evaluated · 3 forecast approaches compared",
    "images": [
        ("Bankdata_forecast.png", "December forecast by product line"),
        ("Bankdata_accuracy.png", "Model accuracy comparison"),
    ],
    "detail": {
        "goal": "Help management identify which forecasts were reliable for budgeting and which categories needed adjustment before the planning cycle.",
        "process": "Collected forecast and actual cost/activity data, measured forecast error using MAPE and bias, and analysed accuracy by cost/activity ID, financial institute, and forecast horizon. Compared three forecast approaches and identified categories needing bias correction or manual review.",
        "tools": "Excel · Power BI",
        "challenges": "Forecast accuracy differed strongly between categories — some IDs were stable while others were highly volatile. One single method was not suitable for all categories, and forecast horizon analysis was affected by aggregation differences.",
        "outcomes": "Most forecasts were within an acceptable error range. Several IDs needed review before budgeting. Simple bias correction improved volatile categories. Volatile categories required more careful judgement instead of automatic model trust.",
    },
    "download": "Bankdata_forecast.zip",
}

RESTAURANT = {
    "title": "Restaurant — Price Sensitivity & Sales Forecast",
    "question": "Does pricing or discounting actually drive restaurant sales — and what should we forecast for next week?",
    "tools": ["Excel", "Regression modelling", "Model comparison", "Sales forecasting"],
    "metric": "Final model R² = 0.56 · Forecasted Jan 7, 2019 sales: $2,333",
    "images": [
        ("ResturantRegression-Interaction.webp", "Best model: R²=0.56 — interaction effects"),
        ("ResturantRegression-multivar.webp", "Day-of-week effects"),
        ("ResturantRegression-Prediction.webp", "Concrete forecast output: $2,333"),
    ],
    "detail": {
        "goal": "Understand what drives restaurant sales and produce a reliable forecast for a specific future date.",
        "process": "Started with simple regression models, then progressively added business variables including price, discounts, home game days, lagged sales, and day-of-week. Compared model performance across six versions, selected the final model based on R² and business meaning, and produced a concrete sales forecast.",
        "tools": "Excel",
        "challenges": "Some variables seemed business-relevant but were not statistically meaningful. Discount effects needed testing rather than assuming. The model needed to balance prediction accuracy and simple interpretation for managers.",
        "outcomes": "Final model reached R² = 0.56. Home game days, lagged sales, and day-of-week were the key drivers. Discounts were NOT significant in the final model — recommended reviewing discount strategy before continuing spend. Forecasted sales for Jan 7, 2019: $2,333.",
    },
    "download": "Restaurant regression.xlsx",
}

COFFEEGO = {
    "title": "CoffeeGo — Automated Weather-Adjusted Forecast",
    "question": "How do we automate bi-weekly coffee ordering so it updates without manual work each cycle?",
    "tools": ["Excel", "Power Query", "ETL workflow", "Weather-adjusted forecasting"],
    "metric": "Bi-weekly reports automated · 2 locations · Rain-adjusted per product",
    "images": [
        ("CoffeeGo_PowerQuery.png", "Power Query pipeline"),
        ("CoffeeGo_forecast1.png", "Forecast output — period 1"),
        ("CoffeeGo_forecast2.png", "Forecast output — period 2"),
    ],
    "detail": {
        "goal": "Help CoffeeGo improve bi-weekly coffee ordering by combining POS sales data with weather information and automating the reporting process.",
        "process": "Imported POS data from two locations, cleaned duplicate rows and incomplete transactions, split concatenated OrderId and ProductId fields, replaced missing quantity and product values, combined sales data with weather forecast, identified rainy days, applied product-specific rain multipliers (0.5x rainy, 1x clear), and generated daily sales reports and bi-weekly order forecasts.",
        "tools": "Excel · Power Query",
        "challenges": "POS data had duplicate rows and concatenated fields. Some quantities were shown as NA instead of zero. ProductId was missing for some products. The intended API import was used as designed; CSV import used as a practical fallback when needed.",
        "outcomes": "Created a repeatable Power Query workflow. Produced automated daily sales reports by coffee product. Produced bi-weekly order forecast reports. Eliminated manual copy-paste work from the forecasting process.",
    },
    "download": "CoffeeGo_PowerQuery.zip",
}

FAIRVIEW = {
    "title": "Fairview — Reimbursement Rate Decision Dashboard",
    "question": "Should the company continue reimbursing employees by mileage, or switch to a fixed rate per trip?",
    "tools": ["Power BI", "Dynamic parameters", "Scenario analysis", "Management accounting"],
    "metric": "4,888 trips analysed · $39,658.61 total cost · $8.11 avg. per trip",
    "images": [
        ("Fairview_cost_analysis.webp", "Historical reimbursement cost by office, role, and time of day"),
        ("Fairview_scenario_analysis.webp", "Dynamic flat-rate scenario comparison — CFO tool"),
        ("Fairview_employee_detail.webp", "Per-employee cost impact breakdown"),
    ],
    "detail": {
        "goal": "Support the CFO's decision on whether Fairview should continue mileage-based reimbursement or switch to a fixed rate per trip.",
        "process": "Loaded and cleaned reimbursement trip data, analysed cost by office, role, and time of trip, built a Power BI cost evaluation dashboard, created a dynamic flat-rate parameter slider, compared mileage-based vs fixed-rate scenarios, and added employee-level drill-down for individual impact.",
        "tools": "Power BI",
        "challenges": "The decision was not only about total cost — different offices and roles were affected differently. The CFO needed both overall cost comparison and employee-level impact. The dashboard needed to be interactive rather than static.",
        "outcomes": "Analysed 4,888 trips across 5 offices and 2 roles. At $8.11/trip flat rate, the company saves $16.93 total — essentially cost-neutral but with significantly simpler administration. Dashboard lets CFO test any rate option and see impact live by office and employee.",
    },
    "download": "Fairview.zip",
}

DATASCIENCE = {
    "title": "Customer Analytics & Churn Prediction — Full Analytics Pipeline",
    "question": "Which customers are at risk of churning, and which segments should we prioritise for retention?",
    "tools": ["SQL", "Python", "Power BI", "PCA", "Clustering", "Lasso", "Decision Tree", "KNN", "Random Forest"],
    "metric": "7 ML models compared · 4-page Power BI dashboard · Full SQL → dashboard pipeline",
    "images": [
        ("PCA_all_variance.png", "PCA — variance explained"),
        ("cluster_compare.png", "Customer clustering"),
        ("machineLearning.png", "Model comparison"),
        ("POWERBI_1.png", "Power BI dashboard"),
        ("classification_prediction.png", "Classification results"),
        ("regression_prediction.png", "Regression prediction"),
    ],
    "detail": {
        "goal": "Support marketing, retention, and customer experience decisions by segmenting customers, predicting future value, and identifying risk patterns.",
        "process": "Designed SQL database and wrote business queries for customer, product, order, return, service, and logistics insights. Cleaned and validated customer data in Python, handled missing and corrupted values, applied PCA to reduce behaviour dimensions, used K-means and hierarchical clustering for segmentation, compared 7 predictive models for spending, churn, and satisfaction, and built Power BI dashboards to communicate results to non-technical stakeholders.",
        "tools": "SQL · Python · Power BI",
        "challenges": "The project required a full end-to-end pipeline. Missing and corrupted data needed careful handling. Different models suited different business questions. The best technical model was not always easiest to explain to managers — results needed translating into business-friendly dashboard views.",
        "outcomes": "Built a relational SQL database and queried it for business insights. Identified meaningful customer segments. Lasso Regression best for spending prediction. Decision Tree used for churn interpretation. KNN for satisfaction prediction. Delivered a 4-page Power BI dashboard covering customer overview, segmentation, regression, and risk/experience.",
    },
    "download": "Customer_Analytics_Churn_Prediction.zip",
}

SUPPLYCHAIN = {
    "title": "Supply Chain — Inventory, Supplier & Regional Profitability",
    "question": "Where are the inefficiencies in the supply chain, and which warehouses, suppliers, SKUs, or regions need management attention?",
    "tools": ["Python", "Pandas", "Plotly/Dash", "KPI analysis", "MAPE", "Profitability analysis"],
    "metric": "50 SKUs · 5 warehouses · 10 suppliers · 4 regions analysed",
    "detail": {
        "goal": "Identify supply chain inefficiencies and help managers understand where to focus attention across inventory, suppliers, and regions.",
        "process": "Validated data quality and standardised formats. Calculated inventory, supplier, forecast, promotion, and profitability KPIs. Analysed inventory turnover and reorder point alignment. Compared supplier lead time, cost, and performance. Measured forecast accuracy using MAPE. Assessed promotion impact on sales and profitability. Compared regional profitability and operational patterns. Built interactive Python dashboard.",
        "tools": "Python",
        "challenges": "The dataset was already clean, so value came from structuring the right business KPIs. Operational averages could hide important outliers — the analysis was built to surface them, not smooth them over. Different questions required different data structures and aggregations.",
        "outcomes": "Evaluated inventory efficiency and reorder alignment across 50 SKUs. Compared supplier performance across 10 suppliers. Measured forecast accuracy per SKU and warehouse. Assessed promotion effects on sales value and profitability. Identified regional profitability differences and operational outliers.",
    },
    "download": "SupplyChain_PerformanceAnalysis.zip",
}


# -----------------------------------------------------------------------
# RENDER HELPER
# -----------------------------------------------------------------------

def render_full_case(case):
    st.markdown(
        case_card_html(case["title"], case["question"], case["tools"], case["metric"]),
        unsafe_allow_html=True,
    )

    with st.expander("View full case study"):
        d = case["detail"]
        st.markdown(f"**Goal**  \n{d['goal']}")
        st.markdown(f"**Process**  \n{d['process']}")
        st.markdown(f"**Tools**  \n{d['tools']}")
        st.markdown(f"**Challenges**  \n{d['challenges']}")
        st.markdown(f"**Outcomes**  \n{d['outcomes']}")

        if case.get("images"):
            st.markdown("---")
            cols = st.columns(min(len(case["images"]), 3))
            for i, (fname, caption) in enumerate(case["images"]):
                with cols[i % 3]:
                    show_image(fname, caption)

        if case.get("download"):
            st.markdown("---")
            download_button_for(case["download"], f"📥 Download — {case['title']}")


# -----------------------------------------------------------------------
# TABS
# -----------------------------------------------------------------------

tab_a, tab_b, tab_c, tab_d = st.tabs([
    "A · Forecasting & Planning",
    "B · Cost & Policy",
    "C · Customer Analytics",
    "D · Operational Analytics",
])

with tab_a:
    eyebrow("Section A")
    st.subheader("Forecasting & Planning")
    st.caption("Forecasting and planning help managers prepare for future demand, cost, capacity, and sales. A controller or business analyst supports this by testing forecast accuracy, identifying suitable logic, and explaining when a forecast should be trusted, adjusted, or reviewed manually.")
    render_full_case(BANKDATA)
    render_full_case(RESTAURANT)
    render_full_case(COFFEEGO)

with tab_b:
    eyebrow("Section B")
    st.subheader("Cost & Policy Decision Support")
    st.caption("Cost and policy decision support helps management compare alternatives before changing a business process or financial policy. A controller or analyst supports this by modelling cost impact, creating scenarios, and showing how different offices, roles, or employees would be affected.")
    render_full_case(FAIRVIEW)

with tab_c:
    eyebrow("Section C")
    st.subheader("Customer Analytics & Predictive Decision Support")
    st.caption("Customer analytics helps businesses understand which customers to prioritise, which are at risk, and where marketing or service actions should be focused.")
    render_full_case(DATASCIENCE)

with tab_d:
    eyebrow("Section D")
    st.subheader("Operational Decision Analytics")
    st.caption("Operational decision analytics helps managers understand where processes, resources, suppliers, or regional performance need attention — connecting daily operations with financial outcomes.")
    render_full_case(SUPPLYCHAIN)
    st.video("assets/img/Python_dashapp.mp4")

st.markdown("---")

# -----------------------------------------------------------------------
# DOWNLOADS
# -----------------------------------------------------------------------

eyebrow("Resources")
st.subheader("📥 Downloads")
dl_cols = st.columns(4)
with dl_cols[0]:
    download_button_for("Bankdata_forecast.zip", "🏦 Bankdata Forecast")
    download_button_for("Restaurant regression.xlsx", "🍽️ Restaurant Regression")
with dl_cols[1]:
    download_button_for("CoffeeGo_PowerQuery.zip", "☕ CoffeeGo Power Query")
    download_button_for("Fairview.zip", "🚗 Fairview Reimbursement")
with dl_cols[2]:
    download_button_for("Customer_Analytics_Churn_Prediction.zip", "🎯 Customer Analytics & Churn Prediction")
    download_button_for("Final_PowerBI_Dashboard.pbix", "📊 Data Science Power BI")
with dl_cols[3]:
    download_button_for("SupplyChain_PerformanceAnalysis.zip", "🏭 Supply Chain Performance Analysis")