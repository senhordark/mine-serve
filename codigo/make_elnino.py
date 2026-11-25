"""El Niño recorde (25/11/2026) — baseado em make_raio.py / make_lua.py (mesmo corvo, fundo roxo, 6 fatos)."""
import math, sys, os, random
from PIL import Image, ImageDraw
import make_corvo as C
import make_lua as L
from make_corvo import (W, H, FPS, YELLOW, WHITE, SOFT, paste_crow, star, LH, S2)
from make import ease_out, ease_back
from make_lua import ctext as _ctext
def ctext(d, x, y, s_, size, fill):
    if size >= 2: _ctext(d, x, y, s_, size, fill)

RED = (240, 80, 70); ORANGE = (255, 150, 60); BLUE = (70, 140, 240); DBLUE = (40, 80, 170)
CLOUD = (120, 112, 165); SAND = (226, 186, 120); WOOD = (150, 98, 60)

SCENES = [
    dict(kind="hook", dur=4.0, label="EM ALTA", title="El Niño bate recorde! 6 fatos sobre ele",
         body="O Pacífico nunca esteve tão quente num mês de outubro."),
    dict(kind="nome", dur=5.0, label="FATO 01 / 06", title="“El Niño” quer dizer “o menino”",
         body="Pescadores do Peru viam a água quente chegar logo depois do Natal."),
    dict(kind="recorde", dur=5.0, label="FATO 02 / 06", title="+2,47 °C: recorde histórico",
         body="Maior anomalia já medida no Pacífico para um mês de outubro (Inmet)."),
    dict(kind="ciclo", dur=5.0, label="FATO 03 / 06", title="Volta a cada 2 a 7 anos",
         body="E costuma durar de 9 a 12 meses, segundo a NOAA."),
    dict(kind="dia", dur=5.0, label="FATO 04 / 06", title="Ele deixa o dia mais longo",
         body="Freia a rotação da Terra: em 1983, o dia esticou 0,2 milissegundo."),
    dict(kind="peixes", dur=5.0, label="FATO 05 / 06", title="Ele some com os peixes",
         body="Sem água fria subindo, falta plâncton. Em 1972, as redes de anchova voltaram vazias."),
    dict(kind="brasil", dur=5.0, label="FATO 06 / 06", title="No Brasil, bagunça o tempo",
         body="Chuva forte no Sul, seca no Norte e Nordeste e mais calor."),
    dict(kind="outro", dur=4.5, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]
L.SCENES = C.SCENES = SCENES

def s(v): return v * S2

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))

def sea(d, y, gt, col=BLUE, amp=14, top=None, x0=0, x1=1080, y1=1060):
    pts = [(s(x0), s(y1))]
    for x in range(x0, x1 + 1, 20):
        pts.append((s(x), s(y + amp * math.sin(x / 70 + gt * 2))))
    pts.append((s(x1), s(y1)))
    d.polygon(pts, fill=col)

def sun(d, cx, cy, r, gt, col=(255, 200, 70)):
    for i in range(12):
        a = i * math.pi / 6 + gt * 0.4
        d.line([(s(cx + math.cos(a) * r * 1.25), s(cy + math.sin(a) * r * 1.25)),
                (s(cx + math.cos(a) * r * 1.6), s(cy + math.sin(a) * r * 1.6))], fill=col, width=int(s(12)))
    d.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), fill=col)

def thermo(d, cx, top, bot, level, col=RED):
    w = 46
    d.rounded_rectangle((s(cx - w), s(top - 10), s(cx + w), s(bot + 10)), radius=s(w), fill=(245, 240, 255))
    d.ellipse((s(cx - 80), s(bot - 20), s(cx + 80), s(bot + 140)), fill=(245, 240, 255))
    d.ellipse((s(cx - 60), s(bot), s(cx + 60), s(bot + 120)), fill=col)
    ly = bot - (bot - top) * level
    d.rounded_rectangle((s(cx - 24), s(ly), s(cx + 24), s(bot + 40)), radius=s(24), fill=col)
    for k in range(6):
        yy = top + 30 + k * (bot - top - 60) / 5
        d.line([(s(cx + 46), s(yy)), (s(cx + 80), s(yy))], fill=(245, 240, 255), width=int(s(8)))

