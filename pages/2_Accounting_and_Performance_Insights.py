import streamlit as st
import os
import sys
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_PROJECT_ROOT)
os.chdir(_PROJECT_ROOT)  # ensure relative asset paths work no matter where streamlit was launched from
from theme import apply_theme, hero, case_card_html, eyebrow

st.set_page_config(page_title="Accounting & Performance Insights | Shirley Zhong", page_icon="🧮", layout="wide")
apply_theme()

st.page_link("app.py", label="← Back to home")

# -----------------------------------------------------------------------
# PAGE HEADER
# -----------------------------------------------------------------------

hero(
    icon="🧮",
    title="Accounting & Performance Insights",
    subtitle=(
        "I apply data analytics to accounting and performance problems, including cost control, "
        "financial performance analysis, audit testing, payroll variance analysis, and accounting "
        "data preparation. These cases show how Excel, SQL, Power BI, and ETL workflows can support "
        "clearer reporting, stronger controls, and better management decisions."
    ),
    tags=["Cost analysis", "Financial performance", "Audit analytics", "ETL & data quality", "Dashboard reporting"],
    flow="Accounting question → Data preparation → Analysis / test design → KPI or exception result → Business recommendation",
)

# -----------------------------------------------------------------------
# ASSET / DOWNLOAD PATH BASE — update these to match your repo structure
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


# -----------------------------------------------------------------------
# CASE DATA
# -----------------------------------------------------------------------

FAIRVIEW = {
    "title": "Fairview reimbursement dashboard",
    "question": "Should Fairview continue reimbursing employees based on mileage, or switch to a fixed rate per trip?",
    "tools": ["Power BI", "Dynamic parameters", "Scenario comparison"],
    "metric": "$39,658.61 total reimbursement across 4,888 trips · $8.11 average per trip",
    "images": [
        ("Fairview_cost_analysis.png", "Historical reimbursement cost by office, role, and time of day"),
        ("Fairview_scenario_analysis.png", "Dynamic flat-rate scenario comparison"),
        ("Fairview_employee_detail.png", "Per-employee impact tooltip"),
    ],
    "detail": {
        "goal": "Give the CFO, Isiah Simon, a clear, data-backed basis for deciding whether to keep "
                "mileage-based reimbursement or move to a fixed rate per trip.",
        "process": "Loaded and validated a year of trip-level data (4,888 trips), then built two Power BI "
                   "dashboards: one showing how office, role, and time of day drove historical reimbursement "
                   "cost, and a second dynamic dashboard letting the CFO adjust a proposed flat rate and see "
                   "the cost impact per office and per employee update live.",
        "tools": "Power BI, dynamic parameters, DAX measures, dashboard tooltips.",
        "challenges": "Mileage reimbursement wasn't evenly distributed, so any single flat rate would "
                      "over-pay some groups and under-pay others — the analysis needed to expose that "
                      "variation, not hide it behind one average.",
        "outcomes": "Found reimbursement cost per trip varies nearly 2x by office — Indianapolis averaged "
                    "$11.96/trip versus $6.62 in Kansas City — and Sales trips cost more on average than IT "
                    "trips ($8.41 vs $6.88). This showed a single flat rate would be unfair across offices and "
                    "roles, and gave the CFO a dynamic tool to test rate options before deciding.",
    },
    "download": "Fairview.zip",
}

INTEGRATECO = {
    "title": "IntegrateCo payroll variance analysis",
    "question": "Payroll rose sharply year over year despite fewer employees — what's driving it, and where "
                "is overtime cost concentrated?",
    "tools": ["Excel", "Pivot tables", "Payroll variance", "Data quality checks"],
    "metric": "Gross wages $67.58M \u2192 $85.93M (+27.16%) while headcount fell 851 \u2192 804",
    "images": [
        ("IntegrateCo_WageDiffer_1.png", "Wage change by job code, 2015 vs 2016 (pivot table)"),
        ("IntegrateCo_OvertimeJob.png", "Overtime hours and pay by job code, 2015"),
        ("IntegrateCo_monthly.png", "Monthly payroll trend, 2015 vs 2016"),
    ],
    "detail": {
        "goal": "Explain to Noah why total payroll increased by over 27% year over year, even though the "
                "number of employees decreased, and find where overtime cost could be reduced.",
        "process": "Combined 2015 and 2016 payroll exports plus job code and location reference data in "
                   "Excel, then built pivot tables comparing gross wages by job category and by individual "
                   "employee, and a separate pivot isolating overtime hours and pay by job code.",
        "tools": "Excel, Power Query joins, pivot tables.",
        "challenges": "Job codes had to be matched consistently across the two years' exports before any "
                      "comparison was reliable. The data also had a quality issue worth flagging on its own: "
                      "68 transactions in the 2016 file had no employee number attached, totalling $1,805,269 "
                      "in gross wages with no owner.",
        "outcomes": "Employee Training (+133.74%), Service (+55.65%), Project Management (+47.57%), and "
                    "Office (+42.53%) job codes drove the increase, while headcount actually fell. A separate "
                    "overtime analysis found the Office job code generated the most overtime pay ($208,754) "
                    "and one employee, Cindy Lunt, earned the single largest amount of overtime pay in H1 2015 "
                    "($311,569) — concrete levers for cost control. Also flagged 68 unmatched 2016 transactions "
                    "worth $1.8M as a data-integrity issue for the new payroll system.",
    },
    "download": "IntregrateCo.zip",  # NOTE: matches the spelling of your actual folder/zip on disk
}

