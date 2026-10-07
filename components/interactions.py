"""
components/interactions.py

Custom cursor/scroll/drag-driven visual effects for the portfolio.
Each function returns a self-contained HTML/CSS/JS string meant to be
rendered with streamlit.components.v1.html().

Usage (in a page file):

    import streamlit.components.v1 as stc
    from components.interactions import curtain_wave_intro

    stc.html(
        curtain_wave_intro(
            label="PORTFOLIO",
            name_lines=["Ruyi", "Zhong(Shirley)"],
            subtitle="MSc Data-Driven Business Development | SDU",
            photo_paths=["assets/img/profile_1.jpeg", "assets/img/profile_2.jpeg"],
            height=440,
        ),
        height=440,
    )
"""

from __future__ import annotations

import base64
import os

# Palette pulled from theme.py so the hero matches the rest of the site.
try:
    from theme import INK, CHARCOAL, PAGE_TINT, BORDER, MUTED, FAINT
except ImportError:  # fallback if imported outside the app
    INK, CHARCOAL, PAGE_TINT = "#141414", "#242424", "#F4F3F1"
    BORDER, MUTED, FAINT = "#E3E2DF", "#6b6b6b", "#8a8a8a"


def _image_to_data_uri(path: str) -> str | None:
    """Read a local image file and return a base64 data URI.

    components.html() runs in a sandboxed iframe and cannot resolve local
    file paths, so photos are embedded as base64. Returns None if the file
    can't be read, so callers fall back to a placeholder instead of crashing.
    """
    if not path or not os.path.isfile(path):
        return None

    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
    }.get(ext, "image/jpeg")

    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime};base64,{encoded}"


