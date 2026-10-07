import streamlit as st
import os
import sys
import base64
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # ensure relative asset paths work no matter where streamlit was launched from
from theme import apply_theme, eyebrow
from components.logic_map import render_logic_map
from components.project_carousel import render_project_carousel

st.set_page_config(
    page_title="Ruyi Zhong(Shirley) | Portfolio",
    page_icon="📊",
    layout="wide",
)
apply_theme()

# --- HOME PAGE LAYOUT: tighter sections, larger text, key-phrase highlights, phone tweaks ---
st.markdown(
    """
<style>
.block-container{padding-top:4.2rem !important;}
[data-testid="stVerticalBlock"]{gap:0.7rem;}
hr{margin:16px 0 !important;}
.stApp h3{padding-top:0.15rem !important;padding-bottom:0.45rem !important;}
.eyebrow{margin-bottom:2px;}
.stApp .home-name{font-family:'Archivo',sans-serif !important;font-weight:800 !important;font-size:clamp(2rem,5.5vw,2.6rem) !important;letter-spacing:0.01em;line-height:1.1 !important;margin:8px 0 0 0 !important;color:#141414 !important;}
.stApp .home-lead{font-size:1.25rem !important;font-weight:700 !important;color:#141414 !important;line-height:1.45 !important;margin:4px 0 8px 0 !important;}
.stApp .home-body{font-size:1.08rem !important;line-height:1.7 !important;color:#333 !important;max-width:920px;margin:0 !important;}
.stApp .hl{font-weight:600;color:#141414 !important;background:linear-gradient(transparent 60%,#E4E1DA 60%);padding:0 2px;}
.tag-row{margin:6px 0 2px 0;}
.tag-pill{font-size:0.86rem;}
[data-testid="stMarkdownContainer"] p strong{font-size:1.05rem;}
[data-testid="stCaptionContainer"] p{font-size:0.98rem !important;}
@media (max-width:640px){
  .block-container{padding-left:1.1rem !important;padding-right:1.1rem !important;padding-top:4rem !important;}
  .stApp .home-lead{font-size:1.15rem !important;}
  .stApp .home-body{font-size:1.02rem !important;}
  /* phones: photos first, then name and intro */
  [data-testid="stColumn"]:has(.photo-collage){order:-1;}
  .photo-collage{width:150px !important;height:170px !important;margin:0 0 6px 0 !important;}
}
</style>
""",
    unsafe_allow_html=True,
)

# --- HEADER ---
col1, col2 = st.columns([2, 1])

with col1:
    eyebrow("Portfolio")
    st.markdown('<p class="home-name">Ruyi Zhong(Shirley)</p>', unsafe_allow_html=True)
    st.subheader("MSc Data-Driven Business Development | SDU")

    contact_col1, contact_col2 = st.columns([3, 1])
    with contact_col1:
        st.write("📍 Denmark &nbsp;&nbsp; ✉️ shirley123zhong@gmail.com &nbsp;&nbsp; 🔗 [LinkedIn](https://www.linkedin.com/in/ruyi-zhong-a2252a194/)")
    with contact_col2:
        cv_path = "assets/files/Shirley - CV.pdf"
        if os.path.exists(cv_path):
            with open(cv_path, "rb") as f:
                st.download_button(
                    label="📄 Download CV",
                    data=f,
                    file_name="Shirley - CV.pdf",
                    mime="application/pdf"
                )
        else:
            st.caption(f"Add `{cv_path}` to enable the CV download.")

    st.markdown(
        '<p class="home-lead">I help organisations make better decisions through data.</p>'
        '<p class="home-body">Whether that means analysing <span class="hl">profitability</span> to support '
        'customer and pricing decisions, improving <span class="hl">forecasts</span> for planning, or building '
        '<span class="hl">dashboards</span> that highlight performance and risks, I connect analysis with practical '
        'business needs. I also explore how changes to the way <span class="hl">data is shared, managed and used '
        'across teams</span> could improve collaboration, strengthen control and create new business '
        'opportunities. This portfolio shows the questions I ask, the tools I use and the recommendations I develop.</p>',
        unsafe_allow_html=True,
    )

