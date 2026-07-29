import streamlit as st
import os
import sys
import base64
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # ensure relative asset paths work no matter where streamlit was launched from
from theme import apply_theme, eyebrow, nav_card_html

st.set_page_config(
    page_title="Ruyi Zhong(Shirley) | Portfolio",
    page_icon="📊",
    layout="wide",
)
apply_theme()

# --- HEADER ---
col1, col2 = st.columns([2, 1])

with col1:
    eyebrow("Portfolio")
    st.markdown(
        """
        <p style="font-family:'Archivo',sans-serif; font-weight:800; font-size:2.5rem;
                   letter-spacing:0.01em; margin-bottom:0; color:#141414;">
            Ruyi Zhong(Shirley)
        </p>
        """,
        unsafe_allow_html=True,
    )
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
        """
        <p style="font-size:1.15rem; font-weight:600; color:#141414; line-height:1.5; margin-bottom:6px;">
        I help organisations make better decisions through data.
        </p>
        <p style="color:#444; font-size:1.0rem; line-height:1.6;">
        Whether that means building dashboards that track performance, analysing financial data
        to surface risks, or structuring processes to support digital transformation — this
        portfolio documents how I work: the questions I ask, the tools I use, and the outcomes
        I deliver.
        </p>
        """,
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

# --- NAVIGATION CARDS ---
eyebrow("Portfolio")
st.subheader("Explore my work")
st.caption("Six angles on the same skill set — start wherever's most relevant to the role, or work through in order.")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        nav_card_html(
            "01 · START HERE", "📊", "Business Decision Analytics",
            "Forecasting, regression, customer analytics, and operational insights that support "
            "planning, cost decisions, and management recommendations.",
        ),
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Business_Decision_Analytics.py", label="Explore →")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    st.markdown(
        nav_card_html(
            "02", "🧾", "Accounting & Performance Insights",
            "Accounting-focused analytics for cost control, financial performance, audit testing, "
            "and data-driven management reporting.",
        ),
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_Accounting_and_Performance_Insights.py", label="Explore →")

with col2:
    st.markdown(
        nav_card_html(
            "03", "🔄", "Digital Transformation & Scaling",
            "Diagnosing digital transformation gaps and developing practical recommendations across "
            "strategy, structure, processes, people, culture, and AI adoption.",
        ),
        unsafe_allow_html=True,
    )
    st.page_link("pages/3_Digital_Transformation_and_Scaling.py", label="Explore →")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    st.markdown(
        nav_card_html(
            "04", "💡", "Market Opportunity & Innovation",
            "Using trend data, user research, experiments, and MVP testing to identify unmet needs "
            "and develop business opportunities.",
        ),
        unsafe_allow_html=True,
    )
    st.page_link("pages/4_Market_Opportunity_and_Innovation.py", label="Explore →")

with col3:
    st.markdown(
        nav_card_html(
            "05", "🔍", "Research-Based Problem Solving",
            "Turning business problems into research questions, testing relationships between "
            "variables, and translating evidence into management recommendations.",
        ),
        unsafe_allow_html=True,
    )
    st.page_link("pages/5_Research_Based_Problem_Solving.py", label="Explore →")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    st.markdown(
        nav_card_html(
            "06", "🛠️", "Technical Skills & Code Gallery",
            "Selected technical evidence behind the cases, including Python, SQL, Power BI, Power "
            "Query, R, Excel, Streamlit, and machine learning workflows.",
        ),
        unsafe_allow_html=True,
    )
    st.page_link("pages/6_Technical_Skills_and_Code_Gallery.py", label="Explore →")