def curtain_wave_intro(
    label: str,
    name_lines: list[str],
    subtitle: str,
    photo_paths: list[str] | None = None,
    height: int = 440,
    strip_count: int = 28,
    curtain_color: str = CHARCOAL,
    bg_color: str = PAGE_TINT,
    text_color: str = INK,
) -> str:
    """Cursor-driven curtain wave reveal for the hero/intro section.

    A vertical-strip "curtain" sits over the hero content. As the cursor
    moves across, nearby strips lift with a falloff to neighbouring strips,
    creating a wave that follows the cursor. On touch devices a tap
    triggers one sweep that leaves the curtain open.

    Keep `height` in sync with components.html(height=...) at the call site.
    """

    photo_paths = photo_paths or []
    photo_uris = [_image_to_data_uri(p) for p in photo_paths]

    def _photo_html(uri, placeholder_text):
        if uri:
            return f'<div class="photo"><img src="{uri}" /></div>'
        return f'<div class="photo placeholder"><span>{placeholder_text}</span></div>'

    photo1 = _photo_html(photo_uris[0] if len(photo_uris) > 0 else None, "Photo 1")
    photo2 = _photo_html(photo_uris[1] if len(photo_uris) > 1 else None, "Photo 2")

    name_html = "".join(f"<div>{line}</div>" for line in name_lines)
    strips_html = "".join(f'<div class="strip" data-i="{i}"></div>' for i in range(strip_count))

    return f"""
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<div id="hero-root">
  <style>
    html, body {{ margin: 0; padding: 0; background: transparent; }}

    #hero-root {{
      position: relative;
      width: 100%;
      height: {height}px;
      overflow: hidden;
      background: {bg_color};
      font-family: 'Inter', sans-serif;
      border-radius: 4px;
      border: 1px solid {BORDER};
      box-sizing: border-box;
    }}

    .hero-content {{
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 6%;
      box-sizing: border-box;
    }}

    /* matches .eyebrow in theme.py */
    .hero-text .label {{
      font-family: 'Inter', sans-serif;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: {text_color};
      border-bottom: 1px solid {BORDER};
      display: inline-block;
      padding-bottom: 6px;
      margin-bottom: 18px;
    }}

    .hero-text .name {{
      font-family: 'Archivo', sans-serif;
      font-size: clamp(32px, 4.5vw, 54px);
      font-weight: 800;
      letter-spacing: 0.01em;
      line-height: 1.08;
      color: {text_color};
      margin-bottom: 18px;
    }}

    .hero-text .subtitle {{
      font-family: 'Archivo', sans-serif;
      font-size: clamp(15px, 1.6vw, 20px);
      font-weight: 600;
      color: #3a3a3a;
      max-width: 440px;
      line-height: 1.4;
    }}

    .hero-photos {{
      position: relative;
      width: 42%;
      max-width: 300px;
      height: 78%;
    }}

    .photo {{
      position: absolute;
      border: 3px solid #fff;
      border-radius: 4px;
      box-shadow: 0 6px 16px rgba(0,0,0,0.25);
      overflow: hidden;
      background: #ddd;
    }}

    .photo img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}

    .photo.placeholder {{
      display: flex;
      align-items: center;
      justify-content: center;
      color: {FAINT};
      font-size: 13px;
    }}

    .hero-photos .photo:nth-child(1) {{
      width: 62%;
      height: 62%;
      top: 0;
      left: 0;
      z-index: 1;
      filter: grayscale(15%);
    }}

    .hero-photos .photo:nth-child(2) {{
      width: 62%;
      height: 62%;
      bottom: 0;
      right: 0;
      z-index: 2;
      filter: grayscale(100%);
    }}

    .curtain {{
      position: absolute;
      inset: 0;
      display: flex;
      z-index: 10;
      pointer-events: none;
    }}

    .strip {{
      flex: 1 1 0;
      background: {curtain_color};
      transform: translateY(0%);
      transition: transform 550ms cubic-bezier(0.22, 1, 0.36, 1);
      will-change: transform;
    }}

    .hint {{
      position: absolute;
      bottom: 14px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 20;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: rgba(255,255,255,0.6);
      transition: opacity 0.3s ease;
      pointer-events: none;
    }}

    /* narrow screens: drop the photos so the name has room */
    @media (max-width: 600px) {{
      .hero-photos {{ display: none; }}
      .hero-content {{ padding: 0 8%; }}
    }}
  </style>

  <div class="hero-content">
    <div class="hero-text">
      <div class="label">{label}</div>
      <div class="name">{name_html}</div>
      <div class="subtitle">{subtitle}</div>
    </div>
    <div class="hero-photos">
      {photo1}
      {photo2}
    </div>
  </div>

  <div class="curtain" id="curtain">
    {strips_html}
  </div>

  <div class="hint" id="hint">move your cursor across</div>

  <script>
    (function() {{
      const root = document.getElementById('hero-root');
      const curtain = document.getElementById('curtain');
      const hint = document.getElementById('hint');
      const strips = Array.from(curtain.querySelectorAll('.strip'));
      const n = strips.length;
      const isTouch = window.matchMedia('(hover: none)').matches;

      function applyWave(cursorFraction) {{
        strips.forEach((strip, i) => {{
          const stripFraction = i / (n - 1);
          const dist = Math.abs(stripFraction - cursorFraction);
          const falloff = Math.exp(-Math.pow(dist * 3.2, 2));
          const lift = falloff * 100;
          strip.style.transform = `translateY(-${{lift}}%)`;
        }});
      }}

      function resetWave() {{
        strips.forEach((strip) => {{
          strip.style.transform = 'translateY(0%)';
        }});
      }}

      function openAll() {{
        strips.forEach((strip) => {{
          strip.style.transform = 'translateY(-100%)';
        }});
      }}

      if (!isTouch) {{
        root.addEventListener('mousemove', (e) => {{
          const rect = root.getBoundingClientRect();
          const fraction = Math.min(Math.max((e.clientX - rect.left) / rect.width, 0), 1);
          applyWave(fraction);
          hint.style.opacity = '0';
        }});
        root.addEventListener('mouseleave', () => {{
          resetWave();
          hint.style.opacity = '1';
        }});
      }} else {{
        hint.textContent = 'tap to reveal';
        let revealed = false;
        function autoSweep() {{
          const duration = 1400;
          const start = performance.now();
          function step(now) {{
            const t = Math.min((now - start) / duration, 1);
            applyWave(t);
            if (t < 1) requestAnimationFrame(step);
            else openAll();
          }}
          requestAnimationFrame(step);
          hint.style.opacity = '0';
        }}
        root.addEventListener('touchstart', () => {{
          if (!revealed) {{
            revealed = true;
            autoSweep();
          }}
        }}, {{ once: true }});
      }}
    }})();
  </script>
</div>
"""
