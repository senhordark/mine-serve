"""Urso-polar / meme "Remember November 2026" (27/11/2026) — baseado em make_voyager.py (mesmo corvo, fundo roxo, 6 fatos)."""
import math, sys, os
from PIL import Image, ImageDraw
import make_corvo as C
import make_lua as L
from make_corvo import (W, H, FPS, YELLOW, WHITE, SOFT, paste_crow, star, LH, S2)
from make import ease_out, ease_back
from make_lua import ctext as _ctext
def ctext(d, x, y, s_, size, fill):
    if size >= 2: _ctext(d, x, y, s_, size, fill)

RED = (240, 80, 70); ORANGE = (255, 150, 60); BLUE = (70, 140, 240); ICE = (200, 230, 255)
DARK = (40, 30, 70); PAPER = (245, 240, 255); FUR = (240, 240, 250); FUR2 = (215, 215, 232)
SEA = (40, 90, 170); METAL = (170, 170, 190)

SCENES = [
    dict(kind="hook", dur=4.0, label="EM ALTA", title="O urso do meme “Remember November”",
         body="Novembro de 2026 chegou! 6 segredos do urso-polar."),
    dict(kind="pelo", dur=5.0, label="FATO 01 / 06", title="Ele não é branco",
         body="O pelo é transparente, com fios ocos. E a pele por baixo é preta!"),
    dict(kind="peso", dur=5.0, label="FATO 02 / 06", title="Quase 1 tonelada",
         body="Machos passam de 500 kg. O maior já registrado chegou perto de 1.000 kg."),
    dict(kind="faro", dur=5.0, label="FATO 03 / 06", title="Faro absurdo",
         body="Sente o cheiro do buraco de respiração de uma foca a mais de 800 metros."),
    dict(kind="nado", dur=5.0, label="FATO 04 / 06", title="687 km nadando",
         body="Uma ursa nadou sem parar por 9 dias, segundo cientistas dos EUA."),
    dict(kind="mar", dur=5.0, label="FATO 05 / 06", title="“Urso do mar”",
         body="Ursus maritimus: vive boa parte da vida no gelo do oceano, caçando focas."),
    dict(kind="prisao", dur=5.0, label="FATO 06 / 06", title="Existe prisão de urso!",
         body="Em Churchill, no Canadá, ursos que invadem a cidade vão pra celas e saem de helicóptero."),
    dict(kind="outro", dur=4.5, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]
L.SCENES = C.SCENES = SCENES

def s(v): return v * S2

def bear(d, cx, cy, sc=1.0, flip=False, skin=False, swim=False, sniff=0.0):
    """Urso-polar original simplificado, de lado. (cx, cy) = centro do corpo."""
    fx = -1 if flip else 1
    def P(x, y): return (s(cx + fx * x * sc), s(cy + y * sc))
    def E(x, y, rx, ry, fill):
        a, b = P(x - rx, y - ry), P(x + rx, y + ry)
        d.ellipse((min(a[0], b[0]), a[1], max(a[0], b[0]), b[1]), fill=fill)
    body = (30, 30, 40) if skin else FUR
    shade = (20, 20, 30) if skin else FUR2
    if not swim:
        for lx in (-110, -50, 60, 120):
            d.rounded_rectangle((min(P(lx - 28, 30)[0], P(lx + 28, 30)[0]), P(0, 30)[1], max(P(lx - 28, 30)[0], P(lx + 28, 30)[0]), P(0, 140)[1]), radius=s(20 * sc), fill=shade if lx in (-50, 120) else body)
    E(0, 0, 190, 100, body)
    E(-150, -10, 70, 75, body)
    # cabeça
    hy = -50 + sniff * 30
    E(170, hy, 75, 60, body)
    E(235, hy + 15, 45, 32, body)
    E(270, hy + 8, 14, 12, (20, 20, 25))
    E(195, hy - 18, 9, 9, (20, 20, 25))
    E(130, hy - 52, 20, 18, body); E(130, hy - 52, 10, 9, shade)

def ice(d, x0, x1, y, h=60):
    d.polygon([(s(x0), s(y)), (s(x1), s(y)), (s(x1 - 30), s(y + h)), (s(x0 + 20), s(y + h))], fill=ICE)
    d.polygon([(s(x0), s(y)), (s(x1), s(y)), (s(x1 - 10), s(y + 14)), (s(x0 + 8), s(y + 14))], fill=WHITE)

def sea(d, y, gt):
    pts = [(s(0), s(LH))]
    for i in range(0, 1081, 30):
        pts.append((s(i), s(y + 12 * math.sin(i / 60 + gt * 2))))
    pts.append((s(1080), s(LH)))
    d.polygon(pts, fill=SEA + (230,))

def pill(d, cx, y, w, h, text, size, bg=YELLOW, fg=DARK, k=1.0):
    if k <= 0: return
    w2, h2 = w * k / 2, h * k / 2
    d.rounded_rectangle((s(cx - w2), s(y + h / 2 - h2), s(cx + w2), s(y + h / 2 + h2)), radius=s(h2), fill=bg)
    if k > 0.6: ctext(d, s(cx), s(y + h / 2 - size * 0.62 * k), text, s(size * k), fg)

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    bob = math.sin(gt * 1.8) * 14 * S2; tilt = math.sin(gt * 0.9) * 6; u = lt / dur
    if kind in ("hook", "outro"):
        # urso sentado na neve sob céu roxo (estilo do meme, desenho original)
        d.ellipse((s(60), s(560), s(1020), s(900)), fill=(235, 235, 250))
        bear(d, 330, 520 + math.sin(gt * 1.5) * 6, 0.95)
        pill(d, 780, 300, 440, 110, "NOV 2026", 72, k=ease_back((u - 0.1) / 0.3) if kind == "hook" else 1)
        paste_crow(img, s(820), s(640) + bob, s(400), gt, angle=tilt, flip=True)
        for i, (sx, sy, r) in enumerate([(120, 120, 30), (1000, 330, 24), (480, 200, 20), (620, 60, 18)]):
            k = 0.7 + 0.3 * math.sin(gt * 3 + i)
            star(d, s(sx), s(sy), s(r) * k, (255, 214, 102, 230))
    elif kind == "pelo":
        # metade com pelo, metade revelando pele preta
        bear(d, 300, 330, 0.75)
        bear(d, 300, 740, 0.75, skin=True)
        pill(d, 300, 480, 340, 90, "PELO", 56, k=ease_back(u / 0.3))
        pill(d, 300, 890, 340, 90, "PELE PRETA", 52, bg=PAPER, k=ease_back((u - 0.25) / 0.3))
        # fio oco ampliado
        k = ease_out(min(1, max(0, (u - 0.1) / 0.4)))
        if k > 0:
            hx, hy = 820, 300
            d.rounded_rectangle((s(hx - 50), s(hy - 200 * k), s(hx + 50), s(hy + 200 * k)), radius=s(50), fill=(255, 255, 255, 70), outline=WHITE, width=int(s(8)))
            d.rounded_rectangle((s(hx - 18), s(hy - 170 * k), s(hx + 18), s(hy + 170 * k)), radius=s(18), fill=(120, 100, 180, 120))
            for j in range(4):
                yy = hy - 150 + j * 100 + (gt * 60) % 100
                if abs(yy - hy) < 170 * k:
                    d.ellipse((s(hx - 10), s(yy - 10), s(hx + 10), s(yy + 10)), fill=(255, 240, 180, 220))
        paste_crow(img, s(820), s(780) + bob, s(340), gt, angle=tilt * 0.5, flip=True)
    elif kind == "peso":
        # balança
        bx, by = 400, 620
        d.rectangle((s(bx - 300), s(by), s(bx + 300), s(by + 60)), fill=METAL)
        d.rectangle((s(bx - 330), s(by + 60), s(bx + 330), s(by + 110)), fill=(120, 120, 140))
        bear(d, bx - 20, by - 128, 0.9)
        kg = int(1000 * ease_out(min(1, u / 0.7)))
        pill(d, bx, 760, 460, 130, f"{kg} kg", 84, k=ease_back(u / 0.25))
        paste_crow(img, s(890), s(820) + bob, s(330), gt, angle=tilt * 0.5, flip=True)
    elif kind == "faro":
        ice(d, 0, 1080, 560, 120)
        bear(d, 230, 465, 0.7, sniff=0.5 + 0.5 * math.sin(gt * 3))
        # buraco de foca
        hx = 900
        d.ellipse((s(hx - 70), s(575), s(hx + 70), s(615)), fill=SEA)
        # ondas de cheiro
        for j in range(6):
            p = ((gt * 0.5) + j / 6) % 1
            x = hx - 600 * p; y = 520 - 70 * math.sin(p * math.pi)
            r = 18 * (1 - p * 0.5)
            d.ellipse((s(x - r), s(y - r), s(x + r), s(y + r)), fill=(255, 214, 102, int(220 * (1 - p * 0.5))))
        pill(d, 560, 760, 420, 120, "+800 m", 84, k=ease_back((u - 0.2) / 0.3))
        paste_crow(img, s(880), s(330) + bob, s(300), gt, angle=tilt * 0.5, flip=True)
    elif kind == "nado":
        sea(d, 420, gt)
        x = 260 + 120 * math.sin(gt * 0.6)
        bear(d, x, 440 + math.sin(gt * 2) * 8, 0.8, swim=True)
        for k in range(4):
            d.line([(s(x - 250 - k * 40), s(420 + k * 30)), (s(x - 160 - k * 30), s(420 + k * 30))], fill=(255, 255, 255, 150), width=int(s(6)))
        pill(d, 540, 640, 400, 120, "687 km", 84, k=ease_back((u - 0.1) / 0.3))
        pill(d, 540, 790, 320, 100, "9 DIAS", 64, bg=PAPER, k=ease_back((u - 0.3) / 0.3))
        paste_crow(img, s(880), s(220) + bob, s(300), gt, angle=tilt * 0.5, flip=True)
    elif kind == "mar":
        sea(d, 560, gt)
        ice(d, 140, 760, 530, 90)
        bear(d, 420, 428, 0.75)
        # foca original simples na água
        fx, fy = 900, 610 + math.sin(gt * 2.5) * 10
        d.ellipse((s(fx - 70), s(fy - 40), s(fx + 70), s(fy + 40)), fill=(130, 130, 150))
        d.ellipse((s(fx - 90), s(fy - 60), s(fx - 20), s(fy + 5)), fill=(140, 140, 160))
        d.ellipse((s(fx - 70), s(fy - 40), s(fx - 58), s(fy - 28)), fill=(20, 20, 25))
        pill(d, 540, 110, 560, 120, "URSO DO MAR", 70, k=ease_back((u - 0.1) / 0.3))
        paste_crow(img, s(160), s(860) + bob, s(300), gt, angle=tilt * 0.5)
    elif kind == "prisao":
        # prédio com celas
        d.rounded_rectangle((s(90), s(330), s(690), s(820)), radius=s(20), fill=(110, 100, 150))
        d.polygon([(s(70), s(340)), (s(390), s(220)), (s(710), s(340))], fill=(80, 70, 120))
        d.rectangle((s(190), s(440), s(590), s(760)), fill=(30, 25, 50))
        bear(d, 390, 610, 0.55)
        for j in range(7):
            x = 210 + j * 60
            d.rectangle((s(x), s(440), s(x + 14), s(760)), fill=METAL)
        pill(d, 390, 830, 360, 110, "28 CELAS", 66, k=ease_back((u - 0.15) / 0.3))
        # helicóptero
        hx = 840 + 30 * math.sin(gt * 1.2); hy = 200 + 10 * math.sin(gt * 2)
        d.ellipse((s(hx - 110), s(hy - 50), s(hx + 70), s(hy + 50)), fill=RED)
        d.ellipse((s(hx + 10), s(hy - 35), s(hx + 60), s(hy + 10)), fill=ICE)
        d.rectangle((s(hx - 220), s(hy - 12), s(hx - 100), s(hy + 6)), fill=RED)
        rw = 160 * abs(math.cos(gt * 25))
        d.line([(s(hx - 20 - rw), s(hy - 70)), (s(hx - 20 + rw), s(hy - 70))], fill=DARK, width=int(s(8)))
        d.line([(s(hx - 20), s(hy - 50)), (s(hx - 20), s(hy - 70))], fill=DARK, width=int(s(8)))
        d.line([(s(hx - 90), s(hy + 70)), (s(hx + 40), s(hy + 70))], fill=DARK, width=int(s(8)))
        paste_crow(img, s(880), s(760) + bob, s(320), gt, angle=tilt * 0.5, flip=True)
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
