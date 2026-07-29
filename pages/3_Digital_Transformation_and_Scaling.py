import streamlit as st
import sys
import os
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_PROJECT_ROOT)
os.chdir(_PROJECT_ROOT)  # ensure relative asset paths work no matter where streamlit was launched from
from theme import apply_theme, hero, eyebrow

st.set_page_config(page_title="Digital Transformation & Scaling | Shirley Zhong", page_icon="🔄", layout="wide")
apply_theme()

st.page_link("app.py", label="← Back to home")

# -----------------------------------------------------------------------
# PAGE HEADER
# -----------------------------------------------------------------------

hero(
    icon="🔄",
    title="Digital Transformation & Scaling",
    subtitle=(
        "These cases show how strategy, data, organizational design, and AI readiness connect to "
        "real business outcomes — how digital strategy creates and keeps evolving value, why digital "
        "initiatives struggle to scale, and what conditions must be in place before AI adoption "
        "creates sustainable value."
    ),
    tags=[
        "Digital Strategy", "Transformation Diagnosis", "Organizational Design",
        "AI Adoption", "Digital Scaling", "Business Model Change",
        "Leadership & Culture Alignment", "Continuous Improvement",
    ],
    flow="Business challenge → Current-state diagnosis → Strategy & value creation analysis → "
         "Organizational alignment → Capability gaps → Scaling barriers → Recommendations → Continuous adjustment",
)

# ---------------------------------------------------------------------------
# TAKEAWAY — the executive summary, up front before the case detail
# ---------------------------------------------------------------------------
eyebrow("The takeaway")
st.info(
    "**Across all three cases, the same underlying insight holds:** digital "
    "transformation gets stuck for organizational reasons as often as strategic or "
    "technical ones. Good strategy needs continuous alignment to remain relevant. "
    "Good digital ideas need structure and decision rights to scale. Good AI tools "
    "need governance, role clarity, and readiness before they can create sustainable "
    "value."
)

st.caption(
    "This page shows that I can diagnose why transformation stalls, not just "
    "suggest what technology to adopt — and that I understand digital "
    "transformation as an ongoing process of learning, reaction, and adjustment."
)

st.markdown("---")

# ---------------------------------------------------------------------------
# LOGIC — tab navigation, matching Pages 1-2
# ---------------------------------------------------------------------------
tab_a, tab_b, tab_c = st.tabs([
    "A · Strategy & Value Creation",
    "B · Transformation & Scaling",
    "C · AI Adoption & Readiness",
])

with tab_a:
    eyebrow("Section A")
    st.subheader("Digital Strategy & Value Creation")
    st.caption("Framework: Strategy-as-Practice · Ecosystem Thinking")
    st.markdown(
        "An anonymized case looking at a mobility group with strong access to vehicle, "
        "customer, fleet, and service data, facing the question of how to turn that "
        "data into legal, useful, and commercially valuable services amid EV adoption, "
        "changing customer expectations, and EU data regulation."
    )

    st.image("assets/img/Digital_Strategy_as_an_Ongoing_Process.png",
             caption="Digital strategy as an ongoing process", use_container_width=True)

    with st.expander("Read the full case analysis"):
        st.markdown("**Business challenge**")
        st.markdown(
            "- Not simply \"we have data,\" but how to use vehicle, customer, fleet, "
            "and service data legally, strategically, and commercially\n"
            "- Balancing customer value, OEM and brand requirements, regulatory "
            "responsibility, and investment risk all at once"
        )

        st.markdown("**Company situation**")
        st.markdown(
            "- Operates across import, retail, finance, workshops, used cars, fleet, "
            "IT, data analytics, and customer engagement\n"
            "- Data spread across many brands, countries, and business units\n"
            "- External pressure rising from EV adoption, changing after-sales "
            "economics, digital-first customer expectations, and EU data & "
            "cybersecurity regulation"
        )

        st.markdown("**Diagnosis**")
        st.markdown(
            "- A data-to-value transformation problem, not a data-collection problem\n"
            "- Data access is a strategic asset, but not yet a business model by "
            "itself\n"
            "- Value depends on connecting data to concrete use cases, governance, "
            "customer trust, and organizational execution\n"
            "- Needed clearer prioritization of which data use cases to pursue first"
        )

        st.markdown("**Recommendation**")
        st.markdown(
            "- Prioritize a small number of high-value use cases (predictive "
            "maintenance, battery health reporting, fleet optimization)\n"
            "- Separate safe/feasible ideas from high-risk ones before committing\n"
            "- Build cross-functional data governance early\n"
            "- Move through a gate-based roadmap: basic understanding → market "
            "validation → proof of concept → MVP → full release\n"
            "- Keep the strategy open to learning from pilots, customers, and legal "
            "review"
        )

        st.markdown("**Business value**")
        st.markdown(
            "Shows how a company can move from owning data to creating value from "
            "data — using it responsibly, legally, and strategically to support new "
            "services, customer retention, ecosystem collaboration, and future "
            "business model development."
        )