EY_DUPONT = {
    "title": "EY DuPont financial performance analysis",
    "question": "Which industries and companies show stronger financial performance, and what's actually "
                "driving their ROE?",
    "tools": ["Power BI", "DuPont analysis", "Ratio interpretation", "Industry benchmarking"],
    "metric": "Consumer Services led 2015 ROE (0.16); Finance improved ROE from 6.21% to 9.28% (2013\u20132015)",
    "images": [
        ("EY_DUPONT_Industry1.png", "Industry-level ROE, margin, turnover, and leverage comparison"),
        ("EY_DUPONT_Industry2.png", "Industry ROE change, 2013 to 2015"),
        ("EY_DUPONT_Company1.png", "Company-level ratio drill-down with year-over-year change"),
    ],
    "detail": {
        "goal": "Break down company and industry financial performance into its DuPont components — "
                "profit margin, asset turnover, and financial leverage — to understand what actually drives ROE.",
        "process": "Extracted and matched balance sheet and income statement data across 174 companies and "
                   "6 industries, calculated DuPont ratios for 2013 and 2015, and built Power BI dashboards "
                   "for industry comparison and individual company drill-down.",
        "tools": "Power BI, DuPont ratio decomposition, data accuracy validation.",
        "challenges": "Initial predictions about which industries would lead on each ratio were wrong in "
                      "places, so the analysis had to explain the surprise rather than just confirm expectations.",
        "outcomes": "Consumer Services had the highest 2015 ROE (0.16), not Technology as predicted. Finance "
                    "had the highest profit margin (0.19) and by far the highest leverage (9.23 vs. "
                    "Technology's 2.11), and showed the largest ROE improvement 2013\u20132015 (6.21% \u2192 9.28%), "
                    "driven mainly by leverage and margin rather than efficiency. Also flagged companies with "
                    "negative margin but high turnover as a warning sign — high activity without profitability.",
    },
    "download": "EY_DUPONT.zip",
}