def cloud(d, cx, cy, sc=1.0, col=CLOUD):
    for (dx, dy, r) in [(-110, 20, 70), (-40, -20, 90), (50, -10, 80), (120, 25, 60), (0, 40, 70)]:
        d.ellipse((s(cx + (dx - r) * sc), s(cy + (dy - r) * sc), s(cx + (dx + r) * sc), s(cy + (dy + r) * sc)), fill=col)
    d.rounded_rectangle((s(cx - 170 * sc), s(cy + 20 * sc), s(cx + 170 * sc), s(cy + 100 * sc)), radius=s(40 * sc), fill=col)

def fish(d, x, y, sc=1.0, col=(180, 200, 230), flip=False):
    k = -1 if flip else 1
    d.ellipse((s(x - 40 * sc), s(y - 15 * sc), s(x + 40 * sc), s(y + 15 * sc)), fill=col)
    d.polygon([(s(x - k * 35 * sc), s(y)), (s(x - k * 65 * sc), s(y - 18 * sc)), (s(x - k * 65 * sc), s(y + 18 * sc))], fill=col)
    d.ellipse((s(x + k * 22 * sc - 5 * sc), s(y - 6 * sc), s(x + k * 22 * sc + 5 * sc), s(y + 4 * sc)), fill=(20, 20, 40))

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    bob = math.sin(gt * 1.8) * 14 * S2; tilt = math.sin(gt * 0.9) * 6; u = lt / dur
    if kind in ("hook", "outro"):
        sun(d, 820, 220, 95, gt)
        # oceano esquentando: faixa azul -> vermelha
        warm = 0.5 + 0.5 * math.sin(gt * 0.8)
        sea(d, 760, gt, col=lerp(BLUE, RED, 0.35 + 0.4 * warm), y1=1060)
        sea(d, 820, gt + 1.3, col=lerp(DBLUE, (200, 60, 60), 0.3 + 0.4 * warm), amp=10)
        paste_crow(img, s(330), s(560) + bob, s(780), gt, angle=tilt)
        for i, (sx, sy, r) in enumerate([(150, 140, 30), (1000, 460, 24), (110, 420, 20), (560, 80, 18)]):
            k = 0.7 + 0.3 * math.sin(gt * 3 + i)
            star(d, s(sx), s(sy), s(r) * k, (255, 214, 102, 230))
    elif kind == "nome":
        sun(d, 880, 170, 70, gt)
        sea(d, 640, gt, col=DBLUE)
        # corrente quente chegando (faixa laranja avançando)
        cx_w = -200 + 1300 * ease_out(min(1, u / 0.8))
        for k in range(3):
            yy = 720 + k * 70
            pts = [(s(x), s(yy + 12 * math.sin(x / 60 + gt * 3 + k))) for x in range(-200, int(cx_w), 20)]
            if len(pts) > 1: d.line(pts, fill=(255, 140 - k * 20, 60, 220), width=int(s(22)))
        # barco
        bx, by = 600, 620 + math.sin(gt * 2) * 10
        d.polygon([(s(bx - 200), s(by)), (s(bx + 200), s(by)), (s(bx + 150), s(by + 80)), (s(bx - 150), s(by + 80))], fill=WOOD)
        d.line([(s(bx), s(by)), (s(bx), s(by - 260))], fill=(90, 60, 40), width=int(s(14)))
        d.polygon([(s(bx + 8), s(by - 250)), (s(bx + 170), s(by - 40)), (s(bx + 8), s(by - 40))], fill=(245, 240, 255))
        paste_crow(img, s(470), s(by - 120) + bob * 0.3, s(330), gt, angle=tilt * 0.5)
        # calendário DEZ
        k = ease_back((u - 0.15) / 0.3)
        if k > 0:
            cx, cy, w, h = 180, 230, 130 * k, 150 * k
            d.rounded_rectangle((s(cx - w), s(cy - h), s(cx + w), s(cy + h)), radius=s(24), fill=(245, 240, 255))
            d.rounded_rectangle((s(cx - w), s(cy - h), s(cx + w), s(cy - h + 80 * k)), radius=s(24), fill=RED)
            if k > 0.6:
                ctext(d, s(cx), s(cy - h + 8 * k), "DEZ", s(56 * k), WHITE)
                ctext(d, s(cx), s(cy - 50 * k), "25", s(130 * k), (40, 30, 70))
    elif kind == "recorde":
        sea(d, 820, gt, col=lerp(BLUE, RED, 0.6))
        lvl = 0.15 + 0.8 * ease_out(min(1, u / 0.7))
        thermo(d, 300, 130, 640, lvl)
        paste_crow(img, s(820), s(640) + bob, s(480), gt, angle=tilt * 0.5, flip=True)
        k = ease_back((u - 0.2) / 0.3)
        if k > 0:
            d.rounded_rectangle((s(520), s(150), s(1020), s(330)), radius=s(40), fill=RED)
            ctext(d, s(770), s(165), "+2,47 °C", s(120 * min(1, k)), WHITE)
        k2 = ease_back((u - 0.4) / 0.3)
        if k2 > 0:
            d.rounded_rectangle((s(600), s(360), s(940), s(450)), radius=s(45), fill=YELLOW)
            ctext(d, s(770), s(370), "RECORDE", s(62 * min(1, k2)), (40, 30, 70))
    elif kind == "ciclo":
        cx, cy, R = 540, 470, 300
        ang = gt * 60
        d.arc((s(cx - R), s(cy - R), s(cx + R), s(cy + R)), ang, ang + 300, fill=YELLOW, width=int(s(34)))
        a = math.radians(ang + 300)
        hx, hy = cx + R * math.cos(a), cy + R * math.sin(a)
        ta = a + math.pi / 2
        d.polygon([(s(hx + 60 * math.cos(ta)), s(hy + 60 * math.sin(ta))),
                   (s(hx + 55 * math.cos(a)), s(hy + 55 * math.sin(a))),
                   (s(hx - 55 * math.cos(a)), s(hy - 55 * math.sin(a)))], fill=YELLOW)
        ctext(d, s(cx), s(cy - 150), "2 a 7", s(170), WHITE)
        ctext(d, s(cx), s(cy + 40), "ANOS", s(90), YELLOW)
        paste_crow(img, s(860), s(860) + bob, s(380), gt, angle=tilt * 0.5, flip=True)
        sun(d, 190, 860, 60, gt, col=(255, 150, 60))
    elif kind == "dia":
        cx, cy, R = 380, 500, 240
        d.ellipse((s(cx - R), s(cy - R), s(cx + R), s(cy + R)), fill=(60, 120, 220))
        rot = gt * 0.6
        for (ox, oy, rx, ry) in [(-80, -90, 90, 60), (70, 40, 110, 70), (-40, 140, 60, 40), (120, -140, 50, 30), (-200, 60, 80, 55), (-140, -150, 50, 30), (200, 120, 70, 45), (230, -60, 60, 50), (-250, -40, 55, 40)]:
            x = cx + ((ox / R + rot) % 2.4 - 1.2) * R
            if abs(x - cx) < R * 0.85:
                d.ellipse((s(x - rx), s(cy + oy - ry), s(x + rx), s(cy + oy + ry)), fill=(80, 190, 120))
        d.arc((s(cx - R - 60), s(cy - 80), s(cx + R + 60), s(cy + 80)), 200, 340, fill=(255, 255, 255, 150), width=int(s(10)))
        # relógio
        kx, ky, kr = 850, 260, 130
        d.ellipse((s(kx - kr), s(ky - kr), s(kx + kr), s(ky + kr)), fill=(245, 240, 255))
        a = gt * 2
        d.line([(s(kx), s(ky)), (s(kx + 100 * math.sin(a)), s(ky - 100 * math.cos(a)))], fill=RED, width=int(s(10)))
        d.line([(s(kx), s(ky)), (s(kx + 60 * math.sin(a / 12)), s(ky - 60 * math.cos(a / 12)))], fill=(40, 30, 70), width=int(s(14)))
        k = ease_back((u - 0.25) / 0.3)
        if k > 0:
            d.rounded_rectangle((s(670), s(440), s(1030), s(550)), radius=s(50), fill=YELLOW)
            ctext(d, s(850), s(450), "+0,2 ms", s(78 * min(1, k)), (40, 30, 70))
        paste_crow(img, s(820), s(830) + bob, s(380), gt, angle=tilt * 0.5, flip=True)
    elif kind == "peixes":
        sea(d, 330, gt, col=(50, 100, 200))
        d.rectangle((0, s(700), lw, lh), fill=(30, 60, 150))
        # setas de água fria bloqueadas
        for i, x in enumerate((220, 540, 860)):
            p = (gt * 0.5 + i * 0.3) % 1
            y = 1000 - 260 * p
            d.line([(s(x), s(y + 120)), (s(x), s(y))], fill=(150, 220, 255, int(200 * (1 - p))), width=int(s(16)))
            d.polygon([(s(x - 30), s(y)), (s(x + 30), s(y)), (s(x), s(y - 40))], fill=(150, 220, 255, int(200 * (1 - p))))
        d.line([(s(60), s(700)), (s(1020), s(700))], fill=(255, 140, 60, 220), width=int(s(18)))
        # peixes sumindo
        fade = 1 - ease_out(min(1, max(0, (u - 0.2) / 0.6)))
        for i, (fx, fy) in enumerate([(300, 470), (520, 560), (760, 450), (420, 640), (850, 610)]):
            al = int(255 * fade)
            if al > 5:
                fish(d, fx + 30 * math.sin(gt * 2 + i), fy, 1.2, col=(190, 210, 240, al), flip=i % 2 == 1)
        # barco com rede vazia
        bx, by = 540, 300 + math.sin(gt * 2) * 8
        d.polygon([(s(bx - 180), s(by)), (s(bx + 180), s(by)), (s(bx + 130), s(by + 70)), (s(bx - 130), s(by + 70))], fill=WOOD)
        for k2 in range(5):
            d.line([(s(bx + 120 + k2 * 14), s(by + 40)), (s(bx + 100 + k2 * 25), s(by + 230))], fill=(230, 230, 240, 160), width=int(s(4)))
        for k2 in range(4):
            yy = by + 80 + k2 * 40
            d.line([(s(bx + 110), s(yy)), (s(bx + 220), s(yy))], fill=(230, 230, 240, 160), width=int(s(4)))
        paste_crow(img, s(470), s(by - 40) + bob * 0.3, s(300), gt, angle=tilt * 0.4)
    elif kind == "brasil":
        panels = [(190, "SUL", "chuva"), (540, "NORTE/NE", "seca"), (890, "CALOR", "calor")]
        for i, (px, lab, typ) in enumerate(panels):
            k = ease_back((u - 0.05 - i * 0.12) / 0.3)
            if k <= 0: continue
            w, h = 160 * k, 260 * k
            d.rounded_rectangle((s(px - w), s(330 - h), s(px + w), s(330 + h)), radius=s(36), fill=(255, 255, 255, 40))
            if k > 0.7:
                if typ == "chuva":
                    cloud(d, px, 190, 0.6)
                    for j in range(7):
                        rx = px - 90 + j * 30; ry = 300 + ((gt * 300 + j * 47) % 220)
                        d.line([(s(rx), s(ry)), (s(rx - 10), s(ry + 40))], fill=(150, 200, 255), width=int(s(8)))
                elif typ == "seca":
                    sun(d, px, 200, 55, gt)
                    d.rectangle((s(px - 140), s(400), s(px + 140), s(520)), fill=SAND)
                    for (ax, ay, bx2, by2) in [(-120, 430, -40, 470), (-40, 470, 20, 440), (20, 440, 110, 480), (-40, 470, -60, 515), (20, 440, 40, 405), (110, 480, 130, 515)]:
                        d.line([(s(px + ax), s(ay)), (s(px + bx2), s(by2))], fill=(150, 110, 60), width=int(s(6)))
                else:
                    thermo(d, px, 120, 400, 0.9 + 0.05 * math.sin(gt * 3))
                ctext(d, s(px), s(540), lab, s(52), WHITE)
        paste_crow(img, s(540), s(850) + bob, s(360), gt, angle=tilt * 0.5)
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
