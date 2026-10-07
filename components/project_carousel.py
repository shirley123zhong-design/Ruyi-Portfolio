"""
components/project_carousel.py

"Explore my work" as a mouse-follow carousel with scroll-driven zoom.

- On desktop the row follows the mouse: move left to see the first cards,
  right to see the last. On touch, swipe. Arrow buttons and keyboard
  arrows work everywhere.
- The card nearest the centre zooms to full size; the others shrink and
  fade with their distance from the centre (that's the scroll-driven zoom).
- Desktop: click any card to open its page. Touch: tap a side card to
  centre it, tap the centred card to open it.

Usage (app.py):
    from components.project_carousel import render_project_carousel
    render_project_carousel(CARDS)
"""

from __future__ import annotations

import html as _html
import json

import streamlit as st

try:
    from theme import INK, CHARCOAL, PAGE_TINT, BORDER, BADGE_BG, MUTED, FAINT
except ImportError:
    INK, CHARCOAL, PAGE_TINT = "#141414", "#242424", "#F4F3F1"
    BORDER, BADGE_BG, MUTED, FAINT = "#E3E2DF", "#F0EFEC", "#6b6b6b", "#8a8a8a"

HEIGHT = 430


def _embed(markup: str, height: int):
    """st.iframe on newer Streamlit, components.html on older versions."""
    if hasattr(st, "iframe"):
        st.iframe(markup, height=height)
    else:
        import streamlit.components.v1 as stc
        stc.html(markup, height=height)


def _slug(page_path: str) -> str:
    """'pages/1_Business_Decision_Analytics.py' -> 'Business_Decision_Analytics'
    (the URL Streamlit gives a page in the pages/ folder)."""
    name = page_path.rsplit("/", 1)[-1].removesuffix(".py")
    head, _, tail = name.partition("_")
    return tail if head.isdigit() and tail else name


def _card(c: dict, i: int) -> str:
    e = _html.escape
    return f"""
<article class="card" data-i="{i}" data-href="{e(_slug(c['page']))}" tabindex="-1">
  <div class="top"><span class="num">{e(c['number'])}</span><span class="icon">{c['icon']}</span></div>
  <h3>{e(c['title'])}</h3>
  <p>{e(c['description'])}</p>
  <span class="go">Explore &rarr;</span>
</article>"""


def render_project_carousel(cards: list[dict], height: int = HEIGHT):
    cards_html = "".join(_card(c, i) for i, c in enumerate(cards))
    n = len(cards)

    markup = f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;}}
