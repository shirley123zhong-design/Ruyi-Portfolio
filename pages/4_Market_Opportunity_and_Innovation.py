import streamlit as st
import sys
import os
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_PROJECT_ROOT)
os.chdir(_PROJECT_ROOT)  # ensure relative asset paths work no matter where streamlit was launched from
from theme import apply_theme, hero, eyebrow

st.set_page_config(
    page_title="Opportunity Discovery & Innovation | Shirley Zhong",
    page_icon="💡",
    layout="wide",
)
apply_theme()

st.page_link("app.py", label="← Back to home")

# --- HEADER / VALUE ---
hero(
    icon="💡",
    title="Opportunity Discovery & Intrapreneurial Innovation",
    subtitle=(
        "How do you know a problem is real before you spend money on it? This page shows how I take "
        "a business idea from a rough guess to a decision I can defend with data — find the real "
        "problem, test it cheaply, and decide whether to pursue, adjust, or drop it."
    ),
    tags=["Opportunity Discovery", "Hypothesis Testing", "Lean Startup", "MVP Design", "Go / No-Go Decisions"],
    flow="Problem hypothesis → Cheap test → Read the data → Testable hypotheses → Pricing test → Persevere, pivot, or perish",
)

# --- WHY THIS MATTERS FOR THE ROLE (moved before the process) ---
eyebrow("Relevance")
st.subheader("Why this matters for the role")
st.caption("Good business development starts with learning before you invest.")

tab1, tab2, tab3 = st.tabs(["Business Developer", "Business Analyst", "Controller"])
with tab1:
    st.write("Shows I can spot opportunities, test real demand, and build a "
             "business case on evidence instead of a hunch.")
with tab2:
    st.write("Shows I can take something vague, structure it, gather user "
             "insight, and turn it into questions that can actually be tested.")
with tab3:
    st.write("Shows I can validate assumptions and judge whether an initiative "
             "is worth funding, tying it back to resource use, risk, and expected value.")

st.divider()

# --- PROCESS / LOGIC (foldable) ---
eyebrow("Method")
st.subheader("The process")
st.caption("Business question: is there a real, provable need for this, and is it worth pursuing?")

steps = [
    {
        "title": "Step 1 · Don't trust the first version of the problem",
        "body": "The starting assumption was: \"Businesses struggle to cover short term jobs.\"\n\n"
                "At first it looked like a staffing shortage. Interviews and early data "
                "told a different story. The real issue was broader: coordination, "
                "trust, reliability, and admin work, not just a lack of workers.",
        "applied": "Applied to a company, this is the same habit you need when "
                   "you're looking into a variance or a customer complaint. The first "
                   "explanation is rarely the real driver.",
    },
    {
        "title": "Step 2 · Test cheaply before building anything",
        "body": "Instead of building a full platform, we ran a 41 day fake door test, "
                "just a landing page and a QR code, no paid ads, to see if real users "
                "would show interest before spending on development.",
        "applied": "Applied to a company, this is basically a pilot before asking "
                   "for budget. Prove the case first, then ask for the money.",
    },
    {
        "title": "Step 3 · Let the data show where to focus",
        "body": "The test showed stronger interest from job seekers than from job "
                "posters. That changed the question. It wasn't about whether workers "
                "existed, it was about whether businesses could be activated enough "
                "on the demand side.",
        "applied": "Applied to a company, this means reading the numbers to find "
                   "the actual bottleneck instead of sticking to your first assumption.",
    },
    {
        "title": "Step 4 · Turn assumptions into testable hypotheses",
        "body": "Three MVPs tested specific questions. Does visibility speed up "
                "matching? Does filtering improve candidate quality? Does price "
                "change response speed and quality? Each one measured something "
                "concrete.",
        "applied": "Applied to a company, this is the same logic as testing two "
                   "pricing models or two process versions before rolling one out "
                   "across the whole organization.",
    },
    {
        "title": "Step 5 · Use pricing data to test commercial viability",
        "body": "At 50 DKK per hour: 6 applicants, only 1 usable, 176 minutes "
                "average response time.\n\n"
                "At 200 DKK per hour: 11 applicants, 4 usable, 77 minutes average "
                "response time.\n\n"
                "Higher pay clearly sped things up, but it didn't improve quality by "
                "the same amount. That pointed toward a commission based pricing model.",
        "applied": "Applied to a company, this is exactly what controller work "
                   "looks like: testing price and cost sensitivity with real data "
                   "before recommending a pricing or investment structure.",
    },
    {
        "title": "Step 6 · Make the call: persevere, pivot, or perish",
        "body": "The evidence didn't support launching the idea as it was, and it "
                "didn't support dropping it either. The decision was to persevere "
                "with an adjusted prototype.",
        "applied": "Applied to a company, this is the disciplined call to adjust "
                   "and keep going, which is what companies need when a project "
                   "shows promise but isn't proven yet.",
    },
]

