"""Final da Libertadores 2026 (Palmeiras x Estudiantes, 28/11) — baseado em make_raio.py (mesmo corvo, fundo roxo, 6 fatos).
Ilustrações genéricas desenhadas com PIL: sem escudos, logos ou réplica do troféu oficial."""
import math, sys, os, random
from PIL import Image, ImageDraw
import make_corvo as C
import make_lua as L
from make_corvo import (W, H, FPS, YELLOW, WHITE, SOFT, paste_crow, star, LH, S2)
from make import ease_out, ease_back
from make_lua import ctext

RED = (235, 70, 80); GOLD = (245, 190, 60); GOLD2 = (255, 220, 110); INK = (30, 20, 50)
GRASS = (60, 150, 90); GRASS2 = (75, 170, 105); CONCRETE = (200, 195, 225)

SCENES = [
    dict(kind="hook", dur=4.0, label="EM ALTA", title="Final da Libertadores: 6 fatos que você não sabia",
         body="Sábado tem Palmeiras x Estudiantes, em Montevidéu."),
    dict(kind="estadio", dur=5.0, label="FATO 01 / 06", title="Um estádio de Copa do Mundo",
         body="O Centenário foi feito para a Copa de 1930 e recebeu a 1ª final: Uruguai 4x2 Argentina."),
    dict(kind="primeiro", dur=5.0, label="FATO 02 / 06", title="Onde a Libertadores nasceu",
         body="O 1º jogo do torneio foi lá, em 1960: Peñarol 7x1 Jorge Wilstermann."),
    dict(kind="revanche", dur=5.0, label="FATO 03 / 06", title="Revanche de 58 anos",
         body="Em 1968, o Estudiantes venceu o Palmeiras por 2x0 no desempate, no mesmo estádio."),
    dict(kind="tri", dur=5.0, label="FATO 04 / 06", title="Tri seguido",
         body="Aquele título abriu a sequência do Estudiantes: campeão em 1968, 69 e 70."),
    dict(kind="2021", dur=5.0, label="FATO 05 / 06", title="O Palmeiras já foi feliz lá",
         body="Em 2021, bateu o Flamengo por 2x1 na prorrogação e ergueu a taça no Centenário."),
    dict(kind="empate", dur=5.0, label="FATO 06 / 06", title="Brasil 25 x 25 Argentina",
         body="Os dois países estão empatados em títulos. A final de sábado desempata."),
    dict(kind="outro", dur=4.5, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]
L.SCENES = C.SCENES = SCENES

def s(v): return v * S2

def trophy(d, cx, cy, sc=1.0, col=GOLD, hi=GOLD2):
    """Taça genérica (copa com alças) — não é réplica de troféu real."""
    def R(x0, y0, x1, y1): return (s(cx + x0 * sc), s(cy + y0 * sc), s(cx + x1 * sc), s(cy + y1 * sc))
    w = max(2, int(s(22 * sc)))
    d.arc(R(-150, -150, -40, -10), 90, 270, fill=col, width=w)
    d.arc(R(40, -150, 150, -10), 270, 90, fill=col, width=w)
    d.chord(R(-110, -260, 110, 40), 0, 180, fill=col)
    d.rectangle(R(-110, -180, 110, -110), fill=col)
    d.ellipse(R(-110, -205, 110, -155), fill=hi)
    d.rectangle(R(-20, 40, 20, 110), fill=col)
    d.ellipse(R(-45, 20, 45, 60), fill=col)
    d.rounded_rectangle(R(-80, 110, 80, 145), radius=s(8 * sc), fill=col)
    d.rounded_rectangle(R(-105, 145, 105, 205), radius=s(10 * sc), fill=(120, 80, 40))
    d.line([(s(cx - 70 * sc), s(cy - 120 * sc)), (s(cx - 60 * sc), s(cy - 10 * sc))], fill=(255, 245, 200, 180), width=max(2, int(s(10 * sc))))

def ball(d, cx, cy, r, rot=0.0):
    d.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), fill=(250, 250, 255))
    pts = [(cx + r * 0.38 * math.cos(rot + k * 2 * math.pi / 5 - math.pi / 2), cy + r * 0.38 * math.sin(rot + k * 2 * math.pi / 5 - math.pi / 2)) for k in range(5)]
    d.polygon([(s(x), s(y)) for x, y in pts], fill=INK)
    for k in range(5):
        a = rot + k * 2 * math.pi / 5 - math.pi / 2
        x0, y0 = cx + r * 0.38 * math.cos(a), cy + r * 0.38 * math.sin(a)
        x1, y1 = cx + r * 0.92 * math.cos(a), cy + r * 0.92 * math.sin(a)
        d.line([(s(x0), s(y0)), (s(x1), s(y1))], fill=INK, width=max(2, int(s(r * 0.07))))
    d.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), outline=INK, width=max(2, int(s(r * 0.06))))

