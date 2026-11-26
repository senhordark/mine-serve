"""Peru / Dia de Ação de Graças (26/11/2026) — baseado em make_hera.py (mesmo corvo, fundo roxo, 6 fatos)."""
import math, sys, os, random
from PIL import Image, ImageDraw
import make_corvo as C
import make_lua as L
from make_corvo import (W, H, FPS, YELLOW, WHITE, SOFT, paste_crow, star, LH, S2)
from make import ease_out, ease_back
from make_lua import ctext as _ctext
def ctext(d, x, y, s_, size, fill):
    if size >= 2: _ctext(d, x, y, s_, size, fill)

RED = (225, 60, 60); BLUE = (90, 160, 245); ORANGE = (255, 150, 60); GREEN = (90, 190, 110)
BROWN = (120, 72, 40); BROWN2 = (85, 50, 30); TAN = (190, 130, 70); CREAM = (245, 225, 180)
FEATH = [(150, 90, 45), (200, 130, 60), (235, 180, 90), (120, 70, 35)]
INK = (40, 30, 70); PAPER = (250, 238, 205)

SCENES = [
    dict(kind="hook", dur=6.0, label="EM ALTA", title="Hoje é Dia de Ação de Graças!",
         body="6 segredos do peru, a estrela da mesa."),
    dict(kind="nome", dur=8.0, label="FATO 01 / 06", title="O nome é uma confusão",
         body="Lembra o país Peru, mas a ave é nativa da América do Norte e do México."),
    dict(kind="voo", dur=7.0, label="FATO 02 / 06", title="Peru selvagem voa!",
         body="Em voos curtos, ele passa de 80 km/h."),
    dict(kind="corre", dur=7.0, label="FATO 03 / 06", title="Corredor de respeito",
         body="No chão, ele chega a uns 40 km/h."),
    dict(kind="cor", dur=7.0, label="FATO 04 / 06", title="Cabeça que muda de cor",
         body="Agitado, a pele vai do vermelho ao branco e ao azul."),
    dict(kind="canto", dur=7.0, label="FATO 05 / 06", title="Glu-glu de longe",
         body="O canto do macho pode ser ouvido a mais de 1,5 km."),
    dict(kind="carta", dur=9.0, label="FATO 06 / 06", title="Mais respeitável que a águia?",
         body="Foi o que Benjamin Franklin escreveu numa carta de 1784."),
    dict(kind="outro", dur=5.0, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]
L.SCENES = C.SCENES = SCENES

def s(v): return v * S2

def head_col(t):
    """cicla vermelho -> branco -> azul -> vermelho"""
    cs = [RED, (245, 240, 240), BLUE, RED]
    t = t % 3; i = int(t); f = t - i
    a, b = cs[i], cs[i + 1]
    return tuple(int(a[k] + (b[k] - a[k]) * f) for k in range(3))

def turkey(d, cx, cy, k=1.0, gt=0.0, fan=1.0, head=RED, legs=0.0, wings=None, flip=False, beak_open=0.0):
    """Peru original desenhado com formas. (cx, cy) = centro do corpo; k = escala."""
    fx = -1 if flip else 1
    P = lambda x, y: (s(cx + fx * x * k), s(cy + y * k))
    def ell(x, y, rx, ry, fill):
        x0, y0 = P(x - rx, y - ry); x1, y1 = P(x + rx, y + ry)
        d.ellipse((min(x0, x1), y0, max(x0, x1), y1), fill=fill)
    # cauda em leque
    if fan > 0:
        n = 11
        for ring, (R, cols) in enumerate(((230, FEATH), (180, FEATH[1:] + FEATH[:1]), (125, [CREAM, TAN]))):
            for i in range(n):
                a = math.radians(-90 + (i - (n - 1) / 2) * 17 * fan)
                tx, ty = -30 + R * math.sin(a) * 1.0, -40 - R * math.cos(-a) * 0.9 * fan
                d.polygon([P(-30 - 30 * math.cos(a), -40), P(tx - 32 * math.cos(a), ty), P(tx, ty - 26), P(tx + 32 * math.cos(a), ty),
                           P(-30 + 30 * math.cos(a), -40)], fill=cols[i % len(cols)])
            if ring == 0:
                for i in range(n):
                    a = math.radians(-90 + (i - (n - 1) / 2) * 17 * fan)
                    tx, ty = -30 + 205 * math.sin(a), -40 - 205 * math.cos(-a) * 0.9 * fan
                    ell(tx, ty, 14, 14, (40, 30, 25))
    # pernas
    for j, ox in enumerate((-25, 30)):
        sw = math.sin(legs + j * math.pi) * 30 if legs else 0
        d.line([P(ox, 70), P(ox + sw, 150)], fill=ORANGE, width=int(s(12 * k)))
        for dx in (-22, 0, 22):
            d.line([P(ox + sw, 150), P(ox + sw + dx + 14, 165)], fill=ORANGE, width=int(s(8 * k)))
    # corpo
    ell(0, 0, 120, 95, BROWN)
    ell(-20, 15, 95, 70, BROWN2)
    # asa
    if wings is None:
        ell(-15, 5, 75, 50, TAN); ell(-25, 15, 55, 32, FEATH[0])
    else:
        up = wings
        d.polygon([P(-10, -20), P(-150, -20 - 160 * up), P(-200, -10 - 90 * up), P(-120, 30)], fill=TAN)
        d.polygon([P(-10, -10), P(-120, -10 - 110 * up), P(-150, 0 - 50 * up), P(-90, 30)], fill=FEATH[0])
    # pescoço e cabeça
    d.polygon([P(60, -50), P(105, -150), P(140, -140), P(110, -30)], fill=BROWN2)
    ell(122, -170, 40, 40, head)
    ell(132, -178, 10, 10, WHITE); ell(135, -178, 5, 5, INK)
    # bico
    d.polygon([P(155, -175), P(190, -162 - 6 * beak_open), P(155, -155)], fill=(250, 200, 80))
    if beak_open > 0:
        d.polygon([P(155, -160), P(188, -150 + 8 * beak_open), P(155, -150)], fill=(230, 170, 60))
    # carúncula (snood) e barbela
    d.line([P(150, -195), P(158, -150), P(150, -120)], fill=head, width=int(s(12 * k)))
    ell(112, -122, 22, 30, head)

def twinkles(d, gt, pts):
    for i, (sx, sy, r) in enumerate(pts):
        kk = 0.7 + 0.3 * math.sin(gt * 3 + i)
        star(d, s(sx), s(sy), s(r) * kk, (255, 214, 102, 230))

def pill(d, x0, y0, x1, y1, text, size, k, fill=YELLOW, col=INK):
    if k <= 0: return
    d.rounded_rectangle((s(x0), s(y0), s(x1), s(y1)), radius=s((y1 - y0) / 2), fill=fill)
    ctext(d, s((x0 + x1) / 2), s(y0 + (y1 - y0 - size * 1.1) / 2), text, s(size * min(1, k)), col)

def speed_lines(d, x, y, n, length, gt, col=(255, 255, 255, 150)):
    for j in range(n):
        yy = y + (j - n / 2) * 34
        off = (gt * 900 + j * 97) % 200
        d.line([(s(x - off), s(yy)), (s(x - off - length), s(yy))], fill=col, width=int(s(6)))

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    bob = math.sin(gt * 1.8) * 14 * S2; tilt = math.sin(gt * 0.9) * 6; u = lt / dur
    if kind in ("hook", "outro"):
        f = 0.85 + 0.15 * math.sin(gt * 1.2)
        turkey(d, 640, 430 + math.sin(gt * 1.5) * 8, 1.25, gt, fan=f, flip=True)
        paste_crow(img, s(250), s(780) + bob, s(400), gt, angle=tilt)
        twinkles(d, gt, [(1000, 640, 24), (80, 420, 18), (960, 80, 18), (600, 820, 16)])
    elif kind == "nome":
        # placas de direção
        d.rectangle((s(520), s(120), s(545), s(880)), fill=(150, 110, 80))
        k1 = ease_back(u / 0.25); k2 = ease_back((u - 0.35) / 0.3)
        if k1 > 0:
            d.polygon([(s(545), s(150)), (s(545 + 420 * min(1, k1)), s(150)), (s(545 + 460 * min(1, k1)), s(215)), (s(545 + 420 * min(1, k1)), s(280)), (s(545), s(280))], fill=(200, 200, 215))
            ctext(d, s(760), s(180), "PAÍS PERU", s(50 * min(1, k1)), INK)
            if u > 0.3:
                bx, by, r = 1010, 215, 42 * min(1, ease_back((u - 0.3) / 0.2))
                if r > 0:
                    d.ellipse((s(bx - r), s(by - r), s(bx + r), s(by + r)), fill=RED, outline=WHITE, width=int(s(4)))
                    d.line([(s(bx - r * 0.45), s(by - r * 0.45)), (s(bx + r * 0.45), s(by + r * 0.45))], fill=WHITE, width=int(s(9)))
                    d.line([(s(bx + r * 0.45), s(by - r * 0.45)), (s(bx - r * 0.45), s(by + r * 0.45))], fill=WHITE, width=int(s(9)))
        if k2 > 0:
            d.polygon([(s(520), s(330)), (s(520 - 420 * min(1, k2)), s(330)), (s(520 - 470 * min(1, k2)), s(395)), (s(520 - 420 * min(1, k2)), s(460)), (s(520), s(460))], fill=YELLOW)
            ctext(d, s(300), s(345), "AMÉRICA DO", s(40 * min(1, k2)), INK)
            ctext(d, s(300), s(395), "NORTE + MÉXICO", s(40 * min(1, k2)), INK)
        turkey(d, 760, 680, 0.85, gt, fan=0.8, flip=False)
        star(d, s(860), s(470), s(22) * (0.8 + 0.2 * math.sin(gt * 4)), (255, 214, 102, 230))
        paste_crow(img, s(230), s(830) + bob, s(330), gt, angle=tilt * 0.5)
    elif kind == "voo":
        x = 300 + 400 * ease_out(min(1, u / 0.6))
        y = 430 - 80 * math.sin(gt * 2)
        speed_lines(d, x - 180, y, 5, 160, gt)
        turkey(d, x, y, 0.95, gt, fan=0.0, wings=0.5 + 0.5 * math.sin(gt * 12), flip=False)
        for j in range(3):
            cx = (900 - gt * 120 - j * 380) % 1300 - 100
            d.ellipse((s(cx - 90), s(120 + j * 60), s(cx + 90), s(180 + j * 60)), fill=(255, 255, 255, 60))
        pill(d, 80, 620, 520, 720, "+80 km/h", 64, ease_back((u - 0.3) / 0.3))
        paste_crow(img, s(820), s(840) + bob, s(330), gt, angle=tilt * 0.5, flip=True)
    elif kind == "corre":
        d.rectangle((0, s(640), s(1080), s(660)), fill=(255, 255, 255, 40))
        x = 250 + 500 * ease_out(min(1, u / 0.7))
        speed_lines(d, x - 160, 460, 4, 150, gt)
        rng = random.Random(int(gt * 10))
        for j in range(6):
            dx = rng.uniform(-250, -120); r = rng.uniform(12, 30)
            d.ellipse((s(x + dx - r), s(630 - r), s(x + dx + r), s(630 + r)), fill=(220, 200, 170, 140))
        turkey(d, x, 480 + abs(math.sin(gt * 14)) * -12, 0.95, gt, fan=0.0, legs=gt * 14)
        pill(d, 120, 720, 560, 820, "≈ 40 km/h", 62, ease_back((u - 0.3) / 0.3))
        paste_crow(img, s(840), s(850) + bob, s(320), gt, angle=tilt * 0.5, flip=True)
    elif kind == "cor":
        hc = head_col(max(0, lt - 0.8) * 0.9)
        turkey(d, 470, 560, 1.6, gt, fan=0.0, head=hc, flip=False)
        # bolinhas de cor
        for j, c in enumerate((RED, (245, 240, 240), BLUE)):
            kk = ease_back((u - 0.15 - j * 0.12) / 0.25)
            if kk > 0:
                r = 46 * min(1, kk); x = 760 + j * 115
                d.ellipse((s(x - r), s(110 - r), s(x + r), s(110 + r)), fill=c, outline=WHITE, width=int(s(4)))
        paste_crow(img, s(870), s(830) + bob, s(320), gt, angle=tilt * 0.5, flip=True)
    elif kind == "canto":
        talk = abs(math.sin(gt * 9)) if (lt % 1.6) < 0.8 else 0
        turkey(d, 330, 560, 1.0, gt, fan=0.9, beak_open=talk)
        bx, by = 330 + 190, 560 - 165
        for j in range(4):
            ph = (gt * 0.7 + j * 0.25) % 1
            r = 60 + ph * 520
            d.arc((s(bx - r), s(by - r), s(bx + r), s(by + r)), -40, 40, fill=(255, 209, 102, int(230 * (1 - ph))), width=int(s(9)))
        pill(d, 600, 120, 1000, 220, "GLU-GLU!", 58, ease_back((u - 0.15) / 0.3))
        pill(d, 600, 640, 1000, 740, "+1,5 km", 62, ease_back((u - 0.4) / 0.3))
        paste_crow(img, s(860), s(890) + bob, s(280), gt, angle=tilt * 0.5, flip=True)
    elif kind == "carta":
        # carta com pena
        k = ease_back(u / 0.3)
        if k > 0:
            kk = min(1, k)
            x0, y0 = 120, 90
            d.rounded_rectangle((s(x0), s(y0), s(x0 + 480 * kk), s(y0 + 560 * kk)), radius=s(18), fill=PAPER)
            for j in range(9):
                ww = 380 * kk * (0.6 + 0.4 * ((j * 37) % 10) / 10)
                if j * 52 + 70 < 520 * kk:
                    d.line([(s(x0 + 50 * kk), s(y0 + 70 + j * 52 * kk)), (s(x0 + 50 * kk + ww), s(y0 + 70 + j * 52 * kk))], fill=(150, 130, 110), width=int(s(6)))
            ctext(d, s(x0 + 240 * kk), s(y0 + 470 * kk), "1784", s(70 * kk), INK)
            # pena
            px, py = x0 + 470 * kk, y0 + 40
            d.polygon([(s(px), s(py)), (s(px + 90), s(py - 150)), (s(px + 60), s(py - 160)), (s(px - 10), s(py - 10))], fill=WHITE)
            d.line([(s(px - 5), s(py + 5)), (s(px + 80), s(py - 150))], fill=(200, 190, 210), width=int(s(4)))
        turkey(d, 820, 470, 0.8, gt, fan=0.9, flip=True)
        kt = ease_back((u - 0.45) / 0.3)
        if kt > 0:  # coroa
            cx, cy, r = 735, 290, 50 * min(1, kt)
            d.polygon([(s(cx - r), s(cy)), (s(cx - r), s(cy - r)), (s(cx - r / 2), s(cy - r / 2)), (s(cx), s(cy - r * 1.1)),
                       (s(cx + r / 2), s(cy - r / 2)), (s(cx + r), s(cy - r)), (s(cx + r), s(cy))], fill=YELLOW)
        paste_crow(img, s(330), s(860) + bob, s(300), gt, angle=tilt * 0.5)
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
