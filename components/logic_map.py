"""
components/logic_map.py

Home page section: "How I approach a business question".
Horizontal logic map (governance -> enablement -> organisational design ->
practice -> business development) plus where each project sits on it.

Usage (app.py):
    from components.logic_map import render_logic_map
    render_logic_map()
"""

import streamlit as st
from theme import INK, CHARCOAL, BADGE_BG, BORDER, MUTED, FAINT, eyebrow

# ---------- content (edit wording here) ----------

INTRO = (
    "To me, data-driven business development <span class='hl'>doesn't start with the dashboard</span>. "
    "It starts with <span class='hl'>who owns the data and who gets to use it</span>, and it only pays off "
    "when strategy, structure, processes, rewards, people and culture adapt, so a "
    "<span class='hl'>better analysis actually changes a decision</span>."
)

LAYERS = [
    {"name": "Data governance", "question": "Who owns, defines and can access the data?"},
    {"name": "Data enablement", "question": "What can each team actually use to decide?"},
    {
        "name": "Organisational design",
        "question": "What has to change around the data?",
        "levers": ["Strategy", "Structure", "Process", "Rewards", "People", "Culture"],
    },
    {
        "name": "Practice",
        "question": "Where does it show up day to day?",
        "levers": ["Dashboards", "Processes", "Automation", "Decisions"],
    },
    {"name": "Business development", "question": "Value the business can measure", "outcome": True},
]

PROJECTS = [
    {
        "layer": "Governance",
        "focus": "Control, data quality and shared definitions",
        "cases": ["P-Card SQL audit", "ETL cases"],
    },
    {
        "layer": "Enablement",
        "focus": "Turning raw data into something teams can use",
        "cases": ["CoffeeGo Power Query", "SQL-to-BI pipeline", "IntegrateCo payroll"],
    },
    {
        "layer": "Organisational design",
        "focus": "Strategy, structure, people and culture",
        "cases": ["NCG", "NSM", "AI readiness", "Burnout research"],
    },
    {
        "layer": "Practice",
        "focus": "Analysis that feeds a real decision",
        "cases": [
            "Bankdata forecasting", "Restaurant regression", "Fairview dashboard",
            "EY DuPont", "Supply Chain dashboard", "FlexMatch",
        ],
    },
]

# ---------- styling ----------
# Every colour rule is prefixed ".stApp .lm-wrap" + !important so it beats the
# blanket "force INK text" rule in theme.py. No blank lines inside <style>,
# otherwise Streamlit's markdown parser breaks the block.

