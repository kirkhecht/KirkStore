#!/usr/bin/env python3
"""
Food YouTube Short — "SMASH BURGER SECRETS"
15 seconds | 1080×1920 | 30fps | Seamless Infinite Loop
"""

import math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy import VideoClip

W, H  = 1080, 1920
FPS   = 30
DUR   = 15.0   # perfect loop period

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# ── Maths ─────────────────────────────────────────────────────────────────────
def ease_out(t, d=1.0):
    x = min(1.0, max(0.0, t/d));  return 1-(1-x)**3

def lerp(a,b,t): return a+(b-a)*t
def lc(c1,c2,t): return tuple(int(lerp(a,b,max(0,min(1,t)))) for a,b in zip(c1,c2))

def scene_alpha(tn, s_start, s_end, fade=0.06):
    """Alpha for a scene window given tn∈[0,1)."""
    fade_in  = ease_out(max(0, tn - s_start) / fade)
    fade_out = ease_out(max(0, s_end - tn)  / fade)
    return min(fade_in, fade_out) if tn < s_end else ease_out(max(0, s_end+fade - tn) / fade)

# ── Background ────────────────────────────────────────────────────────────────

def warm_bg():
    arr = np.zeros((H,W,3), dtype=np.uint8)
    for y in range(H):
        r = y/H
        arr[y,:,0] = int(10 + r*6)
        arr[y,:,1] = int(5  + r*3)
        arr[y,:,2] = int(2  + r*2)
    return Image.fromarray(arr)

def add_bokeh(img, tn):
    """Soft out-of-focus warm light orbs — food photography feel."""
    rng = np.random.RandomState(42)
    orbs = [
        # (base_x, base_y, radius, color, speed, phase)
        (260,  480, 320, (255,120,30),  0.18, 0.00),
        (820,  350, 260, (255,165,50),  0.12, 0.33),
        (150, 1100, 200, (200, 80,20),  0.22, 0.66),
        (900,  900, 280, (255,140,40),  0.15, 0.12),
        (540,  200, 180, (255,200,80),  0.08, 0.50),
        (400, 1500, 240, (180, 60,10),  0.20, 0.80),
        (720, 1400, 200, (255,110,20),  0.14, 0.25),
    ]
    bokeh_layer = Image.new('RGBA', (W,H), (0,0,0,0))
    bd = ImageDraw.Draw(bokeh_layer)
    for bx, by, br, bc, spd, ph in orbs:
        angle = 2 * math.pi * ((tn * spd + ph) % 1.0)
        ox = int(bx + math.cos(angle) * br * 0.25)
        oy = int(by + math.sin(angle) * br * 0.18)
        r = br
        for step in range(4):
            a = int(22 - step * 5)
            rr = r - step * r//5
            bd.ellipse([ox-rr, oy-rr, ox+rr, oy+rr], fill=(*bc, a))
    bokeh_blur = bokeh_layer.filter(ImageFilter.GaussianBlur(90))
    base = img.convert('RGBA')
    result = Image.alpha_composite(base, bokeh_blur)
    img.paste(result.convert('RGB'))

def add_vignette(img):
    vg = Image.new('RGBA', (W,H), (0,0,0,0))
    vd = ImageDraw.Draw(vg)
    for step in range(12):
        margin = step * 48
        alpha  = int(38 - step * 3)
        if alpha <= 0: break
        vd.rounded_rectangle([margin, margin, W-margin, H-margin],
                              radius=margin//2+1, outline=(0,0,0,alpha), width=48)
    vg_blur = vg.filter(ImageFilter.GaussianBlur(30))
    base = img.convert('RGBA')
    result = Image.alpha_composite(base, vg_blur)
    img.paste(result.convert('RGB'))

def add_film_grain(img, intensity=18):
    rng  = np.random.RandomState(None)
    arr  = np.array(img).astype(np.int16)
    noise = rng.randint(-intensity, intensity, arr.shape, dtype=np.int16)
    arr  = np.clip(arr + noise, 0, 255).astype(np.uint8)
    img.paste(Image.fromarray(arr))

def add_cinematic_bars(img, bar_h=72):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, bar_h],      fill=(0,0,0))
    d.rectangle([0, H-bar_h, W, H],    fill=(0,0,0))

# ── Burger drawing ────────────────────────────────────────────────────────────

