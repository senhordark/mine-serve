"""Superlua (24/11/2026) — baseado em make_corvo.py (mesmo corvo, fundo roxo, 6 fatos)."""
import math, sys, os
from PIL import Image, ImageDraw, ImageFont
import make_corvo as C
from make_corvo import (W, H, FPS, YELLOW, WHITE, SOFT, BG, rays, draw_parts, paste_crow, star, LY, LH, S2)
from make import ease_out, ease_back, text_sprite, pill_sprite, with_alpha, f_title, f_title_s, f_body, f_label, F

SCENES = [
    dict(kind="hook", dur=4.0, label="EM ALTA", title="Amanhã tem superlua! 6 fatos sobre ela",
         body="Dia 24/11 • olhe para o leste à noite"),
    dict(kind="series", dur=5.0, label="FATO 01 / 06", title="A 1ª de 3 superluas seguidas",
         body="Depois vêm dezembro e janeiro, e a de dezembro será a maior do ano."),
    dict(kind="size", dur=5.0, label="FATO 02 / 06", title="Até 14% maior e 30% mais brilhante",
         body="Comparada com a Lua mais fraca do ano."),
    dict(kind="name", dur=5.0, label="FATO 03 / 06", title="O nome veio da astrologia",
         body="“Superlua” foi criado em 1979 por um astrólogo americano, não por astrônomos."),
    dict(kind="beaver", dur=5.0, label="FATO 04 / 06", title="É a “Lua do Castor”",
         body="No hemisfério norte, é quando os castores reforçam as represas antes do inverno."),
    dict(kind="illusion", dur=5.0, label="FATO 05 / 06", title="Gigante no horizonte? É ilusão",
         body="Ela não cresce no horizonte, e a ciência ainda não explica bem por quê."),
    dict(kind="laser", dur=5.0, label="FATO 06 / 06", title="Ela foge 3,8 cm por ano",
         body="Medido com lasers apontados para espelhos deixados pela Apollo 11."),
    dict(kind="outro", dur=4.5, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]
C.SCENES = SCENES

# ---------- moon ----------
_mcache = {}
def moon_sprite(R, bright=1.0, glow=True):
    key = (int(R), round(bright, 2), glow)
    if key in _mcache: return _mcache[key]
    pad = int(R * 0.9) if glow else 4
    S = int(2 * R + 2 * pad)
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    c = S / 2
    if glow:
        for k in range(14, 0, -1):
            r = R + pad * k / 14
            d.ellipse((c - r, c - r, c + r, c + r), fill=(255, 240, 200, int(9 * bright)))
    base = tuple(int(v * (0.55 + 0.45 * bright)) for v in (250, 244, 225))
    d.ellipse((c - R, c - R, c + R, c + R), fill=base)
    mare = tuple(int(v * (0.55 + 0.45 * bright)) for v in (214, 206, 188))
    for (mx, my, mr) in [(-0.3, -0.25, 0.28), (0.15, -0.35, 0.2), (0.25, 0.05, 0.24), (-0.15, 0.3, 0.18), (-0.45, 0.15, 0.12)]:
        d.ellipse((c + (mx - mr) * R, c + (my - mr * 0.8) * R, c + (mx + mr) * R, c + (my + mr * 0.8) * R), fill=mare)
    for (mx, my, mr) in [(0.45, 0.4, 0.07), (-0.05, 0.6, 0.06), (0.55, -0.2, 0.05), (-0.6, -0.4, 0.05)]:
        d.ellipse((c + (mx - mr) * R, c + (my - mr) * R, c + (mx + mr) * R, c + (my + mr) * R), outline=mare, width=max(1, int(R * 0.02)))
    _mcache[key] = img
    return img

def paste_moon(img, cx, cy, R, bright=1.0, glow=True, alpha=1.0):
    spr = moon_sprite(R, bright, glow)
    if alpha < 1: spr = with_alpha(spr, alpha)
    img.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))

