"""Voyager 1 a um dia-luz (27/11/2026) — baseado em make_elnino.py (mesmo corvo, fundo roxo, 6 fatos)."""
import math, sys, os
from PIL import Image, ImageDraw
import make_corvo as C
import make_lua as L
from make_corvo import (W, H, FPS, YELLOW, WHITE, SOFT, paste_crow, star, LH, S2)
from make import ease_out, ease_back
from make_lua import ctext as _ctext
def ctext(d, x, y, s_, size, fill):
    if size >= 2: _ctext(d, x, y, s_, size, fill)

RED = (240, 80, 70); ORANGE = (255, 150, 60); BLUE = (70, 140, 240); DBLUE = (40, 80, 170)
GOLD = (230, 180, 70); DGOLD = (170, 120, 40); METAL = (200, 200, 215); DARK = (40, 30, 70)
PAPER = (245, 240, 255)

SCENES = [
    dict(kind="hook", dur=4.0, label="EM ALTA", title="Voyager 1 a um dia-luz da Terra!",
         body="Primeiro objeto humano a chegar tão longe. 6 fatos sobre ela."),
    dict(kind="dialuz", dur=5.0, label="FATO 01 / 06", title="Mensagem leva 1 dia pra chegar",
         body="Ela está a quase 26 bilhões de km. A resposta leva mais 1 dia pra voltar."),
    dict(kind="lancamento", dur=5.0, label="FATO 02 / 06", title="Lançada em 1977",
         body="Quase 50 anos no espaço. E a gêmea, Voyager 2, saiu 16 dias antes."),
    dict(kind="velocidade", dur=5.0, label="FATO 03 / 06", title="61 mil km por hora",
         body="Nesse ritmo, daria pra ir da Terra à Lua em menos de 7 horas."),
    dict(kind="disco", dur=5.0, label="FATO 04 / 06", title="Leva um disco de ouro",
         body="Saudações em 55 línguas. Em português: “Paz e felicidade a todos”."),
    dict(kind="interestelar", dur=5.0, label="FATO 05 / 06", title="Saiu da “bolha” do Sol",
         body="Em 2012, foi o 1º objeto humano a entrar no espaço interestelar."),
    dict(kind="energia", dur=5.0, label="FATO 06 / 06", title="Sinal de lâmpada de geladeira",
         body="A energia de plutônio cai uns 4 watts por ano: só 2 instrumentos seguem ligados."),
    dict(kind="outro", dur=4.5, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]
L.SCENES = C.SCENES = SCENES

def s(v): return v * S2

def probe(d, cx, cy, sc=1.0, ang=0.0):
    """Sonda original simplificada: antena parabólica, corpo, haste e braço."""
    def P(x, y):
        ca, sa = math.cos(ang), math.sin(ang)
        return (s(cx + (x * ca - y * sa) * sc), s(cy + (x * sa + y * ca) * sc))
    # hastes
    d.line([P(0, 40), P(-230, 120)], fill=METAL, width=int(s(8 * sc)))
    d.line([P(0, 40), P(220, 60)], fill=METAL, width=int(s(8 * sc)))
    d.ellipse([P(-250, 100)[0] - s(22 * sc), P(-250, 100)[1] - s(22 * sc), P(-250, 100)[0] + s(22 * sc), P(-250, 100)[1] + s(22 * sc)], fill=(150, 150, 170))
    d.rectangle([P(210, 45)[0] - s(16 * sc), P(210, 45)[1] - s(16 * sc), P(210, 45)[0] + s(16 * sc), P(210, 45)[1] + s(16 * sc)], fill=(150, 150, 170))
    # corpo
    d.polygon([P(-45, 10), P(45, 10), P(55, 70), P(-55, 70)], fill=(120, 110, 150))
    # disco dourado
    d.ellipse([P(30, 40)[0] - s(14 * sc), P(30, 40)[1] - s(14 * sc), P(30, 40)[0] + s(14 * sc), P(30, 40)[1] + s(14 * sc)], fill=GOLD)
    # antena
    pts = [P(130 * math.cos(t), -20 + 45 * math.sin(t)) for t in [i * math.pi / 20 for i in range(0, 21)]]
    d.polygon(pts, fill=PAPER)
    d.line([P(-130, -20), P(130, -20)], fill=(210, 205, 230), width=int(s(6 * sc)))
    d.line([P(0, -20), P(0, -90)], fill=METAL, width=int(s(6 * sc)))
    d.line([P(0, 10), P(0, -20)], fill=METAL, width=int(s(10 * sc)))

def planet(d, cx, cy, r, col, ring=False):
    d.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), fill=col)
    if ring:
        d.arc((s(cx - r * 1.9), s(cy - r * 0.5), s(cx + r * 1.9), s(cy + r * 0.5)), 160, 380, fill=(240, 220, 170), width=int(s(10)))

