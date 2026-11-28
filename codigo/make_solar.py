"""Tempestade solar (27-28/11/2026) — baseado em make_venus.py / make_elnino.py (mesmo corvo, fundo roxo, 6 fatos)."""
import math, sys, os
from PIL import Image, ImageDraw
import make_corvo as C
import make_lua as L
import make_elnino as E
from make_corvo import (W, H, FPS, YELLOW, WHITE, SOFT, paste_crow, star, LH, S2)
from make import ease_out, ease_back
from make_elnino import ctext, sun, lerp

RED = (240, 80, 70); ORANGE = (255, 150, 60); BLUE = (70, 140, 240); GREEN = (90, 230, 150)
DARKT = (40, 30, 70); SKY = (25, 20, 60)

SCENES = [
    dict(kind="hook", dur=4.0, label="EM ALTA", title="Tempestade solar! 6 fatos sobre ela",
         body="Prevista para 27 e 28 de novembro."),
    dict(kind="escala", dur=5.0, label="FATO 01 / 06", title="Tem escala: de G1 a G5",
         body="A desta vez é G1, a mais fraca: no máximo, pequenas oscilações na rede elétrica."),
    dict(kind="nuvem", dur=5.0, label="FATO 02 / 06", title="Começa com uma nuvem do Sol",
         body="Gás eletrizado que leva alguns dias para chegar até a Terra."),
    dict(kind="1859", dur=5.0, label="FATO 03 / 06", title="1859: telégrafos soltaram faíscas",
         body="Na maior tempestade já registrada, teve aurora vista até no Caribe."),
    dict(kind="1989", dur=5.0, label="FATO 04 / 06", title="1989: Quebec ficou no escuro",
         body="6 milhões de pessoas passaram 9 horas sem luz no Canadá."),
    dict(kind="satelites", dur=5.0, label="FATO 05 / 06", title="Até a fraca dá prejuízo",
         body="Em 2022, uma tempestade derrubou cerca de 40 satélites recém-lançados."),
    dict(kind="brasil", dur=5.0, label="FATO 06 / 06", title="O ponto fraco fica sobre o Brasil",
         body="Na Anomalia do Atlântico Sul, satélites recebem mais radiação."),
    dict(kind="outro", dur=4.5, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]
L.SCENES = C.SCENES = E.SCENES = SCENES

def s(v): return v * S2

def pill(d, cx, cy, w, h, text, size, bg=YELLOW, fg=DARKT, k=1.0):
    k = min(1, k)
    d.rounded_rectangle((s(cx - w / 2 * k), s(cy - h / 2 * k), s(cx + w / 2 * k), s(cy + h / 2 * k)), radius=s(h / 2 * k), fill=bg)
    if k > 0.6: ctext(d, s(cx), s(cy - size * 0.62 * k), text, s(size * k), fg)

def big_sun(d, cx, cy, r, gt):
    for i in range(5, 0, -1):
        rr = r * (1 + i * 0.12)
        d.ellipse((s(cx - rr), s(cy - rr), s(cx + rr), s(cy + rr)), fill=(255, 170, 60, 30))
    d.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), fill=(255, 190, 70))
    for k in range(5):
        a = k * 1.3 + gt * 0.2
        x, y = cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a)
        d.ellipse((s(x - r * 0.12), s(y - r * 0.08), s(x + r * 0.12), s(y + r * 0.08)), fill=(240, 140, 40))
    # labareda (arco)
    fa = math.sin(gt * 2) * 0.1
    d.arc((s(cx + r * 0.4), s(cy - r * 0.9), s(cx + r * 1.3), s(cy - r * 0.1)), 160 + fa * 50, 360, fill=(255, 120, 50), width=int(s(14)))

def earth(d, cx, cy, r, gt, field=True):
    if field:
        for k in range(1, 4):
            rw, rh = r * (1.4 + k * 0.55), r * (0.9 + k * 0.4)
            d.arc((s(cx - rw * 0.35), s(cy - rh), s(cx + rw), s(cy + rh)), 100, 260, fill=(140, 200, 255, 110), width=int(s(5)))
            d.arc((s(cx - rw), s(cy - rh), s(cx + rw * 0.35), s(cy + rh)), 280, 80, fill=(140, 200, 255, 110), width=int(s(5)))
    d.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), fill=(60, 120, 220))
    for (ox, oy, rx, ry) in [(-0.3, -0.3, 0.35, 0.22), (0.25, 0.15, 0.3, 0.25), (-0.1, 0.5, 0.2, 0.15)]:
        d.ellipse((s(cx + (ox - rx) * r), s(cy + (oy - ry) * r), s(cx + (ox + rx) * r), s(cy + (oy + ry) * r)), fill=(80, 190, 120))