with col2:
    img1_path = "assets/img/profile_1.jpeg"
    img2_path = "assets/img/profile_2.jpeg"
    if os.path.exists(img1_path) and os.path.exists(img2_path):
        img1_b64 = base64.b64encode(Path(img1_path).read_bytes()).decode()
        img2_b64 = base64.b64encode(Path(img2_path).read_bytes()).decode()

        st.markdown(f"""
        <style>
        .photo-collage {{
            position: relative;
            width: clamp(140px, 30vw, 190px);
            height: clamp(160px, 34vw, 210px);
            margin: 8px auto 0 auto;
        }}
        .photo-collage img {{
            position: absolute;
            border-radius: 4px;
            filter: grayscale(15%);
            box-shadow: 0 6px 16px rgba(0,0,0,0.4);
            object-fit: cover;
            transition: transform 0.3s ease, box-shadow 0.3s ease, filter 0.3s ease;
            cursor: pointer;
        }}
        .photo-collage img:hover {{
            transform: scale(1.15);
            z-index: 10;
            filter: grayscale(0%);
            box-shadow: 0 10px 24px rgba(0,0,0,0.6);
        }}
        .photo1 {{
            top: 0;
            left: 0;
            width: 62%;
            height: 64%;
            z-index: 1;
            border: 3px solid #FFFFFF;
        }}
        .photo2 {{
            top: 36%;
            left: 42%;
            width: 58%;
            height: 61%;
            z-index: 2;
            border: 3px solid #FFFFFF;
        }}

        @media (max-width: 480px) {{
            .photo-collage {{
                width: 160px;
                height: 185px;
                margin-top: 20px;
            }}
        }}
        </style>

        <div class="photo-collage">
            <img src="data:image/jpeg;base64,{img1_b64}" class="photo1">
            <img src="data:image/jpeg;base64,{img2_b64}" class="photo2">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.caption("Add `assets/img/profile_1.jpeg` and `profile_2.jpeg` to show the photo collage.")

st.divider()

# --- SKILLS SUMMARY ---
eyebrow("Capabilities")
st.subheader("Core skills")

skills_col1, skills_col2, skills_col3, skills_col4 = st.columns(4)

with skills_col1:
    st.markdown("**Business Analytics**")
    pills = "".join(f'<span class="tag-pill">{s}</span>' for s in
        ["Forecasting", "Regression", "KPI analysis", "Dashboard insights", "Decision support"])
    st.markdown(f'<div class="tag-row">{pills}</div>', unsafe_allow_html=True)

with skills_col2:
    st.markdown("**Accounting & Performance**")
    pills = "".join(f'<span class="tag-pill">{s}</span>' for s in
        ["Cost analysis", "Financial performance", "Audit analytics", "Management reporting"])
    st.markdown(f'<div class="tag-row">{pills}</div>', unsafe_allow_html=True)

with skills_col3:
    st.markdown("**Digital Business Development**")
    pills = "".join(f'<span class="tag-pill">{s}</span>' for s in
        ["Digital strategy", "Transformation diagnosis", "Opportunity development", "Business models"])
    st.markdown(f'<div class="tag-row">{pills}</div>', unsafe_allow_html=True)

with skills_col4:
    st.markdown("**Tools & Systems**")
    pills = "".join(f'<span class="tag-pill">{s}</span>' for s in
        ["Power BI", "Excel", "SQL", "Python", "R", "Streamlit", "SAP", "Navision", "Business Central"])
    st.markdown(f'<div class="tag-row">{pills}</div>', unsafe_allow_html=True)

st.divider()

# --- APPROACH (logic map) ---
render_logic_map()

st.divider()

# --- NAVIGATION CARDS ---
eyebrow("Portfolio")
st.subheader("Explore my work")
st.caption("Six angles on the same skill set. Start wherever's most relevant to the role, or work through in order.")

CARDS = [
    {"number": "01 · START HERE", "icon": "📊", "title": "Business Decision Analytics",
     "description": "Forecasting, regression, customer analytics, and operational insights that support "
                    "planning, cost decisions, and management recommendations.",
     "page": "pages/1_Business_Decision_Analytics.py"},
    {"number": "02", "icon": "🧾", "title": "Accounting & Performance Insights",
     "description": "Accounting-focused analytics for cost control, financial performance, audit testing, "
                    "and data-driven management reporting.",
     "page": "pages/2_Accounting_and_Performance_Insights.py"},
    {"number": "03", "icon": "🔄", "title": "Digital Transformation & Scaling",
     "description": "Diagnosing digital transformation gaps and developing practical recommendations across "
                    "strategy, structure, processes, people, culture, and AI adoption.",
     "page": "pages/3_Digital_Transformation_and_Scaling.py"},
    {"number": "04", "icon": "💡", "title": "Market Opportunity & Innovation",
     "description": "Using trend data, user research, experiments, and MVP testing to identify unmet needs "
                    "and develop business opportunities.",
     "page": "pages/4_Market_Opportunity_and_Innovation.py"},
    {"number": "05", "icon": "🔍", "title": "Research-Based Problem Solving",
     "description": "Turning business problems into research questions, testing relationships between "
                    "variables, and translating evidence into management recommendations.",
     "page": "pages/5_Research_Based_Problem_Solving.py"},
    {"number": "06", "icon": "🛠️", "title": "Technical Skills & Code Gallery",
     "description": "Selected technical evidence behind the cases, including Python, SQL, Power BI, Power "
                    "Query, R, Excel, Streamlit, and machine learning workflows.",
     "page": "pages/6_Technical_Skills_and_Code_Gallery.py"},
]

render_project_carousel(CARDS)
