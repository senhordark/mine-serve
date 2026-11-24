"""Raios (alerta de tempestade, 24/11/2026) — baseado em make_bf.py / make_lua.py (mesmo corvo, fundo roxo, 6 fatos)."""
import math, sys, os, random
from PIL import Image, ImageDraw
import make_corvo as C
import make_lua as L
from make_corvo import (W, H, FPS, YELLOW, WHITE, SOFT, paste_crow, star, LH, S2)
from make import ease_out, ease_back
from make_lua import ctext

RED = (235, 70, 80); GOLD = (245, 190, 60); INK = (30, 20, 50); BOLT = (255, 236, 120)
CLOUD = (88, 78, 130); SAND = (226, 186, 120)

SCENES = [
    dict(kind="hook", dur=4.0, label="EM ALTA", title="Alerta de tempestade! 6 fatos sobre raios",
         body="E o Brasil é o país com mais raios do mundo."),
    dict(kind="brasil", dur=5.0, label="FATO 01 / 06", title="Brasil: campeão mundial de raios",
         body="Mais de 77 milhões de descargas por ano, segundo o Inpe."),
    dict(kind="sol", dur=5.0, label="FATO 02 / 06", title="Mais quente que o Sol",
         body="O ar em volta do raio chega a quase 28 mil °C: cerca de 5x a superfície do Sol."),
    dict(kind="predio", dur=5.0, label="FATO 03 / 06", title="Cai 2 vezes no mesmo lugar, sim",
         body="O Empire State, em Nova York, é atingido em média 23 vezes por ano."),
    dict(kind="trovao", dur=5.0, label="FATO 04 / 06", title="Conte até o trovão",
         body="A cada 3 segundos entre o clarão e o trovão, o raio está a ~1 km."),
    dict(kind="vidro", dur=5.0, label="FATO 05 / 06", title="Raio transforma areia em vidro",
         body="Ele derrete os grãos e forma tubos chamados fulguritos."),
    dict(kind="recorde", dur=5.0, label="FATO 06 / 06", title="O maior raio da história",
         body="Cruzou os EUA, do Texas até perto de Kansas City, em 2017."),
    dict(kind="outro", dur=4.5, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]
L.SCENES = C.SCENES = SCENES

def s(v): return v * S2

def cloud(d, cx, cy, sc=1.0, col=CLOUD):
    for (dx, dy, r) in [(-110, 20, 70), (-40, -20, 90), (50, -10, 80), (120, 25, 60), (0, 40, 70)]:
        d.ellipse((s(cx + (dx - r) * sc), s(cy + (dy - r) * sc), s(cx + (dx + r) * sc), s(cy + (dy + r) * sc)), fill=col)
    d.rounded_rectangle((s(cx - 170 * sc), s(cy + 20 * sc), s(cx + 170 * sc), s(cy + 100 * sc)), radius=s(40 * sc), fill=col)

def bolt(d, x0, y0, x1, y1, seed=1, w=12, col=BOLT, glow=True, jag=40, n=7):
    rnd = random.Random(seed)
    pts = [(x0, y0)]
    for k in range(1, n):
        t = k / n
        pts.append((x0 + (x1 - x0) * t + rnd.uniform(-jag, jag), y0 + (y1 - y0) * t + rnd.uniform(-jag * 0.3, jag * 0.3)))
    pts.append((x1, y1))
    P = [(s(x), s(y)) for x, y in pts]
    if glow:
        d.line(P, fill=(255, 240, 180, 60), width=int(s(w * 3.2)), joint="curve")
        d.line(P, fill=(255, 240, 180, 110), width=int(s(w * 1.9)), joint="curve")
    d.line(P, fill=col, width=int(s(w)), joint="curve")
    d.line(P, fill=(255, 255, 255), width=max(2, int(s(w * 0.35))), joint="curve")
    return pts

def icon_bolt(d, cx, cy, sc=1.0, col=BOLT):
    pts = [(0, -90), (-45, 10), (-5, 10), (-25, 90), (45, -15), (5, -15), (25, -90)]
    d.polygon([(s(cx + x * sc), s(cy + y * sc)) for x, y in pts], fill=col)

def flash(d, lw, lh, a):
    if a > 0: d.rectangle((0, 0, lw, lh), fill=(255, 250, 220, int(90 * a)))

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    bob = math.sin(gt * 1.8) * 14 * S2; tilt = math.sin(gt * 0.9) * 6; u = lt / dur
    blink = (gt * 0.8) % 1.0 < 0.12
    if kind in ("hook", "outro"):
        cloud(d, 760, 300, 1.15)
        if blink:
            bolt(d, 680, 390, 600, 700, seed=int(gt * 0.8), w=14)
            bolt(d, 850, 390, 930, 680, seed=int(gt * 0.8) + 7, w=10)
        paste_crow(img, s(330), s(700) + bob, s(760), gt, angle=tilt)
        for i, (sx, sy, r) in enumerate([(150, 140, 30), (1000, 420, 24), (110, 420, 20), (450, 60, 18)]):
            k = 0.7 + 0.3 * math.sin(gt * 3 + i)
            star(d, s(sx), s(sy), s(r) * k, (255, 214, 102, 230))
    elif kind == "brasil":
        # pódio com medalha "1º" e contador de raios
        d.rectangle((s(520), s(420), s(780), s(640)), fill=(245, 240, 255))
        d.rectangle((s(330), s(500), s(520), s(640)), fill=(200, 195, 225))
        d.rectangle((s(780), s(540), s(970), s(640)), fill=(170, 165, 200))
        ctext(d, s(650), s(440), "1º", s(110), INK)
        ctext(d, s(425), s(520), "2º", s(70), INK)
        ctext(d, s(875), s(555), "3º", s(60), INK)
        k = ease_back((u - 0.1) / 0.3)
        if k > 0:
            r = 110 * k
            d.ellipse((s(650 - r), s(260 - r), s(650 + r), s(260 + r)), fill=GOLD)
            d.ellipse((s(650 - r * 0.78), s(260 - r * 0.78), s(650 + r * 0.78), s(260 + r * 0.78)), fill=(255, 215, 90))
            if k > 0.6: icon_bolt(d, 650, 260, 0.85 * k, col=INK)
            d.polygon([(s(600), s(140)), (s(650), s(160)), (s(700), s(140)), (s(690), s(60)), (s(610), s(60))], fill=(60, 160, 90))
        cnt = int(77 * ease_out((u - 0.2) / 0.55))
        if u > 0.2: ctext(d, s(650), s(680), f"{cnt} milhões/ano", s(72), YELLOW)
        for i, x in enumerate((360, 940)):
            if (gt * 1.3 + i * 0.5) % 1.0 < 0.15: bolt(d, x, 130, x + 30, 400, seed=int(gt * 1.3) + i, w=9)
        paste_crow(img, s(200), s(850) + bob, s(380), gt, angle=tilt * 0.4)
    elif kind == "sol":
        # sol x raio com termômetros
        sx, sy = 390, 300
        for j in range(12):
            a = j * math.pi / 6 + gt * 0.3
            d.line([(s(sx + 120 * math.cos(a)), s(sy + 120 * math.sin(a))), (s(sx + 165 * math.cos(a)), s(sy + 165 * math.sin(a)))], fill=(255, 170, 60), width=s(14))
        d.ellipse((s(sx - 100), s(sy - 100), s(sx + 100), s(sy + 100)), fill=(255, 180, 60))
        ctext(d, s(sx), s(sy + 190), "SOL", s(56), WHITE)
        ctext(d, s(sx), s(sy + 260), "~5.500 °C", s(54), SOFT)
        bolt(d, 830, 130, 800, 470, seed=3, w=22, jag=45, n=5)
        ctext(d, s(820), s(500), "RAIO", s(56), WHITE)
        ctext(d, s(820), s(570), "~28.000 °C", s(54), YELLOW)
        k = ease_back((u - 0.35) / 0.3)
        if k > 0:
            r = 80 * k
            d.ellipse((s(610 - r), s(300 - r), s(610 + r), s(300 + r)), fill=RED)
            if k > 0.6: ctext(d, s(610), s(258), "5x", s(80), WHITE)
        paste_crow(img, s(560), s(880) + bob, s(380), gt, angle=tilt * 0.4)
    elif kind == "predio":
        # arranha-céu genérico levando vários raios
        bx = 720; oy = 110
        d.rectangle((s(bx - 120), s(oy + 380), s(bx + 120), s(oy + 900)), fill=(70, 62, 110))
        d.rectangle((s(bx - 85), s(oy + 250), s(bx + 85), s(oy + 380)), fill=(80, 72, 122))
        d.rectangle((s(bx - 50), s(oy + 170), s(bx + 50), s(oy + 250)), fill=(90, 82, 135))
        d.rectangle((s(bx - 8), s(oy + 70), s(bx + 8), s(oy + 170)), fill=(120, 112, 160))
        for r_ in range(9):
            for c_ in range(5):
                lit = (r_ * 5 + c_ * 3) % 4 != 0
                d.rectangle((s(bx - 100 + c_ * 42), s(oy + 410 + r_ * 52), s(bx - 74 + c_ * 42), s(oy + 440 + r_ * 52)),
                            fill=(255, 220, 130) if lit else (50, 45, 80))
        cloud(d, bx, oy + 40, 0.85)
        hits = int(ease_out((u - 0.1) / 0.75) * 23)
        if (gt * 1.6) % 1.0 < 0.2: bolt(d, bx - 30, oy + 40, bx, oy + 75, seed=int(gt * 1.6), w=14, jag=25, n=4)
        ctext(d, s(330), s(240), f"{hits}x", s(140), YELLOW)
        ctext(d, s(330), s(410), "por ano", s(60), WHITE)
        paste_crow(img, s(300), s(800) + bob, s(400), gt, angle=tilt * 0.4)
    elif kind == "trovao":
        cloud(d, 300, 130, 0.95)
        if u < 0.25 or (gt % 3.0) < 0.12:
            bolt(d, 280, 230, 240, 560, seed=5, w=14)
        # ondas sonoras viajando
        for k in range(3):
            ph = (u * 3 + k / 3) % 1
            r = 80 + ph * 420
            d.arc((s(260 - r), s(400 - r), s(260 + r), s(400 + r)), -35, 35, fill=(255, 255, 255, int(160 * (1 - ph))), width=s(8))
        # cronômetro
        cx, cy = 820, 300
        d.ellipse((s(cx - 140), s(cy - 140), s(cx + 140), s(cy + 140)), fill=(245, 240, 255))
        d.rectangle((s(cx - 25), s(cy - 185), s(cx + 25), s(cy - 140)), fill=(245, 240, 255))
        a = -math.pi / 2 + 2 * math.pi * min(1, u / 0.8)
        d.pieslice((s(cx - 120), s(cy - 120), s(cx + 120), s(cy + 120)), -90, math.degrees(a), fill=(255, 209, 102))
        secs = min(3, int(u / 0.8 * 3) + 1)
        ctext(d, s(cx), s(cy - 60), f"{secs}s", s(100), INK)
        k = ease_out((u - 0.6) / 0.25)
        if k > 0:
            d.line([(s(330), s(650)), (s(330 + 640 * k), s(650))], fill=YELLOW, width=s(10))
            d.polygon([(s(330 + 640 * k), s(625)), (s(330 + 640 * k + 40), s(650)), (s(330 + 640 * k), s(675))], fill=YELLOW)
            ctext(d, s(650), s(680), "≈ 1 km", s(80), YELLOW)
        paste_crow(img, s(880), s(900) + bob, s(380), gt, angle=tilt * 0.4, flip=True)
    elif kind == "vidro":
        # corte do solo de areia com tubo de vidro ramificado
        d.rectangle((0, s(300), lw, s(1060)), fill=SAND)
        for i in range(160):
            rx = (i * 97) % 1080; ry = 320 + (i * 53) % 700
            d.ellipse((s(rx), s(ry), s(rx + 8), s(ry + 8)), fill=(196, 156, 96))
        k = ease_out((u - 0.05) / 0.5)
        if u < 0.35: bolt(d, 640, -40, 650, 300, seed=9, w=18, n=5)
        if k > 0:
            def tube(x0, y0, x1, y1, w):
                d.line([(s(x0), s(y0)), (s(x0 + (x1 - x0) * k), s(y0 + (y1 - y0) * k))], fill=(110, 200, 210), width=int(s(w)))
                d.line([(s(x0), s(y0)), (s(x0 + (x1 - x0) * k), s(y0 + (y1 - y0) * k))], fill=(200, 245, 250), width=int(s(w * 0.3)))
            tube(650, 300, 620, 560, 34); tube(620, 560, 660, 800, 26); tube(620, 560, 500, 720, 18)
            tube(660, 800, 600, 960, 16); tube(650, 420, 760, 560, 16); tube(660, 800, 760, 920, 12)
        if u > 0.55:
            d.rounded_rectangle((s(700), s(330), s(1040), s(410)), radius=s(20), fill=INK)
            ctext(d, s(870), s(340), "fulgurito", s(52), YELLOW)
        paste_crow(img, s(250), s(150) + bob * 0.5, s(300), gt, angle=tilt * 0.4)
    elif kind == "recorde":
        # mapa estilizado: pinos e raio horizontal gigante
        d.rounded_rectangle((s(60), s(120), s(1020), s(560)), radius=s(40), fill=(60, 52, 100))
        pA, pB = (160, 470), (900, 200)
        for (px, py), lab in ((pA, "Texas"), (pB, "Kansas City")):
            d.ellipse((s(px - 22), s(py - 22), s(px + 22), s(py + 22)), fill=RED)
            if px < 300: ctext(d, s(px + 40), s(py + 28), lab, s(44), WHITE)
            else: ctext(d, s(px - 90), s(py - 80), lab, s(44), WHITE)
        k = ease_out((u - 0.1) / 0.45)
        if k > 0:
            ex, ey = pA[0] + (pB[0] - pA[0]) * k, pA[1] + (pB[1] - pA[1]) * k
            bolt(d, pA[0], pA[1], ex, ey, seed=11, w=12, jag=35, n=max(2, int(12 * k)))
        if u > 0.5:
            ctext(d, s(540), s(600), "829 km", s(130), YELLOW)
            ctext(d, s(540), s(760), "um único raio!", s(60), WHITE)
        paste_crow(img, s(190), s(860) + bob, s(340), gt, angle=tilt * 0.4)
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
