"""Black Friday (27/11/2026) — baseado em make_lua.py / make_corvo.py (mesmo corvo, fundo roxo, 6 fatos)."""
import math, sys, os
from PIL import Image, ImageDraw
import make_corvo as C
import make_lua as L
from make_corvo import (W, H, FPS, YELLOW, WHITE, SOFT, paste_crow, star, LH, S2)
from make import ease_out, ease_back
from make_lua import ctext

RED = (235, 70, 80); GREEN = (80, 200, 120); GOLD = (245, 190, 60); INK = (30, 20, 50)

SCENES = [
    dict(kind="hook", dur=4.0, label="EM ALTA", title="Black Friday: de onde veio esse nome?",
         body="É nesta sexta, 27/11!"),
    dict(kind="gold", dur=5.0, label="FATO 01 / 06", title="A 1ª Black Friday foi um crash",
         body="Em setembro de 1869, o mercado de ouro dos EUA quebrou. Nada de promoção."),
    dict(kind="police", dur=5.0, label="FATO 02 / 06", title="O nome veio da polícia",
         body="Na Filadélfia, o dia após o Dia de Ação de Graças era caos de multidão e trânsito."),
    dict(kind="big", dur=5.0, label="FATO 03 / 06", title="Tentaram virar “Big Friday”",
         body="Os lojistas odiaram o apelido e quiseram trocar. Não colou."),
    dict(kind="ledger", dur=5.0, label="FATO 04 / 06", title="O “sair do vermelho” é mais novo",
         body="Essa explicação só apareceu nos anos 80, bem depois do nome."),
    dict(kind="calendar", dur=5.0, label="FATO 05 / 06", title="O feriado que mudou de data",
         body="Em 1939, Roosevelt adiantou o feriado para esticar as compras."),
    dict(kind="brazil", dur=5.0, label="FATO 06 / 06", title="No Brasil, chegou em 2010",
         body="Só na internet, com cerca de 50 lojas. Hoje é febre no país todo."),
    dict(kind="outro", dur=4.5, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]
L.SCENES = C.SCENES = SCENES

def s(v): return v * S2

def bag(d, cx, cy, sc, txt=True):
    w, h = 230 * sc, 270 * sc
    d.arc((s(cx - 80 * sc), s(cy - h / 2 - 90 * sc), s(cx + 80 * sc), s(cy - h / 2 + 70 * sc)), 180, 360, fill=YELLOW, width=int(s(16 * sc)))
    d.rounded_rectangle((s(cx - w / 2), s(cy - h / 2), s(cx + w / 2), s(cy + h / 2)), radius=s(26 * sc), fill=(22, 18, 34))
    d.rounded_rectangle((s(cx - w / 2), s(cy - h / 2), s(cx + w / 2), s(cy + h / 2)), radius=s(26 * sc), outline=YELLOW, width=int(s(6 * sc)))
    if txt:
        ctext(d, s(cx), s(cy - 80 * sc), "BLACK", s(52 * sc), WHITE)
        ctext(d, s(cx), s(cy - 10 * sc), "FRIDAY", s(48 * sc), YELLOW)

def tag(d, cx, cy, txt, sc=1.0, col=RED, ang=0):
    w, h = 150 * sc, 80 * sc
    d.polygon([(s(cx - w / 2), s(cy - h / 2)), (s(cx + w / 2 - 25 * sc), s(cy - h / 2)), (s(cx + w / 2), s(cy)),
               (s(cx + w / 2 - 25 * sc), s(cy + h / 2)), (s(cx - w / 2), s(cy + h / 2))], fill=col)
    ctext(d, s(cx - 10 * sc), s(cy - 30 * sc), txt, s(48 * sc), WHITE)

def car(d, x, y, col, sc=1.0):
    d.rounded_rectangle((s(x), s(y + 30 * sc), s(x + 170 * sc), s(y + 90 * sc)), radius=s(20 * sc), fill=col)
    d.rounded_rectangle((s(x + 30 * sc), s(y), s(x + 130 * sc), s(y + 50 * sc)), radius=s(16 * sc), fill=col)
    d.rectangle((s(x + 45 * sc), s(y + 10 * sc), s(x + 115 * sc), s(y + 34 * sc)), fill=(190, 220, 255))
    for wx in (35, 135):
        d.ellipse((s(x + (wx - 20) * sc), s(y + 70 * sc), s(x + (wx + 20) * sc), s(y + 110 * sc)), fill=(20, 20, 28))

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    bob = math.sin(gt * 1.8) * 14 * S2; tilt = math.sin(gt * 0.9) * 6; u = lt / dur
    if kind in ("hook", "outro"):
        pulse = 1 + 0.03 * math.sin(gt * 2.5)
        bag(d, 760, 430, 1.15 * pulse)
        tag(d, 560, 300, "-50%", 1.0, RED)
        tag(d, 950, 640, "27/11", 1.0, (120, 80, 220))
        paste_crow(img, s(330), s(700) + bob, s(760), gt, angle=tilt)
        for i, (sx, sy, r) in enumerate([(150, 140, 30), (1000, 120, 24), (110, 420, 20), (450, 60, 18)]):
            k = 0.7 + 0.3 * math.sin(gt * 3 + i)
            star(d, s(sx), s(sy), s(r) * k, (255, 214, 102, 230))
    elif kind == "gold":
        # falling chart
        d.line([(s(470), s(120)), (s(470), s(600)), (s(1020), s(600))], fill=(255, 255, 255, 120), width=s(6))
        pts = [(480, 160), (600, 190), (700, 150), (780, 300), (860, 260), (1000, 560)]
        k = ease_out((u - 0.05) / 0.6)
        n = max(2, int(2 + k * (len(pts) - 2) + 0.999))
        seg = pts[:n]
        d.line([(s(x), s(y)) for x, y in seg], fill=RED, width=s(14), joint="curve")
        ex, ey = seg[-1]
        d.polygon([(s(ex), s(ey + 40)), (s(ex - 40), s(ey - 15)), (s(ex + 30), s(ey - 25))], fill=RED)
        ctext(d, s(745), s(630), "1869", s(80), YELLOW)
        # gold bars
        for i, (bx, by) in enumerate([(560, 960), (720, 960), (640, 890)]):
            fall = ease_out((u - 0.2 - i * 0.1) / 0.3)
            yy = by - (1 - fall) * 300
            if fall <= 0: continue
            d.polygon([(s(bx), s(yy)), (s(bx + 140), s(yy)), (s(bx + 120), s(yy - 55)), (s(bx + 20), s(yy - 55))], fill=GOLD)
            d.polygon([(s(bx + 20), s(yy - 55)), (s(bx + 120), s(yy - 55)), (s(bx + 110), s(yy - 45)), (s(bx + 30), s(yy - 45))], fill=(255, 225, 130))
        paste_crow(img, s(230), s(760) + bob, s(480), gt, angle=tilt * 0.5)
    elif kind == "police":
        # road
        d.rectangle((0, s(600), lw, s(820)), fill=(45, 40, 70))
        for i in range(6):
            x = ((i * 220 - gt * 40) % 1300) - 100
            d.rectangle((s(x), s(685), s(x + 110), s(697)), fill=(255, 255, 255, 140))
        cols = [(230, 80, 90), (90, 160, 240), (250, 200, 70), (120, 210, 140), (200, 120, 230)]
        for i in range(5):
            jig = math.sin(gt * 6 + i) * 3
            car(d, 20 + i * 210, 640 + jig, cols[i], 0.95)
        # crowd heads
        for i in range(14):
            x = 40 + i * 75; y = 430 + (i % 2) * 25 + math.sin(gt * 4 + i) * 6
            d.ellipse((s(x), s(y), s(x + 50), s(y + 50)), fill=(240, 200, 160) if i % 3 else (150, 100, 70))
            d.rounded_rectangle((s(x - 5), s(y + 50), s(x + 55), s(y + 110)), radius=s(20), fill=cols[i % 5])
        # police badge
        bx, by, br = 820, 200, 140
        k = ease_back((u - 0.1) / 0.35)
        if k > 0:
            pts = []
            for j in range(12):
                a = j * math.pi / 6 - math.pi / 2; rr = br * k * (1 if j % 2 == 0 else 0.72)
                pts.append((s(bx + rr * math.cos(a)), s(by + rr * math.sin(a))))
            d.polygon(pts, fill=GOLD)
            d.ellipse((s(bx - 70 * k), s(by - 70 * k), s(bx + 70 * k), s(by + 70 * k)), fill=(60, 70, 140))
            if k > 0.6: ctext(d, s(bx), s(by - 34), "PD", s(60), WHITE)
        ctext(d, s(720), s(870), "CAOS!", s(90), YELLOW)
        paste_crow(img, s(250), s(880) + bob, s(380), gt, angle=tilt * 0.4)
    elif kind == "big":
        # two signs: BLACK FRIDAY (kept) and BIG FRIDAY (crossed)
        d.rounded_rectangle((s(440), s(80), s(1020), s(260)), radius=s(30), fill=(20, 16, 30))
        d.rounded_rectangle((s(440), s(80), s(1020), s(260)), radius=s(30), outline=YELLOW, width=s(6))
        ctext(d, s(730), s(125), "BLACK FRIDAY", s(64), WHITE)
        k = ease_back((u - 0.1) / 0.3)
        if k > 0:
            d.rounded_rectangle((s(730 - 290 * k), s(360), s(730 + 290 * k), s(540)), radius=s(30), fill=(245, 240, 255))
            if k > 0.6: ctext(d, s(730), s(405), "BIG FRIDAY", s(66), INK)
        x = ease_out((u - 0.45) / 0.25)
        if x > 0:
            d.line([(s(470), s(560)), (s(470 + 520 * x), s(560 - 220 * x))], fill=RED, width=s(18))
            d.line([(s(990), s(560)), (s(990 - 520 * x), s(560 - 220 * x))], fill=RED, width=s(18))
        if u > 0.7: ctext(d, s(730), s(600), "não colou!", s(66), YELLOW)
        paste_crow(img, s(260), s(740) + bob, s(520), gt, angle=math.sin(gt * 5) * 8)
    elif kind == "ledger":
        # account book
        X0, Y0, X1, Y1 = 470, 90, 1010, 640
        d.rounded_rectangle((s(X0), s(Y0), s(X1), s(Y1)), radius=s(24), fill=(250, 246, 235))
        for i in range(7):
            y = Y0 + 80 + i * 70
            d.line([(s(X0 + 30), s(y)), (s(X1 - 30), s(y))], fill=(180, 200, 230), width=s(3))
        d.line([(s(X0 + 330), s(Y0 + 20)), (s(X0 + 330), s(Y1 - 20))], fill=(235, 140, 140), width=s(3))
        k = ease_out((u - 0.25) / 0.35)
        ctext(d, s(740), s(170), "LUCRO", s(54), (90, 90, 110))
        if k < 0.5:
            ctext(d, s(740), s(290), "-R$ 100", s(90), RED)
        else:
            ctext(d, s(740), s(290), "+R$ 100", s(90), (30, 150, 80))
        ctext(d, s(740), s(470), "anos 80", s(76), INK)
        paste_crow(img, s(240), s(740) + bob, s(520), gt, angle=tilt * 0.5)
    elif kind == "calendar":
        X, Y, w2, h2 = 690, 380, 330, 300
        d.rounded_rectangle((s(X - w2), s(Y - h2), s(X + w2), s(Y + h2)), radius=s(30), fill=(245, 240, 255))
        d.rounded_rectangle((s(X - w2), s(Y - h2), s(X + w2), s(Y - h2 + 110)), radius=s(30), fill=RED)
        d.rectangle((s(X - w2), s(Y - h2 + 70), s(X + w2), s(Y - h2 + 110)), fill=RED)
        ctext(d, s(X), s(Y - h2 + 18), "NOV 1939", s(66), WHITE)
        cw = 2 * w2 / 7
        for idx in range(30):
            day = idx + 1; col = (idx + 3) % 7; row = (idx + 3) // 7
            cx = X - w2 + cw * (col + 0.5); cy = Y - h2 + 150 + row * 85
            fill = (120, 110, 150)
            if day in (23, 30):
                fill = INK
                if day == 23 and u > 0.45:
                    r = 42 * ease_back((u - 0.45) / 0.25)
                    d.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), fill=GREEN)
                    fill = WHITE
            ctext(d, s(cx), s(cy - 22), str(day), s(40), fill)
            if day == 30:
                k = ease_out((u - 0.15) / 0.25)
                if k > 0:
                    d.line([(s(cx - 35), s(cy - 35)), (s(cx - 35 + 70 * k), s(cy - 35 + 70 * k))], fill=RED, width=s(10))
                    d.line([(s(cx + 35), s(cy - 35)), (s(cx + 35 - 70 * k), s(cy - 35 + 70 * k))], fill=RED, width=s(10))
        ctext(d, s(690), s(720), "1 semana antes!", s(66), YELLOW)
        paste_crow(img, s(230), s(800) + bob, s(440), gt, angle=tilt * 0.4)
    elif kind == "brazil":
        # laptop with cart
        X, Y = 720, 300
        d.rounded_rectangle((s(X - 280), s(Y - 190), s(X + 280), s(Y + 160)), radius=s(22), fill=(40, 40, 60))
        d.rounded_rectangle((s(X - 255), s(Y - 168), s(X + 255), s(Y + 138)), radius=s(10), fill=(70, 160, 110))
        d.polygon([(s(X - 340), s(Y + 175)), (s(X + 340), s(Y + 175)), (s(X + 300), s(Y + 210)), (s(X - 300), s(Y + 210))], fill=(150, 150, 175))
        # cart
        cx, cy = X - 30, Y - 30
        d.line([(s(cx - 140), s(cy - 80)), (s(cx - 100), s(cy - 80)), (s(cx - 60), s(cy + 40)), (s(cx + 100), s(cy + 40)), (s(cx + 130), s(cy - 50)), (s(cx - 85), s(cy - 50))], fill=WHITE, width=s(14), joint="curve")
        for wx in (-40, 80):
            d.ellipse((s(cx + wx - 18), s(cy + 60), s(cx + wx + 18), s(cy + 96)), fill=WHITE)
        k = ease_back((u - 0.1) / 0.3)
        if k > 0:
            r = 95 * k
            d.ellipse((s(X + 230 - r), s(Y - 210 - r), s(X + 230 + r), s(Y - 210 + r)), fill=YELLOW)
            if k > 0.6: ctext(d, s(X + 230), s(Y - 250), "2010", s(64), INK)
        # little stores
        for i in range(5):
            kk = ease_back((u - 0.35 - i * 0.07) / 0.25)
            if kk <= 0: continue
            x = 470 + i * 115; y = 640
            d.rectangle((s(x), s(y - 70 * kk), s(x + 90), s(y)), fill=(245, 240, 255))
            for j in range(4):
                d.rectangle((s(x + j * 22.5), s(y - 90 * kk), s(x + j * 22.5 + 22.5), s(y - 70 * kk)), fill=RED if j % 2 == 0 else WHITE)
        if u > 0.6: ctext(d, s(700), s(670), "~50 lojas", s(66), YELLOW)
        paste_crow(img, s(210), s(800) + bob, s(440), gt, angle=tilt * 0.4)
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
            ims.append(L.frame_at(SCENES[i], L.build_text(SCENES[i]), lt, st[i] + lt).resize((360, 640)))
        sh = Image.new("RGB", (360 * 4, 640 * 2)); [sh.paste(im, ((k % 4) * 360, (k // 4) * 640)) for k, im in enumerate(ims)]
        sh.save("outc/sheet.jpg", quality=88)
    else:
        only = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else range(len(SCENES))
        for i in only: C.render_scene(i, st[i])
