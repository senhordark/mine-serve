"""Vênus no brilho máximo (28/11/2026) — baseado em make_elnino.py (mesmo corvo, fundo roxo, 6 fatos)."""
import math, sys, os
from PIL import Image, ImageDraw
import make_corvo as C
import make_lua as L
import make_elnino as E
from make_corvo import (W, H, FPS, YELLOW, WHITE, SOFT, paste_crow, star, LH, S2)
from make import ease_out, ease_back
from make_elnino import ctext, sun, thermo, sea, lerp

RED = (240, 80, 70); ORANGE = (255, 150, 60); BLUE = (70, 140, 240); DBLUE = (40, 80, 170)
VEN = (238, 196, 120); VEN2 = (210, 160, 90); ROCK = (176, 96, 56); DARKT = (40, 30, 70)

SCENES = [
    dict(kind="hook", dur=4.0, label="EM ALTA", title="Vênus no brilho máximo! 6 fatos sobre ele",
         body="Olhe para o leste antes do amanhecer."),
    dict(kind="dia", dur=5.0, label="FATO 01 / 06", title="Um dia dura mais que um ano",
         body="243 dias pra girar uma vez, 225 pra dar a volta no Sol."),
    dict(kind="oeste", dur=5.0, label="FATO 02 / 06", title="Lá o Sol nasce no oeste",
         body="Vênus gira ao contrário da maioria dos planetas."),
    dict(kind="quente", dur=5.0, label="FATO 03 / 06", title="O planeta mais quente",
         body="Mais de 460 °C, mais que Mercúrio, por causa do efeito estufa."),
    dict(kind="pressao", dur=5.0, label="FATO 04 / 06", title="Pressão 90 vezes maior",
         body="Como estar a quase 1 km de profundidade no oceano."),
    dict(kind="nuvens", dur=5.0, label="FATO 05 / 06", title="Nuvens de ácido sulfúrico",
         body="Elas refletem a luz do Sol e deixam Vênus tão brilhante."),
    dict(kind="venera", dur=5.0, label="FATO 06 / 06", title="127 minutos lá embaixo",
         body="Em 1982, a sonda Venera 13 mandou as primeiras fotos coloridas do chão."),
    dict(kind="outro", dur=4.5, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]
L.SCENES = C.SCENES = E.SCENES = SCENES

def s(v): return v * S2

def planet(d, cx, cy, r, gt, bands=True):
    d.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), fill=VEN)
    if bands:
        for k in range(5):
            yy = cy - r * 0.7 + k * r * 0.35
            off = math.sin(gt * 0.8 + k) * r * 0.15
            hw = math.sqrt(max(0, r * r - (yy - cy) ** 2)) * 0.85
            d.arc((s(cx - hw + off), s(yy - r * 0.12), s(cx + hw + off), s(yy + r * 0.12)), 10, 170,
                  fill=VEN2, width=int(s(max(4, r * 0.06))))
    d.ellipse((s(cx - r * 0.55), s(cy - r * 0.75), s(cx - r * 0.1), s(cy - r * 0.45)), fill=(255, 235, 190, 120))

def glow_point(d, cx, cy, r, gt):
    k = 0.85 + 0.15 * math.sin(gt * 3)
    for i in range(6, 0, -1):
        rr = r * (1 + i * 0.7) * k
        d.ellipse((s(cx - rr), s(cy - rr), s(cx + rr), s(cy + rr)), fill=(255, 240, 200, 18))
    star(d, s(cx), s(cy), s(r * 2.6 * k), (255, 250, 230, 255))
    d.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), fill=(255, 252, 240))

