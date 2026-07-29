"""
theme.py
Shared visual design system for Shirley Zhong's Streamlit portfolio.

Styled to match the CV: charcoal / near-black panels, bold geometric
headings, wide-tracked uppercase section labels, and a clean monochrome
(black / charcoal / white / grey) palette with no colour accent — the
same visual language as "RUYI ZHONG (SHIRLEY)".

Import once at the top of every page:

    from theme import apply_theme, hero, badge_row

    apply_theme()
    hero(
        icon="📊",
        title="Business Decision Analytics",
        subtitle="I use data to support practical business decisions across forecasting, "
                  "cost evaluation, customer insight, and operational performance.",
        tags=["Forecasting & Planning", "Cost & Policy Decisions", "Customer Segmentation"],
        flow="Business question → Data preparation → Analysis method → Decision insight → Recommendation",
    )

Everything below only adds CSS classes / small HTML wrappers — it does not
touch any of the actual case content, data, or business logic on the pages.
Function names/signatures are unchanged from the previous theme, so no
other page needs to be edited for this restyle to take effect.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# PALETTE — monochrome, matching the CV (black / charcoal / white / grey).
# No colour accent; contrast and typography carry the design instead.
# ---------------------------------------------------------------------------
INK = "#141414"          # near-black, primary text / headings
CHARCOAL = "#242424"      # dark panel background (hero, CV sidebar tone)
CHARCOAL_2 = "#1A1A1A"    # darker end of the panel gradient
CARD = "#FFFFFF"
PAGE_TINT = "#F4F3F1"     # soft warm-grey page background, like the CV's name plate
BORDER = "#E3E2DF"
BADGE_BG = "#F0EFEC"
MUTED = "#6b6b6b"
FAINT = "#8a8a8a"


def apply_theme():
    """Inject global CSS. Call once near the top of every page, right after st.set_page_config."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"]  {{
            font-family: 'Inter', sans-serif;
        }}

        h1, h2, h3 {{
            font-family: 'Archivo', sans-serif;
            font-weight: 700;
            color: {INK} !important;
            letter-spacing: -0.01em;
        }}

        /* ------------------------------------------------------------------
           FORCE READABLE TEXT — this site sets a fixed light page background,
           so text color must be forced too, regardless of whether the visitor
           has Streamlit's light or dark theme active. Without this, body text
           inherits white (dark-theme default) and disappears on our light bg.
           ------------------------------------------------------------------ */
        .stApp, .stApp p, .stApp span, .stApp li, .stApp label,
        .stApp div, .stMarkdown, .stCaption,
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p,
        [data-testid="stMetricLabel"],
        [data-testid="stWidgetLabel"] p {{
            color: {INK} !important;
        }}

        [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {{
            color: {MUTED} !important;
        }}

        .stApp a, [data-testid="stMarkdownContainer"] a {{
            color: #1a56db !important;
        }}

        /* keep the dark hero banner's own text white, overriding the rule above */
        .hero-banner, .hero-banner p, .hero-banner span, .hero-banner div {{
            color: #FFFFFF !important;
        }}
        .hero-subtitle {{
            color: rgba(255,255,255,0.82) !important;
        }}

        /* any dark badge/tile (e.g. the grade tile, nav card numbers) needs forced white text —
           uses .stApp prefix twice to out-specificity the blanket text-color rule above */
        .stApp .grade-tile, .stApp .grade-tile *,
        .stApp .dark-badge, .stApp .dark-badge * {{
            color: #FFFFFF !important;
        }}

        /* ------------------------------------------------------------------
           RESPONSIVE — keep the hero banner, cards, and grade tiles usable
           on narrow (mobile) viewports instead of overflowing or squeezing.
           ------------------------------------------------------------------ */
        @media (max-width: 640px) {{
            .hero-banner {{
                padding: 22px 20px 20px 20px;
            }}
            .hero-title {{
                font-size: 1.5rem;
            }}
            .hero-subtitle {{
                font-size: 0.92rem;
            }}
            .case-card {{
                padding: 14px 16px;
            }}
            .hero-flow-step {{
                font-size: 0.68rem;
                padding: 6px 10px;
            }}
        }}

        /* subtle page background */
        .stApp {{
            background: linear-gradient(180deg, {PAGE_TINT} 0%, #FFFFFF 320px);
        }}

        /* ---- hero banner ---- */
        .hero-banner {{
            background: linear-gradient(155deg, {CHARCOAL} 0%, {CHARCOAL_2} 100%);
            border-radius: 4px;
            padding: 34px 38px 28px 38px;
            margin: 4px 0 22px 0;
            box-shadow: 0 8px 24px rgba(0,0,0,0.16);
            position: relative;
            overflow: hidden;
        }}
        .hero-banner::before {{
            content: "";
            position: absolute;
            left: 0; top: 0; bottom: 0;
            width: 6px;
            background: #FFFFFF;
            opacity: 0.9;
        }}
        .hero-icon {{
            font-size: 2.1rem;
            margin-bottom: 6px;
            display: block;
        }}
        .hero-title {{
            font-family: 'Archivo', sans-serif;
            color: #FFFFFF;
            font-size: 2.0rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.02em;
            margin: 0 0 4px 0;
            line-height: 1.18;
        }}
        .hero-rule {{
            width: 46px; height: 3px;
            background: #FFFFFF;
            border-radius: 0;
            margin: 12px 0 14px 0;
        }}
        .hero-subtitle {{
            color: rgba(255,255,255,0.82);
            font-size: 1.0rem;
            max-width: 760px;
            line-height: 1.6;
            margin: 0;
        }}
        .hero-flow-row {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 6px;
            margin-top: 18px;
        }}
        .hero-flow-step {{
            display: inline-block;
            padding: 7px 13px;
            background: rgba(255,255,255,0.09);
            border: 1px solid rgba(255,255,255,0.32);
            border-radius: 2px;
            font-size: 0.74rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            white-space: nowrap;
        }}
        .hero-flow-arrow {{
            color: rgba(255,255,255,0.45);
            font-size: 0.85rem;
            padding: 0 1px;
        }}

        /* badge pills (capability tags) — outlined, monochrome */
        .tag-row {{ margin: 14px 0 4px 0; }}
        .tag-pill {{
            background: {BADGE_BG};
            color: {INK};
            padding: 5px 14px;
            border-radius: 2px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin-right: 6px;
            margin-bottom: 8px;
            display: inline-block;
            border: 1px solid {BORDER};
            transition: all 0.15s ease;
        }}
        .tag-pill:hover {{
            border-color: {INK};
        }}
        .tag-pill-dark {{
            background: {CHARCOAL};
            color: #FFF;
            border-color: {CHARCOAL};
        }}

        /* case-study cards */
        .case-card {{
            border: 1px solid {BORDER};
            border-left: 4px solid {INK};
            border-radius: 4px;
            padding: 18px 22px;
            margin-bottom: 16px;
            background: {CARD};
            transition: box-shadow 0.18s ease, transform 0.18s ease;
        }}
        .case-card:hover {{
            box-shadow: 0 10px 26px rgba(20,20,20,0.10);
            transform: translateY(-2px);
        }}
        .case-title {{
            font-family: 'Archivo', sans-serif;
            font-weight: 700;
            font-size: 1.05rem;
            margin: 0 0 6px 0;
            color: {INK};
        }}
        .case-card .case-question {{
            color: #555 !important;
            font-size: 0.93rem;
            margin: 0 0 10px 0;
            font-style: italic;
        }}
        .case-metric {{
            font-weight: 600;
            font-size: 0.9rem;
            margin: 4px 0 0 0;
            color: {INK};
        }}
        .case-metric::before {{
            content: "▪ ";
            color: {INK};
        }}

        /* section eyebrow label — wide-tracked caps, like the CV's "C O N T A C T :" */
        .eyebrow {{
            color: {INK};
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            margin-bottom: 6px;
            padding-bottom: 6px;
            border-bottom: 1px solid {BORDER};
            display: inline-block;
        }}

        /* tabs — a cleaner underline-nav feel */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 6px;
            border-bottom: 1px solid {BORDER};
        }}
        .stTabs [data-baseweb="tab"] {{
            font-weight: 600;
            font-size: 1.0rem;
            color: {INK};
            opacity: 0.55;
            padding: 9px 16px;
            border-radius: 4px 4px 0 0;
            letter-spacing: 0.01em;
            transition: background-color 0.15s ease, opacity 0.15s ease;
        }}
        .stTabs [aria-selected="true"] {{
            opacity: 1 !important;
            font-weight: 700;
            background-color: {INK} !important;
        }}
        .stTabs [aria-selected="true"] p,
        .stTabs [aria-selected="true"] div {{
            color: #FFFFFF !important;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            opacity: 0.85;
            background-color: {BADGE_BG};
        }}
        .stTabs [aria-selected="true"]:hover {{
            opacity: 1;
            background-color: {INK} !important;
        }}
        /* Streamlit's own sliding tab-indicator bar defaults to red; hide it — the filled
           background above already makes the active tab unambiguous */
        .stTabs [data-baseweb="tab-highlight"] {{
            background-color: transparent !important;
        }}
        .stTabs [data-baseweb="tab-border"] {{
            background-color: {BORDER} !important;
        }}

        /* expanders */
        .streamlit-expanderHeader, [data-testid="stExpander"] summary {{
            font-weight: 600;
            color: {INK};
        }}
        [data-testid="stExpander"] {{
            border: 1px solid {BORDER} !important;
            border-radius: 4px !important;
            background: #FDFDFC;
        }}

        /* metrics */
        [data-testid="stMetric"] {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 4px;
            padding: 14px 16px 10px 16px;
        }}
        [data-testid="stMetricLabel"] {{ color: {MUTED}; }}
        [data-testid="stMetricValue"] {{ color: {INK}; font-family: 'Archivo', sans-serif; }}

        /* buttons — force explicit background so text is never dark-on-dark */
        .stDownloadButton button, .stButton button {{
            background-color: #FFFFFF !important;
            border-radius: 2px;
            border: 1px solid {INK} !important;
            color: {INK} !important;
            font-weight: 600;
            letter-spacing: 0.02em;
        }}
        .stDownloadButton button:hover, .stButton button:hover {{
            background-color: {INK} !important;
            color: #FFF !important;
            border-color: {INK} !important;
        }}
        .stDownloadButton button p, .stButton button p {{
            color: inherit !important;
        }}

        /* quiet horizontal rule */
        hr {{
            border: none;
            border-top: 1px solid {BORDER};
            margin: 10px 0;
        }}

        /* pull-quote / info callouts */
        [data-testid="stAlert"] {{
            border-radius: 4px;
            border-left: 4px solid {INK};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(icon: str, title: str, subtitle: str, tags=None, flow: str = ""):
    """Render the consistent page-header banner used at the top of every page."""
    tags_html = ""
    if tags:
        tags_html = '<div class="tag-row">' + "".join(
            f'<span class="tag-pill">{t}</span>' for t in tags
        ) + "</div>"

    flow_html = ""
    if flow:
        steps = [s.strip() for s in flow.split("→") if s.strip()]
        chips = []
        for i, step in enumerate(steps):
            if i > 0:
                chips.append('<span class="hero-flow-arrow">→</span>')
            chips.append(f'<span class="hero-flow-step">{step}</span>')
        flow_html = f'<div class="hero-flow-row">{"".join(chips)}</div>'

    st.markdown(
        f"""
        <div class="hero-banner">
            <span class="hero-icon">{icon}</span>
            <p class="hero-title">{title}</p>
            <div class="hero-rule"></div>
            <p class="hero-subtitle">{subtitle}</p>
            {flow_html}
        </div>
        {tags_html}
        """,
        unsafe_allow_html=True,
    )


def badge_row(items, dark=False):
    """Standalone capability badge row (used outside the hero, e.g. mid-page)."""
    cls = "tag-pill tag-pill-dark" if dark else "tag-pill"
    html = "".join(f'<span class="{cls}">{t}</span>' for t in items)
    st.markdown(f'<div class="tag-row">{html}</div>', unsafe_allow_html=True)


def eyebrow(text: str):
    st.markdown(f'<div class="eyebrow">{text}</div>', unsafe_allow_html=True)


def case_card_html(title: str, question: str, tools, metric: str) -> str:
    """Return the HTML for a case-study summary card (title/question/tags/metric)."""
    tools_html = " ".join(f'<span class="tag-pill">{t}</span>' for t in tools)
    return f"""
    <div class="case-card">
        <p class="case-title">{title}</p>
        <p class="case-question">{question}</p>
        <div style="margin-bottom:10px;">{tools_html}</div>
        <p class="case-metric">{metric}</p>
    </div>
    """


def nav_card_html(number: str, icon: str, title: str, description: str) -> str:
    """Return the HTML for a numbered homepage navigation card (icon + title + blurb)."""
    return f"""
    <div class="case-card" style="min-height:168px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <span class="dark-badge" style="font-family:'Archivo',sans-serif; font-weight:800; font-size:0.78rem;
                         background:#141414; border-radius:2px; padding:2px 8px;
                         white-space:nowrap;">{number}</span>
            <span style="font-size:1.3rem;">{icon}</span>
        </div>
        <p class="case-title" style="margin-bottom:6px;">{title}</p>
        <p style="color:#555; font-size:0.9rem; line-height:1.5; margin:0;">{description}</p>
    </div>
    """