def bold(size): return ImageFont.truetype(F + "InterDisplay-Black.otf", int(size))
def ctext(d, x, y, s, size, fill):
    fb = bold(size); d.text((x - fb.getlength(s) / 2, y), s, font=fb, fill=fill)

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    cx = lw / 2; bob = math.sin(gt * 1.8) * 14 * S2
    tilt = math.sin(gt * 0.9) * 6
    u = lt / dur
    if kind in ("hook", "outro"):
        pulse = 1 + 0.03 * math.sin(gt * 2.5)
        paste_moon(img, 700 * S2, 330 * S2, 230 * S2 * pulse)
        paste_crow(img, 360 * S2, 640 * S2 + bob, 820 * S2, gt, angle=tilt)
        for i, (sx, sy, r) in enumerate([(150, 140, 30), (980, 640, 24), (120, 420, 20), (420, 90, 18)]):
            k = 0.7 + 0.3 * math.sin(gt * 3 + i)
            star(d, sx * S2, sy * S2, r * S2 * k, (255, 214, 102, 230))
    elif kind == "series":
        paste_crow(img, 230 * S2, 760 * S2 + bob, 520 * S2, gt, angle=tilt * 0.5)
        items = [("NOV", 300, 170, 330), ("DEZ", 560, 260, 200), ("JAN", 860, 200, 330)]
        for i, (lab, x, r, y) in enumerate(items):
            k = ease_back((u - 0.05 - i * 0.18) / 0.3)
            if k <= 0: continue
            paste_moon(img, x * S2, y * S2, r * S2 * k * 0.62, bright=1.0 if lab != "DEZ" else 1.0)
            if k > 0.5:
                col = YELLOW if lab == "DEZ" else WHITE
                ctext(d, x * S2, 520 * S2, lab, 64 * S2, col)
        if u > 0.65:
            k = ease_back((u - 0.65) / 0.2)
            bx, by = 560 * S2, 700 * S2
            w2 = 210 * S2 * k
            d.rounded_rectangle((bx - w2, by - 45 * S2 * k, bx + w2, by + 45 * S2 * k), radius=40 * S2, fill=YELLOW)
            if k > 0.7: ctext(d, bx, by - 34 * S2, "A MAIOR!", 58 * S2, (30, 20, 50))
    elif kind == "size":
        paste_crow(img, 270 * S2, 820 * S2 + bob, 420 * S2, gt, angle=tilt * 0.4)
        g = ease_out((u - 0.1) / 0.5)
        paste_moon(img, 270 * S2, 360 * S2, 150 * S2, bright=0.55, glow=False)
        Rb = (150 + 21 * g) * S2
        paste_moon(img, 770 * S2, 360 * S2, Rb, bright=0.55 + 0.45 * g, glow=True)
        ctext(d, 270 * S2, 560 * S2, "mais fraca", 50 * S2, SOFT)
        ctext(d, 770 * S2, 565 * S2, "superlua", 54 * S2, WHITE)
        if g > 0.3:
            ctext(d, 770 * S2, 40 * S2, "+14% tamanho", 56 * S2, WHITE)
            ctext(d, 770 * S2, 640 * S2, "+30% brilho", 56 * S2, YELLOW)
    elif kind == "name":
        paste_crow(img, 300 * S2, 640 * S2 + bob, 700 * S2, gt, angle=tilt * 0.5)
        # calendar page "1979"
        k = ease_back((u - 0.1) / 0.35)
        if k > 0:
            X, Y = 770 * S2, 330 * S2; w2, h2 = 200 * S2 * k, 230 * S2 * k
            d.rounded_rectangle((X - w2, Y - h2, X + w2, Y + h2), radius=30 * S2, fill=(245, 240, 255))
            d.rounded_rectangle((X - w2, Y - h2, X + w2, Y - h2 + 110 * S2 * k), radius=30 * S2, fill=(235, 90, 110))
            d.rectangle((X - w2, Y - h2 + 60 * S2 * k, X + w2, Y - h2 + 110 * S2 * k), fill=(235, 90, 110))
            for rx in (-0.5, 0.5):
                d.ellipse((X + rx * w2 - 16 * S2 * k, Y - h2 - 20 * S2 * k, X + rx * w2 + 16 * S2 * k, Y - h2 + 20 * S2 * k), fill=(60, 50, 90))
            if k > 0.6:
                ctext(d, X, Y - 40 * S2, "1979", 130 * S2, (40, 30, 70))
                paste_moon(img, X, Y + 150 * S2, 55 * S2, glow=False)
        # little stars orbiting the calendar (astrology vibe)
        for i in range(5):
            a = gt * 0.9 + i * 2 * math.pi / 5
            star(d, 770 * S2 + math.cos(a) * 290 * S2, 330 * S2 + math.sin(a) * 290 * S2, 22 * S2, (255, 214, 102, 210))
    elif kind == "beaver":
        paste_moon(img, 820 * S2, 280 * S2, 130 * S2)
        # water
        d.rectangle((0, 820 * S2, lw, lh), fill=(40, 70, 150, 200))
        for i in range(4):
            yy = (850 + i * 50) * S2; off = math.sin(gt * 2 + i) * 30 * S2
            d.line([(80 * S2 + off, yy), (980 * S2 + off, yy)], fill=(140, 180, 255, 90), width=5 * S2)
        # dam of logs
        for row in range(3):
            for j in range(5 - row):
                x0 = (470 + j * 110 + row * 55) * S2; y0 = (790 - row * 62) * S2
                d.rounded_rectangle((x0, y0, x0 + 150 * S2, y0 + 58 * S2), radius=28 * S2, fill=(120, 78, 44))
                d.ellipse((x0 + 110 * S2, y0 + 6 * S2, x0 + 150 * S2, y0 + 52 * S2), fill=(196, 150, 100))
        # simple original beaver carrying a stick
        bx, by = 300 * S2, 700 * S2 + math.sin(gt * 3) * 8 * S2
        BR = (130, 86, 50); DK = (90, 58, 34)
        d.ellipse((bx - 250 * S2, by + 20 * S2, bx - 60 * S2, by + 110 * S2), fill=(70, 60, 70))  # flat tail
        d.ellipse((bx - 130 * S2, by - 120 * S2, bx + 110 * S2, by + 110 * S2), fill=BR)      # body
        d.ellipse((bx + 20 * S2, by - 190 * S2, bx + 190 * S2, by - 30 * S2), fill=BR)        # head
        d.ellipse((bx + 30 * S2, by - 200 * S2, bx + 75 * S2, by - 155 * S2), fill=DK)        # ear
        d.ellipse((bx + 140 * S2, by - 95 * S2, bx + 205 * S2, by - 50 * S2), fill=(160, 110, 70))  # snout
        d.ellipse((bx + 180 * S2, by - 100 * S2, bx + 205 * S2, by - 78 * S2), fill=(40, 30, 30))   # nose
        d.rectangle((bx + 160 * S2, by - 55 * S2, bx + 190 * S2, by - 22 * S2), fill=(255, 250, 235))  # teeth
        d.line([(bx + 175 * S2, by - 55 * S2), (bx + 175 * S2, by - 22 * S2)], fill=(200, 190, 170), width=3 * S2)
        d.ellipse((bx + 110 * S2, by - 150 * S2, bx + 140 * S2, by - 118 * S2), fill=(25, 20, 30))  # eye
        d.ellipse((bx + 120 * S2, by - 146 * S2, bx + 130 * S2, by - 136 * S2), fill=WHITE)
        d.line([(bx + 60 * S2, by - 20 * S2), (bx + 330 * S2, by - 70 * S2)], fill=(150, 100, 60), width=22 * S2)  # stick
        paste_crow(img, 830 * S2, 520 * S2 + bob, 360 * S2, gt, angle=tilt * 0.4, flip=True)
    elif kind == "illusion":
        # horizon with hills
        d.rectangle((0, 760 * S2, lw, lh), fill=(25, 18, 55))
        d.pieslice((-200 * S2, 640 * S2, 500 * S2, 900 * S2), 180, 360, fill=(35, 26, 72))
        d.pieslice((400 * S2, 600 * S2, 1300 * S2, 920 * S2), 180, 360, fill=(30, 22, 64))
        # big-looking moon at horizon, small moon high — same real size
        Rr = 110 * S2
        paste_moon(img, 260 * S2, 300 * S2, Rr, glow=False)
        paste_moon(img, 650 * S2, 640 * S2, Rr * 1.55, glow=True)
        k = ease_out((u - 0.35) / 0.3)
        if k > 0:
            # dashed outline: real size overlay on the horizon moon
            cxm, cym = 650 * S2, 640 * S2
            for a in range(0, 360, 20):
                d.arc((cxm - Rr, cym - Rr, cxm + Rr, cym + Rr), a, a + 11, fill=(255, 90, 90, int(255 * k)), width=8 * S2)
            ctext(d, 650 * S2, 420 * S2, "mesmo tamanho!", 56 * S2, (255, 120, 120, int(255 * k)))
        paste_crow(img, 170 * S2, 840 * S2 + bob, 420 * S2, gt, angle=tilt * 0.4)
    elif kind == "laser":
        # earth bottom-left, moon drifting top-right
        ex, ey, ER = 230 * S2, 830 * S2, 190 * S2
        d.ellipse((ex - ER, ey - ER, ex + ER, ey + ER), fill=(60, 130, 230))
        for (mx, my, rx, ry) in [(-0.3, -0.2, 0.35, 0.25), (0.3, 0.25, 0.3, 0.3), (0.1, -0.55, 0.2, 0.12)]:
            d.ellipse((ex + (mx - rx) * ER, ey + (my - ry) * ER, ex + (mx + rx) * ER, ey + (my + ry) * ER), fill=(80, 180, 110))
        drift = ease_out(u) * 60 * S2
        mx_, my_ = 820 * S2 + drift, 230 * S2 - drift * 0.5
        paste_moon(img, mx_, my_, 120 * S2, glow=True)
        # laser pulses Earth -> Moon
        sx, sy = ex + 120 * S2, ey - 140 * S2
        d.line([(sx, sy), (mx_ - 80 * S2, my_ + 80 * S2)], fill=(255, 60, 80, 90), width=6 * S2)
        for i in range(3):
            p = (gt * 0.9 + i / 3) % 1
            px, py = sx + (mx_ - 80 * S2 - sx) * p, sy + (my_ + 80 * S2 - sy) * p
            d.ellipse((px - 16 * S2, py - 16 * S2, px + 16 * S2, py + 16 * S2), fill=(255, 80, 100))
        # arrow away
        ax, ay = mx_ + 40 * S2, my_ + 170 * S2
        d.line([(ax, ay), (ax + 120 * S2, ay - 60 * S2)], fill=YELLOW, width=12 * S2)
        d.polygon([(ax + 150 * S2, ay - 75 * S2), (ax + 95 * S2, ay - 75 * S2), (ax + 130 * S2, ay - 25 * S2)], fill=YELLOW)
        ctext(d, 820 * S2, 600 * S2, "+3,8 cm/ano", 64 * S2, YELLOW)
        paste_crow(img, 560 * S2, 860 * S2 + bob, 400 * S2, gt, angle=tilt * 0.4)
    return img.resize((W, LH), Image.LANCZOS)