html,body{{margin:0;padding:0;background:transparent;font-family:'Inter',sans-serif;color:{INK};}}
.wrap{{position:relative;}}
.track{{
  display:flex;gap:22px;overflow-x:auto;overflow-y:hidden;
  padding:14px calc(50% - 180px) 20px;
  scroll-snap-type:x mandatory;scrollbar-width:none;
  user-select:none;-webkit-user-select:none;
  touch-action:pan-x pan-y;
}}
.track::-webkit-scrollbar{{display:none;}}
.card{{
  flex:0 0 360px;min-height:244px;scroll-snap-align:center;
  background:#fff;border:1px solid {BORDER};border-left:4px solid {INK};border-radius:4px;
  padding:20px 22px;display:flex;flex-direction:column;gap:8px;
  transform-origin:center center;transition:box-shadow .2s ease;
  will-change:transform,opacity;outline:none;
}}
.card.active{{box-shadow:0 14px 32px rgba(20,20,20,.14);cursor:pointer;}}
.card.active:hover .go{{text-decoration:underline;}}
.top{{display:flex;align-items:center;gap:10px;}}
.num{{font-family:'Archivo',sans-serif;font-weight:800;font-size:.74rem;letter-spacing:.04em;
  background:{INK};color:#fff;border-radius:2px;padding:2px 8px;white-space:nowrap;}}
.icon{{font-size:1.3rem;}}
h3{{font-family:'Archivo',sans-serif;font-weight:700;font-size:1.2rem;margin:4px 0 0;line-height:1.25;}}
p{{color:#3d3d3d;font-size:1rem;line-height:1.55;margin:0;flex:1;}}
.go{{font-weight:600;font-size:.95rem;color:{INK};margin-top:6px;}}
.track.follow{{scroll-snap-type:none;cursor:default;}}
.track.follow .card{{cursor:pointer;}}
.bar{{display:flex;align-items:center;justify-content:center;gap:22px;padding:4px 0 0;}}
.btn{{width:58px;height:58px;border:1.5px solid {INK};background:#fff;color:{INK};border-radius:2px;
  font-size:1.6rem;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .15s;}}
.btn:hover{{background:{INK};color:#fff;}}
.btn:disabled{{opacity:.25;cursor:default;background:#fff;color:{INK};}}
.count{{font-family:'Archivo',sans-serif;font-weight:800;font-size:1rem;letter-spacing:.1em;min-width:78px;text-align:center;}}
.progress{{width:min(320px,60%);height:2px;background:{BORDER};position:relative;margin:14px auto 0;}}
.progress span{{position:absolute;left:0;top:0;bottom:0;background:{INK};transition:width .2s ease;}}
.hint{{display:block;text-align:center;margin-top:10px;font-size:.74rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:{FAINT};}}
@media (max-width:520px){{
  .card{{flex-basis:82vw;padding:18px 18px;}}
  .track{{padding-left:9vw;padding-right:9vw;padding-top:10px;}}
  p{{font-size:.98rem;}}
  .btn{{width:48px;height:48px;font-size:1.35rem;}}
}}
@media (prefers-reduced-motion:reduce){{.card{{transition:none;}}}}
</style></head><body>
<div class="wrap">
  <div class="track" id="track" tabindex="0" aria-label="Portfolio sections">{cards_html}</div>
  <div class="bar">
    <button class="btn" id="prev" aria-label="Previous">&larr;</button>
    <span class="count" id="count">01 / {n:02d}</span>
    <button class="btn" id="next" aria-label="Next">&rarr;</button>
  </div>
  <div class="progress"><span id="prog"></span></div>
  <span class="hint" id="hint">Move your mouse across to browse</span>
</div>
<script>
(function(){{
  const track=document.getElementById('track');
  const cards=[...track.querySelectorAll('.card')];
  const n=cards.length, prev=document.getElementById('prev'), next=document.getElementById('next');
  const count=document.getElementById('count'), prog=document.getElementById('prog');
  const hint=document.getElementById('hint');
  let active=0, raf=null;

  // ---- scroll-driven zoom: scale + fade by distance from the centre ----
  function update(){{
    raf=null;
    const mid=track.scrollLeft+track.clientWidth/2;
    let best=0, bestD=Infinity;
    cards.forEach((c,i)=>{{
      const centre=c.offsetLeft+c.offsetWidth/2;
      const d=Math.abs(centre-mid);
      const t=Math.min(d/(c.offsetWidth+22),1.4);
      c.style.transform='scale('+(1-0.13*Math.min(t,1)).toFixed(3)+')';
      c.style.opacity=(1-0.5*Math.min(t,1)).toFixed(3);
      if(d<bestD){{bestD=d;best=i;}}
    }});
    if(best!==active||!cards[active].classList.contains('active')){{
      cards.forEach(c=>c.classList.remove('active'));
      cards[best].classList.add('active'); active=best;
    }}
    count.textContent=String(active+1).padStart(2,'0')+' / '+String(n).padStart(2,'0');
    prog.style.width=((active+1)/n*100)+'%';
    prev.disabled=active===0; next.disabled=active===n-1;
  }}
  const queue=()=>{{ if(!raf) raf=requestAnimationFrame(update); }};
  track.addEventListener('scroll',queue,{{passive:true}});
  window.addEventListener('resize',queue);

  const hover=matchMedia('(hover: hover) and (pointer: fine)').matches;
  if(hover) track.classList.add('follow');
  const maxScroll=()=>track.scrollWidth-track.clientWidth;
  const centreOf=i=>cards[i].offsetLeft+cards[i].offsetWidth/2-track.clientWidth/2;

  // eased scrolling toward a target position (mouse devices)
  let target=track.scrollLeft, anim=null;
  function animate(){{
    const diff=target-track.scrollLeft;
    if(Math.abs(diff)<0.5){{ track.scrollLeft=target; anim=null; return; }}
    track.scrollLeft+=diff*0.09;
    anim=requestAnimationFrame(animate);
  }}
  function scrollToX(x){{
    target=Math.max(0,Math.min(maxScroll(),x));
    if(hover){{ if(!anim) anim=requestAnimationFrame(animate); }}
    else track.scrollTo({{left:target,behavior:'smooth'}});
  }}
  function goTo(i){{ i=Math.max(0,Math.min(n-1,i)); scrollToX(centreOf(i)); }}

  prev.onclick=()=>goTo(active-1);
  next.onclick=()=>goTo(active+1);
  track.addEventListener('keydown',e=>{{
    if(e.key==='ArrowRight'){{e.preventDefault();goTo(active+1);}}
    if(e.key==='ArrowLeft'){{e.preventDefault();goTo(active-1);}}
    if(e.key==='Enter') open(cards[active]);
  }});

  // ---- mouse position drives the scroll: left edge = first card, right edge = last ----
  if(hover){{
    track.addEventListener('mousemove',e=>{{
      const r=track.getBoundingClientRect();
      const edge=r.width*0.15;
      const f=Math.max(0,Math.min(1,(e.clientX-r.left-edge)/(r.width-2*edge)));
      scrollToX(f*maxScroll());
    }});
    track.addEventListener('mouseleave',()=>goTo(active));   // settle on the nearest card
  }} else {{
    hint.textContent='Swipe to browse';
  }}

  // ---- click opens a card; on touch, a side card is centred first ----
  // Streamlit's frame may not change the page address itself, so we click
  // the matching (hidden) st.page_link in the parent page instead.
  function open(c){{
    const slug=c.dataset.href;
    try{{
      const links=[...window.parent.document.querySelectorAll('a[href]')];
      const a=links.find(x=>{{
        try{{ return new URL(x.href).pathname.replace(/\\/$/,'').endsWith('/'+slug); }}catch(e){{ return false; }}
      }});
      if(a){{ a.click(); return; }}
    }}catch(err){{}}
    window.open(slug,'_blank');   // last resort: open in a new tab
  }}
  cards.forEach((c,i)=>c.addEventListener('click',()=>{{
    if(hover||i===active) open(c); else goTo(i);
  }}));

  update();
}})();
</script>
</body></html>"""

    _embed(markup, height)

    # Hidden page links the carousel clicks to navigate (see open() above).
    st.markdown("<style>.st-key-pc_nav_links{display:none !important;}</style>", unsafe_allow_html=True)
    with st.container(key="pc_nav_links"):
        for c in cards:
            st.page_link(c["page"], label=c["title"])
