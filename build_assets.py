#!/usr/bin/env python3
"""
Generates the SVG asset set for the AVIVASHISHTA29 profile README.

Design language: dark terminal / monospace.
Constraints imposed by GitHub:
  - SVGs are rendered as <img> through camo, so NO scripts and NO external
    font/@import loads. Only generic font families and inline CSS/SMIL.
  - Declarative CSS animations and SMIL DO work.
  - No hover / tooltips are possible in an <img> context, so every chart here
    is fully labelled statically. Axis ticks + selective direct labels carry
    the read.
  - Every asset paints its own background so it looks intentional in both
    GitHub light and dark themes.

Content is sourced from avivashishta.com/llms.txt. Chart data is real, pulled
from the GitHub GraphQL contributions API (see YEARLY / MONTHLY below).

Run:  python3 build_assets.py
"""

import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

W = 880

# ---------------------------------------------------------------- palette
BG      = "#0A0A0B"
PANEL   = "#101014"
INSET   = "#16161B"
BORDER  = "#1F1F25"
TEXT    = "#EDEDEF"
DIM     = "#7A7A85"
FAINT   = "#4A4A54"
ACCENT  = "#00E5A0"
WARM    = "#FF7A45"
BLUE    = "#5AC8FA"
VIOLET  = "#C084FC"

MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

# ------------------------------------------------------------- chart data
# GitHub contributions, AVIVASHISHTA29. Verified via the GraphQL
# contributionsCollection API on 2026-07-27. 2026 is a partial year and is
# always rendered as such — never plot an incomplete period as if it closed.
YEARLY = [
    ("2021", 186,  False),
    ("2022", 1780, False),
    ("2023", 1402, False),
    ("2024", 3637, False),
    ("2025", 7887, False),
    ("2026", 5377, True),   # partial — Jan 1 to Jul 27
]