def pill(d, cx, cy, w, h, text, size, bg=YELLOW, fg=DARKT, k=1.0):
    k = min(1, k)
    d.rounded_rectangle((s(cx - w / 2 * k), s(cy - h / 2 * k), s(cx + w / 2 * k), s(cy + h / 2 * k)), radius=s(h / 2 * k), fill=bg)
    if k > 0.6: ctext(d, s(cx), s(cy - size * 0.62 * k), text, s(size * k), fg)

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    bob = math.sin(gt * 1.8) * 14 * S2; tilt = math.sin(gt * 0.9) * 6; u = lt / dur
    if kind in ("hook", "outro"):
        # amanhecer: faixa laranja no horizonte, ponto brilhante no leste
        for i in range(8):
            yy = 560 + i * 40
            d.rectangle((0, s(yy), lw, s(yy + 40)), fill=lerp((60, 40, 110), (255, 150, 90), i / 7) + (int(90 + i * 15),))
        glow_point(d, 820, 250, 16, gt)
        d.polygon([(0, s(900)), (s(300), s(760)), (s(620), s(840)), (s(1080), s(740)), (lw, lh), (0, lh)], fill=(30, 20, 60))
        paste_crow(img, s(330), s(620) + bob, s(640), gt, angle=tilt)
        for i, (sx, sy, r) in enumerate([(150, 140, 26), (980, 520, 18), (110, 420, 18), (560, 80, 16)]):
            kk = 0.7 + 0.3 * math.sin(gt * 3 + i)
            star(d, s(sx), s(sy), s(r) * kk, (255, 214, 102, 220))
    elif kind == "dia":
        sun(d, 330, 560, 80, gt)
        d.ellipse((s(330 - 250), s(560 - 190), s(330 + 250), s(560 + 190)), outline=(255, 255, 255, 90), width=int(s(5)))
        a = gt * 0.5
        px, py = 330 + 250 * math.cos(a), 560 + 190 * math.sin(a)
        planet(d, px, py, 70, gt)
        k1 = ease_back((u - 0.15) / 0.3); k2 = ease_back((u - 0.35) / 0.3)
        if k1 > 0: pill(d, 800, 230, 400, 110, "DIA: 243", 70, k=k1)
        if k2 > 0: pill(d, 800, 380, 400, 110, "ANO: 225", 70, bg=(245, 240, 255), k=k2)
        paste_crow(img, s(820), s(780) + bob, s(400), gt, angle=tilt * 0.5, flip=True)
    elif kind == "oeste":
        # céu de Vênus alaranjado, Sol subindo no lado ESQUERDO marcado OESTE
        for i in range(10):
            yy = 130 + i * 55
            d.rectangle((s(40), s(yy), s(1040), s(yy + 55)), fill=lerp((120, 70, 60), (240, 170, 90), i / 9) + (200,))
        rise = ease_out(min(1, u / 0.8))
        sun(d, 230, 640 - 330 * rise, 70, gt, col=(255, 220, 140))
        d.rectangle((s(40), s(640), s(1040), s(720)), fill=ROCK)
        ctext(d, s(230), s(660), "OESTE", s(50), WHITE)
        ctext(d, s(850), s(660), "LESTE", s(50), (255, 255, 255, 120))
        # seta de rotação ao contrário
        d.arc((s(600), s(170), s(980), s(470)), 200, 340, fill=YELLOW, width=int(s(20)))
        ax, ay = 600 + 190 + 190 * math.cos(math.radians(200)), 320 + 150 * math.sin(math.radians(200))
        d.polygon([(s(ax - 40), s(ay + 10)), (s(ax + 30), s(ay - 10)), (s(ax - 10), s(ay + 60))], fill=YELLOW)
        paste_crow(img, s(760), s(850) + bob, s(380), gt, angle=tilt * 0.5, flip=True)
    elif kind == "quente":
        planet(d, 360, 440, 230, gt)
        for i in range(10):
            a = i * math.pi / 5 + gt * 0.3
            d.line([(s(360 + math.cos(a) * 260), s(440 + math.sin(a) * 260)),
                    (s(360 + math.cos(a) * 300), s(440 + math.sin(a) * 300))], fill=(255, 110, 70, 200), width=int(s(12)))
        lvl = 0.2 + 0.75 * ease_out(min(1, u / 0.7))
        thermo(d, 830, 120, 540, lvl)
        k = ease_back((u - 0.25) / 0.3)
        if k > 0: pill(d, 780, 740, 380, 120, "460 °C", 86, bg=RED, fg=WHITE, k=k)
        paste_crow(img, s(300), s(860) + bob, s(330), gt, angle=tilt * 0.5)
    elif kind == "pressao":
        d.rectangle((s(60), s(80), s(1020), s(1000)), fill=(40, 90, 190, 140))
        for k2 in range(6):
            d.rectangle((s(60), s(80 + k2 * 150), s(1020), s(230 + k2 * 150)), fill=(10, 20, 60, 30 + k2 * 18))
        # régua de profundidade
        for k2 in range(9):
            yy = 120 + k2 * 100
            d.line([(s(110), s(yy)), (s(150 if k2 % 2 else 180), s(yy))], fill=(255, 255, 255, 160), width=int(s(6)))
        ctext(d, s(250), s(880), "~1 km", s(54), WHITE)
        # bolhas
        for i in range(8):
            p = (gt * 0.3 + i * 0.13) % 1
            bx = 300 + i * 80 + 20 * math.sin(gt * 2 + i); by = 960 - 820 * p
            d.ellipse((s(bx - 10), s(by - 10), s(bx + 10), s(by + 10)), outline=(220, 240, 255, int(200 * (1 - p))), width=int(s(4)))
        # caixa sendo esmagada
        sq = 1 - 0.35 * ease_out(min(1, u / 0.7))
        cx, cy = 640, 640
        d.rounded_rectangle((s(cx - 150), s(cy - 120 * sq), s(cx + 150), s(cy + 120 * sq)), radius=s(20), fill=(150, 160, 180))
        for dx in (-220, 220):
            d.polygon([(s(cx + dx), s(cy - 30)), (s(cx + dx * 0.78), s(cy)), (s(cx + dx), s(cy + 30))], fill=YELLOW)
        k = ease_back((u - 0.2) / 0.3)
        if k > 0: pill(d, 640, 260, 300, 130, "90x", 100, k=k)
        paste_crow(img, s(870), s(880) + bob, s(300), gt, angle=tilt * 0.5, flip=True)
    elif kind == "nuvens":
        sun(d, 140, 260, 60, gt)
        # raios do Sol batendo e voltando
        for i in range(3):
            y0 = 330 + i * 60
            p = (gt * 0.6 + i * 0.3) % 1
            d.line([(s(200), s(y0)), (s(200 + 260 * p), s(y0 + 90 * p))], fill=(255, 230, 120, 200), width=int(s(10)))
        planet(d, 560, 560, 280, gt, bands=False)
        for k2 in range(7):
            yy = 350 + k2 * 60
            off = 30 * math.sin(gt * 1.2 + k2)
            hw = math.sqrt(max(0, 280 ** 2 - (yy - 560) ** 2)) * 0.9
            d.rounded_rectangle((s(560 - hw + off), s(yy), s(560 + hw * 0.7 + off), s(yy + 34)), radius=s(17), fill=(255, 240, 170, 150))
        k = ease_back((u - 0.25) / 0.3)
        if k > 0: pill(d, 560, 900, 420, 110, "ÁCIDO!", 74, bg=(160, 225, 100), k=k)
        paste_crow(img, s(920), s(780) + bob, s(300), gt, angle=tilt * 0.5, flip=True)
    elif kind == "venera":
        for i in range(8):
            yy = 130 + i * 64
            d.rectangle((s(40), s(yy), s(1040), s(yy + 64)), fill=lerp((150, 90, 50), (230, 150, 70), i / 7) + (200,))
        d.polygon([(s(40), s(640)), (s(1040), s(600)), (s(1040), s(1000)), (s(40), s(1000))], fill=ROCK)
        for (rx, ry, rw) in [(150, 700, 90), (420, 760, 60), (900, 690, 70), (700, 820, 110)]:
            d.polygon([(s(rx - rw), s(ry + 30)), (s(rx - rw * 0.4), s(ry - 20)), (s(rx + rw * 0.5), s(ry - 15)), (s(rx + rw), s(ry + 30))], fill=(130, 70, 40))
        # sonda: anel + corpo + antena
        land = ease_out(min(1, u / 0.5))
        cx, cy = 560, 160 + 420 * land
        d.ellipse((s(cx - 170), s(cy + 40), s(cx + 170), s(cy + 100)), fill=(200, 200, 210))
        d.rounded_rectangle((s(cx - 90), s(cy - 120), s(cx + 90), s(cy + 70)), radius=s(30), fill=(230, 230, 240))
        d.ellipse((s(cx - 90), s(cy - 200), s(cx + 90), s(cy - 80)), fill=(210, 210, 225))
        d.line([(s(cx), s(cy - 200)), (s(cx), s(cy - 290))], fill=(230, 230, 240), width=int(s(10)))
        d.ellipse((s(cx - 22), s(cy - 40), s(cx + 22), s(cy + 4)), fill=(40, 40, 60))
        k = ease_back((u - 0.45) / 0.3)
        if k > 0: pill(d, 270, 250, 360, 120, "127 min", 82, k=k)
        if u > 0.6 and (gt * 4) % 1 < 0.15:
            d.rectangle((s(40), s(130), s(1040), s(1000)), fill=(255, 255, 255, 70))
        paste_crow(img, s(870), s(840) + bob, s(300), gt, angle=tilt * 0.5, flip=True)
    return img.resize((W, LH), Image.LANCZOS)
L.illustration = C.illustration = E.illustration = illustration

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