def earth(d, cx, cy, r):
    d.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), fill=(60, 120, 220))
    for (ox, oy, rx, ry) in [(-0.3, -0.2, 0.35, 0.25), (0.25, 0.25, 0.3, 0.3), (0.2, -0.45, 0.2, 0.12)]:
        d.ellipse((s(cx + (ox - rx) * r), s(cy + (oy - ry) * r), s(cx + (ox + rx) * r), s(cy + (oy + ry) * r)), fill=(80, 190, 120))

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
        earth(d, 170, 860, 110)
        # trilha de luz até a sonda
        for k in range(14):
            p = ((gt * 0.4) + k / 14) % 1
            x = 250 + 650 * p; y = 800 - 600 * p
            d.ellipse((s(x - 8), s(y - 8), s(x + 8), s(y + 8)), fill=(255, 214, 102, int(220 * (1 - p * 0.6))))
        probe(d, 860, 190 + math.sin(gt * 1.3) * 10, 0.8, ang=-0.35 + 0.05 * math.sin(gt))
        paste_crow(img, s(560), s(640) + bob, s(560), gt, angle=tilt)
        for i, (sx, sy, r) in enumerate([(150, 140, 30), (1000, 520, 24), (110, 420, 20), (560, 80, 18)]):
            k = 0.7 + 0.3 * math.sin(gt * 3 + i)
            star(d, s(sx), s(sy), s(r) * k, (255, 214, 102, 230))
    elif kind == "dialuz":
        earth(d, 150, 560, 90)
        probe(d, 900, 520, 0.6, ang=-0.2)
        # pulso de luz viajando
        d.line([(s(250), s(560)), (s(780), s(560))], fill=(255, 255, 255, 50), width=int(s(6)))
        p = (u * 1.4) % 1
        x = 250 + 530 * p
        for j in range(6):
            xx = x - j * 18
            if xx > 250: d.ellipse((s(xx - 16 + j * 2), s(544 + j * 2), s(xx + 16 - j * 2), s(576 - j * 2)), fill=(255, 214, 102, 230 - j * 35))
        # relógio 24h
        kx, ky, kr = 540, 230, 120
        d.ellipse((s(kx - kr), s(ky - kr), s(kx + kr), s(ky + kr)), fill=PAPER)
        a = gt * 2.5
        d.line([(s(kx), s(ky)), (s(kx + 95 * math.sin(a)), s(ky - 95 * math.cos(a)))], fill=RED, width=int(s(10)))
        d.line([(s(kx), s(ky)), (s(kx + 55 * math.sin(a / 12)), s(ky - 55 * math.cos(a / 12)))], fill=DARK, width=int(s(14)))
        pill(d, 540, 680, 380, 110, "24 HORAS", 70, k=ease_back((u - 0.2) / 0.3))
        paste_crow(img, s(540), s(900) + bob, s(360), gt, angle=tilt * 0.5)
    elif kind == "lancamento":
        # dois foguetes, um subindo antes do outro
        for i, (x, delay, lab) in enumerate([(320, 0.0, "V2"), (700, 0.25, "V1")]):
            p = ease_out(max(0, min(1, (u - delay) / 0.6)))
            y = 760 - 520 * p
            d.polygon([(s(x - 40), s(y)), (s(x + 40), s(y)), (s(x + 40), s(y + 230)), (s(x - 40), s(y + 230))], fill=PAPER)
            d.polygon([(s(x - 40), s(y)), (s(x + 40), s(y)), (s(x), s(y - 80))], fill=RED)
            d.polygon([(s(x - 40), s(y + 160)), (s(x - 85), s(y + 240)), (s(x - 40), s(y + 230))], fill=RED)
            d.polygon([(s(x + 40), s(y + 160)), (s(x + 85), s(y + 240)), (s(x + 40), s(y + 230))], fill=RED)
            if p > 0.02:
                fl = 1 + 0.2 * math.sin(gt * 30 + i)
                d.polygon([(s(x - 30), s(y + 230)), (s(x + 30), s(y + 230)), (s(x), s(y + 230 + 140 * fl))], fill=ORANGE)
                d.polygon([(s(x - 15), s(y + 230)), (s(x + 15), s(y + 230)), (s(x), s(y + 230 + 80 * fl))], fill=YELLOW)
            ctext(d, s(x), s(y + 70), lab, s(54), DARK)
        pill(d, 510, 40, 340, 120, "1977", 90, k=ease_back((u - 0.1) / 0.3))
        paste_crow(img, s(900), s(880) + bob, s(360), gt, angle=tilt * 0.5, flip=True)
    elif kind == "velocidade":
        earth(d, 160, 380, 120)
        # Lua
        d.ellipse((s(840), s(300), s(1000), s(460)), fill=(215, 215, 225))
        d.ellipse((s(880), s(340), s(915), s(375)), fill=(180, 180, 195))
        d.ellipse((s(930), s(400), s(955), s(425)), fill=(180, 180, 195))
        # sonda indo da Terra à Lua, linhas de velocidade
        p = (u * 1.2) % 1
        x = 300 + 500 * ease_out(p)
        for k in range(5):
            d.line([(s(x - 150 - k * 30), s(330 + k * 25)), (s(x - 60 - k * 20), s(330 + k * 25))], fill=(255, 255, 255, 120), width=int(s(6)))
        probe(d, x, 360, 0.45)
        pill(d, 540, 560, 520, 120, "< 7 HORAS", 80, k=ease_back((u - 0.25) / 0.3))
        paste_crow(img, s(540), s(870) + bob, s(360), gt, angle=tilt * 0.5)
    elif kind == "disco":
        cx, cy, R = 470, 420, 290
        k = ease_back(u / 0.35)
        if k > 0:
            r = R * k
            d.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), fill=GOLD)
            for j in range(1, 8):
                rr = r * (0.3 + j * 0.09)
                d.ellipse((s(cx - rr), s(cy - rr), s(cx + rr), s(cy + rr)), outline=DGOLD, width=int(s(3)))
            d.ellipse((s(cx - r * 0.22), s(cy - r * 0.22), s(cx + r * 0.22), s(cy + r * 0.22)), fill=DGOLD)
            d.ellipse((s(cx - 10), s(cy - 10), s(cx + 10), s(cy + 10)), fill=DARK)
            # brilho girando
            a = gt * 1.5
            d.line([(s(cx + r * 0.3 * math.cos(a)), s(cy + r * 0.3 * math.sin(a))), (s(cx + r * 0.95 * math.cos(a)), s(cy + r * 0.95 * math.sin(a)))], fill=(255, 245, 200, 160), width=int(s(10)))
        pill(d, 470, 750, 280, 110, "55", 80, k=ease_back((u - 0.2) / 0.3))
        if u > 0.35:
            ctext(d, s(470), s(865), "LÍNGUAS", s(56), WHITE)
        # balão de fala
        k2 = ease_back((u - 0.35) / 0.3)
        if k2 > 0:
            d.rounded_rectangle((s(760), s(110), s(760 + 280 * k2), s(260)), radius=s(40), fill=PAPER)
            d.polygon([(s(800), s(250)), (s(860), s(250)), (s(790), s(310))], fill=PAPER)
            if k2 > 0.8: ctext(d, s(900), s(140), "Olá!", s(70), DARK)
        paste_crow(img, s(880), s(620) + bob, s(360), gt, angle=tilt * 0.5, flip=True)
    elif kind == "interestelar":
        # Sol e bolha (heliosfera)
        cx, cy = 380, 470
        for j, (r, al) in enumerate([(330, 40), (300, 50)]):
            d.ellipse((s(cx - r * 1.15), s(cy - r), s(cx + r * 0.9), s(cy + r)), outline=(150, 200, 255, 180 - j * 60), width=int(s(10)))
        d.ellipse((s(cx - 330 * 1.15), s(cy - 330), s(cx + 330 * 0.9), s(cy + 330)), fill=(150, 200, 255, 25))
        for i in range(12):
            a = i * math.pi / 6 + gt * 0.4
            d.line([(s(cx + math.cos(a) * 95), s(cy + math.sin(a) * 95)), (s(cx + math.cos(a) * 125), s(cy + math.sin(a) * 125))], fill=(255, 200, 70), width=int(s(10)))
        d.ellipse((s(cx - 75), s(cy - 75), s(cx + 75), s(cy + 75)), fill=(255, 200, 70))
        # sonda saindo da bolha
        p = ease_out(min(1, u / 0.7))
        px = 560 + 380 * p; py = 300 - 120 * p
        probe(d, px, py, 0.4, ang=-0.3)
        pill(d, 820, 640, 260, 110, "2012", 80, k=ease_back((u - 0.3) / 0.3))
        paste_crow(img, s(840), s(880) + bob, s(340), gt, angle=tilt * 0.5, flip=True)
    elif kind == "energia":
        # lâmpada
        bx, by = 300, 330
        glow = 0.6 + 0.4 * math.sin(gt * 4)
        d.ellipse((s(bx - 170), s(by - 170), s(bx + 170), s(by + 170)), fill=(255, 220, 120, int(50 * glow)))
        d.ellipse((s(bx - 110), s(by - 120), s(bx + 110), s(by + 100)), fill=(255, 230, 150))
        d.rectangle((s(bx - 55), s(by + 80), s(bx + 55), s(by + 170)), fill=METAL)
        for j in range(3):
            d.line([(s(bx - 55), s(by + 105 + j * 25)), (s(bx + 55), s(by + 105 + j * 25))], fill=(150, 150, 170), width=int(s(6)))
        # bateria descendo
        ux, uy, uw, uh = 760, 170, 200, 400
        d.rounded_rectangle((s(ux - 40), s(uy - 40), s(ux + 40), s(uy)), radius=s(10), fill=PAPER)
        d.rounded_rectangle((s(ux - uw / 2), s(uy), s(ux + uw / 2), s(uy + uh)), radius=s(30), outline=PAPER, width=int(s(14)))
        lvl = 0.75 - 0.5 * ease_out(min(1, u / 0.8))
        col = YELLOW if lvl > 0.4 else RED
        d.rounded_rectangle((s(ux - uw / 2 + 20), s(uy + 20 + (uh - 40) * (1 - lvl)), s(ux + uw / 2 - 20), s(uy + uh - 20)), radius=s(16), fill=col)
        pill(d, 760, 620, 300, 100, "-4 W/ano", 62, k=ease_back((u - 0.25) / 0.3))
        paste_crow(img, s(420), s(850) + bob, s(360), gt, angle=tilt * 0.5)
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
