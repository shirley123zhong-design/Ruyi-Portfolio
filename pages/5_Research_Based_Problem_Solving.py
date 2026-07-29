import streamlit as st
import os
import re
import base64
import sys
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_PROJECT_ROOT)
os.chdir(_PROJECT_ROOT)  # ensure relative asset paths work no matter where streamlit was launched from
from theme import apply_theme, hero, eyebrow, case_card_html

st.set_page_config(page_title="Research-Based Problem Solving | Shirley Zhong", page_icon="🔬", layout="wide")
apply_theme()

st.page_link("app.py", label="← Back to home")

# -----------------------------------------------------------------------
# PAGE HEADER
# -----------------------------------------------------------------------

hero(
    icon="🔬",
    title="Research-Based Problem Solving",
    subtitle=(
        "I use research design, survey data, and statistical modelling to help companies solve "
        "problems that are complex, people-related, and don't have one obvious cause. This case "
        "shows how I turn a vague management concern into a testable research design, validate the "
        "data, and hand back a short list of decisions leadership can act on."
    ),
    tags=[
        "Research design", "Survey / people analytics", "Regression",
        "Mediation & moderation testing", "Data validation (CFA / reliability)",
        "Evidence-based HR recommendations",
    ],
    flow="Business concern → Research question → Data validation → Statistical testing → "
         "Qualitative follow-up → Management recommendation",
)

# -----------------------------------------------------------------------
# TAKEAWAY — the executive summary, up front before the case detail
# -----------------------------------------------------------------------
eyebrow("The takeaway")
st.info(
    "**The company shouldn't fix complex problems with generic programs — it should diagnose "
    "the real driver first.** In this case, that meant recognizing stress (not deadlines) as "
    "the actual mechanism, keeping work-hour monitoring on the table, and treating AI adoption "
    "as a role-design question rather than a technology problem."
)

st.markdown("---")

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