def scoreboard(d, cx, cy, left, right, score, w=760, tag=None):
    d.rounded_rectangle((s(cx - w / 2), s(cy - 95), s(cx + w / 2), s(cy + 95)), radius=s(30), fill=INK)
    d.rounded_rectangle((s(cx - w / 2 + 10), s(cy - 85), s(cx + w / 2 - 10), s(cy + 85)), radius=s(24), outline=(120, 100, 190), width=s(4))
    ctext(d, s(cx), s(cy - 75), score, s(120), YELLOW)
    ctext(d, s(cx - w / 2 + 95), s(cy - 30), left, s(50), WHITE)
    ctext(d, s(cx + w / 2 - 95), s(cy - 30), right, s(50), WHITE)
    if tag:
        tw = 30 * len(tag) + 60
        d.rounded_rectangle((s(cx - tw / 2), s(cy + 105), s(cx + tw / 2), s(cy + 175)), radius=s(30), fill=RED)
        ctext(d, s(cx), s(cy + 113), tag, s(44), WHITE)

def stadium(d, cx, cy, sc=1.0):
    """Estádio genérico em perspectiva com torre (silhueta simples)."""
    def P(x, y): return (s(cx + x * sc), s(cy + y * sc))
    d.ellipse([P(-420, -150), P(420, 190)], fill=(70, 62, 110))
    d.ellipse([P(-360, -105), P(360, 140)], fill=(95, 86, 140))
    d.ellipse([P(-290, -60), P(290, 95)], fill=GRASS)
    for k in range(-3, 4, 2):
        d.chord([P(-290, -60), P(290, 95)], 0, 360, fill=None)
    d.line([P(0, -60), P(0, 95)], fill=(230, 255, 235), width=max(2, int(s(5 * sc))))
    d.ellipse([P(-50, -5), P(50, 40)], outline=(230, 255, 235), width=max(2, int(s(5 * sc))))
    d.rectangle([P(-30, -400), P(30, -110)], fill=CONCRETE)
    d.polygon([P(-55, -400), P(55, -400), P(30, -440), P(-30, -440)], fill=(230, 225, 245))
    for j in range(6):
        d.rectangle([P(-12, -380 + j * 45), P(12, -360 + j * 45)], fill=(120, 110, 170))

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    bob = math.sin(gt * 1.8) * 14 * S2; tilt = math.sin(gt * 0.9) * 6; u = lt / dur
    if kind in ("hook", "outro"):
        glow = 0.5 + 0.5 * math.sin(gt * 3)
        for rr, al in ((260, 25), (200, 40)):
            d.ellipse((s(760 - rr), s(330 - rr), s(760 + rr), s(330 + rr)), fill=(255, 210, 100, int(al * (0.6 + 0.4 * glow))))
        trophy(d, 760, 350 + math.sin(gt * 1.5) * 10, 1.25)
        ball(d, 930, 700, 70, rot=gt * 1.2)
        paste_crow(img, s(330), s(700) + bob, s(760), gt, angle=tilt)
        for i, (sx, sy, r) in enumerate([(150, 140, 30), (1010, 120, 24), (110, 420, 20), (560, 70, 18)]):
            k = 0.7 + 0.3 * math.sin(gt * 3 + i)
            star(d, s(sx), s(sy), s(r) * k, (255, 214, 102, 230))
    elif kind == "estadio":
        stadium(d, 560, 600, 1.0)
        k = ease_back((u - 0.1) / 0.3)
        if k > 0:
            d.rounded_rectangle((s(850 - 150 * k), s(250 - 70 * k), s(850 + 150 * k), s(250 + 70 * k)), radius=s(30), fill=RED)
            if k > 0.6: ctext(d, s(850), s(195), "1930", s(100), WHITE)
        if u > 0.4:
            scoreboard(d, 560, 900, "URU", "ARG", "4 x 2", w=720)
        paste_crow(img, s(180), s(450) + bob, s(330), gt, angle=tilt * 0.4)
    elif kind == "primeiro":
        k = ease_back((u - 0.05) / 0.3)
        if k > 0:
            d.rounded_rectangle((s(540 - 190 * k), s(170 - 80 * k), s(540 + 190 * k), s(170 + 80 * k)), radius=s(34), fill=(245, 240, 255))
            if k > 0.6:
                ctext(d, s(540), s(110), "1960", s(110), INK)
        ctext(d, s(540), s(285), "JOGO Nº 1", s(64), YELLOW)
        if u > 0.3:
            scoreboard(d, 540, 500, "PEÑ", "WIL", "7 x 1", w=800)
        # bola entrando no gol
        gx, gy = 700, 740
        d.rectangle((s(gx), s(gy), s(gx + 300), s(gy + 180)), outline=WHITE, width=s(10))
        for j in range(1, 6): d.line([(s(gx + j * 50), s(gy)), (s(gx + j * 50), s(gy + 180))], fill=(255, 255, 255, 90), width=s(3))
        for j in range(1, 4): d.line([(s(gx), s(gy + j * 45)), (s(gx + 300), s(gy + j * 45))], fill=(255, 255, 255, 90), width=s(3))
        p = (gt * 0.7) % 1.0
        bx, by = 380 + p * 420, 900 - math.sin(p * math.pi) * 160 - p * 60
        ball(d, bx, by, 45, rot=gt * 4)
        paste_crow(img, s(230), s(820) + bob, s(380), gt, angle=tilt * 0.4)
    elif kind == "revanche":
        # linha do tempo 1968 -> 2026
        x0, x1, y = 200, 880, 390
        k = ease_out((u - 0.1) / 0.5)
        d.line([(s(x0), s(y)), (s(x0 + (x1 - x0) * k), s(y))], fill=YELLOW, width=s(12))
        for (x, lab) in ((x0, "1968"), (x1, "2026")):
            if x == x1 and k < 0.98: continue
            d.ellipse((s(x - 34), s(y - 34), s(x + 34), s(y + 34)), fill=YELLOW)
            ctext(d, s(x), s(y + 50), lab, s(80), WHITE)
        if u > 0.45:
            kk = ease_back((u - 0.45) / 0.25)
            d.rounded_rectangle((s(540 - 170 * kk), s(y - 150), s(540 + 170 * kk), s(y - 60)), radius=s(40), fill=RED)
            if kk > 0.6: ctext(d, s(540), s(y - 145), "58 anos", s(66), WHITE)
        scoreboard(d, 540, 680, "EST", "PAL", "2 x 0", w=720, tag="DESEMPATE")
        paste_crow(img, s(890), s(900) + bob, s(340), gt, angle=tilt * 0.4, flip=True)
        ball(d, 170, 930, 60, rot=gt * 1.5)
    elif kind == "tri":
        for i, (x, yr) in enumerate(((250, "1968"), (540, "1969"), (830, "1970"))):
            k = ease_back((u - 0.08 - i * 0.15) / 0.3)
            if k <= 0: continue
            trophy(d, x, 330 - (40 if i == 1 else 0), 0.85 * k)
            if k > 0.6: ctext(d, s(x), s(530 - (40 if i == 1 else 0) + 20), yr, s(70), WHITE)
        if u > 0.6:
            kk = ease_back((u - 0.6) / 0.25)
            d.rounded_rectangle((s(540 - 230 * kk), s(650), s(540 + 230 * kk), s(760)), radius=s(50), fill=RED)
            if kk > 0.6: ctext(d, s(540), s(660), "3 SEGUIDAS", s(72), WHITE)
        paste_crow(img, s(540), s(940) + bob * 0.6, s(300), gt, angle=tilt * 0.4)
    elif kind == "2021":
        rnd = random.Random(5)
        for i in range(40):
            px = rnd.uniform(40, 1040); sp = rnd.uniform(120, 260); ph = rnd.uniform(0, 1)
            py = ((ph + gt * sp / 1000) % 1.0) * 1000
            col = rnd.choice([(255, 209, 102), (120, 220, 150), (255, 255, 255), (235, 70, 80)])
            a = gt * 3 + i
            d.polygon([(s(px + 12 * math.cos(a)), s(py + 12 * math.sin(a))), (s(px - 12 * math.cos(a)), s(py - 12 * math.sin(a))),
                       (s(px - 6 * math.sin(a)), s(py + 6 * math.cos(a)))], fill=col)
        scoreboard(d, 540, 290, "PAL", "FLA", "2 x 1", w=720, tag="PRORROGAÇÃO")
        k = ease_back((u - 0.25) / 0.35)
        if k > 0: trophy(d, 770, 730, 0.95 * k)
        paste_crow(img, s(330), s(800) + bob, s(520), gt, angle=tilt * 0.5)
    elif kind == "empate":
        # balança equilibrada
        sw = math.sin(gt * 1.6) * 3
        cx, cy = 540, 260
        d.polygon([(s(cx - 30), s(cy)), (s(cx + 30), s(cy)), (s(cx + 90), s(cy + 560)), (s(cx - 90), s(cy + 560))], fill=CONCRETE)
        d.rounded_rectangle((s(cx - 180), s(cy + 540), s(cx + 180), s(cy + 590)), radius=s(20), fill=CONCRETE)
        a = math.radians(sw)
        L_ = 380
        lx, ly = cx - L_ * math.cos(a), cy - L_ * math.sin(a)
        rx, ry = cx + L_ * math.cos(a), cy + L_ * math.sin(a)
        d.line([(s(lx), s(ly)), (s(rx), s(ry))], fill=CONCRETE, width=s(18))
        d.ellipse((s(cx - 30), s(cy - 30), s(cx + 30), s(cy + 30)), fill=YELLOW)
        for (px, py, name, c1, c2) in ((lx, ly, "BRASIL", (40, 160, 90), (255, 215, 60)), (rx, ry, "ARGENTINA", (120, 190, 240), (255, 255, 255))):
            d.line([(s(px), s(py)), (s(px - 110), s(py + 220))], fill=(220, 215, 240), width=s(5))
            d.line([(s(px), s(py)), (s(px + 110), s(py + 220))], fill=(220, 215, 240), width=s(5))
            d.chord((s(px - 150), s(py + 140), s(px + 150), s(py + 300)), 0, 180, fill=c1)
            d.rounded_rectangle((s(px - 150), s(py + 205), s(px + 150), s(py + 230)), radius=s(10), fill=c2)
            k = ease_out((u - 0.15) / 0.5)
            ctext(d, s(px), s(py + 40), f"{int(25 * k)}", s(110), YELLOW)
            ctext(d, s(px), s(py + 310), name, s(50), WHITE)
        if u > 0.6:
            kk = ease_back((u - 0.6) / 0.25)
            d.ellipse((s(cx - 110 * kk), s(cy + 330 - 110 * kk), s(cx + 110 * kk), s(cy + 330 + 110 * kk)), fill=RED)
            if kk > 0.6: ctext(d, s(cx), s(cy + 280), "26?", s(90), WHITE)
        paste_crow(img, s(880), s(900) + bob, s(320), gt, angle=tilt * 0.4, flip=True)
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
