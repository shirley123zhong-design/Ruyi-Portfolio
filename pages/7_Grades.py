import streamlit as st
from pathlib import Path
import sys
import os
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_PROJECT_ROOT)
os.chdir(_PROJECT_ROOT)  # ensure relative asset paths work no matter where streamlit was launched from
from theme import apply_theme, hero, eyebrow

st.set_page_config(
    page_title="Grades | Shirley Zhong",
    page_icon="🎓",
    layout="wide"
)
apply_theme()

st.page_link("app.py", label="← Back to home")

# ── HELPER ─────────────────────────────────────────────────────────────
def download_file(label, path, file_name, mime="application/pdf"):
    file_path = Path(path)
    if file_path.exists():
        with open(file_path, "rb") as f:
            st.download_button(
                label=label,
                data=f,
                file_name=file_name,
                mime=mime
            )
    else:
        st.warning(f"File not found: {path}")


def course_card(title, grade, ects_grade, description, skills):
    st.markdown(
        f"""
        <div class="case-card" style="border-left-color:#141414;">
            <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:flex-start; gap:16px;">
                <div style="flex:1 1 260px; min-width:0;">
                    <h3 style="margin-bottom:6px; color:#141414; font-size:1.15rem;">{title}</h3>
                    <p style="font-size:15.5px; color:#444; line-height:1.55; margin-bottom:10px;">
                        {description}
                    </p>
                    <p style="font-size:14.5px; color:#555; margin-bottom:0;">
                        <b>Key skills:</b> {skills}
                    </p>
                </div>
                <div class="grade-tile" style="
                    min-width:105px;
                    background:linear-gradient(155deg, #242424, #1A1A1A);
                    border-radius:4px;
                    padding:15px;
                    text-align:center;
                ">
                    <div style="font-size:30px; font-weight:800; font-family:'Archivo',sans-serif;">{grade}</div>
                    <div style="font-size:14px;">ECTS {ects_grade}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ── PAGE HEADER ───────────────────────────────────────────────────────
hero(
    icon="🎓",
    title="Grades & Course Transcript",
    subtitle=(
        "This page summarises my completed MSc courses in Data-Driven Business Development at the "
        "University of Southern Denmark. The courses combine business analytics, accounting analytics, "
        "digital strategy, research methodology, programming, and opportunity development."
    ),
)

# ── SUMMARY METRICS ──────────────────────────────────────────────────
eyebrow("At a glance")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Completed ECTS", "70")

with m2:
    st.metric("Average grade", "11.4")

with m3:
    st.metric("Highest grade", "12 / A")

with m4:
    st.metric("Courses completed", "7")

st.caption(
    "Grades are based on the official SDU transcript. Danish grade 12 corresponds to ECTS grade A, and Danish grade 10 corresponds to ECTS grade B."
)

st.divider()

# ── DOWNLOAD TRANSCRIPT ───────────────────────────────────────────────
left, right = st.columns([2, 1])

with left:
    eyebrow("Verification")
    st.subheader("Official transcript")
    st.write(
        "The official transcript confirms the completed courses, grades, ECTS credits, and enrolment "
        "in the MSc programme in Economics and Business Administration — Data-Driven Business Development."
    )

with right:
    download_file(
        label="📄 Download official SDU transcript",
        path="assets/files/SDU_transcript.pdf",
        file_name="SDU_Transcript_Ruyi_Zhong.pdf"
    )

st.divider()

# ── COURSE CARDS ─────────────────────────────────────────────────────
eyebrow("Transcript detail")
st.subheader("Completed courses")

course_card(
    title="Digital Business Strategies",
    grade="12",
    ects_grade="A",
    description=(
        "Studied how digitalization, data, algorithms, AI, IoT, and big data reshape strategy, "
        "innovation, competition, business models, ecosystems, and organizational transformation. "
        "The course emphasized strategy as an iterative and case-based process in the digital age."
    ),
    skills="Digital strategy · Business models · Digital transformation · AI · Big data · Case analysis"
)

course_card(
    title="Data Science for Business Development",
    grade="10",
    ects_grade="B",
    description=(
        "Applied databases, data extraction, data analysis, machine learning, and data visualization "
        "to business development problems. The course focused on the full business data lifecycle and "
        "how analytical results can be communicated through visualization tools."
    ),
    skills="SQL · Databases · Data modelling · Machine learning · Power BI · Business analytics"
)

course_card(
    title="Programming for Data Science",
    grade="12",
    ects_grade="A",
    description=(
        "Developed Python-based data analysis workflows, including data modelling, gathering, cleaning, "
        "processing, and visualization. The course strengthened practical coding ability for structured "
        "data work and interactive result communication."
    ),
    skills="Python · Data cleaning · Data processing · Visualization · Streamlit · Interactive result pages"
)

course_card(
    title="Methodologies for Business Research",
    grade="10",
    ects_grade="B",
    description=(
        "Designed and evaluated empirical business studies using qualitative and quantitative research methods. "
        "The course covered research design, data collection, scientific quality criteria, qualitative interpretation, "
        "quantitative analysis, mediation, moderation, and reporting of findings."
    ),
    skills="Research design · Qualitative analysis · Quantitative analysis · Mediation · Moderation · R/statistics"
)

course_card(
    title="Organizing and Scaling Digital Business",
    grade="12",
    ects_grade="A",
    description=(
        "Explored how firms organize, lead, and scale digital businesses by aligning structure, processes, "
        "rewards, people, culture, and leadership with emerging digital technologies and data-driven business strategies."
    ),
    skills="Organizational design · Digital scaling · Leadership · Culture · Transformation alignment"
)

course_card(
    title="Idea and Opportunity Development",
    grade="12",
    ects_grade="A",
    description=(
        "Developed entrepreneurial opportunities through data-supported problem identification, idea generation, "
        "evaluation, prototyping, Lean Startup testing, Business Model Canvas, effectuation, and scaling under uncertainty."
    ),
    skills="Entrepreneurship · Opportunity development · MVP testing · Lean Startup · BMC · Prototyping"
)

course_card(
    title="Data Analytics in Accounting",
    grade="12",
    ects_grade="A",
    description=(
        "Applied data analytics to accounting problems and reflected on how technology changes auditing, "
        "financial accounting, and management accounting. The course involved Excel, SQL, Power BI, ETL, "
        "visualization, and communication of data-driven accounting insights."
    ),
    skills="Excel · SQL · Power BI · ETL · Forecasting · Accounting analytics · Dashboard communication"
)

st.divider()

# ── BUSINESS VALUE SUMMARY ───────────────────────────────────────────
eyebrow("Why it matters")
st.subheader("What these courses show")

b1, b2, b3 = st.columns(3)

with b1:
    st.markdown("""
    **Business analysis foundation**  
    Forecasting, customer analytics, SQL, Python, Power BI, and machine learning applied to business problems.
    """)

with b2:
    st.markdown("""
    **Controller and accounting relevance**  
    Accounting analytics, ETL, financial performance analysis, audit testing, cost control, and management reporting.
    """)

with b3:
    st.markdown("""
    **Business development perspective**  
    Digital transformation, innovation, opportunity development, research-based problem solving, and strategic thinking.
    """)