def draw_burger(img, tn):
    """Layered photorealistic burger cross-section."""
    d  = ImageDraw.Draw(img)
    cx = W // 2
    cy = H // 2 + 80   # slightly below centre

    # Gentle floating
    hover   = int(14 * math.sin(2 * math.pi * tn))
    # Cheese drip cycles twice per loop
    drip_t  = (math.sin(2 * math.pi * tn * 2) + 1) / 2   # 0→1→0→1→0
    drip_px = int(drip_t * 72)

    # ── Drop shadow ──────────────────────────────────────────────────────────
    for shadow_step in range(6):
        sa = 20 - shadow_step * 3
        sr = 8 + shadow_step * 12
        d.ellipse([cx-220+sr//2, cy+370+hover+shadow_step*8,
                   cx+220-sr//2, cy+418+hover+shadow_step*8],
                  fill=(0, 0, 0, sa) if False else (0,0,0))

    # ── Bottom bun ───────────────────────────────────────────────────────────
    by = cy + 305 + hover
    # Shadow
    d.ellipse([cx-215, by+82, cx+215, by+118], fill=(3,1,0))
    # Main bun body — three layers for gradient
    d.ellipse([cx-208, by,    cx+208, by+95 ], fill=(148,62,18))
    d.ellipse([cx-198, by+5,  cx+198, by+88 ], fill=(168,74,22))
    d.ellipse([cx-188, by+10, cx+188, by+80 ], fill=(182,84,26))
    # Highlight stripe
    d.ellipse([cx-130, by+10, cx+90,  by+38 ], fill=(210,108,40))
    d.ellipse([cx-80,  by+14, cx+28,  by+28 ], fill=(228,132,60))
    # Sesame seeds bottom bun (4 seeds)
    for sx, sy in [(cx-62,by+22),(cx+48,by+18),(cx-8,by+14),(cx+100,by+28)]:
        d.ellipse([sx-11,sy-5,sx+11,sy+5], fill=(202,160,80))
        d.ellipse([sx-5, sy-2,sx+2, sy+1], fill=(228,195,120))

    # ── Lettuce ──────────────────────────────────────────────────────────────
    ly = by - 38
    ruffle_offsets = [(0,0,188),(28,-6,168),(-32,-4,178),(55,5,158),(-58,3,162),
                      (75,-8,148),(-78,-2,152),(88,8,138),(-90,4,145)]
    for rx,ry,green in ruffle_offsets:
        d.ellipse([cx-200+rx, ly+ry, cx+200+rx, ly+48+ry],
                  fill=(22, green//2+30, 18))
    # Bright edge highlights
    for rx,ry,green in ruffle_offsets[:5]:
        d.ellipse([cx-185+rx, ly+ry,   cx-170+rx, ly+12+ry], fill=(50,155,35))
        d.ellipse([cx+162+rx, ly+ry+2, cx+185+rx, ly+14+ry], fill=(45,148,30))

    # ── Beef patty ───────────────────────────────────────────────────────────
    py = by - 95
    # Outer crust (very dark)
    d.ellipse([cx-202, py,    cx+202, py+74], fill=(22, 8, 3))
    # Inner meat
    d.ellipse([cx-188, py+7,  cx+188, py+64], fill=(48,18, 6))
    d.ellipse([cx-175, py+12, cx+175, py+58], fill=(55,22, 8))
    # Juicy pockets
    for jx,jy,jr in [(cx-85,py+22,22),(cx+38,py+28,18),(cx-15,py+40,16),(cx+105,py+20,14)]:
        d.ellipse([jx-jr,jy-jr//2,jx+jr,jy+jr//2], fill=(72,30,10))
    # Sear grid marks
    for i in range(4):
        sx = cx - 120 + i*80
        d.line([(sx-25,py+14),(sx+18,py+60)], fill=(12,4,1), width=10)
        d.line([(sx-20,py+14),(sx+12,py+60)], fill=(16,6,2), width=5)
    for i in range(3):
        sx = cx - 80 + i*80
        d.line([(sx-18,py+14),(sx+22,py+60)], fill=(14,5,1), width=7)
    # Maillard crust edge
    d.arc([cx-202,py,cx+202,py+74], start=0, end=180, fill=(15,5,1), width=12)

    # ── Cheese ───────────────────────────────────────────────────────────────
    chy = py - 28
    # Cheese body
    d.ellipse([cx-222, chy,    cx+222, chy+38], fill=(255,192,12))
    d.ellipse([cx-215, chy+2,  cx+215, chy+32], fill=(255,205,25))
    # Cheese highlight
    d.ellipse([cx-150, chy+4,  cx+50,  chy+16], fill=(255,228,80))
    # Drips (animated)
    drip_positions = [cx-148, cx-55, cx+52, cx+148]
    for i, dx in enumerate(drip_positions):
        offset = int(drip_px * (0.7 + i*0.12))
        # Drip body
        pts = [dx-14, chy+30, dx+14, chy+30,
               dx+9,  chy+30+offset,
               dx,    chy+44+offset,
               dx-9,  chy+30+offset]
        d.polygon(pts, fill=(255,188,8))
        # Drip tip highlight
        if offset > 15:
            d.ellipse([dx-5, chy+46+offset, dx+5, chy+54+offset],
                      fill=(255,215,50))

    # ── Sauce ────────────────────────────────────────────────────────────────
    # Red sauce drips along cheese edge — subtle
    for sx in [cx-180, cx-60, cx+70, cx+175]:
        sauce_len = int(22 + 10 * math.sin(2*math.pi*tn + sx*0.01))
        d.ellipse([sx-8, chy+32, sx+8, chy+32+sauce_len], fill=(185,25,15))
        d.ellipse([sx-4, chy+28, sx+4, chy+32],           fill=(200,35,20))

    # ── Top bun ──────────────────────────────────────────────────────────────
    ty = cy - 330 + hover
    # Dome shadow underneath
    d.ellipse([cx-215, ty+185, cx+215, ty+220], fill=(3,1,0))
    # Dome — 6 layers, darkest at bottom
    bun_layers = [
        (0,   168,78,20, 210),
        (1,   178,82,22, 200),
        (2,   188,88,24, 190),
        (3,   196,96,27, 178),
        (4,   205,105,30,162),
        (5,   215,115,35,145),
    ]
    for layer, r, g, b, layer_h in bun_layers:
        m = layer * 9
        d.ellipse([cx-210+m, ty+layer*10, cx+210-m, ty+layer_h], fill=(r,g,b))
    # Crown highlight (golden)
    d.ellipse([cx-140, ty+10, cx+60,  ty+65 ], fill=(225,145,52))
    d.ellipse([cx-90,  ty+15, cx+10,  ty+42 ], fill=(242,170,72))
    # Specular
    d.ellipse([cx-55,  ty+18, cx-5,   ty+32 ], fill=(255,205,115))
    # Sesame seeds — scattered on crown
    seeds = [(cx-90,ty+52,14,5),(cx+25,ty+42,13,5),(cx-20,ty+35,12,5),
             (cx+80,ty+58,13,5),(cx-130,ty+68,12,4),(cx+118,ty+65,11,4),
             (cx+52, ty+75,12,5),(cx-55, ty+80,13,5),(cx+8,  ty+80,11,4),
             (cx-165,ty+90,10,4),(cx+155,ty+88,10,4)]
    for sx,sy,sw,sh in seeds:
        d.ellipse([sx-sw,sy-sh,sx+sw,sy+sh], fill=(205,158,78))
        d.ellipse([sx-sw//2,sy-sh//2,sx,sy+sh//4], fill=(230,192,115))

    return img

# ── Steam wisps ───────────────────────────────────────────────────────────────

def add_steam(img, tn):
    steam_layer = Image.new('RGBA', (W,H), (0,0,0,0))
    sd = ImageDraw.Draw(steam_layer)
    cx = W // 2
    steam_sources = [cx-95, cx, cx+95]
    for i, sx in enumerate(steam_sources):
        phase = tn + i * 0.33
        for j in range(8):
            t_wsp = (phase + j * 0.125) % 1.0
            y     = int(H//2 - 330 - t_wsp * 340)
            x_off = int(28 * math.sin(t_wsp * math.pi * 3.5 + i * 1.1))
            alpha = int(80 * math.sin(t_wsp * math.pi))
            r     = max(1, int(8 + t_wsp * 22))
            if alpha > 4:
                sd.ellipse([sx+x_off-r, y-r, sx+x_off+r, y+r],
                           fill=(235, 210, 185, alpha))
    steam_blur = steam_layer.filter(ImageFilter.GaussianBlur(6))
    base = img.convert('RGBA')
    result = Image.alpha_composite(base, steam_blur)
    img.paste(result.convert('RGB'))

# ── Text & scene overlays ─────────────────────────────────────────────────────

def glow_text(img, text, x, y, font, color, glow_col, glow_r=22, anchor="mm"):
    gl = Image.new('RGBA', (W,H), (0,0,0,0))
    gd = ImageDraw.Draw(gl)
    for step in range(1, 5):
        a = max(0, 100 - step * 20)
        for dx, dy in [(-step*2,0),(step*2,0),(0,-step*2),(0,step*2),
                       (-step,  -step),(step,-step),(-step,step),(step,step)]:
            gd.text((x+dx, y+dy), text, font=font, fill=(*glow_col, a), anchor=anchor)
    gl = gl.filter(ImageFilter.GaussianBlur(glow_r))
    base   = img.convert('RGBA')
    merged = Image.alpha_composite(base, gl).convert('RGB')
    ImageDraw.Draw(merged).text((x, y), text, font=font, fill=color, anchor=anchor)
    img.paste(merged)

def tag_pill(img, text, cx, y, font, text_col, bg_col, border_col):
    d  = ImageDraw.Draw(img)
    bb = font.getbbox(text)
    tw = bb[2]-bb[0]; th = bb[3]-bb[1]
    px, py = 26, 14
    d.rounded_rectangle([cx-tw//2-px, y-py, cx+tw//2+px, y+th+py],
                         radius=40, fill=(*bg_col,200), outline=border_col, width=2)
    d.text((cx, y+th//2+2), text, font=font, fill=text_col, anchor="mm")

def alpha_paste(img, overlay_img, alpha):
    """Blend overlay_img (RGB) onto img with given alpha 0-1."""
    if alpha <= 0: return
    if alpha >= 1:
        img.paste(overlay_img); return
    blend = Image.blend(img, overlay_img, alpha)
    img.paste(blend)

def scene_overlays(img, tn):
    """Text scenes keyed to tn ∈ [0,1)."""

    f80  = ImageFont.truetype(FB, 80)
    f100 = ImageFont.truetype(FB, 100)
    f120 = ImageFont.truetype(FB, 120)
    f44  = ImageFont.truetype(FB, 44)
    f38  = ImageFont.truetype(FR, 38)
    f36  = ImageFont.truetype(FB, 36)
    f32  = ImageFont.truetype(FR, 32)
    f28  = ImageFont.truetype(FR, 28)

    cx   = W // 2
    WHITE  = (255,255,255)
    CREAM  = (255,245,215)
    AMBER  = (255,172,40)
    RED    = (220,55,35)
    GOLD   = (255,200,20)
    GRAY   = (190,172,148)

    # ── Scene 0: Hook  (tn 0.00 – 0.22) ─────────────────────────────────────
    # "The SMASH BURGER secret nobody tells you"
    if tn < 0.22:
        # fade in 0-0.05, hold, fade out 0.18-0.22
        a = ease_out(tn / 0.05) if tn < 0.05 else (
            ease_out((0.22 - tn) / 0.04) if tn > 0.18 else 1.0)
        if a > 0.02:
            # Top eyebrow
            tag_layer = img.copy()
            tag_font  = ImageFont.truetype(FB, 34)
            tag_pill(tag_layer, "  FOOD HACK  ", cx, 138,
                     tag_font, (8,4,2), (255,172,40), (255,172,40))
            alpha_paste(img, tag_layer, a)

            # Main hook text
            txt_layer = img.copy()
            glow_text(txt_layer, "SMASH", cx, H//2+360, f120, WHITE, AMBER, 30)
            glow_text(txt_layer, "BURGER", cx, H//2+475, f120, AMBER, AMBER, 38)
            alpha_paste(img, txt_layer, a)

            # Sub
            sub_layer = img.copy()
            glow_text(sub_layer, "secrets nobody tells you", cx, H//2+565, f44, CREAM, AMBER, 14)
            alpha_paste(img, sub_layer, a)

    # ── Scene 1: The secret ingredient reveal  (tn 0.20 – 0.48) ─────────────
    if 0.20 < tn < 0.48:
        a = ease_out((tn-0.20)/0.05) if tn < 0.25 else (
            ease_out((0.48-tn)/0.04) if tn > 0.44 else 1.0)
        if a > 0.02:
            # "SECRET #1" tag
            tl = img.copy()
            glow_text(tl, "SECRET #1", cx, H//2+335, f80, RED, RED, 22)
            alpha_paste(img, tl, a)
            # Fact
            fl = img.copy()
            glow_text(fl, "Butter + Mayo smash sauce", cx, H//2+425, f44, CREAM, AMBER, 14)
            glow_text(fl, "= 5× more caramelisation", cx, H//2+485, f44, GOLD,  AMBER, 18)
            alpha_paste(img, fl, a)
            # Micro tip
            ml = img.copy()
            d = ImageDraw.Draw(ml)
            d.text((cx, H//2+548), "press hard — within first 30 seconds of contact",
                   font=f28, fill=(*GRAY, int(a*200)), anchor="mm")
            alpha_paste(img, ml, a)

    # ── Scene 2: The cheese pull secret  (tn 0.46 – 0.72) ───────────────────
    if 0.46 < tn < 0.72:
        a = ease_out((tn-0.46)/0.05) if tn < 0.51 else (
            ease_out((0.72-tn)/0.04) if tn > 0.68 else 1.0)
        if a > 0.02:
            tl = img.copy()
            glow_text(tl, "SECRET #2", cx, H//2+335, f80, AMBER, AMBER, 22)
            alpha_paste(img, tl, a)
            fl = img.copy()
            glow_text(fl, "Double-stack your American", cx, H//2+418, f44, CREAM, AMBER, 14)
            glow_text(fl, "cheese — while still hot", cx, H//2+475, f44, GOLD,  AMBER, 18)
            alpha_paste(img, fl, a)
            ml = img.copy()
            d = ImageDraw.Draw(ml)
            d.text((cx, H//2+540), "cover 30 sec · it steam-melts perfectly",
                   font=f28, fill=(*GRAY, int(a*200)), anchor="mm")
            alpha_paste(img, ml, a)

    # ── Scene 3: The bun toast  (tn 0.70 – 0.90) ─────────────────────────────
    if 0.70 < tn < 0.90:
        a = ease_out((tn-0.70)/0.05) if tn < 0.75 else (
            ease_out((0.90-tn)/0.05) if tn > 0.85 else 1.0)
        if a > 0.02:
            tl = img.copy()
            glow_text(tl, "SECRET #3", cx, H//2+335, f80, (50,220,120), (50,220,120), 22)
            alpha_paste(img, tl, a)
            fl = img.copy()
            glow_text(fl, "Toast bun in beef tallow",  cx, H//2+418, f44, CREAM, AMBER, 14)
            glow_text(fl, "not butter — 180 °C, 45s",  cx, H//2+475, f44, GOLD,  AMBER, 18)
            alpha_paste(img, fl, a)
            ml = img.copy()
            d = ImageDraw.Draw(ml)
            d.text((cx, H//2+540), "golden, crisp — holds the sauce",
                   font=f28, fill=(*GRAY, int(a*200)), anchor="mm")
            alpha_paste(img, ml, a)

    # ── Scene 4: CTA / loop-back  (tn 0.88 – 1.00) ───────────────────────────
    if tn > 0.88:
        a = ease_out((tn-0.88)/0.05) if tn < 0.93 else (
            ease_out((1.0-tn)/0.04)  if tn > 0.96 else 1.0)
        if a > 0.02:
            tl = img.copy()
            glow_text(tl, "NOW MAKE IT", cx, H//2+360, f100, WHITE, AMBER, 28)
            alpha_paste(img, tl, a)
            ctl = img.copy()
            bounce = int(8 * math.sin(tn * math.pi * 2 * 8))
            glow_text(ctl, "↑  watch the smash again  ↑",
                      cx, H//2+470+bounce, f44, AMBER, AMBER, 18)
            alpha_paste(img, ctl, a)

    # ── Persistent bottom caption bar ─────────────────────────────────────────
    cap_layer = img.copy()
    d = ImageDraw.Draw(cap_layer)
    # Gradient-like dark strip
    for strip_y in range(H-145, H-72):
        fade_a = int(180 * (strip_y - (H-145)) / 73)
        d.rectangle([0, strip_y, W, strip_y+1], fill=(0,0,0))
    d.text((cx, H-100), "#SmashBurger  #FoodTok  #BurgerSecrets",
           font=f28, fill=(185,160,130), anchor="mm")
    img.paste(cap_layer)

# ── Frame renderer ─────────────────────────────────────────────────────────────

def make_frame(t):
    tn  = (t % DUR) / DUR     # normalised loop time, always [0, 1)

    img = warm_bg()
    add_bokeh(img, tn)
    add_vignette(img)
    draw_burger(img, tn)
    add_steam(img, tn)
    scene_overlays(img, tn)
    add_film_grain(img, 14)
    add_cinematic_bars(img)

    return np.array(img)

# ── Entry ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    out = "/home/user/KirkStore/food_short_smashburger.mp4"
    print(f"Rendering {W}×{H} @ {FPS}fps | {DUR}s seamless loop → {out}")
    clip = VideoClip(make_frame, duration=DUR)
    clip.write_videofile(
        out, fps=FPS, codec="libx264", audio=False,
        logger="bar", preset="fast",
        ffmpeg_params=["-crf", "18", "-pix_fmt", "yuv420p"],
    )
    print("Done.")
