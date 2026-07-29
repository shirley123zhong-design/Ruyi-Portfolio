import streamlit as st
import os
import mimetypes
import sys
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_PROJECT_ROOT)
os.chdir(_PROJECT_ROOT)  # ensure relative asset paths work no matter where streamlit was launched from
from theme import apply_theme, hero, eyebrow

st.set_page_config(page_title="Downloads | Shirley Zhong", page_icon="📥", layout="wide")
apply_theme()

st.page_link("app.py", label="← Back to home")

FILES_DIR = "assets/files"


def download_button_for(filename: str, label: str, note: str = ""):
    """
    Renders a download button for a file in assets/files/, but only if the
    file actually exists on disk. Silently skips (with a small warning) if
    the file is missing, so a broken path never breaks the page.
    """
    filepath = os.path.join(FILES_DIR, filename)

    if not os.path.isfile(filepath):
        st.warning(f"⚠️ Missing file: `{filename}`")
        return

    mime_type, _ = mimetypes.guess_type(filepath)
    mime_type = mime_type or "application/octet-stream"

    with open(filepath, "rb") as f:
        file_bytes = f.read()

    st.markdown(
        f"""
        <div style="border:1px solid #E3E2DF;border-left:3px solid #141414;border-radius:4px;
                     padding:12px 16px;margin-bottom:10px;background:#FFFFFF;
                     display:flex;justify-content:space-between;align-items:center;">
            <div>
                <p style="margin:0;font-weight:600;color:#141414;font-size:0.96rem;">{label}</p>
                <p style="margin:2px 0 0 0;color:#8a8a8a;font-size:0.82rem;">{note}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.download_button(
        label="⬇ Download",
        data=file_bytes,
        file_name=filename,
        mime=mime_type,
        key=f"dl_{filename}",
    )


hero(
    icon="📥",
    title="Downloads",
    subtitle=(
        "Everything below is available to download directly — my CV, transcript, and the underlying "
        "files behind each case study on this site."
    ),
)

# --- Core documents ---
eyebrow("Start here")
st.subheader("Core Documents")
download_button_for("Shirley - CV.pdf", "CV", "My current CV")
download_button_for("SDU_transcript.pdf", "SDU Transcript", "Official academic transcript")

st.divider()

# --- Case study deliverables ---
eyebrow("Evidence")
st.subheader("Case Study Files")
download_button_for("Fairview.zip", "Fairview",
    "Should reimbursement move from mileage to a flat rate? Built a dynamic Power BI tool showing the cost impact by office and employee.")
download_button_for("CoffeeGo_PowerQuery.zip", "CoffeeGo (Power Query)",
    "Bi-weekly coffee ordering needed manual rework every cycle — built a repeatable, weather-adjusted Power Query pipeline.")
download_button_for("Bankdata_forecast.zip", "Bankdata Forecast",
    "Which forecasts could management trust before budgeting? Tested 3 methods and flagged the volatile categories needing review.")
download_button_for("EY_DUPONT.zip", "EY DuPont",
    "Which industries and companies were financially strongest, and why? Broke ROE into margin, turnover, and leverage to find the real driver.")
download_button_for("Pcards.zip", "P-Cards",
    "Were employees following card spending rules? SQL audit flagged split purchases, limit violations, and prohibited expense combinations.")
download_button_for("IntregrateCo.zip", "IntegrateCo",
    "Payroll rose 27% despite fewer staff — traced the increase to specific job codes and a $1.8M payroll data-integrity gap.")
download_button_for("ELT.zip", "ELT Case",
    "Messy, inconsistently structured source data across 4 cases — cleaned, split, and validated it using Power Query and Excel.")
download_button_for("Customer_Analytics_Churn_Prediction.zip", "Customer Analytics & Churn Prediction",
    "Which customers were at risk of churning? Built a full SQL-to-Power BI pipeline, comparing 7 models to segment and predict.")
download_button_for("SupplyChain_PerformanceAnalysis.zip", "Supply Chain Performance Analysis",
    "Where were the supply chain inefficiencies? Built KPIs across inventory, suppliers, and regions to find and rank them.")
download_button_for("Employee_Burnout_Research_Study.pdf", "Employee Burnout Research Study",
    "What's actually driving employee burnout — deadlines or something else? Found stress, not deadlines, was the real mechanism.")
download_button_for("FlexMatch_Marketplace_Validation.pdf", "FlexMatch — Gig Marketplace Validation",
    "Was there a real market for a hyper-local gig-matching platform? Tested it with a 41-day fake-door MVP before committing to build.")