_CSS = f"""<style>
.stApp .lm-wrap{{margin:6px 0 10px 0;}}
.stApp .lm-wrap .lm-intro{{font-size:1.08rem;line-height:1.7;color:#333 !important;max-width:920px;margin:0;}}
.stApp .lm-wrap .hl{{font-weight:600;color:{INK} !important;background:linear-gradient(transparent 60%,#E4E1DA 60%);padding:0 2px;}}
.stApp .lm-wrap .lm-flow{{display:flex;align-items:stretch;margin:18px 0 8px 0;}}
.stApp .lm-wrap .lm-node{{flex:1 1 0;min-width:0;background:{BADGE_BG};border:1px solid {BORDER};border-radius:4px;padding:16px 16px 18px 16px;display:flex;flex-direction:column;gap:8px;}}
.stApp .lm-wrap .lm-out{{background:{CHARCOAL};border-color:{CHARCOAL};}}
.stApp .lm-wrap .lm-step{{font-family:'Archivo',sans-serif;font-size:0.76rem;font-weight:800;letter-spacing:0.18em;text-transform:uppercase;color:{FAINT} !important;}}
.stApp .lm-wrap .lm-name{{font-family:'Archivo',sans-serif;font-weight:700;font-size:1.12rem;line-height:1.25;color:{INK} !important;}}
.stApp .lm-wrap .lm-q{{font-size:0.98rem;line-height:1.5;color:#3d3d3d !important;}}
.stApp .lm-wrap .lm-out .lm-step{{color:rgba(255,255,255,0.55) !important;}}
.stApp .lm-wrap .lm-out .lm-name{{color:#FFFFFF !important;}}
.stApp .lm-wrap .lm-out .lm-q{{color:rgba(255,255,255,0.82) !important;}}
.stApp .lm-wrap .lm-levers{{display:flex;flex-wrap:wrap;gap:4px;margin-top:4px;}}
.stApp .lm-wrap .lm-lever{{font-size:0.8rem;font-weight:600;background:#FFFFFF;border:1px solid {BORDER};border-radius:2px;padding:2px 7px;color:{INK} !important;}}
.stApp .lm-wrap .lm-arrow{{flex:0 0 26px;display:flex;align-items:center;justify-content:center;font-size:1.05rem;color:{FAINT} !important;}}
.stApp .lm-wrap .lm-loop{{font-size:0.95rem;color:{MUTED} !important;margin:6px 0 18px 0;padding-bottom:16px;border-bottom:1px solid {BORDER};}}
.stApp .lm-wrap .lm-sub{{font-family:'Archivo',sans-serif;font-weight:700;font-size:1.2rem;color:{INK} !important;margin:0 0 12px 0;}}
.stApp .lm-wrap .lm-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;}}
.stApp .lm-wrap .lm-col{{border-top:3px solid {INK};padding-top:12px;}}
.stApp .lm-wrap .lm-col-name{{font-family:'Archivo',sans-serif;font-weight:700;font-size:1.08rem;color:{INK} !important;}}
.stApp .lm-wrap .lm-col-focus{{font-size:0.97rem;line-height:1.45;color:#4a4a4a !important;margin:4px 0 10px 0;}}
.stApp .lm-wrap .lm-chips .tag-pill{{font-size:0.84rem;padding:4px 10px;}}
.stApp .lm-wrap .lm-node{{position:relative;transition:transform .25s ease,box-shadow .25s ease,background-color .25s ease,border-color .25s ease,opacity .25s ease;}}
@media (hover:hover){{
.stApp .lm-wrap .lm-node:hover{{transform:scale(1.05);z-index:2;background:#FFFFFF;border-color:{INK};box-shadow:0 14px 32px rgba(20,20,20,0.16);}}
.stApp .lm-wrap .lm-out:hover{{background:{INK};border-color:{INK};box-shadow:0 14px 32px rgba(20,20,20,0.30);}}
.stApp .lm-wrap .lm-flow:hover .lm-node:not(:hover){{opacity:0.55;}}
.stApp .lm-wrap .lm-node:hover .lm-step{{color:{INK} !important;}}
.stApp .lm-wrap .lm-out:hover .lm-step{{color:rgba(255,255,255,0.75) !important;}}
.stApp .lm-wrap .lm-node:hover .lm-lever{{border-color:{INK};}}
}}
@media (prefers-reduced-motion:reduce){{.stApp .lm-wrap .lm-node{{transition:none;}}.stApp .lm-wrap .lm-node:hover{{transform:none;}}}}
@media (max-width:900px){{
.stApp .lm-wrap .lm-flow{{flex-direction:column;}}
.stApp .lm-wrap .lm-node{{padding:14px 16px;}}
.stApp .lm-wrap .lm-grid{{gap:20px;}}
.stApp .lm-wrap .lm-arrow{{flex:0 0 24px;transform:rotate(90deg);}}
}}
</style>"""


def _flow_html() -> str:
    parts = []
    for i, layer in enumerate(LAYERS):
        out = layer.get("outcome", False)
        cls = "lm-node lm-out" if out else "lm-node"
        step = "Outcome" if out else f"0{i + 1}"
        levers = ""
        if layer.get("levers"):
            levers = '<div class="lm-levers">' + "".join(
                f'<span class="lm-lever">{l}</span>' for l in layer["levers"]
            ) + "</div>"
        parts.append(
            f'<div class="{cls}"><div class="lm-step">{step}</div>'
            f'<div class="lm-name">{layer["name"]}</div>'
            f'<div class="lm-q">{layer["question"]}</div>{levers}</div>'
        )
        if i < len(LAYERS) - 1:
            parts.append('<div class="lm-arrow">&rarr;</div>')
    return '<div class="lm-flow">' + "".join(parts) + "</div>"


def _projects_html() -> str:
    cols = []
    for p in PROJECTS:
        chips = "".join(f'<span class="tag-pill">{c}</span>' for c in p["cases"])
        cols.append(
            f'<div class="lm-col"><div class="lm-col-name">{p["layer"]}</div>'
            f'<div class="lm-col-focus">{p["focus"]}</div>'
            f'<div class="lm-chips">{chips}</div></div>'
        )
    return '<div class="lm-grid">' + "".join(cols) + "</div>"


def render_logic_map():
    eyebrow("Approach")
    st.subheader("How I approach a business question")
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown(
        '<div class="lm-wrap">'
        f'<p class="lm-intro">{INTRO}</p>'
        f"{_flow_html()}"
        '<div class="lm-loop">&#8635; Every decision creates new data, and the cycle starts again.</div>'
        '<div class="lm-sub">Where my projects sit on this line</div>'
        f"{_projects_html()}"
        "</div>",
        unsafe_allow_html=True,
    )