# Trailing 12 months, same source.
MONTHLY = [
    ("AUG", 664,  False), ("SEP", 597,  False), ("OCT", 806,  False),
    ("NOV", 664,  False), ("DEC", 890,  False), ("JAN", 868,  False),
    ("FEB", 731,  False), ("MAR", 1270, False), ("APR", 776,  False),
    ("MAY", 782,  False), ("JUN", 585,  False), ("JUL", 365,  True),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, extra_defs="", extra_css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img">
<defs>
<style>
  .m {{ font-family:{MONO}; }}
  @keyframes fadein {{ from {{ opacity:0; transform:translateY(6px); }} to {{ opacity:1; transform:translateY(0); }} }}
  @keyframes blink  {{ 0%,49% {{ opacity:1; }} 50%,100% {{ opacity:0; }} }}
  /* 'backwards' (not 'both') is deliberate: if a renderer ignores CSS
     animation entirely, the element falls back to its natural opacity:1
     instead of staying invisible. */
  .fi {{ animation: fadein .6s ease-out backwards; }}
  .cursor {{ animation: blink 1.1s step-end infinite; }}
{extra_css}
</style>
{extra_defs}
</defs>
<rect width="{w}" height="{h}" rx="10" fill="{BG}"/>
{body}
</svg>
'''


def write(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {name}  ({len(content)} bytes)")


def txt(x, y, s, size=14, fill=TEXT, weight="400", anchor="start",
        cls="", ls="0", opacity="1", cursor=False):
    """cursor=True appends a blinking block as a <tspan> inside the same
    <text> node. Doing it in-flow rather than as a separately positioned
    <rect> is the only reliable way to place it: the exact advance width of
    'monospace' differs per platform, so any hardcoded x would drift."""
    c = "m" + (" " + cls if cls else "")
    inner = esc(s)
    if cursor:
        inner += f'<tspan class="cursor" fill="{ACCENT}"> █</tspan>'
    return (f'<text x="{x}" y="{y}" class="{c}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{ls}" '
            f'opacity="{opacity}">{inner}</text>')


def delay(i, step=0.07, base=0.1):
    return f'style="animation-delay:{base + i*step:.2f}s"'


def bar_path(x, y, w, h, r=4):
    """Bar with only the data-end rounded, anchored flat to the baseline.
    Degrades to a plain rect when the bar is shorter than the corner radius."""
    if h <= r:
        return f'<rect x="{x:.1f}" y="{y + h - max(h, 1):.1f}" width="{w:.1f}" height="{max(h, 1):.1f}"/>'
    return (f'<path d="M {x:.1f} {y + h:.1f} V {y + r:.1f} Q {x:.1f} {y:.1f} {x + r:.1f} {y:.1f} '
            f'H {x + w - r:.1f} Q {x + w:.1f} {y:.1f} {x + w:.1f} {y + r:.1f} '
            f'V {y + h:.1f} Z"/>')


# ============================================================ 00 · header
def header():
    h = 230
    grid = "".join(
        f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{BORDER}" stroke-width="1" opacity=".55"/>'
        for x in range(0, W, 44)
    ) + "".join(
        f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{BORDER}" stroke-width="1" opacity=".55"/>'
        for y in range(0, h, 44)
    )

    body = f'''
  <g clip-path="url(#hclip)">
    {grid}
    <circle cx="742" cy="70" r="150" fill="url(#glow)"/>
    <rect x="0" y="0" width="{W}" height="{h}" fill="url(#vig)"/>
    <rect id="scan" x="0" y="0" width="{W}" height="2" fill="{ACCENT}" opacity=".16">
      <animate attributeName="y" values="-4;{h};-4" dur="7s" repeatCount="indefinite"/>
    </rect>
  </g>

  <g class="fi" style="animation-delay:.05s">
    {txt(44, 62, "$ ./introduce --self", 13, ACCENT)}
  </g>

  <g class="fi" style="animation-delay:.20s">
    {txt(44, 118, "AVI VASHISHTA", 44, TEXT, "700", ls="1", cursor=True)}
  </g>

  <g class="fi" style="animation-delay:.34s">
    {txt(44, 150, "Fullstack developer  ·  AI builder  ·  instructor", 15, DIM)}
  </g>

  <g class="fi" style="animation-delay:.46s">
    <line x1="44" y1="172" x2="836" y2="172" stroke="{BORDER}"/>
    {txt(44, 197, "NEW DELHI, IN", 11, FAINT, ls="1.6")}
    {txt(180, 197, "NEXT.JS · NODE · GRAPHQL · AI · THREE.JS", 11, FAINT, ls="1.6")}
    {txt(836, 197, "OPEN TO COLLABORATE", 11, ACCENT, anchor="end", ls="1.6")}
  </g>
'''
    defs = f'''
<clipPath id="hclip"><rect width="{W}" height="{h}" rx="10"/></clipPath>
<radialGradient id="glow"><stop offset="0%" stop-color="{ACCENT}" stop-opacity=".14"/><stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
<linearGradient id="vig" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{BG}" stop-opacity="0"/><stop offset="100%" stop-color="{BG}" stop-opacity=".85"/></linearGradient>
'''
    write("header.svg", svg(W, h, body, defs))


# ===================================================== 01-09 section rules
def section(num, label, note):
    h = 56
    # Label width is estimated from monospace advance (~0.6em) + letter-spacing.
    lw = len(label) * (15 * 0.6 + 2.4)
    rule_x = 56 + lw + 24
    body = f'''
  {txt(0, 34, num, 13, ACCENT, "700", ls="1")}
  {txt(30, 34, "—", 13, FAINT)}
  {txt(56, 34, label.upper(), 15, TEXT, "700", ls="2.4")}
  <line x1="{rule_x:.0f}" y1="29" x2="{W - len(note)*7 - 24}" y2="29" stroke="{BORDER}"/>
  {txt(W, 34, note, 11, FAINT, anchor="end", ls="1.6")}
'''
    write(f"s{num}.svg", svg(W, h, body))


# ============================================================= 01 whoami
def whoami():
    rows = [
        ("role",     '"Software Engineer @ Dock.us"'),
        ("age",      "23"),
        ("based",    '"New Delhi, India"'),
        ("degree",   '"BTech CS, IIIT Delhi \'24"'),
        ("was",      '["founding engineer", "instructor", "founder"]'),
        ("builds",   '["AI products", "web", "mobile", "3D interfaces"]'),
        ("taught",   "100_000  // developers, MERN stack"),
        ("open_to",  '"Interesting problems, good teams"'),
    ]
    h = 236 + (len(rows) - 6) * 22
    out = [f'<rect x="0" y="0" width="{W}" height="{h}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>']
    # window chrome
    out.append(f'<line x1="0" y1="38" x2="{W}" y2="38" stroke="{BORDER}"/>')
    for i, c in enumerate(["#3A3A42", "#3A3A42", "#3A3A42"]):
        out.append(f'<circle cx="{22 + i*17}" cy="19" r="5" fill="{c}"/>')
    out.append(txt(84, 24, "avi@dock ~ /about", 11, FAINT, ls="1"))

    y = 78
    out.append(f'<g class="fi" {delay(0)}>{txt(32, y, "const", 14, WARM)}{txt(88, y, "avi", 14, TEXT)}{txt(124, y, "= {", 14, DIM)}</g>')
    for i, (k, v) in enumerate(rows):
        yy = y + 24 + i*22
        if i < len(rows) - 1:
            # The comma belongs before a trailing // comment, not after it.
            head, sep, tail = v.partition("//")
            v = f"{head.rstrip()}, {sep}{tail}" if sep else v + ","
        out.append(
            f'<g class="fi" {delay(i+1)}>'
            f'{txt(56, yy, k + ":", 14, ACCENT)}'
            f'{txt(56 + 100, yy, v, 14, TEXT)}'
            f'</g>'
        )
    out.append(f'<g class="fi" {delay(len(rows)+1)}>{txt(32, y + 24 + len(rows)*22, "};", 14, DIM)}</g>')
    write("whoami.svg", svg(W, h, "\n".join(out)))


# =============================================================== 02 dock
def dock():
    h = 320
    metrics = [
        ("DEAL ROOMS",  "buyer-facing workspaces"),
        ("CONTENT",     "one library, one link"),
        ("ONBOARDING",  "mutual action plans"),
    ]
    resp = [
        "Ship AI-powered features on a Next.js, Node.js and GraphQL stack",
        "Build against AWS SQS for asynchronous messaging infrastructure",
        "Own features end to end — schema, API, interface, rollout",
    ]
    out = [f'<rect x="0" y="0" width="{W}" height="{h}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>']
    out.append(f'<rect x="0" y="0" width="4" height="{h}" rx="2" fill="{ACCENT}"/>')

    out.append(f'<g class="fi" {delay(0)}>{txt(32, 46, "DOCK", 26, TEXT, "700", ls="2")}'
               f'{txt(148, 46, "dock.us", 12, ACCENT)}</g>')
    out.append(f'<g class="fi" {delay(1)}>'
               f'<rect x="662" y="26" width="186" height="26" rx="13" fill="{ACCENT}" fill-opacity=".09" stroke="{ACCENT}" stroke-opacity=".35"/>'
               f'<circle cx="680" cy="39" r="4" fill="{ACCENT}"><animate attributeName="opacity" values="1;.25;1" dur="2.2s" repeatCount="indefinite"/></circle>'
               f'{txt(692, 43, "HERE SINCE MAR 2025", 10, ACCENT, ls="1.4")}</g>')

    out.append(f'<g class="fi" {delay(2)}>{txt(32, 76, "AI revenue enablement — deal rooms, content and onboarding in one place.", 13, DIM)}</g>')
    out.append(f'<line x1="32" y1="98" x2="848" y2="98" stroke="{BORDER}"/>')

    for i, (k, v) in enumerate(metrics):
        x = 32 + i*272
        out.append(f'<g class="fi" {delay(3+i)}>'
                   f'<rect x="{x}" y="116" width="248" height="60" rx="6" fill="{INSET}" stroke="{BORDER}"/>'
                   f'{txt(x+16, 140, k, 11, ACCENT, "700", ls="1.4")}'
                   f'{txt(x+16, 160, v, 11, DIM)}</g>')

    out.append(f'<g class="fi" {delay(6)}>{txt(32, 210, "// what I do here", 12, FAINT)}</g>')
    for i, r in enumerate(resp):
        out.append(f'<g class="fi" {delay(7+i)}>'
                   f'{txt(32, 236 + i*24, "→", 13, ACCENT)}'
                   f'{txt(56, 236 + i*24, r, 13, TEXT)}</g>')
    write("dock.svg", svg(W, h, "\n".join(out)))


# ========================================================= 03 system map
def ecosystem():
    """Hub-and-spoke node graph. Wires draw themselves in, then the nodes
    pop; the hub breathes. Everything degrades to a fully visible static
    diagram if CSS animation is ignored."""
    h = 430
    NW, NH = 200, 68
    HUB_X, HUB_Y, HUB_W, HUB_H = 340, 181, 200, 68

    left = [
        ("AI PRODUCTS", ["Fin-AI · 99%+ accuracy", "tutoring · proctoring"], ACCENT),
        ("TEACHING",    ["100K+ developers", "17 tutorials · 100K+ views"],  VIOLET),
        ("MOBILE",      ["Expo · React Native", "BFF · wallet · ticketing"], BLUE),
    ]
    right = [
        ("WEB PLATFORMS", ["multi-tenant CMS · RBAC", "realtime · Next.js"],  BLUE),
        ("SHIPPED AT",    ["Dock.us · Turgon AI", "AccioJob (YC 2021)"],      ACCENT),
        ("3D INTERFACES", ["Three.js · R3F · GSAP", "MediaPipe gestures"],    WARM),
    ]
    rows_y = [40, 181, 322]

    # Same fallback discipline as .fi: the *base* state is the finished state
    # (dashoffset 0 = fully drawn) and the keyframe reaches back to the hidden
    # state, with fill-mode 'backwards'. A renderer that drops the animation
    # shows a complete diagram instead of nothing.
    css = '''
  .wire { stroke-dasharray: 420; stroke-dashoffset: 0; animation: draw 1.5s cubic-bezier(.6,0,.2,1) backwards; }
  @keyframes draw { from { stroke-dashoffset: 420; } to { stroke-dashoffset: 0; } }
  .flow { stroke-dasharray: 3 10; animation: march 1.5s linear infinite; }
  @keyframes march { to { stroke-dashoffset: -13; } }
  .core { animation: breathe 3.4s ease-in-out infinite; }
  @keyframes breathe { 0%,100% { opacity:1 } 50% { opacity:.5 } }
'''
    out = []

    # ---- wires first, so nodes paint over their endpoints
    for side, col in (("l", left), ("r", right)):
        for i in range(3):
            cy = rows_y[i] + NH / 2
            if side == "l":
                x0, x1 = HUB_X, 40 + NW
                d = f"M {x0} 215 C {x0-46} 215, {x1+46} {cy}, {x1} {cy}"
            else:
                x0, x1 = HUB_X + HUB_W, W - 40 - NW
                d = f"M {x0} 215 C {x0+46} 215, {x1-46} {cy}, {x1} {cy}"
            dl = f'style="animation-delay:{0.15 + i*0.12:.2f}s"'
            out.append(f'<path class="wire" d="{d}" stroke="{FAINT}" stroke-width="1.5" opacity=".6" {dl}/>')
            out.append(f'<path class="flow" d="{d}" stroke="{col[i][2]}" stroke-width="1" opacity=".38"/>')

    # ---- hub
    out.append(f'<g class="fi" style="animation-delay:.05s">'
               f'<rect x="{HUB_X}" y="{HUB_Y}" width="{HUB_W}" height="{HUB_H}" rx="8" fill="{INSET}" stroke="{ACCENT}" stroke-opacity=".5"/>'
               f'<circle class="core" cx="{HUB_X+HUB_W/2}" cy="{HUB_Y+22}" r="4" fill="{ACCENT}"/>'
               f'{txt(HUB_X+HUB_W/2, 218, "AVI VASHISHTA", 13, TEXT, "700", anchor="middle", ls="1.4")}'
               f'{txt(HUB_X+HUB_W/2, 236, "one pipeline", 10, FAINT, anchor="middle", ls="1")}'
               f'</g>')

    # ---- satellite nodes
    for side, col in (("l", left), ("r", right)):
        x = 40 if side == "l" else W - 40 - NW
        for i, (name, lines, c) in enumerate(col):
            y = rows_y[i]
            dl = f'style="animation-delay:{0.85 + i*0.1 + (0 if side == "l" else 0.05):.2f}s"'
            out.append(f'<g class="fi" {dl}>')
            out.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="8" fill="{PANEL}" stroke="{BORDER}"/>')
            out.append(f'<rect x="{x}" y="{y+14}" width="3" height="{NH-28}" rx="1.5" fill="{c}" opacity=".85"/>')
            out.append(txt(x + 18, y + 26, name, 11, c, "700", ls="1.4"))
            for j, ln in enumerate(lines):
                out.append(txt(x + 18, y + 44 + j*15, ln, 10, DIM))
            out.append("</g>")

    write("ecosystem.svg", svg(W, h, "\n".join(out), extra_css=css))


# ======================================================= 04 by the numbers
def numbers():
    """Mixed-unit headline metrics. These are magnitudes with no common
    scale, so they get stat tiles rather than a bar chart."""
    tiles = [
        ("100K+", "DEVELOPERS TAUGHT",       "MERN stack, online",       ACCENT),
        ("500+",  "PULL REQUESTS REVIEWED",  "as founding engineer",     BLUE),
        ("300+",  "FEATURES SHIPPED",        "highest on the team",      VIOLET),
        ("20K+",  "GITHUB CONTRIBUTIONS",    "since 2021",               ACCENT),
        ("2×",    "YC-BACKED COMPANIES",     "AccioJob · Dock.us",       WARM),
        ("2",     "BOOKS PUBLISHED",         "written at 16 and 18",     DIM),
    ]
    tw, gap, th = 272, 20, 92
    h = 16 + 2*(th + gap) - gap + 16
    out = []
    for i, (big, label, sub, c) in enumerate(tiles):
        x = 16 + (i % 3)*(tw + gap)
        y = 16 + (i // 3)*(th + gap)
        out.append(f'<g class="fi" {delay(i, step=0.08)}>')
        out.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="8" fill="{PANEL}" stroke="{BORDER}"/>')
        out.append(f'<rect x="{x}" y="{y}" width="{tw}" height="2" rx="1" fill="{c}" opacity=".55"/>')
        out.append(txt(x + 20, y + 46, big, 28, c, "700", ls="1"))
        out.append(txt(x + 20, y + 66, label, 10, TEXT, "700", ls="1.4"))
        out.append(txt(x + 20, y + 81, sub, 10, FAINT))
        out.append("</g>")
    write("numbers.svg", svg(W, h, "\n".join(out)))


# ======================================================== 05a growth line
def growth():
    """Contributions per year — one series, so no legend; the title names it.
    Recessive grid, 2px line, 8px markers, direct labels only on the peak and
    the latest point. The partial year is drawn dashed and hollow so an
    incomplete period is never read as a closed one."""
    h = 300
    x0, x1 = 84, 840
    yb, yt = 232, 66          # baseline / top of plot
    ymax = 8000
    step = (x1 - x0) / (len(YEARLY) - 1)

    def px(i):
        return x0 + i*step

    def py(v):
        return yb - (v / ymax) * (yb - yt)

    out = [f'<rect x="0" y="0" width="{W}" height="{h}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>']
    out.append(txt(32, 40, "CONTRIBUTIONS PER YEAR", 12, TEXT, "700", ls="1.6"))
    out.append(txt(848, 40, "GITHUB · AVIVASHISHTA29", 10, FAINT, anchor="end", ls="1.2"))

    # grid + y ticks
    for gv in range(0, ymax + 1, 2000):
        gy = py(gv)
        out.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="{BORDER}" opacity=".8"/>')
        lab = "0" if gv == 0 else f"{gv // 1000}k"
        out.append(txt(x0 - 14, gy + 4, lab, 10, FAINT, anchor="end"))

    solid = [(i, v) for i, (_, v, p) in enumerate(YEARLY) if not p]
    # area under the closed years, closing down to the baseline
    area = " ".join(f"{'M' if k == 0 else 'L'} {px(i):.1f} {py(v):.1f}" for k, (i, v) in enumerate(solid))
    area += f" L {px(solid[-1][0]):.1f} {yb} L {px(0):.1f} {yb} Z"
    out.append(f'<path d="{area}" fill="url(#garea)" opacity=".9"/>')

    line = " ".join(f"{'M' if k == 0 else 'L'} {px(i):.1f} {py(v):.1f}" for k, (i, v) in enumerate(solid))
    out.append(f'<path class="gline" d="{line}" stroke="{ACCENT}" stroke-width="2" '
               f'stroke-linecap="round" stroke-linejoin="round" fill="none"/>')

    # the partial-year leg: dashed, to read as provisional
    li, lv = solid[-1]
    pi, pv, _ = len(YEARLY) - 1, YEARLY[-1][1], True
    out.append(f'<path d="M {px(li):.1f} {py(lv):.1f} L {px(pi):.1f} {py(pv):.1f}" stroke="{ACCENT}" '
               f'stroke-width="2" stroke-dasharray="5 5" opacity=".55" fill="none"/>')

    # markers + x labels
    for i, (yr, v, partial) in enumerate(YEARLY):
        cx, cy = px(i), py(v)
        if partial:
            out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="{PANEL}" stroke="{ACCENT}" stroke-width="2" opacity=".8"/>')
        else:
            out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="{ACCENT}" stroke="{PANEL}" stroke-width="2"/>')
        out.append(txt(cx, yb + 24, yr + ("*" if partial else ""), 11, DIM if not partial else FAINT, anchor="middle", ls="1"))

    # selective direct labels: the peak and the latest reading
    peak_i = max(range(len(YEARLY)), key=lambda i: YEARLY[i][1] if not YEARLY[i][2] else -1)
    out.append(txt(px(peak_i), py(YEARLY[peak_i][1]) - 14, f"{YEARLY[peak_i][1]:,}", 12, TEXT, "700", anchor="middle"))
    out.append(txt(px(len(YEARLY) - 1), py(YEARLY[-1][1]) - 14, f"{YEARLY[-1][1]:,}", 12, DIM, "700", anchor="end"))

    out.append(txt(32, 274, "* 2026 is year-to-date (Jan 1 – Jul 27), not a closed year.", 10, FAINT))

    defs = f'''
<linearGradient id="garea" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="{ACCENT}" stop-opacity=".30"/>
  <stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/>
</linearGradient>
'''
    css = '''
  .gline { stroke-dasharray: 2400; stroke-dashoffset: 0; animation: trace 2s cubic-bezier(.6,0,.2,1) backwards; animation-delay:.2s; }
  @keyframes trace { from { stroke-dashoffset: 2400; } to { stroke-dashoffset: 0; } }
'''
    write("growth.svg", svg(W, h, "\n".join(out), defs, css))


# ========================================================= 05b cadence bar
def cadence():
    """Trailing-12-month contributions. One series, so no legend. Bars grow
    from the baseline; the in-progress month is hollow, not solid."""
    h = 268
    x0, x1 = 84, 840
    yb, yt = 200, 62
    ymax = 1400
    slot = (x1 - x0) / len(MONTHLY)
    bw = slot - 14        # leaves a wide surface gap between adjacent bars

    def py(v):
        return yb - (v / ymax) * (yb - yt)

    out = [f'<rect x="0" y="0" width="{W}" height="{h}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>']
    out.append(txt(32, 40, "MONTHLY CADENCE — TRAILING 12 MONTHS", 12, TEXT, "700", ls="1.6"))
    out.append(txt(848, 40, "AUG 2025 → JUL 2026", 10, FAINT, anchor="end", ls="1.2"))

    for gv in range(0, ymax + 1, 400):
        gy = py(gv)
        out.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="{BORDER}" opacity=".8"/>')
        out.append(txt(x0 - 14, gy + 4, "0" if gv == 0 else str(gv), 10, FAINT, anchor="end"))

    peak = max(v for _, v, p in MONTHLY if not p)
    for i, (mon, v, partial) in enumerate(MONTHLY):
        bx = x0 + i*slot + 7
        by = py(v)
        bh = yb - by
        # Bars carry no transform of their own, so the no-animation fallback
        # is already correct; the reveal is a single clip-path wipe.
        if partial:
            out.append(f'<g fill="none" stroke="{ACCENT}" stroke-width="1.5" opacity=".6" clip-path="url(#wipe)">'
                       f'{bar_path(bx, by, bw, bh)}</g>')
        else:
            op = "1" if v == peak else ".62"
            out.append(f'<g fill="{ACCENT}" opacity="{op}" clip-path="url(#wipe)">{bar_path(bx, by, bw, bh)}</g>')
        out.append(txt(bx + bw/2, yb + 22, mon, 10, FAINT if partial else DIM, anchor="middle", ls=".6"))
        if v == peak:
            out.append(txt(bx + bw/2, by - 10, str(v), 11, TEXT, "700", anchor="middle"))

    out.append(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{FAINT}" opacity=".7"/>')
    out.append(txt(32, 242, "JUL 2026 is partial (through the 27th) — drawn hollow.", 10, FAINT))

    # The rect's authored width is already the full plot, so a renderer that
    # ignores SMIL clips nothing and every bar shows. The <animate> starts it
    # back at 0 and freezes open — same 'degrade to visible' rule as the CSS.
    defs = f'''
<clipPath id="wipe">
  <rect x="{x0 - 4}" y="{yt - 20}" width="{x1 - x0 + 12}" height="{yb - yt + 40}">
    <animate attributeName="width" from="0" to="{x1 - x0 + 12}" dur="1.4s" begin="0.1s" fill="freeze" calcMode="spline" keySplines=".5 0 .2 1" keyTimes="0;1"/>
  </rect>
</clipPath>
'''
    write("cadence.svg", svg(W, h, "\n".join(out), defs))


# ========================================================== 06 experience
def experience():
    roles = [
        ("DOCK.US",          "Software Engineer",  "MAR 2025 — PRESENT",
         "AI features on Next.js, Node.js, GraphQL and AWS SQS.", ACCENT, True),
        ("TURGON AI",        "Founding Engineer",  "OCT 2024 — JUN 2025",
         "Led a team across three AI products. 500+ PRs reviewed.", BLUE, False),
        ("ACCIOJOB",         "SDE · Instructor",   "OCT 2022 — OCT 2024",
         "300+ features across four repos. Taught 90,000+ students.", VIOLET, False),
        ("STV TECHNOLOGIES", "Founder",            "OCT 2021 — AUG 2022",
         "Freelancing firm at 20. 30+ projects, INR 10L revenue.", WARM, False),
    ]
    rh = 74
    h = 24 + len(roles)*rh + 34
    out = [f'<rect x="0" y="0" width="{W}" height="{h}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>']
    # the spine
    out.append(f'<line x1="48" y1="46" x2="48" y2="{24 + (len(roles)-1)*rh + 46}" stroke="{BORDER}" stroke-width="1.5"/>')

    for i, (org, role, when, note, c, current) in enumerate(roles):
        y = 46 + i*rh
        out.append(f'<g class="fi" {delay(i, step=0.1)}>')
        if current:
            out.append(f'<circle cx="48" cy="{y}" r="7" fill="{c}" fill-opacity=".18"/>'
                       f'<circle cx="48" cy="{y}" r="4" fill="{c}">'
                       f'<animate attributeName="opacity" values="1;.3;1" dur="2.2s" repeatCount="indefinite"/></circle>')
        else:
            out.append(f'<circle cx="48" cy="{y}" r="4" fill="{PANEL}" stroke="{c}" stroke-width="1.5" opacity=".85"/>')
        out.append(txt(76, y + 5, org, 14, TEXT, "700", ls="1.2"))
        out.append(txt(76 + len(org)*9.6 + 18, y + 5, role, 12, c))
        out.append(txt(848, y + 5, when, 10, FAINT, anchor="end", ls="1.2"))
        out.append(txt(76, y + 26, note, 11, DIM))
        out.append("</g>")

    out.append(txt(76, h - 18, "+ fullstack and mobile internships at Attrilu and Fitzura (2022).", 10, FAINT))
    write("experience.svg", svg(W, h, "\n".join(out)))


# ============================================================== 07 stack
def stack():
    layers = [
        ("FRONTEND", ["React", "Next.js", "TypeScript", "Tailwind", "Redux", "Zustand"], ACCENT),
        ("3D / MOTION", ["Three.js", "R3F", "GSAP", "Framer Motion", "MediaPipe"],       WARM),
        ("BACKEND",  ["Node.js", "NestJS", "Express", "GraphQL", "Python", "Django"],    BLUE),
        ("AI",       ["LangChain", "Vercel AI SDK", "OpenAI", "Eleven Labs"],            ACCENT),
        ("DATA",     ["PostgreSQL", "Prisma", "MongoDB", "Firebase", "Upstash Redis"],   VIOLET),
        ("PLATFORM", ["AWS", "Docker", "CI/CD", "Vercel", "Supabase", "PostHog"],        DIM),
        ("MOBILE",   ["React Native", "Expo", "Kotlin", "Unity", "C#"],                  BLUE),
    ]
    row_h = 54
    h = 40 + len(layers)*row_h + 20
    out = [f'<rect x="0" y="0" width="{W}" height="{h}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>']
    for i, (name, items, col) in enumerate(layers):
        y = 34 + i*row_h
        out.append(f'<g class="fi" {delay(i, step=0.09)}>')
        out.append(f'<rect x="24" y="{y}" width="4" height="30" rx="2" fill="{col}" opacity=".9"/>')
        out.append(txt(44, y + 20, name, 11, col, "700", ls="1.6"))
        x = 168
        for it in items:
            w = len(it)*7.6 + 26
            out.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="{INSET}" stroke="{BORDER}"/>')
            out.append(txt(x + w/2, y + 20, it, 12, TEXT, anchor="middle"))
            x += w + 10
        out.append("</g>")
        if i < len(layers) - 1:
            out.append(f'<line x1="24" y1="{y+42}" x2="856" y2="{y+42}" stroke="{BORDER}" opacity=".7"/>')
    write("stack.svg", svg(W, h, "\n".join(out)))


# =============================================================== 08 work
def work():
    # Descriptions are capped at DESC_MAX so they cannot run past the card
    # border — at 12px mono a 412px card fits roughly 50 characters.
    DESC_MAX = 50
    projects = [
        ("Portfolio v3", "Hand-gesture and head-tracking controls.",
         "React 19 · Three.js · R3F · MediaPipe", "LIVE"),
        ("AI For Messaging", "Turns rough thoughts into clear messages.",
         "React Native · Flask · OpenAI", ""),
        ("BOLDBot", "Customer service for Instagram businesses.",
         "Next.js · NestJS · Redux · Firebase", ""),
        ("BOLD Store", "One-click marketplace off a Facebook feed.",
         "React Native · Expo · Node.js", ""),
        ("podcast-app-react-rec", "Podcast platform, custom player and auth.",
         "React · Firebase · Redux Toolkit", "★ 5"),
        ("crypto-dashboard-dec", "Crypto tracker with custom watchlists.",
         "React · Chart.js · Framer Motion", "★ 2"),
        ("Portfolio2021", "Animated personal portfolio site.",
         "React · Framer Motion · MUI", "★ 3"),
        ("Infinite Rider", "Infinite runner, shipped in 2D and 3D.",
         "Unity · C#", ""),
    ]
    over = [p[0] for p in projects if len(p[1]) > DESC_MAX]
    assert not over, f"description too long, will overflow the card: {over}"
    cols, cw, gap = 2, 412, 24
    rows = (len(projects) + 1) // 2
    ch = 104
    h = 20 + rows*(ch + 16) + 4
    out = []
    for i, (name, desc, tech, tag) in enumerate(projects):
        cx = 16 + (i % cols)*(cw + gap)
        cy = 16 + (i // cols)*(ch + 16)
        out.append(f'<g class="fi" {delay(i, step=0.08)}>')
        out.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="8" fill="{PANEL}" stroke="{BORDER}"/>')
        out.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="2" rx="1" fill="{ACCENT}" opacity=".5"/>')
        out.append(txt(cx + 20, cy + 32, name, 14, TEXT, "700"))
        if tag:
            out.append(txt(cx + cw - 20, cy + 32, tag, 11, ACCENT if tag == "LIVE" else WARM,
                           "700" if tag == "LIVE" else "400", anchor="end", ls="1.2"))
        out.append(txt(cx + 20, cy + 56, desc, 12, DIM))
        out.append(txt(cx + 20, cy + 82, tech, 11, ACCENT, ls=".4"))
        out.append("</g>")
    write("work.svg", svg(W, h, "\n".join(out)))


# ============================================================= 10 footer
def footer():
    h = 108
    out = [f'<rect x="0" y="0" width="{W}" height="{h}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>']
    out.append(f'<g class="fi">{txt(32, 44, "$", 15, ACCENT)}'
               f'{txt(52, 44, "echo $STATUS", 15, TEXT)}</g>')
    out.append(f'<g class="fi" {delay(2)}>{txt(32, 74, "Building AI products at Dock. Open to interesting problems and good teams.", 13, DIM, cursor=True)}</g>')
    out.append(txt(848, 74, "avivashishta.com", 11, FAINT, anchor="end", ls="1.2"))
    write("footer.svg", svg(W, h, "\n".join(out)))


if __name__ == "__main__":
    print("building assets ->", OUT)
    header()
    section("01", "whoami",       "IDENTITY")
    section("02", "currently",    "DOCK.US")
    section("03", "system map",   "ECOSYSTEM")
    section("04", "by the numbers", "IMPACT")
    section("05", "trajectory",   "GROWTH")
    section("06", "experience",   "TIMELINE")
    section("07", "stack",        "TOOLING")
    section("08", "selected work", "PROJECTS")
    section("09", "telemetry",    "ACTIVITY")
    whoami()
    dock()
    ecosystem()
    numbers()
    growth()
    cadence()
    experience()
    stack()
    work()
    footer()
    print("done.")
