#!/usr/bin/env python3
"""
YouTube Short Video Generator
Topic: Short-Form Content Optimization & Algorithmic Performance 2026
Resolution: 1080x1920 (9:16) | FPS: 30 | Duration: 60s
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy import VideoClip

# ── Constants ─────────────────────────────────────────────────────────────────
W, H   = 1080, 1920
FPS    = 30
DUR    = 60

F_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_REG  = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

BG     = (6,   6,  18)
PANEL  = (16, 16,  38)
RED    = (255, 55,  85)
BLUE   = (0,  210, 255)
GOLD   = (255, 205,  0)
GREEN  = (50,  245, 130)
PURPLE = (185,  80, 255)
WHITE  = (255, 255, 255)
GRAY   = (140, 140, 170)
DIM    = ( 40,  40,  75)

# ── Maths helpers ─────────────────────────────────────────────────────────────

def ease_out(t, d=1.0):
    x = min(1.0, max(0.0, t / d))
    return 1 - (1 - x) ** 3

def ease_io(t, d=1.0):
    x = min(1.0, max(0.0, t / d))
    return (1 - math.cos(math.pi * x)) / 2

def lerp(a, b, t): return a + (b - a) * t
def lc(c1, c2, t): return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))

def fade(t, start, d=0.45):
    return min(1.0, max(0.0, ease_out(max(0, t - start), d)))

def slide(t, start, from_x, to_x, d=0.45):
    p = ease_out(max(0, t - start), d)
    return int(lerp(from_x, to_x, p))

# ── Drawing helpers ───────────────────────────────────────────────────────────

def mk_img():
    return Image.new('RGB', (W, H), BG)

def gradient_bg(t):
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    shift = math.sin(t * 0.25) * 6
    for y in range(H):
        r = H - y
        arr[y, :, 0] = max(0, min(255, int(6  + r / H * 10 + shift)))
        arr[y, :, 1] = max(0, min(255, int(6  + r / H * 8)))
        arr[y, :, 2] = max(0, min(255, int(18 + r / H * 22 + shift * 1.5)))
    return Image.fromarray(arr)

def grid_lines(img, t):
    draw = ImageDraw.Draw(img)
    sp  = 80
    off = int(t * 18) % sp
    col = (28, 28, 68)
    for x in range(-sp, W + sp, sp):
        draw.line([(x + off, 0), (x + off, H)], fill=col, width=1)
    for y in range(-sp, H + sp, sp):
        draw.line([(0, y + off), (W, y + off)], fill=col, width=1)

def particles(img, t, n=22, seed=7):
    rng = np.random.RandomState(seed)
    pos = rng.rand(n, 2)
    spd = rng.rand(n) * 0.04 + 0.008
    sz  = rng.randint(2, 7, n)
    cols = [BLUE, RED, GOLD, GREEN, PURPLE]
    draw = ImageDraw.Draw(img)
    for i in range(n):
        x = int((pos[i, 0] + spd[i] * t * 0.08) % 1.0 * W)
        y = int((pos[i, 1] + spd[i] * t * 0.04) % 1.0 * H)
        c = cols[i % len(cols)]
        s = sz[i]
        draw.ellipse([x-s, y-s, x+s, y+s], fill=c)

def glow_txt(img, text, x, y, font, color, glow, glow_r=18, anchor="mm"):
    """Render text with a soft glow bloom."""
    gl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    for step in range(1, 4):
        a = 90 - step * 20
        for dx, dy in [(-step*2, 0), (step*2, 0), (0, -step*2), (0, step*2)]:
            gd.text((x + dx, y + dy), text, font=font, fill=(*glow, a), anchor=anchor)
    gl = gl.filter(ImageFilter.GaussianBlur(glow_r))
    base = img.convert('RGBA')
    base = Image.alpha_composite(base, gl)
    result = base.convert('RGB')
    ImageDraw.Draw(result).text((x, y), text, font=font, fill=color, anchor=anchor)
    return result

def panel(img, x1, y1, x2, y2, fill=PANEL, outline=BLUE, ow=2, r=22):
    ImageDraw.Draw(img).rounded_rectangle([x1, y1, x2, y2], radius=r,
        fill=fill, outline=(*outline, 160), width=ow)

def badge(img, x, y, label, color, font):
    d  = ImageDraw.Draw(img)
    bb = font.getbbox(label)
    w  = bb[2] - bb[0]
    d.rounded_rectangle([x, y - 30, x + w + 44, y + 44], radius=14, fill=color)
    d.text((x + 22, y + 7), label, font=font, fill=BG)

def dot_nav(img, current, total=6):
    d = ImageDraw.Draw(img)
    for i in range(total):
        c = WHITE if i == current else DIM
        r = 7 if i == current else 4
        cx = W // 2 + (i - total // 2) * 36
        d.ellipse([cx-r, H-58-r, cx+r, H-58+r], fill=c)

# ── Scene renderers ───────────────────────────────────────────────────────────

def s0_hook(img, t):
    """0–4 s  The 2-Second Rule hook"""
    d = ImageDraw.Draw(img)
    f36  = ImageFont.truetype(F_BOLD, 36)
    f90  = ImageFont.truetype(F_BOLD, 92)
    f130 = ImageFont.truetype(F_BOLD, 132)
    f44  = ImageFont.truetype(F_REG,  44)
    f38  = ImageFont.truetype(F_REG,  38)
    f42  = ImageFont.truetype(F_BOLD, 42)

    # Label pill
    a = fade(t, 0.0, 0.4)
    if a > 0:
        lbl = "YOUTUBE SHORTS  2026"
        bb = f36.getbbox(lbl); lw = bb[2]-bb[0]
        lx = W//2 - lw//2 - 20
        d.rounded_rectangle([lx, 118, lx+lw+40, 168], radius=24,
            fill=(*BLUE, int(a*35)), outline=(*BLUE, int(a*180)), width=2)
        d.text((W//2, 143), lbl, font=f36, fill=(*BLUE, int(a*255)), anchor="mm")

    # "THE" slides in from right
    a1 = fade(t, 0.15, 0.55)
    x1 = slide(t, 0.15, W+200, W//2, 0.55)
    if a1 > 0:
        img = glow_txt(img, "THE", x1, 490, f90, WHITE, BLUE, 18)

    # "2-SECOND" slides in from left  (big, red glow)
    a2 = fade(t, 0.3, 0.55)
    x2 = slide(t, 0.3, -W-200, W//2, 0.55)
    if a2 > 0:
        img = glow_txt(img, "2-SECOND", x2, 640, f130, RED, RED, 38)

    # "RULE" slides in from right
    a3 = fade(t, 0.45, 0.55)
    x3 = slide(t, 0.45, W+200, W//2, 0.55)
    if a3 > 0:
        img = glow_txt(img, "RULE", x3, 790, f90, WHITE, BLUE, 18)

    # Subtitle
    a4 = fade(t, 0.85, 0.55)
    if a4 > 0:
        d = ImageDraw.Draw(img)
        d.text((W//2, 910), "The metric that decides if your", font=f44,
               fill=(*GRAY, int(a4*240)), anchor="mm")
        d.text((W//2, 966), "Short goes viral or dies instantly", font=f44,
               fill=(*GRAY, int(a4*240)), anchor="mm")

    # Stat panel
    a5 = fade(t, 1.25, 0.55)
    if a5 > 0:
        py = 1055
        panel(img, 100, py, W-100, py+290, fill=(20,8,28), outline=RED, ow=3, r=30)
        f_stat = ImageFont.truetype(F_BOLD, 128)
        img = glow_txt(img, "<30%", W//2, py+108, f_stat, RED, RED, 40)
        d = ImageDraw.Draw(img)
        d.text((W//2, py+200), "Swipe-Away Rate threshold", font=f38,
               fill=(*WHITE, int(a5*220)), anchor="mm")
        d.text((W//2, py+252), "Above 50% = video is dead", font=f38,
               fill=(*GRAY, int(a5*180)), anchor="mm")

    # Bounce hint
    a6 = fade(t, 2.1, 0.5)
    if a6 > 0:
        bounce = int(8 * math.sin(t * 4))
        d = ImageDraw.Draw(img)
        d.text((W//2, 1455+bounce), "▼  The full framework ▼", font=f42,
               fill=(*BLUE, int(a6*195)), anchor="mm")

    dot_nav(img, 0)
    return img

def s1_algo(img, t):
    """4–15 s  Algorithm ranking signals"""
    lt = t - 4.0
    d  = ImageDraw.Draw(img)
    f62 = ImageFont.truetype(F_BOLD, 62)
    f38 = ImageFont.truetype(F_REG,  38)
    f32 = ImageFont.truetype(F_BOLD, 32)
    f68 = ImageFont.truetype(F_BOLD, 68)
    f28 = ImageFont.truetype(F_REG,  28)
    f36 = ImageFont.truetype(F_BOLD, 36)

    a_title = fade(lt, 0, 0.5)
    if a_title > 0:
        img = glow_txt(img, "ALGORITHM", W//2, 210, f62, BLUE,  BLUE, 20)
        img = glow_txt(img, "RANKING SIGNALS", W//2, 292, f62, WHITE, BLUE, 14)
        d = ImageDraw.Draw(img)
        d.text((W//2, 358), "2026 Priority Order — master all five",
               font=f38, fill=(*GOLD, int(a_title*220)), anchor="mm")

    metrics = [
        ("SWIPE-AWAY",  "<30%",  RED,    "First 2s — above 50% kills it"),
        ("AVG % VIEWED", ">70%", GREEN,  "Top performers hit 85%+"),
        ("RE-WATCH",    "∞",     BLUE,   "Loops maximise this signal"),
        ("EXT. SHARES", "5×",    GOLD,   "WhatsApp/DMs weighted 5x"),
        ("L/F CLICK-THR","↑↑",  PURPLE, "Boosts Shorts distribution"),
    ]

    bsy = 430
    bh  = 182
    bg  = 14

    for i, (label, val, col, desc) in enumerate(metrics):
        it = lt - i * 0.28
        ai = fade(it, 0.5, 0.4)
        xi = slide(it, 0.5, W+280, 80, 0.42)
        if ai > 0:
            y  = bsy + i * (bh + bg)
            pw = W - 160
            px = xi
            panel(img, px, y, px+pw, y+bh, fill=(14,14,38), outline=col, ow=2, r=20)
            # accent bar
            ImageDraw.Draw(img).rounded_rectangle(
                [px, y, px+10, y+bh], radius=8, fill=col)

            d = ImageDraw.Draw(img)
            d.text((px+32, y+32), label, font=f32, fill=(*GRAY, int(ai*220)))
            img = glow_txt(img, val, px+32, y+115, f68, col, col, 14, anchor="lm")
            d = ImageDraw.Draw(img)
            d.text((px+pw-18, y+115), desc, font=f28,
                   fill=(*GRAY, int(ai*185)), anchor="rm")

    a_foot = fade(lt, 3.6, 0.5)
    if a_foot > 0:
        d = ImageDraw.Draw(img)
        d.text((W//2, 1822), "Master these → viral growth",
               font=f36, fill=(*BLUE, int(a_foot*200)), anchor="mm")

    dot_nav(img, 1)
    return img

def s2_hrr(img, t):
    """15–28 s  Hook-Retain-Reward framework"""
    lt   = t - 15.0
    f60  = ImageFont.truetype(F_BOLD, 60)
    f50  = ImageFont.truetype(F_BOLD, 50)
    f44  = ImageFont.truetype(F_BOLD, 44)
    f36  = ImageFont.truetype(F_REG,  36)
    f32  = ImageFont.truetype(F_BOLD, 32)

    a_title = fade(lt, 0, 0.5)
    if a_title > 0:
        img = glow_txt(img, "THE WINNING FRAMEWORK", W//2, 200, f60, WHITE, BLUE, 16)
        img = glow_txt(img, "Hook  ·  Retain  ·  Reward", W//2, 278, f50, BLUE, BLUE, 22)

    phases = [
        {
            "title": "HOOK",
            "time":  "0:00–0:03",
            "col":   RED,
            "pts":   ["Competence — show your skill",
                      "Connection — shared pain point",
                      "Curiosity — counterintuitive claim"],
            "py":    360,
        },
        {
            "title": "RETAIN",
            "time":  "0:03–0:55",
            "col":   BLUE,
            "pts":   ["Lists, steps, or narrative stories",
                      "Visual evidence beats verbal claims",
                      "Recent proof > dated proof"],
            "py":    790,
        },
        {
            "title": "REWARD",
            "time":  "0:55–End",
            "col":   GOLD,
            "pts":   ["Final value payoff for the viewer",
                      "OR seamless loop (remove end cues)",
                      "Leave them wanting one more watch"],
            "py":    1220,
        },
    ]

    for i, ph in enumerate(phases):
        pt = lt - i * 0.65
        ap = fade(pt, 0.3, 0.5)
        xp = slide(pt, 0.3, -W-180, 60, 0.5)
        if ap > 0:
            px = xp; py = ph["py"]; col = ph["col"]
            pw = W - 120

            panel(img, px, py, px+pw, py+390, fill=(14,14,38), outline=col, ow=3, r=26)

            # badge
            bb = f44.getbbox(ph["title"]); tw = bb[2]-bb[0]
            ImageDraw.Draw(img).rounded_rectangle(
                [px+18, py-32, px+18+tw+46, py+38], radius=14, fill=col)
            ImageDraw.Draw(img).text((px+42, py+4), ph["title"], font=f44, fill=BG)

            # time
            ImageDraw.Draw(img).text((px+pw-20, py+18), ph["time"],
                font=f36, fill=(*col, int(ap*200)), anchor="rm")

            for j, pt_txt in enumerate(ph["pts"]):
                pa = fade(pt, 0.55 + j * 0.18, 0.38)
                if pa > 0:
                    dot_y = py + 75 + j * 102
                    d = ImageDraw.Draw(img)
                    d.ellipse([px+28, dot_y+10, px+46, dot_y+28], fill=col)
                    d.text((px+60, dot_y+2), pt_txt, font=f36,
                           fill=(*WHITE, int(pa*220)))

    dot_nav(img, 2)
    return img

def s3_loop(img, t):
    """28–40 s  Infinite Loop technique"""
    lt  = t - 28.0
    f68 = ImageFont.truetype(F_BOLD, 68)
    f36 = ImageFont.truetype(F_REG,  36)
    f34 = ImageFont.truetype(F_REG,  34)
    f44 = ImageFont.truetype(F_BOLD, 44)
    f80 = ImageFont.truetype(F_BOLD, 80)

    a_title = fade(lt, 0, 0.5)
    if a_title > 0:
        img = glow_txt(img, "THE INFINITE", W//2, 198, f68, WHITE,  PURPLE, 15)
        img = glow_txt(img, "LOOP SECRET",  W//2, 282, f68, PURPLE, PURPLE, 28)

    # Circular loop visualisation
    a_circ = fade(lt, 0.4, 0.8)
    if a_circ > 0:
        cx, cy = W//2, 660
        r = 195
        prog = min(1.0, ease_out(max(0, lt - 0.4), 1.8))
        max_deg = int(prog * 340)
        d = ImageDraw.Draw(img)
        for deg in range(0, max_deg, 4):
            angle = math.radians(deg - 90)
            x = cx + int(r * math.cos(angle))
            y = cy + int(r * math.sin(angle))
            intensity = int(180 * a_circ)
            # Gradient colour along arc
            blend = deg / 340.0
            col = lc(BLUE, PURPLE, blend)
            d.ellipse([x-9, y-9, x+9, y+9], fill=(*col, intensity))

        # Rotating arrow head
        if lt > 2.3:
            spin = ((lt - 2.3) * 55) % 360
            ha   = math.radians(spin - 90)
            hx   = cx + int(r * math.cos(ha))
            hy   = cy + int(r * math.sin(ha))
            img  = glow_txt(img, "▶", hx, hy, ImageFont.truetype(F_BOLD, 48),
                            PURPLE, PURPLE, 22)

        # Centre infinity
        img = glow_txt(img, "∞", cx, cy - 10, f80, PURPLE, PURPLE, 35)
        d = ImageDraw.Draw(img)
        d.text((cx, cy+60), "REWATCH  LOOP", font=f36, fill=GRAY, anchor="mm")

    # Script example panel
    a_sc = fade(lt, 2.1, 0.6)
    if a_sc > 0:
        py = 900
        panel(img, 60, py, W-60, py+340, fill=(20,8,40), outline=PURPLE, ow=2, r=26)
        d = ImageDraw.Draw(img)
        d.text((W//2, py+36), "THE SEAMLESS SENTENCE", font=f44,
               fill=(*PURPLE, int(a_sc*220)), anchor="mm")
        lines = [
            '"...the only way to do this',
            'is by using..."  →  loops back  →',
            '"...this specific setting that..."',
        ]
        for i, ln in enumerate(lines):
            la = fade(lt, 2.3 + i*0.2, 0.35)
            if la > 0:
                d = ImageDraw.Draw(img)
                d.text((W//2, py+112+i*82), ln, font=f34,
                       fill=(*WHITE, int(la*210)), anchor="mm")

    # Dos & Don'ts
    a_tips = fade(lt, 3.4, 0.5)
    tips = [
        ("✗  Never say 'Thanks for watching'", RED),
        ("✗  Remove all end-signal phrases",    RED),
        ("✓  Match first & last frame visually", GREEN),
    ]
    if a_tips > 0:
        for i, (tip, col) in enumerate(tips):
            ta = fade(lt, 3.4+i*0.2, 0.38)
            d  = ImageDraw.Draw(img)
            d.text((W//2, 1368+i*92), tip, font=f36,
                   fill=(*col, int(ta*225)), anchor="mm")

    dot_nav(img, 3)
    return img

def s4_ai(img, t):
    """40–52 s  AI Production Workflow"""
    lt  = t - 40.0
    f68 = ImageFont.truetype(F_BOLD, 68)
    f42 = ImageFont.truetype(F_REG,  42)
    f36 = ImageFont.truetype(F_REG,  36)
    f46 = ImageFont.truetype(F_BOLD, 46)
    f34 = ImageFont.truetype(F_REG,  34)
    f110= ImageFont.truetype(F_BOLD, 110)
    f40 = ImageFont.truetype(F_BOLD, 40)

    a_title = fade(lt, 0, 0.5)
    if a_title > 0:
        img = glow_txt(img, "AI-POWERED", W//2, 198, f68, GOLD,  GOLD,  28)
        img = glow_txt(img, "WORKFLOW",   W//2, 282, f68, WHITE, GOLD,  14)

    a_spd = fade(lt, 0.4, 0.5)
    if a_spd > 0:
        img = glow_txt(img, "10–15", W//2, 488, f110, GOLD, GOLD, 38)
        d = ImageDraw.Draw(img)
        d.text((W//2, 574), "clips per hour — zero filming", font=f42,
               fill=(*WHITE, int(a_spd*225)), anchor="mm")

    tools = [
        ("Opus Clip",    "Repurpose long-form VODs → viral clips", BLUE),
        ("Vizard",       "Auto-caption & smart reframe to 9:16",   GREEN),
        ("Argil",        "AI clone scripts — no camera needed",    RED),
        ("StreamLadder", "Merge streams + auto vertical crop",     PURPLE),
    ]

    tsy = 650; th = 172; tg = 14
    for i, (name, desc, col) in enumerate(tools):
        it = lt - i * 0.32
        ai = fade(it, 0.85, 0.42)
        xi = slide(it, 0.85, W+240, 60, 0.42)
        if ai > 0:
            tx = xi; ty = tsy + i*(th+tg); pw = W-120
            panel(img, tx, ty, tx+pw, ty+th, fill=(14,14,38), outline=col, ow=2, r=20)
            ImageDraw.Draw(img).rounded_rectangle(
                [tx, ty, tx+12, ty+th], radius=8, fill=col)
            img = glow_txt(img, name, tx+36, ty+48, f46, col, col, 12, anchor="lm")
            d   = ImageDraw.Draw(img)
            d.text((tx+36, ty+108), desc, font=f34, fill=(*GRAY, int(ai*205)))

    a_foot = fade(lt, 3.8, 0.5)
    if a_foot > 0:
        d = ImageDraw.Draw(img)
        d.text((W//2, 1822), "Scale your output — kill the burnout",
               font=f40, fill=(*GOLD, int(a_foot*200)), anchor="mm")

    dot_nav(img, 4)
    return img

def s5_growth(img, t):
    """52–60 s  Growth Formula + loop-back"""
    lt  = t - 52.0
    f70 = ImageFont.truetype(F_BOLD, 70)
    f120= ImageFont.truetype(F_BOLD, 120)
    f40 = ImageFont.truetype(F_REG,  40)
    f44 = ImageFont.truetype(F_BOLD, 44)
    f48 = ImageFont.truetype(F_BOLD, 48)
    f34 = ImageFont.truetype(F_REG,  34)
    f52 = ImageFont.truetype(F_BOLD, 52)
    f42 = ImageFont.truetype(F_BOLD, 42)

    a_title = fade(lt, 0, 0.5)
    if a_title > 0:
        img = glow_txt(img, "THE GROWTH", W//2, 198, f70, GREEN, GREEN, 28)
        img = glow_txt(img, "FORMULA",    W//2, 285, f70, WHITE, GREEN, 14)

    # Posting cadence panel
    a_post = fade(lt, 0.4, 0.5)
    if a_post > 0:
        py = 368
        panel(img, 60, py, W-60, py+262, fill=(8,28,16), outline=GREEN, ow=2, r=26)
        img = glow_txt(img, "3–7", W//2, py+110, f120, GREEN, GREEN, 38)
        d   = ImageDraw.Draw(img)
        d.text((W//2, py+205), "Shorts per week  (optimal cadence)", font=f40,
               fill=(*WHITE, int(a_post*225)), anchor="mm")

    # Monetisation header
    a_mono = fade(lt, 1.2, 0.5)
    if a_mono > 0:
        d = ImageDraw.Draw(img)
        d.text((W//2, 710), "MONETISATION PATHS  (YPP 2026)", font=f44,
               fill=(*GOLD, int(a_mono*220)), anchor="mm")

    paths = [
        ("Path A", "1K subs  +  10M Shorts views (90 days)", BLUE),
        ("Path B", "1K subs  +  4K long-form watch hours",   RED),
    ]
    for i, (path, desc, col) in enumerate(paths):
        pt = lt - i * 0.42
        ap = fade(pt, 1.65, 0.42)
        xp = slide(pt, 1.65, -W-200, 60, 0.42)
        if ap > 0:
            px = xp; py = 780 + i*215; pw = W-120
            panel(img, px, py, px+pw, py+188, fill=(14,14,38), outline=col, ow=2, r=20)
            ImageDraw.Draw(img).rounded_rectangle(
                [px, py, px+12, py+188], radius=8, fill=col)
            img = glow_txt(img, path, px+36, py+55, f48, col, col, 12, anchor="lm")
            d   = ImageDraw.Draw(img)
            d.text((px+36, py+128), desc, font=f34, fill=(*GRAY, int(ap*205)))

    # Revenue share
    a_rev = fade(lt, 3.1, 0.5)
    if a_rev > 0:
        py = 1252
        panel(img, 60, py, W-60, py+148, fill=(28,22,4), outline=GOLD, ow=2, r=20)
        img = glow_txt(img, "45 % Revenue Share  (YPP)", W//2, py+74, f52,
                       GOLD, GOLD, 22)

    # Loop-back CTA (bouncing)
    a_cta = fade(lt, 4.6, 0.6)
    if a_cta > 0:
        pulse   = 0.72 + 0.28 * math.sin(lt * 5)
        bounce  = int(10 * math.sin(lt * 3.8))
        d       = ImageDraw.Draw(img)
        d.text((W//2, 1472+bounce), "↑  Now apply the 2-Second Rule  ↑",
               font=f42, fill=(*BLUE, int(a_cta * pulse * 215)), anchor="mm")

    dot_nav(img, 5)
    return img

# ── Frame router ──────────────────────────────────────────────────────────────

SCENE_CUTS = [0, 4, 15, 28, 40, 52, 60]

def make_frame(t):
    img = gradient_bg(t)
    grid_lines(img, t)

    # dispatch
    if   t < SCENE_CUTS[1]: img = s0_hook(img, t)
    elif t < SCENE_CUTS[2]: img = s1_algo(img, t)
    elif t < SCENE_CUTS[3]: img = s2_hrr(img, t)
    elif t < SCENE_CUTS[4]: img = s3_loop(img, t)
    elif t < SCENE_CUTS[5]: img = s4_ai(img, t)
    else:                    img = s5_growth(img, t)

    particles(img, t)
    return np.array(img)

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    out = "/home/user/KirkStore/youtube_short_2026.mp4"
    print(f"Rendering {W}x{H} @ {FPS}fps — {DUR}s  →  {out}")
    clip = VideoClip(make_frame, duration=DUR)
    clip.write_videofile(
        out, fps=FPS, codec="libx264", audio=False,
        logger="bar", preset="fast",
        ffmpeg_params=["-crf", "22", "-pix_fmt", "yuv420p"],
    )
    print("\nDone.")
