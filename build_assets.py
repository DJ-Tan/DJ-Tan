"""Builds the SVG banner and repo cards used by the profile README.

Run `python build_assets.py`; files are written to ./assets.
Palette and type follow the dj-tan.github.io mission console.
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).parent / "assets"

BASE, PANEL = "#0a0908", "#13110d"
BORDER, BORDER_DIM = "#463719", "#2a2014"
TEXT, TEXT_DIM, MUTED = "#f0e7d4", "#b5a883", "#8a7d5e"
AMBER, AMBER_DIM = "#ffb700", "#d9a01a"
GREEN, RED = "#5fd35f", "#ff3838"

SANS = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, Consolas, Menlo, monospace"

STYLE = """<style>
.m{font-family:%s}.s{font-family:%s}
@keyframes blink{0%%,49%%{opacity:1}50%%,100%%{opacity:0}}
@keyframes pulse{0%%,100%%{opacity:1}50%%{opacity:.3}}
@keyframes twinkle{0%%,100%%{opacity:.15}50%%{opacity:.8}}
@keyframes march{to{stroke-dashoffset:-40}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes drain{from{transform:scaleX(1)}to{transform:scaleX(0)}}
.blink{animation:blink 1.1s steps(1) infinite}
.pulse{animation:pulse 1.8s ease-in-out infinite}
.tw{animation:twinkle 4s ease-in-out infinite}
.march{animation:march 3s linear infinite}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>""" % (MONO, SANS)


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{title}">'
        f"<title>{title}</title>{STYLE}{body}</svg>\n"
    )


def mono_width(text, size, spacing=0.0):
    # 0.6em is the advance of JetBrains Mono / SF Mono / Menlo
    return len(text) * (size * 0.6 + spacing)


def frame(w, h, accent, left, right, status_color, strip=44):
    """Panel chrome: border, corner brackets, header strip with status."""
    c = 18
    return f"""
<defs><linearGradient id="strip" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{AMBER}" stop-opacity=".07"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
</linearGradient></defs>
<rect width="{w}" height="{h}" fill="{BASE}"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" fill="none" stroke="{BORDER}"/>
<rect x="1" y="1" width="{w-2}" height="{strip-1}" fill="url(#strip)"/>
<line x1="1" y1="{strip}" x2="{w-1}" y2="{strip}" stroke="{BORDER}"/>
<path d="M.5 {c}V.5H{c}M{w-c} {h-.5}H{w-.5}V{h-c}" fill="none" stroke="{accent}" stroke-width="1.5"/>
<text class="m" x="24" y="{strip/2+4.5}" font-size="12" letter-spacing="2" fill="{AMBER_DIM}">{left}</text>
<text class="m" x="{w-42}" y="{strip/2+4.5}" font-size="12" letter-spacing="2" fill="{TEXT_DIM}" text-anchor="end">{right}</text>
<circle class="pulse" cx="{w-29}" cy="{strip/2}" r="3.5" fill="{status_color}"/>"""


def stars(n, x0, y0, x1, y1, seed, twinkle=6):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        r = rnd.choice([0.6, 0.8, 0.8, 1.1, 1.4])
        if i < twinkle:
            delay = rnd.uniform(0, 4)
            out.append(f'<circle class="tw" style="animation-delay:{delay:.1f}s" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{TEXT}"/>')
        else:
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{TEXT}" opacity="{rnd.uniform(.12, .4):.2f}"/>')
    return "".join(out)


def tags(x, y, items, color=TEXT_DIM, border=BORDER):
    out = []
    for item in items:
        label = item.upper()
        w = mono_width(label, 11, 1) + 18
        out.append(
            f'<rect x="{x}" y="{y}" width="{w:.0f}" height="22" fill="{PANEL}" stroke="{border}"/>'
            f'<text class="m" x="{x+9}" y="{y+15}" font-size="11" letter-spacing="1" fill="{color}">{label}</text>'
        )
        x += w + 8
    return "".join(out)


def card(name, idx, status, status_color, accent, art, title, blurb, meta, tag_items, desc):
    w, h = 600, 320
    body = frame(w, h, accent, f"REPO.{idx:02d}", status, status_color)
    body += f'<rect x="1" y="45" width="{w-2}" height="151" fill="{PANEL}" opacity=".55"/>'
    body += art
    body += f'<line x1="1" y1="196" x2="{w-1}" y2="196" stroke="{BORDER_DIM}"/>'
    body += f'<text class="s" x="24" y="236" font-size="26" font-weight="700" letter-spacing="-.4" fill="{TEXT}">{title}</text>'
    body += f'<text class="m" x="576" y="234" font-size="11.5" letter-spacing="1" fill="{MUTED}" text-anchor="end">{meta}</text>'
    body += f'<text class="s" x="24" y="263" font-size="15" fill="{TEXT_DIM}">{blurb}</text>'
    body += tags(24, 280, tag_items)
    (OUT / f"card-{name}.svg").write_text(svg(w, h, body, desc), encoding="utf-8")


# ── header banner ───────────────────────────────────────────────────────────
def header():
    w, h = 1200, 320
    cx, cy = 1012, 186
    body = frame(w, h, AMBER, "STATION :: DT-001", "UPLINK :: STABLE", GREEN, strip=48)
    body += stars(70, 10, 56, w - 10, h - 10, seed=7, twinkle=10)
    body += f"""
<defs>
<filter id="glow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="14"/></filter>
<radialGradient id="halo"><stop offset="0" stop-color="{AMBER}" stop-opacity=".16"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>
</defs>
<text class="m" x="60" y="104" font-size="14" letter-spacing="4.5" fill="{AMBER_DIM}">// OPERATOR PROFILE : DT-001</text>
<text class="s" x="58" y="198" font-size="100" font-weight="800" letter-spacing="-3" fill="{AMBER}" opacity=".35" filter="url(#glow)" textLength="560" lengthAdjust="spacing">DAREN TAN</text>
<text class="s" x="58" y="198" font-size="100" font-weight="800" letter-spacing="-3" fill="{TEXT}" textLength="560" lengthAdjust="spacing">DAREN TAN</text>
<rect class="blink" x="636" y="132" width="10" height="68" fill="{AMBER}"/>
<line x1="60" y1="232" x2="780" y2="232" stroke="{BORDER}"/>
<g class="m" font-size="14" letter-spacing=".5">
<text x="60" y="262"><tspan fill="{MUTED}">role.</tspan><tspan fill="{AMBER}" dx="8">AI SOFTWARE ENGINEER</tspan></text>
<text x="330" y="262"><tspan fill="{MUTED}">domain.</tspan><tspan fill="{TEXT}" dx="8">multimodal models</tspan></text>
<text x="590" y="262"><tspan fill="{MUTED}">base.</tspan><tspan fill="{TEXT}" dx="8">Singapore</tspan></text>
</g>
<text class="m" x="60" y="290" font-size="12.5" letter-spacing="1" fill="{MUTED}">&gt; pre-training · data platforms · agents that run experiments</text>

<circle cx="{cx}" cy="{cy}" r="150" fill="url(#halo)"/>
<circle cx="{cx}" cy="{cy}" r="112" fill="none" stroke="{AMBER}" stroke-opacity=".35" stroke-dasharray="2 6"/>
<circle cx="{cx}" cy="{cy}" r="80" fill="none" stroke="{AMBER}" stroke-width="1.6"/>
<path d="M{cx-71} {cy-37}A80 80 0 0 1 {cx-40} {cy-69}" fill="none" stroke="{AMBER}" stroke-width="5" stroke-linecap="round" opacity=".35"/>
<text class="m" x="{cx}" y="{cy+14}" font-size="40" font-weight="700" letter-spacing="-1" fill="{AMBER}" text-anchor="middle">DT</text>
"""
    ticks = []
    for i in range(8):
        a =math.radians(i * 45 - 90)
        ticks.append(f'<circle cx="{cx+112*math.cos(a):.1f}" cy="{cy+112*math.sin(a):.1f}" r="2" fill="{AMBER}" opacity=".7"/>')
    body += "".join(ticks)
    body += f"""
<g style="transform-origin:{cx}px {cy}px;animation:spin 36s linear infinite">
<circle cx="{cx+112}" cy="{cy}" r="5" fill="{AMBER}"/><circle cx="{cx+112}" cy="{cy}" r="11" fill="{AMBER}" opacity=".18"/>
</g>
<g style="transform-origin:{cx}px {cy}px;animation:spin 20s linear infinite reverse">
<circle cx="{cx}" cy="{cy-80}" r="3.5" fill="{GREEN}"/>
</g>
"""
    (OUT / "header.svg").write_text(
        svg(w, h, body, "Daren Tan, AI software engineer. Operator profile DT-001."), encoding="utf-8"
    )


# ── card art ────────────────────────────────────────────────────────────────
def art_orbit():
    path = "M66 166C120 112 196 66 252 80C306 94 296 150 356 162C410 172 452 150 480 140"
    return f"""
{stars(34, 10, 52, 590, 190, seed=3, twinkle=5)}
<defs><radialGradient id="sun"><stop offset="0" stop-color="{AMBER}" stop-opacity=".45"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient></defs>
<circle cx="262" cy="126" r="54" fill="url(#sun)"/>
<circle cx="262" cy="126" r="20" fill="{AMBER}"/>
<circle cx="418" cy="80" r="11" fill="#2b261c" stroke="{MUTED}"/>
<circle cx="140" cy="176" r="7" fill="#2b261c" stroke="{MUTED}"/>
<path d="{path}" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="1 9" class="march" opacity=".9"/>
<circle cx="500" cy="144" r="18" fill="#17301a" stroke="{GREEN}" stroke-width="1.5"/>
<ellipse cx="500" cy="144" rx="31" ry="7" fill="none" stroke="{GREEN}" opacity=".6" transform="rotate(-14 500 144)"/>
<path d="M500 126V112M500 118C493 117 490 112 490 108C496 108 500 112 500 118M500 115C507 114 510 109 510 105C504 105 500 109 500 115" fill="{GREEN}" stroke="{GREEN}" stroke-width="1.4" stroke-linejoin="round"/>
<circle r="4.5" fill="{GREEN}"><animateMotion dur="5s" repeatCount="indefinite" path="{path}"/></circle>
<line x1="66" y1="166" x2="44" y2="184" stroke="{GREEN}" stroke-opacity=".5" stroke-dasharray="3 3"/>
<text class="m" x="24" y="70" font-size="11" letter-spacing="1.5" fill="{MUTED}">MEADOW BELT · PLOT 22</text>
<text class="m" x="576" y="70" font-size="11" letter-spacing="1.5" fill="{GREEN}" text-anchor="end" opacity=".8">★ ★ ★</text>"""


HAND_OPEN = [(0, 60), (-18, 48), (-32, 34), (-40, 20), (-46, 8), (-14, 18), (-16, 0), (-17, -12), (-18, -24),
             (-2, 15), (-2, -4), (-2, -18), (-2, -30), (10, 18), (11, 0), (12, -12), (12, -22),
             (20, 24), (24, 10), (26, 0), (28, -10)]
HAND_PEACE = [(0, 60), (-14, 48), (-20, 38), (-14, 30), (-6, 30), (-14, 18), (-20, 0), (-24, -14), (-28, -28),
              (-2, 15), (0, -4), (2, -20), (4, -34), (10, 18), (16, 6), (14, -2), (8, 2),
              (20, 24), (26, 14), (24, 6), (18, 8)]
HAND_EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (9, 10), (10, 11), (11, 12),
              (13, 14), (14, 15), (15, 16), (17, 18), (18, 19), (19, 20), (5, 9), (9, 13), (13, 17), (0, 17)]


def hand(points, ox, oy, color, mirror=False, scale=1.2):
    pts = [(ox + (-x if mirror else x) * scale, oy + y * scale) for x, y in points]
    lines = "".join(f'<line x1="{pts[a][0]:.1f}" y1="{pts[a][1]:.1f}" x2="{pts[b][0]:.1f}" y2="{pts[b][1]:.1f}"/>' for a, b in HAND_EDGES)
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6"/>' for x, y in pts)
    return f'<g stroke="{color}" stroke-opacity=".6" stroke-width="1.6">{lines}</g><g fill="{color}">{dots}</g>'


def reticle(x, y, w, h, color, c=14):
    return (f'<path d="M{x} {y+c}V{y}H{x+c}M{x+w-c} {y}H{x+w}V{y+c}M{x+w} {y+h-c}V{y+h}H{x+w-c}M{x+c} {y+h}H{x}V{y+h-c}" '
            f'fill="none" stroke="{color}" stroke-width="1.5"/>')


def label(x, y, text, bg):
    w = mono_width(text, 10.5, 1) + 12
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="18" fill="{bg}"/>'
            f'<text class="m" x="{x+6}" y="{y+12.5}" font-size="10.5" letter-spacing="1" font-weight="700" fill="{BASE}">{text}</text>')


def art_sigil():
    return f"""
{reticle(48, 60, 176, 124, AMBER_DIM)}{reticle(376, 60, 176, 124, RED)}
{label(48, 60, "P1 · MOVE2 0.94", AMBER)}{label(376, 60, "P2 · MOVE4 0.88", RED)}
{hand(HAND_OPEN, 140, 121, AMBER, scale=1.05)}{hand(HAND_PEACE, 462, 121, RED, mirror=True, scale=1.05)}
<text class="s" x="300" y="128" font-size="34" font-weight="800" fill="{TEXT}" text-anchor="middle" letter-spacing="-1">VS</text>
<text class="m" x="300" y="152" font-size="10.5" letter-spacing="2" fill="{MUTED}" text-anchor="middle">ROUND 03</text>
<rect x="258" y="162" width="84" height="4" fill="{BORDER_DIM}"/>
<rect x="258" y="162" width="84" height="4" fill="{AMBER}" style="transform-box:fill-box;transform-origin:left;animation:drain 5s linear infinite"/>
<text class="m" x="300" y="182" font-size="10" letter-spacing="1" fill="{TEXT_DIM}" text-anchor="middle">1 → 2 → 3</text>"""


def art_kuro():
    rnd = random.Random(11)
    thumbs = []
    for r in range(4):
        for c in range(3):
            x, y = 40 + c * 24 + rnd.uniform(-3, 3), 72 + r * 22 + rnd.uniform(-3, 3)
            dup = (r, c) in {(1, 2), (3, 0)}
            stroke = RED if dup else AMBER_DIM
            thumbs.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="16" height="14" fill="{PANEL}" stroke="{stroke}" stroke-opacity="{.9 if dup else .55}"/>')
    grid = []
    for r in range(5):
        for c in range(4):
            fill = AMBER if r == 0 else BORDER
            op = ".8" if r == 0 else ".55"
            grid.append(f'<rect x="{326 + c*22}" y="{78 + r*16}" width="18" height="10" fill="{fill}" opacity="{op}"/>')
    flow = "M110 118H186M262 118H318M418 118H468"
    particles = "".join(
        f'<circle r="2.5" fill="{AMBER}"><animateMotion dur="3.6s" begin="{d}s" repeatCount="indefinite" path="M110 118H520"/></circle>'
        for d in (0, 1.2, 2.4)
    )
    return f"""
{''.join(thumbs)}
<path d="{flow}" fill="none" stroke="{AMBER_DIM}" stroke-opacity=".6" stroke-dasharray="4 6" class="march"/>
{particles}
<path d="M190 82H258L238 118V150H210V118Z" fill="{PANEL}" stroke="{AMBER}" stroke-width="1.3" stroke-linejoin="round"/>
<text class="m" x="224" y="106" font-size="11" fill="{AMBER}" text-anchor="middle">#</text>
<rect x="318" y="70" width="100" height="94" fill="{BASE}" stroke="{BORDER}"/>
{''.join(grid)}
<rect x="486" y="92" width="64" height="48" fill="{BASE}" stroke="{BORDER}"/>
<rect x="478" y="100" width="64" height="48" fill="{BASE}" stroke="{AMBER_DIM}" stroke-opacity=".7"/>
<rect x="470" y="108" width="64" height="48" fill="{PANEL}" stroke="{AMBER}"/>
<text class="m" x="502" y="136" font-size="10" fill="{AMBER}" text-anchor="middle">.arrow</text>
<g class="m" font-size="10" letter-spacing="1.5" fill="{MUTED}" text-anchor="middle">
<text x="76" y="182">INGEST</text><text x="224" y="182">DEDUPE</text><text x="368" y="182">CATALOGUE</text><text x="508" y="182">EXPORT</text>
</g>"""


def art_pillbot():
    # phone: the app's six-container pill storage screen
    cells = [(89, 97), (123, 97), (89, 127), (123, 127), (89, 157), (123, 157)]
    pills = [
        f'<rect x="81" y="93.5" width="16" height="7" rx="3.5" fill="{AMBER}"/>',
        f'<circle cx="123" cy="97" r="5" fill="{GREEN}"/>',
        f'<ellipse cx="89" cy="127" rx="7" ry="4.5" fill="{TEXT_DIM}"/>',
        f'<path d="M123 121L129 127L123 133L117 127Z" fill="{RED}"/>',
        f'<rect x="81" y="153.5" width="16" height="7" rx="3.5" fill="{AMBER_DIM}"/><rect x="89" y="153.5" width="8" height="7" rx="3.5" fill="{TEXT}"/>',
        "",
    ]
    slots = "".join(
        f'<rect x="{x-15}" y="{y-12}" width="30" height="24" rx="3" fill="{BASE}" stroke="{BORDER}"'
        + (' stroke-dasharray="3 3"' if i == 5 else "") + "/>"
        for i, (x, y) in enumerate(cells)
    )
    # dispenser: six-compartment carousel that indexes one slot per dose
    cx, cy = 460, 114
    spokes = "".join(
        f'<line x1="{cx+8*math.cos(math.radians(a)):.1f}" y1="{cy+8*math.sin(math.radians(a)):.1f}" '
        f'x2="{cx+26*math.cos(math.radians(a)):.1f}" y2="{cy+26*math.sin(math.radians(a)):.1f}"/>'
        for a in range(0, 360, 60)
    )
    doses = "".join(
        f'<circle cx="{cx+17*math.cos(math.radians(a)):.1f}" cy="{cy+17*math.sin(math.radians(a)):.1f}" r="3" fill="{c}"/>'
        for a, c in zip(range(30, 390, 60), [AMBER, GREEN, TEXT_DIM, RED, AMBER_DIM, AMBER])
    )
    flow = "M152 120H246M294 120H400"
    return f"""
<rect x="64" y="54" width="84" height="134" rx="10" fill="{BASE}" stroke="{BORDER}"/>
<rect x="70" y="66" width="72" height="112" fill="{PANEL}"/>
<rect x="96" y="59" width="20" height="2.5" rx="1.25" fill="{BORDER}"/>
<text class="m" x="76" y="78" font-size="7.5" letter-spacing="1.5" fill="{AMBER_DIM}">PILLS</text>
{slots}{''.join(pills)}
<path d="{flow}" fill="none" stroke="{AMBER_DIM}" stroke-opacity=".6" stroke-dasharray="4 6" class="march"/>
<circle r="2.5" fill="{AMBER}"><animateMotion dur="2.4s" repeatCount="indefinite" path="M152 120H400"/></circle>
<path d="M248 102V132A22 6 0 0 0 292 132V102" fill="{PANEL}" stroke="{AMBER_DIM}"/>
<ellipse cx="270" cy="102" rx="22" ry="6" fill="{PANEL}" stroke="{AMBER}"/>
<path d="M248 117A22 6 0 0 0 292 117" fill="none" stroke="{AMBER_DIM}" stroke-opacity=".6"/>
<text class="m" x="270" y="158" font-size="10" letter-spacing="1.5" fill="{MUTED}" text-anchor="middle">MYSQL</text>
<rect x="400" y="80" width="120" height="104" rx="6" fill="{PANEL}" stroke="{BORDER}"/>
<circle cx="{cx}" cy="{cy}" r="26" fill="{BASE}" stroke="{AMBER}" stroke-width="1.4"/>
<g style="transform-origin:{cx}px {cy}px;animation:spin 12s steps(6) infinite">
<g stroke="{AMBER_DIM}" stroke-opacity=".7">{spokes}</g>{doses}
</g>
<circle cx="{cx}" cy="{cy}" r="5" fill="{PANEL}" stroke="{AMBER}"/>
<path d="M452 142H468L465 158H455Z" fill="{BASE}" stroke="{BORDER}"/>
<rect x="440" y="164" width="40" height="10" rx="2" fill="{BASE}" stroke="{BORDER}"/>
<circle cx="{cx}" r="3" fill="{AMBER}">
<animate attributeName="cy" values="146;146;169;169" keyTimes="0;.5;.8;1" dur="2s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.5;.85;1" dur="2s" repeatCount="indefinite"/>
</circle>
<circle class="pulse" cx="508" cy="92" r="2.5" fill="{GREEN}"/>
<text class="m" x="576" y="70" font-size="11" letter-spacing="1.5" fill="{MUTED}" text-anchor="end">NEXT DOSE · 08:00 · ×2</text>"""


def main():
    OUT.mkdir(exist_ok=True)
    header()
    card("orbit-orchard", 1, "PLAYABLE", GREEN, GREEN, art_orbit(), "orbit-orchard",
         "Gravity-slingshot puzzle game for the browser", "110 PLOTS · 5 WORLDS",
         ["JavaScript", "Firebase", "Generative audio"],
         "orbit-orchard: a seed curves around a sun toward a green soil planet")
    card("sigil-strike", 2, "PUBLIC", GREEN, AMBER, art_sigil(), "sigil-strike",
         "Two-player hand-sign fighter, read live from a webcam", "DSO WOS 2026",
         ["Python", "MediaPipe", "CNN", "PyInstaller"],
         "sigil-strike: two hand-landmark skeletons face off with detection labels")
    card("kuro", 3, "RESTRICTED", AMBER, AMBER, art_kuro(), "kuro",
         "Training-data platform for a 50+ TB multimodal corpus", "10M+ SAMPLES",
         ["Ray", "DuckDB", "PyArrow", "CLIP", "Streamlit"],
         "kuro: media is ingested, deduplicated, catalogued and exported as shards")
    card("pillbot", 4, "PUBLIC", GREEN, AMBER, art_pillbot(), "PillBot",
         "Android companion app for an automated pill dispenser", "NUS ORBITAL 2021",
         ["Java", "Android", "MySQL"],
         "PillBot: the app's pill grid syncs through MySQL to a dispenser carousel dropping a dose")


if __name__ == "__main__":
    main()
