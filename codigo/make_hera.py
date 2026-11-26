"""Hera: primeiras imagens de Dimorphos (26/11/2026) — baseado em make_tiangong.py (mesmo corvo, fundo roxo, 6 fatos)."""
import math, sys, os, random
from PIL import Image, ImageDraw
import make_corvo as C
import make_lua as L
from make_corvo import (W, H, FPS, YELLOW, WHITE, SOFT, paste_crow, star, LH, S2)
from make import ease_out, ease_back
from make_lua import ctext as _ctext
def ctext(d, x, y, s_, size, fill):
    if size >= 2: _ctext(d, x, y, s_, size, fill)

RED = (240, 80, 70); BLUE = (70, 140, 240); ORANGE = (255, 150, 60)
ROCK = (150, 130, 120); ROCK2 = (110, 95, 90); ROCK3 = (185, 165, 150)
METAL = (220, 220, 235); METAL2 = (165, 165, 190); PANEL = (60, 90, 200); PANEL2 = (110, 150, 255)
GOLD = (220, 170, 60); INK = (40, 30, 70)

SCENES = [
    dict(kind="hook", dur=6.0, label="EM ALTA", title="Fotos do asteroide que a NASA acertou!",
         body="6 fatos sobre Dimorphos e a sonda Hera."),
    dict(kind="dart", dur=8.0, label="FATO 01 / 06", title="Uma batida de propósito",
         body="Em 2022, a sonda DART acertou Dimorphos a quase 22 mil km/h."),
    dict(kind="orbita", dur=7.0, label="FATO 02 / 06", title="33 minutos a menos",
         body="A volta dele em torno do asteroide Didymos ficou mais curta."),
    dict(kind="cratera", dur=8.0, label="FATO 03 / 06", title="Cratera do tamanho de um estádio",
         body="Ocupa quase a face inteira de um asteroide de uns 150 metros."),
    dict(kind="caos", dur=7.0, label="FATO 04 / 06", title="Ele ficou “tonto”",
         body="Agora gira sem rumo, como um barril rolando escada abaixo."),
    dict(kind="pedras", dur=6.0, label="FATO 05 / 06", title="Centenas de pedregulhos",
         body="Flutuam em volta dos dois asteroides, como uma nuvem de destroços."),
    dict(kind="radar", dur=9.0, label="FATO 06 / 06", title="Radar dentro de um asteroide",
         body="Um minissatélite da Hera vai olhar o interior de um asteroide pela 1ª vez."),
    dict(kind="outro", dur=5.0, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]
L.SCENES = C.SCENES = SCENES

def s(v): return v * S2

def rock_poly(cx, cy, R, seed, rot=0.0, squash=0.8, n=18):
    rng = random.Random(seed); pts = []
    for i in range(n):
        a = rot + i * 2 * math.pi / n
        r = R * rng.uniform(0.82, 1.08)
        pts.append((s(cx + r * math.cos(a)), s(cy + r * squash * math.sin(a))))
    return pts

def asteroid(d, cx, cy, R, seed, rot=0.0, squash=0.8, crater=0.0, base=ROCK):
    d.polygon(rock_poly(cx, cy, R, seed, rot, squash), fill=base)
    rng = random.Random(seed + 7)
    # sombra lado direito
    d.polygon(rock_poly(cx + R * 0.18, cy + R * 0.1, R * 0.8, seed, rot, squash * 0.9), fill=ROCK2)
    d.polygon(rock_poly(cx - R * 0.12, cy - R * 0.08, R * 0.78, seed + 1, rot, squash * 0.9), fill=base)
    for k in range(7):
        a = rot + rng.uniform(0, 6.28); rr = rng.uniform(0.1, 0.55) * R
        x, y = cx + rr * math.cos(a), cy + rr * squash * math.sin(a); r = R * rng.uniform(0.05, 0.11)
        d.ellipse((s(x - r), s(y - r * 0.8), s(x + r), s(y + r * 0.8)), fill=ROCK2)
        d.ellipse((s(x - r * 0.7), s(y - r * 0.6), s(x + r * 0.5), s(y + r * 0.4)), fill=ROCK3)
    if crater > 0:
        r = R * 0.72 * crater
        d.ellipse((s(cx - r), s(cy - r * squash * 0.95), s(cx + r), s(cy + r * squash * 0.95)), fill=(90, 75, 72))
        d.ellipse((s(cx - r * 0.82), s(cy - r * squash * 0.7), s(cx + r * 0.9), s(cy + r * squash * 0.95)), fill=(65, 52, 52))
        d.arc((s(cx - r), s(cy - r * squash * 0.95), s(cx + r), s(cy + r * squash * 0.95)), 190, 350, fill=ROCK3, width=int(s(6)))

def probe(d, cx, cy, k=1.0, gold=True):
    P = lambda v: v * k
    d.rectangle((s(cx - P(250)), s(cy - P(45)), s(cx - P(70)), s(cy + P(45))), fill=PANEL)
    d.rectangle((s(cx + P(70)), s(cy - P(45)), s(cx + P(250)), s(cy + P(45))), fill=PANEL)
    for xx in (-190, -130, 130, 190):
        d.line([(s(cx + P(xx)), s(cy - P(45))), (s(cx + P(xx)), s(cy + P(45)))], fill=PANEL2, width=max(1, int(s(3 * k))))
    d.rectangle((s(cx - P(70)), s(cy - P(6)), s(cx + P(70)), s(cy + P(6))), fill=METAL2)
    d.rounded_rectangle((s(cx - P(62)), s(cy - P(62)), s(cx + P(62)), s(cy + P(62))), radius=s(P(10)), fill=GOLD if gold else METAL)
    d.ellipse((s(cx - P(40)), s(cy - P(78)), s(cx + P(40)), s(cy - P(40))), fill=(240, 240, 250))
    d.ellipse((s(cx - P(16)), s(cy + P(20)), s(cx + P(16)), s(cy + P(52))), fill=INK)

def twinkles(d, gt, pts):
    for i, (sx, sy, r) in enumerate(pts):
        k = 0.7 + 0.3 * math.sin(gt * 3 + i)
        star(d, s(sx), s(sy), s(r) * k, (255, 214, 102, 230))

def pill(d, x0, y0, x1, y1, text, size, k, fill=YELLOW, col=INK):
    if k <= 0: return
    d.rounded_rectangle((s(x0), s(y0), s(x1), s(y1)), radius=s((y1 - y0) / 2), fill=fill)
    ctext(d, s((x0 + x1) / 2), s(y0 + (y1 - y0 - size * 1.1) / 2), text, s(size * min(1, k)), col)

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    bob = math.sin(gt * 1.8) * 14 * S2; tilt = math.sin(gt * 0.9) * 6; u = lt / dur
    if kind in ("hook", "outro"):
        asteroid(d, 640, 400, 230, 3, rot=gt * 0.05)
        a = gt * 0.8
        asteroid(d, 640 + 360 * math.cos(a), 400 + 110 * math.sin(a), 60, 9, rot=gt * 0.4, crater=1.0)
        probe(d, 230, 230 + math.sin(gt * 1.3) * 10, 0.55)
        # "flash" de câmera
        if kind == "hook" and (lt % 1.6) < 0.15:
            d.ellipse((s(190), s(190), s(270), s(270)), fill=(255, 255, 255, 200))
        paste_crow(img, s(300), s(760) + bob, s(420), gt, angle=tilt)
        twinkles(d, gt, [(1000, 640, 24), (80, 520, 18), (950, 80, 18), (560, 700, 16)])
    elif kind == "dart":
        tx, ty = 760, 430
        asteroid(d, tx, ty, 150, 9, rot=0.3)
        k = min(1, u / 0.45)
        px, py = 80 + (tx - 150 - 80) * k, 120 + (ty - 120) * k
        if k < 1:
            for j in range(1, 12):
                xx, yy = px - j * 26, py - j * 26 * (ty - 120) / (tx - 230)
                r = 16 - j
                if r > 0: d.ellipse((s(xx - r), s(yy - r), s(xx + r), s(yy + r)), fill=(255, 209, 102, 200 - j * 15))
            d.rectangle((s(px - 60), s(py - 14), s(px - 22), s(py + 14)), fill=PANEL)
            d.rounded_rectangle((s(px - 22), s(py - 22), s(px + 22), s(py + 22)), radius=s(5), fill=METAL)
        else:
            e = (u - 0.45) / 0.55
            r = 50 + 170 * ease_out(min(1, e * 1.5))
            al = int(210 * max(0, 1 - e) ** 1.5)
            d.ellipse((s(tx - 150 - r), s(ty - r), s(tx - 150 + r), s(ty + r)), fill=(255, 200, 90, al))
            d.ellipse((s(tx - 150 - r * 0.5), s(ty - r * 0.5), s(tx - 150 + r * 0.5), s(ty + r * 0.5)), fill=(255, 245, 200, al))
            rng = random.Random(5)
            for _ in range(18):
                a = rng.uniform(math.pi * 0.55, math.pi * 1.45); sp = rng.uniform(150, 420)
                xx, yy = tx - 150 + math.cos(a) * sp * e, ty + math.sin(a) * sp * e
                rr = rng.uniform(5, 12)
                d.ellipse((s(xx - rr), s(yy - rr), s(xx + rr), s(yy + rr)), fill=ROCK3)
        pill(d, 120, 560, 600, 670, "≈ 22.000 km/h", 58, ease_back((u - 0.2) / 0.3))
        paste_crow(img, s(820), s(820) + bob, s(340), gt, angle=tilt * 0.5, flip=True)
    elif kind == "orbita":
        cx, cy = 540, 360
        d.ellipse((s(cx - 380), s(cy - 150), s(cx + 380), s(cy + 150)), outline=(255, 255, 255, 110), width=int(s(5)))
        asteroid(d, cx, cy, 170, 3, rot=gt * 0.05)
        a = gt * 1.2
        asteroid(d, cx + 380 * math.cos(a), cy + 150 * math.sin(a), 48, 9, rot=gt * 0.4)
        # relógio
        k = ease_back((u - 0.25) / 0.3)
        if k > 0:
            ox, oy, R = 190, 690, 110 * min(1, k)
            d.ellipse((s(ox - R), s(oy - R), s(ox + R), s(oy + R)), fill=(245, 240, 255))
            d.ellipse((s(ox - R * 0.9), s(oy - R * 0.9), s(ox + R * 0.9), s(oy + R * 0.9)), outline=INK, width=int(s(5)))
            d.pieslice((s(ox - R * 0.8), s(oy - R * 0.8), s(ox + R * 0.8), s(oy + R * 0.8)), -90, -90 + 198 * ease_out(min(1, max(0, (u - 0.35) / 0.4))), fill=(255, 120, 100))
            d.line([(s(ox), s(oy)), (s(ox), s(oy - R * 0.7))], fill=INK, width=int(s(8)))
        pill(d, 330, 640, 690, 740, "−33 min", 64, ease_back((u - 0.45) / 0.3))
        paste_crow(img, s(790), s(820) + bob, s(360), gt, angle=tilt * 0.5, flip=True)
    elif kind == "cratera":
        asteroid(d, 540, 450, 270, 9, rot=0.1, squash=0.85, crater=ease_out(min(1, u / 0.5)))
        k = ease_back((u - 0.4) / 0.3)
        if k > 0:
            # mini estádio
            sx, sy = 880, 690
            d.ellipse((s(sx - 140 * k), s(sy - 70 * k), s(sx + 140 * k), s(sy + 70 * k)), fill=(235, 235, 245))
            d.ellipse((s(sx - 100 * k), s(sy - 45 * k), s(sx + 100 * k), s(sy + 45 * k)), fill=(80, 180, 100))
            d.line([(s(sx), s(sy - 45 * k)), (s(sx), s(sy + 45 * k))], fill=WHITE, width=int(s(3)))
            d.ellipse((s(sx - 16 * k), s(sy - 12 * k), s(sx + 16 * k), s(sy + 12 * k)), outline=WHITE, width=int(s(3)))
            ctext(d, s(880), s(780), "≈ ESTÁDIO", s(44 * min(1, k)), WHITE)
        pill(d, 340, 110, 740, 200, "≈ 150 m", 58, ease_back((u - 0.2) / 0.3))
        paste_crow(img, s(240), s(820) + bob, s(360), gt, angle=tilt * 0.5)
    elif kind == "caos":
        rot = gt * 2.3 + math.sin(gt * 3.1) * 1.2
        sq = 0.75 + 0.2 * math.sin(gt * 2.7)
        asteroid(d, 560, 360, 220, 9, rot=rot, squash=sq, crater=0.6 + 0.4 * abs(math.sin(gt * 1.7)))
        for j in range(3):
            a0 = gt * 200 + j * 120
            d.arc((s(560 - 300), s(360 - 260), s(560 + 300), s(360 + 260)), a0, a0 + 50, fill=(255, 209, 102, 200), width=int(s(10)))
        # estrelinhas de "tontura" no corvo
        for j in range(3):
            a = gt * 3 + j * 2.09
            star(d, s(300 + 90 * math.cos(a)), s(640 + 30 * math.sin(a)), s(18), (255, 214, 102, 240))
        paste_crow(img, s(300), s(830) + bob, s(340), gt, angle=math.sin(gt * 2.4) * 14)
    elif kind == "pedras":
        asteroid(d, 470, 380, 190, 3, rot=gt * 0.05)
        asteroid(d, 860, 230, 55, 9, rot=gt * 0.3)
        rng = random.Random(21)
        n = int(60 * ease_out(min(1, u / 0.5)))
        for i in range(60):
            if i >= n: break
            a = rng.uniform(0, 6.28) + gt * rng.uniform(0.05, 0.25); rr = rng.uniform(250, 470)
            x, y = 560 + rr * math.cos(a), 360 + rr * 0.55 * math.sin(a)
            r = rng.uniform(6, 16)
            d.polygon(rock_poly(x, y, r, i, rot=gt, n=7), fill=ROCK3 if i % 3 else ROCK)
        pill(d, 640, 560, 1040, 660, "CENTENAS", 58, ease_back((u - 0.3) / 0.3))
        paste_crow(img, s(250), s(830) + bob, s(340), gt, angle=tilt * 0.5)
    elif kind == "radar":
        asteroid(d, 640, 420, 230, 9, rot=0.2)
        # interior revelado (corte) com ondas de radar
        k = ease_out(min(1, max(0, (u - 0.25) / 0.4)))
        if k > 0:
            d.ellipse((s(640 - 130 * k), s(420 - 90 * k), s(640 + 130 * k), s(420 + 90 * k)), fill=(80, 60, 70, 230))
            rng = random.Random(4)
            for _ in range(int(14 * k)):
                x, y, r = 640 + rng.uniform(-100, 100) * k, 420 + rng.uniform(-60, 60) * k, rng.uniform(8, 18)
                d.ellipse((s(x - r), s(y - r), s(x + r), s(y + r)), fill=ROCK3)
        # minissatélite (caixa de sapato)
        cx, cy = 200, 140 + math.sin(gt * 1.5) * 8
        d.rectangle((s(cx - 110), s(cy - 20), s(cx - 45), s(cy + 20)), fill=PANEL)
        d.rectangle((s(cx + 45), s(cy - 20), s(cx + 110), s(cy + 20)), fill=PANEL)
        d.rounded_rectangle((s(cx - 45), s(cy - 32), s(cx + 45), s(cy + 32)), radius=s(6), fill=METAL)
        d.line([(s(cx), s(cy + 32)), (s(cx), s(cy + 70))], fill=METAL2, width=int(s(5)))
        for j in range(4):
            ph = ((gt * 0.8 + j * 0.25) % 1)
            r = 60 + ph * 380
            d.arc((s(cx - r), s(cy + 70 - r), s(cx + r), s(cy + 70 + r)), 10, 80, fill=(255, 209, 102, int(220 * (1 - ph))), width=int(s(7)))
        pill(d, 60, 560, 420, 660, "1ª VEZ", 64, ease_back((u - 0.45) / 0.3))
        paste_crow(img, s(830), s(840) + bob, s(330), gt, angle=tilt * 0.5, flip=True)
    return img.resize((W, LH), Image.LANCZOS)
L.illustration = C.illustration = illustration

if __name__ == "__main__":
    os.makedirs("outc", exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[1] == "durs":
        for sc, d_ in zip(SCENES, [float(x) for x in sys.argv[2].split(",")]): sc["dur"] = d_
        sys.argv = sys.argv[:1] + sys.argv[3:]
    st = C.starts()
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for i in range(8):
            lt = SCENES[i]["dur"] * 0.8
            ims.append(L.frame_at(SCENES[i], L.build_text(SCENES[i]), lt, st[i] + lt).resize((540, 960)))
        sh = Image.new("RGB", (540 * 4, 960 * 2)); [sh.paste(im, ((k % 4) * 540, (k // 4) * 960)) for k, im in enumerate(ims)]
        sh.save("outc/sheet.jpg", quality=88)
    else:
        only = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else range(len(SCENES))
        for i in only: C.render_scene(i, st[i])