PCARD = {
    "title": "P-Card internal audit analytics",
    "question": "Are employees following P-card spending rules, or are there transactions that need audit "
                "follow-up?",
    "tools": ["SQL", "Audit analytics", "Internal control testing", "Continuous auditing"],
    "metric": "254 split-purchase flags · 289 travel expense exceptions · 127 annual limit violations",
    "detail": {
        "goal": "Test whether university employees complied with P-card purchasing policy and identify "
                "transactions that require audit follow-up.",
        "process": "Designed SQL queries against a year of P-card transaction data to test 7 internal "
                   "controls covering spending limits, split-purchase evasion, and prohibited travel expenses.",
        "tools": "SQL, internal control test design, exception flagging.",
        "challenges": "Splitting purchases to dodge transaction limits can take several forms — same person, "
                      "same vendor, different cardholders — so each pattern needed its own query logic rather "
                      "than one blanket rule.",
        "outcomes": "Flagged 127 employees over the annual limit, 457 monthly-limit violations, 254 "
                    "same-person split-purchase cases, 48 multi-cardholder splits, 118 multi-vendor splits, "
                    "and 289 suspicious travel/food expense combinations. Recommended these become standing "
                    "automated monitoring checks rather than one-off tests.",
    },
    "queries": [
        {
            "label": "Test 1 — Annual spending limit ($50,000/year) · 127 flags",
            "sql": """SELECT FullName, SUM(Amount) AS TotalAmountSpent
FROM pcards
WHERE Year = 2014
GROUP BY FullName
HAVING SUM(Amount) > 50000
ORDER BY TotalAmountSpent DESC;""",
            "image": ("Pcards_user_over_spent.png", "Result: 127 employees over the annual limit, sorted by total spend"),
        },
        {
            "label": "Test 4 — Same-person split purchase (>$5,000 combined, same vendor/day) · 254 flags",
            "sql": """SELECT p.FullName, p.Amount, p.Description, p.Vendor, p.TransactionDate, p.PostedDate, p.MCC
FROM pcards AS p
JOIN (
    SELECT FullName, TransactionDate, Vendor,
           SUM(Amount) AS TotalAmountSpent, COUNT(*) AS TransactionCount
    FROM pcards
    GROUP BY FullName, Vendor, TransactionDate
    HAVING COUNT(*) > 1 AND SUM(Amount) > 5000
) AS SplitSpentControl
  ON p.FullName = SplitSpentControl.FullName
 AND p.Vendor = SplitSpentControl.Vendor
 AND p.TransactionDate = SplitSpentControl.TransactionDate
WHERE Year = 2014
ORDER BY p.TransactionDate ASC;""",
            "image": ("Pcards_split_transaction.png", "Result: 254 same-person split-purchase transactions"),
        },
        {
            "label": "Test 7 — Prohibited travel food expenses (hotel/motel + food/restaurant, same day) · 289 flags",
            "sql": """SELECT p.FullName, p.Amount, p.Description, p.Vendor, p.TransactionDate, p.PostedDate, p.MCC
FROM pcards AS p
JOIN (
    SELECT FullName, TransactionDate
    FROM pcards
    GROUP BY FullName, TransactionDate
    HAVING SUM(CASE WHEN LOWER(MCC) LIKE '%hotel%' OR LOWER(MCC) LIKE '%motel%'
                      OR LOWER(MCC) LIKE '%resort%' OR LOWER(MCC) LIKE '%inn%'
                     THEN 1 ELSE 0 END) > 0
       AND SUM(CASE WHEN LOWER(MCC) LIKE '%food%' OR LOWER(MCC) LIKE '%restaurant%'
                     THEN 1 ELSE 0 END) > 0
) AS ProhibitPurchase
  ON p.FullName = ProhibitPurchase.FullName
 AND p.TransactionDate = ProhibitPurchase.TransactionDate
WHERE Year = 2014
ORDER BY p.FullName ASC, p.Amount ASC;""",
            "image": ("Pcards_prohibited_transaction.png", "Result: 289 same-day hotel + food/restaurant exceptions"),
        },
    ],
    "download": "Pcards.zip",
}

ETL_1 = {
    "title": "Identify error / transform import — Power Query error handling",
    "question": "A comma-delimited financial import silently misaligned data for some companies — how do you "
                "catch it and fix it without losing records?",
    "tools": ["Power Query", "Conditional columns", "Append queries"],
    "metric": "23 companies' financial data repaired with zero record loss",
    "detail": {
        "goal": "Diagnose why part of a comma-delimited financial dataset (23 companies, 3 years each) "
                "imported with data shifted into the wrong columns, and fix it without dropping any rows.",
        "process": "Traced the problem to company names that themselves contain a comma (e.g. \"Apple, Inc.\") "
                   "— the parser treated that comma as a field break, shifting everything after it one column "
                   "to the right. In Power Query, added an index column, then split the query into two "
                   "references: rows that parsed correctly, and rows that didn't, using a conditional test "
                   "(IF [Year] = \"Inc.\" THEN ... ELSE ...) to flag the broken ones.",
        "tools": "Power Query, custom conditional columns, reference queries, Append Queries.",
        "challenges": "The broken rows were real data, not errors to discard — the fix had to reconstruct the "
                      "correct company name (rejoining the two shifted pieces with a comma) before the rows "
                      "could be merged back in, and needed Reference rather than Duplicate queries so the "
                      "fix stayed traceable back to the original source.",
        "outcomes": "Repaired every misaligned row and reunified the corrected and originally-correct rows "
                    "with Append Queries, recovering the full 23-company dataset with no data loss.",
    },
    "images": [
        ("ETL_Case1_before_after.png", "Before: rows misaligned with text-formatted values. After: corrected and fully numeric."),
    ],
}