def _inline_md(text):
    """Lightweight **bold** / *italic* -> HTML, since this text sits inside a raw HTML block."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*(?!\*)", r"<em>\1</em>", text)
    return text


def float_block(image_filename, caption, paragraphs, width_pct=38, side="right"):
    """
    Newspaper-style block: image (with caption) floats to one side, and the given
    paragraphs of text wrap around it, continuing full-width once the image ends —
    instead of leaving empty space below a shorter image in a fixed side-by-side column.
    """
    path = os.path.join(IMG_DIR, image_filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        img_html = f"""
        <div style="float:{side}; width:{width_pct}%; max-width:420px; margin:0 0 16px 20px;">
            <img src="data:image/png;base64,{b64}" style="width:100%; border-radius:8px;">
            <p style="font-size:0.78rem; color:#888; margin-top:6px; line-height:1.3;">{caption}</p>
        </div>
        """
    else:
        img_html = (
            f'<div style="float:{side}; width:{width_pct}%; max-width:420px; margin:0 0 16px 20px; '
            f'color:#888; font-size:0.8rem;">Screenshot placeholder — add `{path}` to your repo.</div>'
        )

    paragraphs_html = "".join(
        f'<p style="line-height:1.65; margin:0 0 12px 0;">{_inline_md(p)}</p>' for p in paragraphs
    )

    st.markdown(
        f'<div style="overflow:auto;">{img_html}{paragraphs_html}</div>'
        f'<div style="clear:both;"></div>',
        unsafe_allow_html=True,
    )


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

BURNOUT = {
    "title": "Reducing burnout risk in a hybrid, AI-enabled company",
    "question": "What is actually driving employee burnout — deadlines, hours, manager support, "
                "autonomy, or AI tool use — and which levers genuinely reduce it?",
    "tools": ["Survey design", "CFA / reliability", "Regression", "Mediation", "Moderation"],
    "metric": "9,230 employees surveyed · full mediation confirmed (indirect effect \u03b2=.116, p<.001) · "
              "2 of 3 proposed moderators not supported",
    "images": [
        ("p5_Research_Questions.png", "Business concern translated into testable research questions, "
                                        "with a deductive (survey/stats) and inductive (interview) track"),
        ("p5_correlation_matrix.png", "Correlation matrix: burnout is most strongly linked to stress "
                                        "and weekly work hours"),
        ("p5_extended_regression.png", "Extended regression: stress becomes the strongest predictor "
                                         "once added to the model"),
        ("p5_extended_regression_detail.png", "Full predictor tables for both models — the sign flip "
                                                "on deadline pressure once stress is added is the key detail"),
    ],
    "path_image": ("test_pathes.png", "The mechanism being tested: job demands \u2192 stress \u2192 "
                   "burnout, with job resources (manager support & autonomy) as the proposed buffer"),
    "detail": {
        "goal": "A technology company was seeing rising burnout in a hybrid, AI-adopting workforce. "
                "Deadline pressure, long hours, hybrid work, and daily AI tool use were all plausible "
                "suspects — management needed to know which ones were actually driving the problem "
                "before committing budget to a wellbeing program.",
        "process": "Validated the survey measures first (Cronbach's alpha, then CFA), built construct "
                   "scores for burnout, stress, deadline pressure, manager support, and autonomy, then "
                   "tested direct effects, mediation (does stress explain the deadline\u2013burnout link?), "
                   "and moderation (do manager support, autonomy, or AI use change how strongly demands "
                   "translate into burnout?).",
        "tools": "R (lavaan, psych), CFA, Cronbach's alpha/omega reliability, OLS regression, "
                 "mediation and moderation analysis, VIF/residual diagnostics.",
        "challenges": "The obvious hypothesis — that manager support and autonomy would buffer high "
                      "deadline pressure — turned out not to hold statistically. The harder job was "
                      "reporting that honestly instead of forcing a tidier story.",
        "outcomes": "Deadline pressure only predicts burnout through stress — once stress is in the "
                    "model, deadline pressure stops mattering directly (full mediation, indirect effect "
                    "\u03b2=.116, p<.001). Manager support and autonomy reduce burnout directly, but do not "
                    "significantly buffer the deadline\u2013burnout relationship. Daily AI tool users report "
                    "higher burnout overall, but AI use does not amplify or buffer the effect of workload "
                    "— pointing to role design, not the tool itself, as the real issue.",
    },
    "followup": {
        "why": "Statistics show what's related to burnout — not why it happens in daily work, and a "
               "manager can't act on a beta coefficient.",
        "bridge": "This is why the qualitative phase comes *after* the quantitative modelling, not "
                  "before it: the survey already told us where the effects are and how strong they "
                  "are (stress mediates deadline pressure; support and autonomy don't buffer it; AI "
                  "users run hotter). The interviews and focus groups exist to explain *why* those "
                  "specific patterns show up — and the strongest survey paths are what set the focus "
                  "of the interview questions, rather than starting from a blank slate.",
        "questions": [
            "Why does deadline pressure turn into stress for some people and not others?",
            "Why do long hours persist even when support and autonomy are high?",
            "Is AI creating extra learning burden or speed expectations — or are AI-heavy roles "
            "just already more demanding?",
        ],
        "employee_design": {
            "logic": "The survey shows *where* and *how strong* the effects are; interviews explain "
                     "the *why* behind the regression, mediation, and moderation results — and this "
                     "directly addresses the cross-sectional limitation of the survey data.",
            "sampling": "Purposive sampling on the burnout factor scores from the CFA model — not a "
                        "random draw. Two contrasting groups: high-burnout vs. low-burnout employees "
                        "(top/bottom tertile), matched on deadline pressure and work hours so both "
                        "groups face similarly high demand. This isolates why some employees report "
                        "lower burnout despite facing similar demands — especially useful since the "
                        "survey didn't support manager support or autonomy as statistical buffers. "
                        "Scope: 15–20 interviews, stratified across work mode and business area.",
            "why_it_matters": "Turns coefficients into mechanisms executives can act on, and surfaces "
                              "resilience practices the company can scale.",
        },
        "manager_design": {
            "logic": "Manager support is employee-rated in the survey, so we only ever see the demand "
                     "side of it. Managers are a distinct unit of analysis: do they actually have the "
                     "time, tools, and mandate to support staff and reduce demands? Two complementary "
                     "modes: focus groups for shared, team-level norms, and a diary study for daily "
                     "within-person variation.",
            "design": "3–5 focus groups of 5–6 managers each, across divisions and seniority levels, "
                      "discussing workload planning, delegation, meeting culture, and barrier removal — "
                      "plus a 2-week manager diary study logging meeting load, after-hours work, and "
                      "perceived pressure day to day.",
            "why_it_matters": "Targets interventions at the work system, not just individuals — "
                              "workload planning, meeting hygiene, delegation mandates — and manager "
                              "ownership of the resulting solutions raises the odds they actually get "
                              "implemented.",
        },
    },
    "quant_recommendations": [
        "**Track deadline pressure and stress together on one dashboard, not separately** — since "
        "the model shows deadline pressure only matters through stress, a KPI that watches them in "
        "isolation will miss the early-warning signal; watching the combination catches it sooner",
        "**Monitor work hours directly, by team** — deadlines aside, hours are an independent risk "
        "factor and should be tracked on their own",
        "**Re-run the regression quarterly, segmented by team and by AI-tool usage** — turns the "
        "one-off analysis into a standing early-warning system rather than a single snapshot, and "
        "flags exactly which teams' risk profile is shifting",
    ],
    "qual_recommendations": [
        "**Attack stress, not just deadlines** — better prioritization and workload planning, since "
        "stress is the real pathway to burnout",
        "**Keep investing in manager support and autonomy** — they reduce burnout overall, even if "
        "they don't specifically buffer high-pressure moments",
        "**Audit AI-heavy roles**, not AI adoption itself — the issue looks like workload and role "
        "design, not the tool",
        "**Use interview and diary findings to redesign work, not just monitor it** — the "
        "qualitative follow-up should feed directly into how managers prioritize and delegate.",
    ],
    "mod_image": ("p5_mediation__moderation_path.png", "Mediation & moderation results: deadline "
                  "pressure \u2192 stress \u2192 burnout is fully mediated by stress; manager support and "
                  "autonomy do not significantly buffer it"),
    "download": "Employee_Burnout_Research_Study.pdf",
}

VIVA = {
    "intro": "A separate but related decision the company faced: should the annual engagement "
             "survey be replaced by passive behavioral monitoring (Microsoft Viva Insights) instead "
             "of continuing to ask people how they feel?",
    "strengths_weaknesses": {
        "strengths": [
            "Objective, continuous, high-frequency data",
            "No recall bias or social desirability bias",
            "Covers the entire workforce automatically",
            "Reveals hidden behavioral patterns (e.g. large redundant meetings pushing engineers "
            "to work outside normal hours)",
        ],
        "weaknesses": [
            "Misses motivation and psychological safety",
            "Misses stress, burnout, and emotional exhaustion directly",
            "Misses trust in leadership and perceived fairness",
            "Captures behavior, not the *why* behind it",
        ],
    },
    "validity": "Viva measures are behavioral proxies, not the constructs themselves — after-hours "
                "activity is a proxy for burnout, not a measure of it. Meeting density is a proxy for "
                "deadline pressure, not a measure of felt time pressure. Autonomy has no equivalent "
                "trace-data metric at all. The survey stays closer to what we actually mean by each "
                "construct; Viva stays closer to what's easy to log automatically.",
    "validity_image": ("VIVA_validty.png", "Validity comparison: survey measures vs. Viva's "
                        "behavioral proxies, construct by construct"),
    "reliability": "Viva Insights is highly reliable in the measurement sense — automated, "
                   "consistent, no human input error. The survey is less reliable by that narrow "
                   "definition (Cronbach's alpha ranged .732–.804 here, acceptable but not perfect, "
                   "and subject to mood, timing, and survey fatigue) — but reliability isn't the same "
                   "as validity, and a perfectly consistent proxy for the wrong construct isn't more "
                   "useful than a slightly noisier measure of the right one.",
    "reliability_image": ("VIVA_reliability.png", "Reliability comparison: Viva Insights vs. the "
                          "annual survey"),
    "ethics": "Passive collection raises real governance questions the survey doesn't: employees may "
              "not know what's being captured, consent is implicit rather than opt-in, individual-level "
              "behavioral data carries higher re-identification risk, and there's a real risk of scope "
              "creep from 'wellbeing signal' into 'performance surveillance.'",
    "ethics_image": ("VIVA_Ethical.png", "Ethical considerations: provenance, purpose, protection, "
                     "privacy, and preparation, compared across survey vs. Viva"),
    "implementation": "Rolling this out would also mean GDPR compliance work, active management of "
                       "cultural resistance ('are we being watched?'), manager training so behavioral "
                       "data doesn't get used punitively, and accepting the loss of employee voice — "
                       "trace data can't tell you what people want to say, only what they did.",
    "recommendation": "Don't replace the survey — combine both. Use Viva-style behavioral signals as "
                       "a continuous early-warning system, keep the survey (shortened, run more "
                       "frequently) for the psychological experience only a self-report can capture, "
                       "and use targeted qualitative follow-ups to explain why the patterns in both "
                       "are showing up.",
    "rec_image": ("p5_viva_recommendation.png", "Recommendation: do NOT replace surveys with "
                  "behavioral tracking — combine them"),
}


# -----------------------------------------------------------------------
# RENDER HELPERS
# -----------------------------------------------------------------------

def render_case_card(case):
    st.markdown(
        case_card_html(case["title"], case["question"], case["tools"], case["metric"]),
        unsafe_allow_html=True,
    )
    st.caption(
        "Group project (Workshop 3, Group 11) — my contribution: designed and led the quantitative "
        "analysis, including data validation (CFA/reliability), regression modelling, and mediation "
        "& moderation testing."
    )


# -----------------------------------------------------------------------
# TABS — SECTIONS A / B / C / D / E
# -----------------------------------------------------------------------

tab_a, tab_b, tab_c, tab_d, tab_e = st.tabs(
    [
        "A · Business Problem",
        "B · Quantitative Evidence",
        "C · Qualitative Follow-Up",
        "D · VIVA Discussion",
        "E · Recommendations",
    ]
)

with tab_a:
    eyebrow("Section A")
    st.subheader("The Business Problem")
    render_case_card(BURNOUT)
    with st.expander("View full case study", expanded=True):
        d = BURNOUT["detail"]
        fname, caption = BURNOUT["images"][0]
        float_block(fname, caption, [d["goal"]])

with tab_b:
    eyebrow("Section B")
    st.subheader("Quantitative Evidence — What the Data Showed")
    d = BURNOUT["detail"]

    st.markdown(
        "We validated the survey measures first, then tested which factors actually predict "
        "burnout versus which just look related on the surface. **Bottom line: stress — not "
        "deadlines — is the real driver, and manager support/autonomy don't buffer high-pressure "
        "periods the way we expected.**"
    )

    # Lead visual: the core mechanism being tested, shown before the fold
    fname, caption = BURNOUT["path_image"]
    float_block(fname, caption, [
        "Before running any statistics, this is the mechanism we set out to test: do job "
        "demands (deadline pressure, work hours) drive burnout directly, or mainly through "
        "stress — and do job resources (manager support, autonomy) act as a buffer along the way?",
    ])

    with st.expander("View the full quantitative analysis (correlation, regression, mediation & moderation)"):
        st.markdown(f"**Process**  \n{d['process']}")
        st.markdown(f"**Tools**  \n{d['tools']}")

        st.markdown("---")

        fname, caption = BURNOUT["images"][1]  # correlation matrix
        float_block(fname, caption, [
            "**The correlation matrix** was the first check — it showed burnout was most "
            "strongly linked to stress and weekly work hours, with manager support and "
            "autonomy moving in the opposite direction. This is what pointed us toward "
            "testing stress as a mediator rather than treating deadline pressure as the "
            "direct cause.",
        ])

        fname, caption = BURNOUT["images"][2]  # extended regression overview
        fname2, caption2 = BURNOUT["images"][3]  # extended regression full predictor tables
        float_block(fname, caption, [
            "**The extended regression** confirmed it: once stress is added to the model, "
            "it becomes the strongest predictor of burnout, and the model's explanatory "
            "power roughly doubles — evidence this isn't just a deadline problem. The full "
            "predictor tables show deadline pressure's effect flipping from significant to "
            "non-significant once stress enters the model — the clearest single piece of "
            "evidence for the mediation story.",
        ])
        show_image(fname2, caption2)

        fname, caption = BURNOUT["mod_image"]
        float_block(fname, caption, [
            "**Mediation and moderation testing** confirmed the mechanism: deadline "
            "pressure → stress → burnout is a full mediation (indirect effect β=.116, "
            "p<.001), meaning deadline pressure only matters *through* stress. Manager "
            "support and autonomy reduce burnout directly, but neither one significantly "
            "buffers the deadline-pressure pathway — so they help overall, without "
            "specifically protecting people during high-pressure periods.",
        ])

        st.markdown("---")
        st.markdown(f"**Challenges**  \n{d['challenges']}")
        st.markdown(f"**Outcomes**  \n{d['outcomes']}")

with tab_c:
    eyebrow("Section C")
    st.subheader("Qualitative Follow-Up — What We Still Needed to Ask Employees")
    f = BURNOUT["followup"]

    st.markdown(
        "Statistics tell you *what* is related to burnout, not *why* it happens in daily "
        "work — so the qualitative phase comes after the modelling, not before it, and the "
        "strongest survey paths set the focus of the interview questions."
    )

    with st.expander("View the interview and focus group design"):
        st.markdown(f["why"])
        st.markdown(_inline_md(f["bridge"]), unsafe_allow_html=True)

        st.markdown("**Open questions the numbers couldn't answer:**")
        for q in f["questions"]:
            st.markdown(f"- {q}")

        st.markdown("---")

        ed = f["employee_design"]
        float_block(
            "p5_employee_research.png",
            "Employee interview design: purposive sampling on CFA burnout scores, contrasting "
            "high- vs low-burnout groups",
            [
                "#### Employee interviews",
                f"**Design logic**  \n{ed['logic']}",
                f"**Sampling**  \n{ed['sampling']}",
                f"**Why it matters**  \n{ed['why_it_matters']}",
            ],
        )

        st.markdown("---")

        md = f["manager_design"]
        float_block(
            "p5_manager_research.png",
            "Manager focus group and diary study design",
            [
                "#### Manager focus groups",
                f"**Design logic**  \n{md['logic']}",
                f"**Design**  \n{md['design']}",
                f"**Why it matters**  \n{md['why_it_matters']}",
            ],
        )

with tab_d:
    eyebrow("Section D")
    st.subheader("Should Annual Surveys Be Replaced by Microsoft Viva Insights?")
    st.markdown(VIVA["intro"])
    st.markdown(f"**Bottom line:** {VIVA['recommendation']}")

    with st.expander("View the full strengths/weaknesses, validity, reliability & ethics comparison"):
        st.markdown("**Strengths vs. weaknesses**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("*Viva strengths*")
            for s in VIVA["strengths_weaknesses"]["strengths"]:
                st.markdown(f"- {s}")
        with col2:
            st.markdown("*What Viva misses*")
            for w in VIVA["strengths_weaknesses"]["weaknesses"]:
                st.markdown(f"- {w}")

        st.markdown("---")

        fname, caption = VIVA["validity_image"]
        float_block(fname, caption, [f"**Validity**  \n{VIVA['validity']}"])

        fname, caption = VIVA["reliability_image"]
        float_block(fname, caption, [f"**Reliability**  \n{VIVA['reliability']}"], side="left")

        fname, caption = VIVA["ethics_image"]
        float_block(fname, caption, [f"**Ethical considerations**  \n{VIVA['ethics']}"])

        st.markdown(f"**Implementation challenges**  \n{VIVA['implementation']}")

        st.markdown("---")

        fname, caption = VIVA["rec_image"]
        float_block(fname, caption, [f"**Recommendation**  \n{VIVA['recommendation']}"])

with tab_e:
    eyebrow("Section E")
    st.subheader("What the Company Should Do")

    st.markdown(
        "A prioritized, evidence-backed action list — split into what to keep measuring and "
        "what to actually change in how people work."
    )

    with st.expander("View the full recommendations"):
        st.markdown("**Quantitative — what to keep measuring**")
        for i, r in enumerate(BURNOUT["quant_recommendations"], start=1):
            st.markdown(f"{i}. {r}")

        st.markdown("")
        st.markdown("**Qualitative — what to change in how people work**")
        for i, r in enumerate(BURNOUT["qual_recommendations"], start=1):
            st.markdown(f"{i}. {r}")

        st.caption("See the **D · VIVA Discussion** tab for the survey-vs-behavioral-tracking recommendation.")

st.markdown("---")

# -----------------------------------------------------------------------
# DOWNLOADS
# -----------------------------------------------------------------------

eyebrow("Resources")
st.subheader("Downloads")
download_button_for(BURNOUT["download"], "Download full methodology deck (PDF)")