with tab_b:
    eyebrow("Section B")
    st.subheader("Digital Transformation Diagnosis & Scaling")
    st.caption("Framework: Dynamic Capabilities: Sense–Seize–Transform · Star Model")
    st.markdown(
        "A case looking at an insurance company that could spot digital opportunities "
        "early and build fast prototypes, but struggled to turn pilots into scalable "
        "business solutions — a story about the gap between digital ambition and "
        "scalable execution."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.image("assets/img/Sense–Seize–Transform.png",
                  caption="Sense–Seize–Transform diagnosis", use_container_width=True)
    with col2:
        st.image("assets/img/STAR_model.png",
                  caption="Star Model — organizational alignment", use_container_width=True)

    with st.expander("Read the full case analysis"):
        st.markdown("**Business challenge**")
        st.markdown(
            "- How to move from digital experiments to scalable digital services "
            "before competitors capture the value\n"
            "- Shift needed: from \"we can build promising pilots\" to \"we can "
            "prioritize, govern, scale, and improve the initiatives that create real "
            "business value\""
        )

        st.markdown("**Company situation**")
        st.markdown(
            "- Invested in cloud infrastructure, a data platform, and APIs\n"
            "- Could spot market opportunities early and build prototypes quickly\n"
            "- Many initiatives stuck as pilots — too many competing for the same "
            "resources\n"
            "- Several pilots ran for months without a clear stop/go decision\n"
            "- Finance, legal, risk, and operations only got involved after the demo "
            "stage"
        )

        st.markdown("**Diagnosis**")
        st.markdown(
            "- A pilot-to-scale capability gap, not an ideas gap\n"
            "- Strong at sensing opportunities and reasonably able to seize them via "
            "prototypes\n"
            "- Weakness appears after the pilot stage: mobilizing resources, fast "
            "rollout decisions, aligning departments, redesigning processes\n"
            "- The bottleneck is the organization's capability to scale, not a lack of "
            "ideas"
        )

        st.markdown("**Digital maturity position**")
        st.markdown(
            "- Low customer experience: low app rating, unclear claim status, weak "
            "online quote-to-bind conversion\n"
            "- Low operational efficiency: slower, less standardized workflows than "
            "competitors\n"
            "- Low on both dimensions places the company in the **\"silos and "
            "spaghetti\"** quadrant — the least mature position"
        )
        st.image("assets/img/NSM_Digital_Maturity.png",
                  caption="Digital maturity position & transformation direction",
                  use_container_width=True)

        st.markdown("**Recommendation**")
        st.markdown(
            "- Prioritize fewer digital initiatives\n"
            "- Create clear stop/go gates with defined owners and metrics\n"
            "- Assign accountable business owners beyond technical delivery\n"
            "- Build cross-functional rollout teams involved from the start, not after "
            "the demo\n"
            "- Speed up decision rights; plan process and training changes during the "
            "pilot, not after it succeeds\n"
            "- **Recommended pathway: customer experience first** — fixing visible pain "
            "points (onboarding, app usability, claim transparency) builds momentum "
            "faster than an efficiency-first push, supported by cross-functional teams "
            "and faster decision rights so operations can catch up"
        )

        st.markdown("**Business value**")
        st.markdown(
            "Shows how a company can move from digital experimentation to digital "
            "execution — the value isn't just having strong digital ideas, but "
            "building the organizational capability to prioritize, fund, govern, and "
            "scale the initiatives that create real business value."
        )

with tab_c:
    eyebrow("Section C")
    st.subheader("AI Adoption & Organizational Readiness")
    st.caption("Framework: AI Governance & Readiness · Work Design Thinking")
    st.markdown(
        "A case looking at how the same insurance company gained short-term "
        "efficiency from AI automation, but risked employee learning, professional "
        "judgment, and innovation capacity in the process — and how to rebalance "
        "automation with augmentation."
    )

    st.image("assets/img/AI_readiness.png", caption="AI Readiness Framework",
              use_container_width=True)

    with st.expander("Read the full case analysis"):
        st.markdown("**Business challenge**")
        st.markdown(
            "- How to use AI to improve efficiency without weakening human judgment, "
            "learning, innovation, and long-term adaptability\n"
            "- Shift needed: from \"automate as much as possible\" to \"automate "
            "routine work while strengthening human judgment in complex work\""
        )

        st.markdown("**Company situation**")
        st.markdown(
            "- AI-driven automation in claims and service operations delivered clear "
            "short-term results: lower cost per claim, faster cycle times, most claims "
            "routed without human review\n"
            "- Employee feedback told a different story: less time for learning, fewer "
            "discussions of unusual cases, a sense that \"the system decides and I just "
            "click\""
        )

        st.markdown("**Diagnosis**")
        st.markdown(
            "- An automation–augmentation imbalance\n"
            "- AI used mainly to standardize and automate, improving cost and speed\n"
            "- But reduced employee involvement, sensemaking, learning, and innovation "
            "capacity\n"
            "- A one-sided automation strategy that becomes harder for employees to "
            "question or improve over time"
        )

        st.markdown("**Recommendation — a three-step path to rebalance automation and augmentation**")
        st.markdown(
            "1. **Differentiation** — split work into two types: small, repetitive "
            "tasks suited to full automation, and complex, judgment-heavy tasks that "
            "need human involvement\n"
            "2. **Integration** — one coherent workflow where AI handles routine "
            "front-end volume while employees take on complex cases, model feedback, "
            "and improvement work\n"
            "3. **Organizational design** — decentralized, cross-functional teams; "
            "flexible workflows; incentives that reward innovation and engagement, not "
            "just throughput; higher-skill roles"
        )
        st.image("assets/img/NSM_AI_AutomationAugmentation.png",
                  caption="AI automation + augmentation strategy — three-step resolution",
                  use_container_width=True)
        st.markdown(
            "Together, these three steps aim for a **virtuous cycle** — keeping the "
            "efficiency gains from automation while restoring the learning, judgment, "
            "and innovation capacity that one-sided automation was eroding."
        )

        st.markdown("**Business value**")
        st.markdown(
            "Shows how a company can gain efficiency from AI without losing the human "
            "capabilities needed for long-term transformation — combining automation "
            "with human judgment, employee learning, and continuous improvement so the "
            "organization stays efficient, adaptive, and responsible over time."
        )