C.illustration = illustration

def flame_pill(text):
    p = pill_sprite(text, f_label, (20, 30, 50), YELLOW)
    w, h = p.width + 44, p.height
    img = Image.new("RGBA", (w * 2, h * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), radius=h, fill=YELLOW)
    img = img.resize((w, h), Image.LANCZOS); img.alpha_composite(p, (0, 0))
    d = ImageDraw.Draw(img); fx, fy = p.width + 8, h / 2
    d.polygon([(fx + 14, fy - 24), (fx + 30, fy + 2), (fx + 26, fy + 20), (fx + 2, fy + 20), (fx - 2, fy + 2), (fx + 8, fy - 6)], fill=(235, 70, 40))
    d.polygon([(fx + 14, fy - 2), (fx + 22, fy + 10), (fx + 18, fy + 18), (fx + 8, fy + 18), (fx + 6, fy + 8)], fill=(255, 150, 40))
    return img

def build_text(sc):
    items = [flame_pill(sc["label"]) if sc["kind"] == "hook" else pill_sprite(sc["label"], f_label, (20, 30, 50), YELLOW)]
    tf = f_title if len(sc["title"]) < 26 else f_title_s
    items.append(text_sprite(sc["title"], tf, WHITE, 940, spacing=1.05))
    if sc["body"]: items.append(text_sprite(sc["body"], f_body, SOFT, 900, spacing=1.3))
    return items