def aurora(d, y0, gt, alpha=150):
    for k in range(3):
        pts = [(s(x), s(y0 + k * 40 + 30 * math.sin(x / 120 + gt * 1.5 + k))) for x in range(0, 1081, 30)]
        col = (GREEN if k < 2 else (190, 120, 255)) + (alpha - k * 30,)
        d.line(pts, fill=col, width=int(s(34 - k * 8)))

def satellite(d, x, y, sc=1.0, ang=0.0, col=(220, 225, 240)):
    ca, sa = math.cos(ang), math.sin(ang)
    def R(px, py): return (s(x + (px * ca - py * sa) * sc), s(y + (px * sa + py * ca) * sc))
    d.polygon([R(-30, -20), R(30, -20), R(30, 20), R(-30, 20)], fill=col)
    d.polygon([R(-120, -14), R(-40, -14), R(-40, 14), R(-120, 14)], fill=(70, 110, 200))
    d.polygon([R(40, -14), R(120, -14), R(120, 14), R(40, 14)], fill=(70, 110, 200))

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    bob = math.sin(gt * 1.8) * 14 * S2; tilt = math.sin(gt * 0.9) * 6; u = lt / dur
    if kind in ("hook", "outro"):
        big_sun(d, 170, 260, 170, gt)
        earth(d, 860, 330, 90, gt)
        for i in range(10):
            p = (gt * 0.35 + i * 0.1) % 1
            x = 330 + 430 * p; y = 280 + 60 * math.sin(i * 1.7) * (1 - p * 0.5)
            d.ellipse((s(x - 8), s(y - 8), s(x + 8), s(y + 8)), fill=(255, 200, 90, int(230 * (1 - p))))
        aurora(d, 560, gt, 110)
        paste_crow(img, s(500), s(780) + bob, s(560), gt, angle=tilt)
    elif kind == "escala":
        labels = ["G1", "G2", "G3", "G4", "G5"]
        for i, lab in enumerate(labels):
            k = ease_back((u - 0.05 - i * 0.08) / 0.3)
            if k <= 0: continue
            x = 140 + i * 190; h = (110 + i * 85) * min(1, k)
            on = i == 0
            col = YELLOW if on else lerp((255, 200, 90), RED, i / 4) + (90,)
            d.rounded_rectangle((s(x - 70), s(720 - h), s(x + 70), s(720)), radius=s(20), fill=col)
            ctext(d, s(x), s(740), lab, s(58), WHITE if on else (255, 255, 255, 140))
        k = ease_back((u - 0.45) / 0.3)
        if k > 0:
            ay = 520 + 12 * math.sin(gt * 4)
            d.polygon([(s(140 - 40), s(ay)), (s(140 + 40), s(ay)), (s(140), s(ay + 60))], fill=WHITE)
            pill(d, 230, 440, 300, 100, "FRACA", 62, bg=WHITE, k=k)
        paste_crow(img, s(860), s(890) + bob, s(320), gt, angle=tilt * 0.5, flip=True)
    elif kind == "nuvem":
        big_sun(d, 60, 400, 230, gt)
        earth(d, 900, 420, 80, gt)
        p = ease_out(min(1, u / 0.9))
        cx = 330 + 420 * p; r = 70 + 90 * p
        for k in range(14):
            a = k * 2 * math.pi / 14 + gt
            rr = r * (0.6 + 0.4 * math.sin(k * 2.1 + gt * 2))
            x, y = cx + rr * math.cos(a), 420 + rr * math.sin(a) * 0.8
            d.ellipse((s(x - 26), s(y - 26), s(x + 26), s(y + 26)), fill=(255, 150, 70, 120))
        d.ellipse((s(cx - r * 0.5), s(420 - r * 0.4), s(cx + r * 0.5), s(420 + r * 0.4)), fill=(255, 200, 110, 140))
        k = ease_back((u - 0.35) / 0.3)
        if k > 0: pill(d, 640, 170, 460, 110, "ALGUNS DIAS", 64, k=k)
        paste_crow(img, s(560), s(860) + bob, s(320), gt, angle=tilt * 0.5)
    elif kind == "1859":
        d.rectangle((s(40), s(100), s(1040), s(700)), fill=SKY + (230,))
        aurora(d, 200, gt, 170)
        d.rectangle((s(40), s(700), s(1040), s(760)), fill=(50, 40, 80))
        for px in (220, 700):
            d.rectangle((s(px - 14), s(380), s(px + 14), s(710)), fill=(120, 80, 50))
            d.rectangle((s(px - 80), s(400), s(px + 80), s(420)), fill=(120, 80, 50))
        for yy in (400, 414):
            d.line([(s(40), s(yy + 20)), (s(220), s(yy)), (s(700), s(yy)), (s(1040), s(yy + 20))], fill=(200, 190, 230), width=int(s(5)))
        # faíscas
        for i in range(6):
            if (gt * 5 + i * 0.37) % 1 < 0.5:
                a = i * 1.05 + gt * 3
                x, y = 460 + 30 * math.sin(i), 402
                d.line([(s(x), s(y)), (s(x + 70 * math.cos(a)), s(y + 70 * math.sin(a)))], fill=(255, 240, 120), width=int(s(8)))
        star(d, s(460), s(402), s(50 + 10 * math.sin(gt * 9)), (255, 250, 200, 255))
        k = ease_back((u - 0.3) / 0.3)
        if k > 0: pill(d, 830, 200, 280, 110, "1859", 80, k=k)
        paste_crow(img, s(320), s(860) + bob, s(320), gt, angle=tilt * 0.5)
    elif kind == "1989":
        aurora(d, 150, gt, 120)
        off = ease_out(min(1, max(0, (u - 0.25) / 0.25)))
        bld = [(120, 420, 150), (290, 300, 130), (440, 470, 160), (620, 340, 150), (790, 260, 140), (950, 450, 120)]
        for (bx, top, bw) in bld:
            d.rectangle((s(bx - bw / 2), s(top), s(bx + bw / 2), s(760)), fill=(45, 40, 80))
            for wy in range(top + 30, 740, 60):
                for wx in range(int(bx - bw / 2 + 25), int(bx + bw / 2 - 25), 45):
                    lit = ((wx * 7 + wy * 3) % 5) != 0 and off < 1 - ((wx + wy) % 7) / 7
                    d.rectangle((s(wx), s(wy), s(wx + 22), s(wy + 30)), fill=(255, 220, 110) if lit else (30, 28, 55))
        k1 = ease_back((u - 0.45) / 0.3); k2 = ease_back((u - 0.6) / 0.3)
        if k1 > 0: pill(d, 300, 840, 400, 110, "6 milhões", 66, k=k1)
        if k2 > 0: pill(d, 300, 970, 260, 100, "9 horas", 60, bg=(245, 240, 255), k=k2)
        paste_crow(img, s(820), s(890) + bob, s(300), gt, angle=tilt * 0.5, flip=True)
    elif kind == "satelites":
        R = 900
        d.ellipse((s(540 - R), s(860), s(540 + R), s(860 + 2 * R)), fill=(60, 120, 220))
        d.ellipse((s(540 - R - 30), s(830), s(540 + R + 30), s(890 + 2 * R)), outline=(140, 200, 255, 90), width=int(s(14)))
        for i in range(7):
            p = ease_out(min(1, max(0, (u - i * 0.05) / 0.8)))
            x0 = 120 + i * 140
            x = x0 + 60 * p; y = 140 + (i % 3) * 90 + 520 * p
            satellite(d, x, y, 0.55, ang=0.3 + 1.2 * p * (1 if i % 2 else -1))
            if p > 0.3:
                d.line([(s(x - 30), s(y - 40)), (s(x - 70), s(y - 110))], fill=(255, 150, 70, 160), width=int(s(10)))
        k = ease_back((u - 0.35) / 0.3)
        if k > 0: pill(d, 840, 240, 260, 110, "~40", 84, k=k)
        paste_crow(img, s(870), s(560) + bob, s(280), gt, angle=tilt * 0.5, flip=True)
    elif kind == "brasil":
        cx, cy, r = 470, 470, 330
        d.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), fill=(60, 120, 220))
        # América do Sul simplificada
        sa = [(-40, -260), (60, -250), (150, -170), (230, -90), (200, 20), (120, 90), (60, 200), (0, 290), (-40, 300), (-50, 180), (-70, 40), (-150, -60), (-150, -170), (-90, -230)]
        d.polygon([(s(cx + x), s(cy + y)) for (x, y) in sa], fill=(80, 190, 120))
        # mancha da anomalia (pulsando) sobre o Brasil e o Atlântico Sul
        pk = 0.9 + 0.1 * math.sin(gt * 3)
        ax, ay = cx + 90, cy + 60
        for i in range(3, 0, -1):
            rr = 45 * i * pk
            d.ellipse((s(ax - rr * 1.4), s(ay - rr), s(ax + rr * 1.4), s(ay + rr)), outline=(255, 90, 120, 230), width=int(s(8)))
        d.ellipse((s(ax - 25), s(ay - 18), s(ax + 25), s(ay + 18)), fill=(255, 90, 120))
        # satélite passando com faíscas
        a = gt * 0.7
        sx, sy = cx + 420 * math.cos(a), cy + 380 * math.sin(a) * 0.6
        satellite(d, sx, sy, 0.5, ang=a)
        if abs(sx - ax) < 260 and (gt * 6) % 1 < 0.5:
            star(d, s(sx), s(sy), s(40), (255, 240, 120, 255))
        k = ease_back((u - 0.3) / 0.3)
        if k > 0: pill(d, 820, 200, 380, 100, "RADIAÇÃO", 58, bg=(255, 90, 120), fg=WHITE, k=k)
        paste_crow(img, s(880), s(880) + bob, s(300), gt, angle=tilt * 0.5, flip=True)
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