ETL_2 = {
    "title": "Employee code parsing — regular format",
    "question": "How do you turn a composite code like JAP1080-19M into usable Location, Employee ID, Plant "
                "ID, and Pay Period fields?",
    "tools": ["Text-to-Columns", "Excel formulas"],
    "metric": "597 employee codes parsed into 4 fields, two methods compared",
    "detail": {
        "goal": "Convert a composite employee code into four separate, usable fields for payroll analysis.",
        "process": "Solved it two ways in parallel: Text-to-Columns (splitting on fixed character positions) "
                   "for most fields, and LEFT/MID/RIGHT formulas for a version that stays live if the "
                   "source data changes.",
        "tools": "Excel Text-to-Columns, LEFT/MID/RIGHT formulas.",
        "challenges": "Text-to-Columns is a one-time operation — it has to be manually re-run if the source "
                      "data changes, which is fine for a one-off report but risky for anything recurring.",
        "outcomes": "Delivered clean Location, Employee ID, Plant ID, and Pay Period columns for 597 employee "
                    "records, using the formula-based version wherever the field needed to update "
                    "automatically on refresh.",
    },
    "images": [
        ("ETL_Case2_solution.png", "Raw employee code alongside Text-to-Columns and formula-based results"),
    ],
}

ETL_3 = {
    "title": "Employee code parsing — irregular format (Flash Fill error found)",
    "question": "Same parsing task, but the codes aren't consistently formatted — which method actually "
                "holds up: Flash Fill or formulas?",
    "tools": ["Flash Fill", "Excel formulas", "Pattern validation"],
    "metric": "Formula parsing held up 100%; Flash Fill mislabeled location on irregular codes",
    "detail": {
        "goal": "Parse employee codes with inconsistent formats (Japan177-3Mo, AUS551-2Mo, Canada351-3W, "
                "ARG363-4Mo) into the same four fields as Case 2 — a tougher test of which method is "
                "actually reliable.",
        "process": "Solved the split two ways again: explicit formulas, and Excel's Flash Fill (Ctrl+E), to "
                   "directly compare a rule-based approach against automated pattern-matching on messier data.",
        "tools": "Excel Flash Fill, formulas, pattern validation.",
        "challenges": "Flash Fill isn't rule-based — it guesses the pattern from a couple of typed examples, "
                      "and that guess can be wrong in ways that aren't obvious without checking.",
        "outcomes": "Found real errors in the Flash Fill output: it mapped ARG363-4Mo to location \"Japan\" "
                    "instead of \"ARG,\" and mislabeled several other irregular rows the same way, while the "
                    "formula-based version stayed accurate throughout. Takeaway for real work: verify Flash "
                    "Fill output against a formula-based check before trusting it on messy production data.",
    },
    "images": [
        ("ETL_Case3_solution.png", "Formula column (correct) vs Flash Fill column (mislabeled location) side by side"),
    ],
}

ETL_4 = {
    "title": "General ledger enrichment — XLOOKUP vs VLOOKUP",
    "question": "How do you enrich 789 raw journal entry lines with business unit, account, and preparer "
                "detail for management reporting, without dropping or duplicating any lines?",
    "tools": ["XLOOKUP", "VLOOKUP", "Multi-table joins"],
    "metric": "789 GL lines enriched via 3-table join, two lookup methods compared",
    "detail": {
        "goal": "Enrich a raw hotel general ledger extract (789 journal entry lines) with human-readable "
                "business unit, account, and preparer information for reporting.",
        "process": "Joined the journal entry line-item table to three reference tables — Business Units, "
                   "Chart of Accounts, and Preparer Info — matching on BusinessUnitID, GLAccountNumber, and "
                   "PreparerID respectively, using both XLOOKUP and VLOOKUP to compare the two methods.",
        "tools": "Excel XLOOKUP, VLOOKUP, multi-table joins.",
        "challenges": "The Chart of Accounts table had similarly structured columns for AccountType and "
                      "AccountClass, which risked pulling the wrong lookup column if the formula wasn't set "
                      "up carefully.",
        "outcomes": "Delivered a fully enriched 789-line general ledger extract with business unit names, GL "
                    "account names/types/classes, and preparer names attached to every line, ready for "
                    "management reporting.",
    },
    "images": [
        ("ETL_Case4_solution.png", "Raw journal entry lines enriched with business unit, account, and preparer detail"),
    ],
}

ETL_CASES = [ETL_1, ETL_2, ETL_3, ETL_4]

BANKDATA_CROSS_LINK = (
    "Also relevant: the **Bankdata forecasting case** (see *Business Decision Analytics*), where forecast "
    "accuracy was evaluated across 3,600+ forecast-vs-actual pairs to support budgeting and cost planning."
)