step_tabs = st.tabs([f"Step {i}" for i in range(1, len(steps) + 1)])
for tab, step in zip(step_tabs, steps):
    with tab:
        st.markdown(f"**{step['title'].split('· ', 1)[-1]}**")
        st.markdown(step["body"])
        st.info(step["applied"])

st.divider()

# --- PROJECT DETAILS (folded, background on the actual project) ---
eyebrow("Background")
st.subheader("Project details")
st.caption("Want the full background on FlexMatch? It's all here, folded away so it doesn't take over the page.")

with st.expander("📌 Research question"):
    st.markdown("""
Is there a real, provable need for a flexible, hyper-local platform matching
short-term jobs with available workers in Denmark, and is it worth pursuing
further?

The starting point came from a broader trend: flexible work and gig-style
jobs are growing fast, but the platforms and channels people currently use
(Facebook groups, staffing agencies) are slow, fragmented, and not built for
small, urgent, private tasks.
""")

with st.expander("🧩 Prototype"):
    st.markdown("""
FlexMatch was designed as a two-sided platform connecting **job posters**
(businesses or individuals needing short-term help) with **job seekers**
(people with flexible time who want extra income).

The initial design included:
- GPS-based matching, so nearby workers get recommended first
- Instant task visibility, instead of waiting on admin approval
- Centralized communication, so everything happens in one place instead of
  scattered Facebook messages
- Administrative support, including payment, contracts, and payroll handling

The idea came from a real gap: current platforms are shaped around
companies and agencies, not small private tasks that need someone in the
next few hours.
""")

with st.expander("🧪 MVP tests"):
    st.markdown("""
Three MVPs were run to test specific parts of the idea before building
anything close to a real platform.

**MVP 1, manual Facebook matching**
A cat-sitting task was posted in four Facebook groups to see if existing
channels could already solve the problem. Result: average visibility delay
of 565.7 minutes and an average response time of 1,058.1 minutes, on top of
fragmented communication and admin approval delays. Existing channels were
clearly too slow for anything urgent.

**MVP 2, structured matching**
A moving-helper task was posted with structured fields (location,
availability, experience). Applicants were compared and ranked manually.
Result: matching worked better when it combined several factors (location,
availability, experience, trust) instead of relying on GPS distance alone.

**MVP 3, pricing sensitivity**
The same moving-helper task was posted at three price points, 50, 120, and
200 DKK per hour. Result: higher pay brought faster responses (176 minutes
down to 77 minutes) and more applicants, but not proportionally better
quality (only 1 usable applicant at 50 DKK/hour versus 4 at 200 DKK/hour).
""")

with st.expander("📊 Results"):
    res_col1, res_col2, res_col3, res_col4 = st.columns(4)
    res_col1.metric("Conversion rate", "81.2 %", "82 of 101 sessions")
    res_col2.metric("Two sided market", "54 : 28", "job seekers to job posters")
    res_col3.metric("Response time at 200 DKK/hr", "77 min", "99 min faster than 50 DKK/hr")
    res_col4.metric("Paid advertising spent", "0 DKK", "over 41 days")

    st.markdown("""
The fake-door test ran for 41 days with no paid advertising and still
pulled in 82 submissions from 101 sessions.

Job posters said they'd pay around 190 DKK per task on average, plus about
66 DKK extra for faster matching. Job seekers expected around 112 DKK an
hour on average.

The final call was to persevere with an adjusted prototype rather than
fully pivot or shut it down.
""")

st.divider()

# --- EVIDENCE / DOWNLOADS ---
eyebrow("Resources")
st.subheader("Evidence & downloads")

try:
    with open("assets/files/FlexMatch_Marketplace_Validation.pdf", "rb") as f:
        st.download_button(
            label="📄 Download full FlexMatch report",
            data=f,
            file_name="FlexMatch_Marketplace_Validation.pdf",
            mime="application/pdf",
        )
except FileNotFoundError:
    st.caption("Add the FlexMatch PDF to assets/files/ to enable this button.")

st.caption(
    "Suggested visuals: problem reframing diagram, Build Measure Learn loop, "
    "fake door result screenshot, MVP price test comparison, Business Model Canvas"
)