C.build_text = build_text

def frame_at(sc, sprites, lt, gt):
    fr = BG.copy(); fr.alpha_composite(rays(gt))
    dur = sc["dur"]; last = sc is SCENES[-1]
    out = 0 if last else ease_out((lt - (dur - 0.35)) / 0.35)
    ill = illustration(sc["kind"], lt, dur, gt)
    p = ease_back(lt / 0.55); a = min(1, lt / 0.3) * (1 - out)
    if p < 0.999: ill = ill.resize((max(1, int(W * p)), max(1, int(LH * p))), Image.BILINEAR)
    fr.alpha_composite(with_alpha(ill, a), (int((W - ill.width) / 2), int(LY + (LH - ill.height) / 2)))
    draw_parts(fr, gt)
    y = 290; gaps = [28, 30]
    for i, sp in enumerate(sprites):
        e = ease_out((lt - 0.08 - i * 0.13) / 0.5)
        al = e * (1 - out); dy = (1 - e) * 70 - out * 40
        if al > 0.01: fr.alpha_composite(with_alpha(sp, al), (70, int(y + dy)))
        y += sp.height + (gaps[i] if i < len(gaps) else 0)
    idx = SCENES.index(sc); d = ImageDraw.Draw(fr)
    if 1 <= idx <= 6:
        sw = 150; step = 158
        for k in range(6):
            x0 = 70 + k * step
            d.rounded_rectangle((x0, 225, x0 + sw, 233), radius=4, fill=(255, 255, 255, 60))
            fw = sw if k + 1 < idx else (sw * min(1, lt / dur) if k + 1 == idx else 0)
            if fw > 0: d.rounded_rectangle((x0, 225, x0 + fw, 233), radius=4, fill=YELLOW)
    return fr.convert("RGB")
C.frame_at = frame_at

if __name__ == "__main__":
    os.makedirs("outc", exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[1] == "durs":
        for sc, d_ in zip(SCENES, [float(x) for x in sys.argv[2].split(",")]): sc["dur"] = d_
        sys.argv = sys.argv[:1] + sys.argv[3:]
    st = C.starts()
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for i in range(8):
            lt = SCENES[i]["dur"] * 0.7
            ims.append(frame_at(SCENES[i], build_text(SCENES[i]), lt, st[i] + lt).resize((360, 640)))
        sh = Image.new("RGB", (360 * 4, 640 * 2)); [sh.paste(im, ((k % 4) * 360, (k // 4) * 640)) for k, im in enumerate(ims)]
        sh.save("outc/sheet.jpg", quality=88)
        for i in (0, 4, 6): ims[i].save(f"outc/p{i}.jpg")
    else:
        only = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else range(len(SCENES))
        for i in only: C.render_scene(i, st[i])