# -----------------------------------------------------------------------
# RENDER HELPERS
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
            cols = st.columns(len(case["images"]))
            for col, (fname, caption) in zip(cols, case["images"]):
                with col:
                    show_image(fname, caption)

        if case.get("queries"):
            st.markdown("---")
            st.markdown("**Query evidence**")
            for q in case["queries"]:
                st.markdown(f"*{q['label']}*")
                st.code(q["sql"], language="sql")
                fname, caption = q["image"]
                show_image(fname, caption)
                st.markdown("")


# -----------------------------------------------------------------------
# TABS — SECTIONS A / B / C / D
# -----------------------------------------------------------------------

tab_a, tab_b, tab_c, tab_d = st.tabs(
    [
        "A · Cost Control",
        "B · Financial Performance",
        "C · Auditing",
        "D · Data Reliability",
    ]
)

with tab_a:
    eyebrow("Section A")
    st.subheader("Management Accounting & Cost Control")
    render_full_case(FAIRVIEW)
    render_full_case(INTEGRATECO)
    st.caption(BANKDATA_CROSS_LINK)

with tab_b:
    eyebrow("Section B")
    st.subheader("Financial Performance Analysis")
    render_full_case(EY_DUPONT)
    st.info(
        "Open **EY DuPont Dashboard** in the sidebar for the interactive recreation of the "
        "Power BI pages (data accuracy, industry benchmarks, company drill-down), built from "
        "`EY_DuPont.xls`."
    )

    st.markdown("---")
    st.markdown(
        case_card_html(
            "Bankdata Case 2 — Financial Performance Benchmarking",
            "How does bank performance differ across data centre groups, and how comparable are those results?",
            ["Excel", "Power Query", "Python", "Financial KPIs"],
            "ROE · ROA · Cost-to-income · Revenue per employee",
        ), unsafe_allow_html=True,
    )
    with st.expander("View the financial benchmarking perspective"):
        st.markdown(
            "**Accounting contribution**  \nPrepared bank financial data, calculated four performance "
            "KPIs, and compared group medians. The analysis considers profitability, cost efficiency, "
            "and employee productivity together rather than treating one ratio as overall performance."
        )
        st.markdown(
            "**Comparability**  \nBank size, mortgage affiliation, repeated observations, and merger "
            "history can influence the comparison. Sensitivity analysis helps distinguish an "
            "observed financial pattern from a defensible claim about data centre affiliation."
        )
        st.markdown(
            "**Decision supported**  \nGive Bankdata a qualified benchmarking narrative for customer "
            "discussions, without presenting financial differences as proof of provider impact."
        )
        st.markdown("---")
        st.markdown("**Dashboard evidence**")
        # Explorer hides extensions; accept common image types and case variants.
        bankdata_images = [
            ("bankdata_marketshare", "Bankdata — market share overview (context for the comparison)"),
            ("Bankdata_association", "Bankdata — data centre affiliation and bank performance analysis"),
        ]
        available_images = sorted(os.listdir(IMG_DIR)) if os.path.isdir(IMG_DIR) else []
        for stem, caption in bankdata_images:
            filename = next(
                (
                    name for name in available_images
                    if os.path.splitext(name)[0].casefold() == stem.casefold()
                    and os.path.splitext(name)[1].lower() in {".png", ".jpg", ".jpeg", ".webp"}
                ),
                stem + ".png",
            )
            show_image(filename, caption)
        st.caption(
            "Market share provides context; it is not one of the four financial performance KPIs."
        )

        st.page_link("pages/5_Research_Based_Problem_Solving.py", label="Read the full Bankdata Case 2 research →")
        download_bankdata_case()

with tab_c:
    eyebrow("Section C")
    st.subheader("Auditing Analytics & Internal Control Testing")
    render_full_case(PCARD)

with tab_d:
    eyebrow("Section D")
    st.subheader("Accounting Data Reliability & ETL")
    st.caption("Cleaning, transforming, joining, and validating accounting data before it's ready for analysis.")
    for case in ETL_CASES:
        render_full_case(case)
    download_button_for("ELT.zip", "Download all 4 ETL case files")

st.markdown("---")

# -----------------------------------------------------------------------
# DOWNLOADS
# -----------------------------------------------------------------------

eyebrow("Resources")
st.subheader("Downloads")
dl_cols = st.columns(5)
with dl_cols[0]:
    download_button_for(FAIRVIEW["download"], "Fairview files")
with dl_cols[1]:
    download_button_for(INTEGRATECO["download"], "IntegrateCo files")
with dl_cols[2]:
    download_button_for(EY_DUPONT["download"], "EY DuPont files")
with dl_cols[3]:
    download_button_for(PCARD["download"], "P-Card files")
with dl_cols[4]:
    download_button_for(PCARD["download"], "ELT files")