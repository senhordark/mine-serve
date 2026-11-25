"""Tiangong recebe 1º astronauta estrangeiro (25/11/2026) — baseado em make_elnino.py (mesmo corvo, fundo roxo, 6 fatos)."""
import math, sys, os
from PIL import Image, ImageDraw
import make_corvo as C
import make_lua as L
from make_corvo import (W, H, FPS, YELLOW, WHITE, SOFT, paste_crow, star, LH, S2)
from make import ease_out, ease_back
from make_lua import ctext as _ctext
def ctext(d, x, y, s_, size, fill):
    if size >= 2: _ctext(d, x, y, s_, size, fill)

RED = (240, 80, 70); BLUE = (70, 140, 240); DBLUE = (40, 80, 170); GREEN = (80, 190, 120)
METAL = (220, 220, 235); METAL2 = (165, 165, 190); PANEL = (60, 90, 200); PANEL2 = (110, 150, 255)
INK = (40, 30, 70)

SCENES = [
    dict(kind="hook", dur=4.0, label="EM ALTA", title="1º estrangeiro na estação da China!",
         body="6 fatos sobre a Tiangong, a estação espacial chinesa."),
    dict(kind="nome", dur=5.0, label="FATO 01 / 06", title="Tiangong = “Palácio Celestial”",
         body="É isso que o nome da estação quer dizer em chinês."),
    dict(kind="visita", dur=5.0, label="FATO 02 / 06", title="Primeiro visitante estrangeiro",
         body="Um astronauta do Paquistão vai passar cerca de uma semana a bordo."),
    dict(kind="modulos", dur=5.0, label="FATO 03 / 06", title="Só 3 módulos",
         body="A Estação Espacial Internacional tem 16."),
    dict(kind="veloc", dur=5.0, label="FATO 04 / 06", title="Voa a 28 mil km/h",
         body="Dá uma volta inteira na Terra a cada 1h30, mais ou menos."),
    dict(kind="braco", dur=5.0, label="FATO 05 / 06", title="Tem um braço robótico gigante",
         body="Foi ele que ajudou a encaixar os módulos lá no espaço."),
    dict(kind="anos", dur=5.0, label="FATO 06 / 06", title="Do 1º astronauta à estação: 18 anos",
         body="Primeiro astronauta chinês em 2003; estação lançada em 2021."),
    dict(kind="outro", dur=4.5, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]
L.SCENES = C.SCENES = SCENES

def s(v): return v * S2

def earth(d, cx, cy, R, gt):
    d.ellipse((s(cx - R - 18), s(cy - R - 18), s(cx + R + 18), s(cy + R + 18)), fill=(120, 170, 255, 60))
    d.ellipse((s(cx - R), s(cy - R), s(cx + R), s(cy + R)), fill=(60, 120, 220))
    rot = gt * 0.25
    for (ox, oy, rx, ry) in [(-0.3, -0.35, 0.35, 0.22), (0.25, 0.1, 0.4, 0.25), (-0.15, 0.5, 0.22, 0.15),
                             (0.45, -0.5, 0.2, 0.12), (-0.75, 0.2, 0.28, 0.2), (0.8, 0.45, 0.25, 0.17)]:
        x = ((ox + rot) % 2.4 - 1.2)
        if abs(x) < 0.85 and (x * x + oy * oy) < 0.8:
            d.ellipse((s(cx + (x - rx) * R), s(cy + (oy - ry) * R), s(cx + (x + rx) * R), s(cy + (oy + ry) * R)), fill=GREEN)

def panel(d, x0, y0, x1, y1):
    d.rectangle((s(x0), s(y0), s(x1), s(y1)), fill=PANEL)
    n = 4
    for k in range(1, n):
        xx = x0 + (x1 - x0) * k / n
        d.line([(s(xx), s(y0)), (s(xx), s(y1))], fill=PANEL2, width=int(s(3)))
    d.line([(s(x0), s((y0 + y1) / 2)), (s(x1), s((y0 + y1) / 2))], fill=PANEL2, width=int(s(3)))

def module(d, x0, y0, x1, y1, col=METAL):
    r = min(x1 - x0, y1 - y0) / 2
    d.rounded_rectangle((s(x0), s(y0), s(x1), s(y1)), radius=s(r), fill=col)
    if x1 - x0 > y1 - y0:
        for k in range(1, 4):
            xx = x0 + (x1 - x0) * k / 4
            d.line([(s(xx), s(y0 + 4)), (s(xx), s(y1 - 4))], fill=METAL2, width=int(s(4)))
    else:
        for k in range(1, 4):
            yy = y0 + (y1 - y0) * k / 4
            d.line([(s(x0 + 4), s(yy)), (s(x1 - 4), s(yy))], fill=METAL2, width=int(s(4)))

def station(d, cx, cy, k=1.0, parts=3):
    """Estação em T: barra horizontal (2 módulos de laboratório) + módulo central descendo."""
    def P(v): return v * k
    # painéis solares das pontas
    if parts >= 2:
        panel(d, cx - P(440), cy - P(110), cx - P(330), cy + P(110))
        d.line([(s(cx - P(330)), s(cy)), (s(cx - P(300)), s(cy))], fill=METAL2, width=int(s(8 * k)))
    if parts >= 3:
        panel(d, cx + P(330), cy - P(110), cx + P(440), cy + P(110))
        d.line([(s(cx + P(300)), s(cy)), (s(cx + P(330)), s(cy))], fill=METAL2, width=int(s(8 * k)))
    if parts >= 2: module(d, cx - P(300), cy - P(36), cx - P(40), cy + P(36))
    if parts >= 3: module(d, cx + P(40), cy - P(36), cx + P(300), cy + P(36))
    # nó central + módulo central
    module(d, cx - P(42), cy - P(60), cx + P(42), cy + P(300), col=(235, 235, 245))
    d.ellipse((s(cx - P(50)), s(cy - P(50)), s(cx + P(50)), s(cy + P(50))), fill=(245, 245, 255))
    panel(d, cx - P(160), cy + P(150), cx - P(46), cy + P(210))
    panel(d, cx + P(46), cy + P(150), cx + P(160), cy + P(210))

def twinkles(d, gt, pts):
    for i, (sx, sy, r) in enumerate(pts):
        k = 0.7 + 0.3 * math.sin(gt * 3 + i)
        star(d, s(sx), s(sy), s(r) * k, (255, 214, 102, 230))

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    bob = math.sin(gt * 1.8) * 14 * S2; tilt = math.sin(gt * 0.9) * 6; u = lt / dur
    if kind in ("hook", "outro"):
        d.ellipse((s(-400), s(860), s(1480), s(2400)), fill=(60, 120, 220))
        d.ellipse((s(-200), s(900), s(500), s(1100)), fill=GREEN)
        d.ellipse((s(650), s(920), s(1100), s(1080)), fill=GREEN)
        sy = 300 + math.sin(gt * 1.1) * 12
        station(d, 600, sy, 0.95)
        paste_crow(img, s(260), s(700) + bob, s(400), gt, angle=tilt)
        twinkles(d, gt, [(120, 120, 26), (1000, 620, 22), (900, 80, 18), (500, 700, 16)])
    elif kind == "nome":
        # palácio flutuando nas nuvens (silhueta genérica)
        px, py = 540, 420 + math.sin(gt * 1.2) * 10
        for (dx, dy, r) in [(-300, 160, 90), (-180, 190, 110), (0, 200, 120), (180, 190, 110), (300, 160, 90)]:
            d.ellipse((s(px + dx - r), s(py + dy - r * 0.6), s(px + dx + r), s(py + dy + r * 0.6)), fill=(235, 230, 255, 230))
        d.rectangle((s(px - 200), s(py - 40), s(px + 200), s(py + 130)), fill=(200, 70, 70))
        for k in range(5):
            xx = px - 160 + k * 80
            d.rectangle((s(xx - 14), s(py - 40), s(xx + 14), s(py + 130)), fill=(150, 40, 50))
        d.rectangle((s(px - 40), s(py + 30), s(px + 40), s(py + 130)), fill=(90, 30, 40))
        d.polygon([(s(px - 280), s(py - 30)), (s(px + 280), s(py - 30)), (s(px + 180), s(py - 120)), (s(px - 180), s(py - 120))], fill=YELLOW)
        d.polygon([(s(px - 300), s(py - 20)), (s(px - 250), s(py - 60)), (s(px - 220), s(py - 30))], fill=YELLOW)
        d.polygon([(s(px + 300), s(py - 20)), (s(px + 250), s(py - 60)), (s(px + 220), s(py - 30))], fill=YELLOW)
        d.rectangle((s(px - 130), s(py - 180), s(px + 130), s(py - 120)), fill=(200, 70, 70))
        d.polygon([(s(px - 200), s(py - 170)), (s(px + 200), s(py - 170)), (s(px + 110), s(py - 250)), (s(px - 110), s(py - 250))], fill=YELLOW)
        twinkles(d, gt, [(150, 130, 30), (930, 160, 26), (90, 520, 18), (990, 480, 20), (540, 70, 22)])
        paste_crow(img, s(860), s(850) + bob, s(340), gt, angle=tilt * 0.5, flip=True)
    elif kind == "visita":
        station(d, 470, 300, 0.85)
        # cápsula chegando da direita para acoplar
        k = ease_out(min(1, u / 0.75))
        cx = 1000 - 380 * k; cy = 700 - 120 * k
        d.polygon([(s(cx - 60), s(cy - 40)), (s(cx + 40), s(cy - 55)), (s(cx + 40), s(cy + 55)), (s(cx - 60), s(cy + 40))], fill=METAL)
        d.rounded_rectangle((s(cx + 40), s(cy - 55), s(cx + 150), s(cy + 55)), radius=s(20), fill=(200, 200, 220))
        panel(d, cx + 60, cy - 130, cx + 130, cy - 60); panel(d, cx + 60, cy + 60, cx + 130, cy + 130)
        k2 = ease_back((u - 0.3) / 0.3)
        if k2 > 0:
            d.rounded_rectangle((s(70), s(560), s(470), s(680)), radius=s(60), fill=YELLOW)
            ctext(d, s(270), s(575), "1ª VEZ", s(80 * min(1, k2)), INK)
        k3 = ease_back((u - 0.45) / 0.3)
        if k3 > 0:
            cx2, cy2, w, h = 210, 840, 120 * k3, 120 * k3
            d.rounded_rectangle((s(cx2 - w), s(cy2 - h), s(cx2 + w), s(cy2 + h)), radius=s(24), fill=(245, 240, 255))
            d.rounded_rectangle((s(cx2 - w), s(cy2 - h), s(cx2 + w), s(cy2 - h + 70 * k3)), radius=s(24), fill=RED)
            if k3 > 0.6:
                ctext(d, s(cx2), s(cy2 - h + 8 * k3), "≈ 1", s(50 * k3), WHITE)
                ctext(d, s(cx2), s(cy2 - 30 * k3), "SEMANA", s(48 * k3), INK)
        paste_crow(img, s(780), s(860) + bob, s(330), gt, angle=tilt * 0.5, flip=True)
    elif kind == "modulos":
        # esquerda: 3 módulos; direita: 16
        ctext(d, s(270), s(40), "TIANGONG", s(60), YELLOW)
        ctext(d, s(810), s(40), "ISS", s(60), WHITE)
        for i in range(3):
            k = ease_back((u - 0.05 - i * 0.08) / 0.3)
            if k > 0:
                y = 180 + i * 130
                module(d, 270 - 150 * k, y, 270 + 150 * k, y + 90 * k, col=YELLOW)
        for i in range(16):
            k = ease_back((u - 0.25 - i * 0.025) / 0.25)
            if k > 0:
                cx = 690 + (i % 4) * 82; cy = 200 + (i // 4) * 100
                module(d, cx - 34 * k, cy - 34 * k, cx + 34 * k, cy + 34 * k, col=(225, 225, 240))
        ctext(d, s(270), s(600), "3", s(150), YELLOW)
        ctext(d, s(810), s(600), "16", s(150), WHITE)
        paste_crow(img, s(540), s(900) + bob, s(300), gt, angle=tilt * 0.5)
    elif kind == "veloc":
        cx, cy, R = 360, 500, 220
        d.ellipse((s(cx - R - 75), s(cy - R - 75), s(cx + R + 75), s(cy + R + 75)), outline=(255, 255, 255, 90), width=int(s(5)))
        earth(d, cx, cy, R, gt)
        a = gt * 1.6
        ox, oy = cx + (R + 75) * math.cos(a), cy + (R + 75) * math.sin(a)
        # rastro
        for j in range(1, 10):
            aa = a - j * 0.08
            rr = 14 - j
            d.ellipse((s(cx + (R + 75) * math.cos(aa) - rr), s(cy + (R + 75) * math.sin(aa) - rr),
                       s(cx + (R + 75) * math.cos(aa) + rr), s(cy + (R + 75) * math.sin(aa) + rr)), fill=(255, 209, 102, 200 - j * 18))
        station(d, ox, oy, 0.13)
        k = ease_back((u - 0.2) / 0.3)
        if k > 0:
            d.rounded_rectangle((s(690), s(150), s(1066), s(260)), radius=s(55), fill=YELLOW)
            ctext(d, s(878), s(174), "28.000 km/h", s(48 * min(1, k)), INK)
        k2 = ease_back((u - 0.4) / 0.3)
        if k2 > 0:
            d.rounded_rectangle((s(755), s(300), s(1005), s(410)), radius=s(55), fill=(245, 240, 255))
            ctext(d, s(880), s(315), "≈ 1h30", s(66 * min(1, k2)), INK)
        paste_crow(img, s(850), s(820) + bob, s(360), gt, angle=tilt * 0.5, flip=True)
    elif kind == "braco":
        # módulo base fixo à esquerda
        module(d, 60, 220, 460, 320)
        panel(d, 120, 60, 260, 210); panel(d, 120, 330, 260, 480)
        # braço: ombro no módulo, levando um módulo até encaixar
        k = ease_out(min(1, u / 0.75))
        sx, sy = 380, 220
        tx = 900 - 430 * k; ty = 560 - 290 * k   # ponta do braço
        mx, my = (sx + tx) / 2 + 40, min(sy, ty) - 140 + 60 * k
        for (a0, a1) in [((sx, sy), (mx, my)), ((mx, my), (tx, ty))]:
            d.line([(s(a0[0]), s(a0[1])), (s(a1[0]), s(a1[1]))], fill=(255, 255, 255), width=int(s(26)))
            d.line([(s(a0[0]), s(a0[1])), (s(a1[0]), s(a1[1]))], fill=METAL2, width=int(s(12)))
        for (jx, jy) in [(sx, sy), (mx, my), (tx, ty)]:
            d.ellipse((s(jx - 26), s(jy - 26), s(jx + 26), s(jy + 26)), fill=YELLOW)
        module(d, tx, ty - 50, tx + 330, ty + 50, col=(235, 235, 245))
        if k > 0.98:
            r = 30 + 40 * ((gt * 2) % 1)
            d.ellipse((s(tx - r), s(ty - r), s(tx + r), s(ty + r)), outline=(255, 209, 102, 200), width=int(s(6)))
        paste_crow(img, s(300), s(800) + bob, s(380), gt, angle=tilt * 0.5)
    elif kind == "anos":
        y0 = 360
        d.line([(s(120), s(y0)), (s(960), s(y0))], fill=(255, 255, 255, 160), width=int(s(10)))
        prog = ease_out(min(1, u / 0.7))
        d.line([(s(120), s(y0)), (s(120 + 840 * prog), s(y0))], fill=YELLOW, width=int(s(14)))
        # foguete 2003
        fx, fy = 200, 220 + math.sin(gt * 2) * 6
        d.rounded_rectangle((s(fx - 35), s(fy - 90), s(fx + 35), s(fy + 60)), radius=s(30), fill=(245, 240, 255))
        d.polygon([(s(fx - 35), s(fy - 60)), (s(fx), s(fy - 140)), (s(fx + 35), s(fy - 60))], fill=RED)
        d.polygon([(s(fx - 35), s(fy + 20)), (s(fx - 70), s(fy + 70)), (s(fx - 35), s(fy + 60))], fill=RED)
        d.polygon([(s(fx + 35), s(fy + 20)), (s(fx + 70), s(fy + 70)), (s(fx + 35), s(fy + 60))], fill=RED)
        d.ellipse((s(fx - 18), s(fy - 50), s(fx + 18), s(fy - 14)), fill=BLUE)
        fl = 40 + 15 * math.sin(gt * 20)
        d.polygon([(s(fx - 22), s(fy + 60)), (s(fx + 22), s(fy + 60)), (s(fx), s(fy + 60 + fl))], fill=(255, 150, 60))
        ctext(d, s(200), s(400), "2003", s(80), WHITE)
        k = ease_back((u - 0.45) / 0.3)
        if k > 0:
            station(d, 840, 180, 0.28 * min(1, k))
            ctext(d, s(840), s(400), "2021", s(80 * min(1, k)), YELLOW)
        k2 = ease_back((u - 0.6) / 0.3)
        if k2 > 0:
            d.rounded_rectangle((s(330), s(540), s(750), s(660)), radius=s(60), fill=YELLOW)
            ctext(d, s(540), s(555), "18 ANOS", s(80 * min(1, k2)), INK)
        paste_crow(img, s(540), s(880) + bob, s(320), gt, angle=tilt * 0.5)
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
