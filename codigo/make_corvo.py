import math, random, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make as M
from make import ease_out, ease_back, text_sprite, pill_sprite, with_alpha, f_title, f_title_s, f_body, f_label, F

W, H, FPS = 1080, 1920, 30
YELLOW, WHITE, SOFT = (255, 209, 102), (255, 255, 255), (215, 205, 245)

SCENES = [
    dict(kind="hook", dur=4.0, label="VOCÊ SABIA?", title="5 fatos que provam que o corvo é um gênio", body=None),
    dict(kind="faces", dur=5.0, label="FATO 01 / 05", title="Ele lembra do seu rosto",
         body="E guarda rancor de quem o ameaçou por mais de dois anos."),
    dict(kind="tools", dur=5.0, label="FATO 02 / 05", title="Fabrica ferramentas",
         body="Corvos-da-nova-caledônia dobram galhos para fazer ganchos."),
    dict(kind="water", dur=5.0, label="FATO 03 / 05", title="Resolve a fábula de Esopo",
         body="Joga pedras na água para o nível subir e alcançar a comida."),
    dict(kind="funeral", dur=5.0, label="FATO 04 / 05", title="Faz “funerais”",
         body="O bando se reúne em volta de um corvo morto para descobrir o que é perigoso."),
    dict(kind="zero", dur=5.0, label="FATO 05 / 05", title="Entende o zero",
         body="Sabe que “nada” também é uma quantidade."),
    dict(kind="outro", dur=4.5, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e segue pra mais curiosidades!"),
]

# ---------- background ----------
yy = np.linspace(0, 1, H)[:, None]
top, bot = np.array([62, 38, 112]), np.array([12, 9, 30])
g = np.zeros((H, W, 3), np.float32)
for c in range(3): g[:, :, c] = top[c] * (1 - yy ** 0.8) + bot[c] * yy ** 0.8
xx = np.linspace(-1, 1, W)[None, :]
glow = np.exp(-((xx) ** 2 * 2.2 + ((np.linspace(0, 1, H)[:, None] - 0.62) ** 2) * 9))
g += glow[:, :, None] * np.array([60, 40, 50])
BG = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

def sparkle_sprite(r):
    s = 4; R = r * s
    img = Image.new("RGBA", (4 * R, 4 * R), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    c = 2 * R
    d.ellipse((c - R * 1.6, c - R * 1.6, c + R * 1.6, c + R * 1.6), fill=(255, 220, 160, 25))
    pts = []
    for i in range(8):
        a = i * math.pi / 4; rr = R if i % 2 == 0 else R * 0.25
        pts.append((c + rr * math.sin(a), c - rr * math.cos(a)))
    d.polygon(pts, fill=(255, 236, 190, 200))
    return img.resize((img.width // s, img.height // s), Image.LANCZOS)

rng = random.Random(11)
PARTS = [dict(x=rng.uniform(30, W - 30), y0=rng.uniform(0, H), sp=rng.uniform(15, 45),
              ph=rng.uniform(0, 6.28), spr=sparkle_sprite(rng.choice([5, 7, 9, 12]))) for _ in range(22)]

def draw_parts(fr, gt):
    for p in PARTS:
        y = (p["y0"] - p["sp"] * gt) % (H + 80) - 40
        x = p["x"] + math.sin(gt * 0.7 + p["ph"]) * 14
        a = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(gt * 2.2 + p["ph"]))
        fr.alpha_composite(with_alpha(p["spr"], a), (int(x), int(y)))

def rays(gt):
    lw, lh = 270, 480
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for i in range(4):
        cx = 40 + i * 65 + math.sin(gt * 0.3 + i * 1.7) * 18
        a = int(12 + 8 * math.sin(gt * 0.7 + i * 2.1))
        d.polygon([(cx - 6, -5), (cx + 6, -5), (cx + 50, lh), (cx - 20, lh)], fill=(210, 190, 255, a))
    return img.filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR)

# ---------- crow sprite ----------
_cache = {}
def crow_sprite(f, blink=False, angry=False):
    """f = pixels per design unit; design box 1080x1080 (bird spans ~300-900 x, 190-930 y)."""
    key = (round(f, 3), blink, angry)
    if key in _cache: return _cache[key]
    S = int(1080 * f)
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    P = lambda x, y: (x * f, y * f)
    def ell(cx, cy, rx, ry, fill): d.ellipse((f * (cx - rx), f * (cy - ry), f * (cx + rx), f * (cy + ry)), fill=fill)
    def poly(pts, fill): d.polygon([P(*p) for p in pts], fill=fill)
    BODY, DARK, SHEEN = (30, 30, 48), (18, 18, 30), (92, 104, 190)
    poly([(420, 700), (300, 900), (360, 915), (410, 880), (440, 930), (500, 780)], DARK)
    for fx in (500, 590):
        d.line([P(fx, 820), P(fx - 8, 900)], fill=(70, 70, 84), width=max(1, int(14 * f)))
        for dx in (-30, 0, 26): d.line([P(fx - 8, 900), P(fx - 8 + dx, 925)], fill=(70, 70, 84), width=max(1, int(11 * f)))
    ell(540, 640, 215, 235, BODY)
    d.arc(P(360, 430) + P(720, 860), 200, 250, fill=SHEEN, width=max(1, int(16 * f)))
    d.chord(P(330, 520) + P(590, 860), 200, 420, fill=DARK)
    poly([(345, 760), (300, 850), (380, 800)], DARK)
    for a in (0, 1, 2):
        d.arc(P(350 + a * 20, 560 + a * 40) + P(570 - a * 10, 840), 95, 160, fill=(52, 52, 82), width=max(1, int(7 * f)))
    ell(600, 390, 165, 155, BODY)
    d.arc(P(460, 250) + P(740, 530), 200, 260, fill=SHEEN, width=max(1, int(14 * f)))
    poly([(560, 245), (590, 190), (605, 245)], BODY); poly([(600, 240), (650, 200), (640, 255)], BODY)
    poly([(720, 380), (860, 425), (720, 460)], (70, 72, 88))
    poly([(720, 380), (860, 425), (725, 418)], (110, 112, 130))
    if blink:
        d.arc(P(600, 330) + P(700, 400), 10, 170, fill=(230, 230, 240), width=max(1, int(9 * f)))
    else:
        ell(650, 365, 58, 62, (255, 255, 255)); ell(660, 372, 36, 38, (255, 186, 40))
        ell(664, 376, 19, 21, (15, 12, 25)); ell(672, 360, 9, 9, (255, 255, 255))
    if angry: d.line([P(590, 270), P(705, 318)], fill=DARK, width=max(1, int(16 * f)))
    else: d.line([P(595, 290), P(700, 300)], fill=DARK, width=max(1, int(12 * f)))
    ell(640, 448, 28, 14, (255, 120, 150, 110))
    _cache[key] = img
    return img

def paste_crow(layer, cx, cy, size, t, angle=0.0, flip=False, blink=None, angry=False, alpha=1.0):
    """size = on-layer pixel width of the 1080 design box; (cx,cy) = where design point (560,560) lands."""
    f = size / 1080
    if blink is None: blink = (t % 3.4) < 0.13
    spr = crow_sprite(f, blink, angry)
    if flip: spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    if abs(angle) > 0.2: spr = spr.rotate(angle, resample=Image.BICUBIC, center=(spr.width / 2, spr.height * 0.6))
    if alpha < 1: spr = with_alpha(spr, alpha)
    layer.alpha_composite(spr, (int(cx - spr.width * 0.52), int(cy - spr.height * 0.52)))

# ---------- illustrations (layer drawn at 2x) ----------
LY, LH, S2 = 760, 1060, 2

def star(d, cx, cy, r, fill):
    pts = []
    for i in range(8):
        a = i * math.pi / 4; rr = r if i % 2 == 0 else r * 0.28
        pts.append((cx + rr * math.sin(a), cy - rr * math.cos(a)))
    d.polygon(pts, fill=fill)

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    cx = lw / 2; bob = math.sin(gt * 1.8) * 14 * S2
    tilt = math.sin(gt * 0.9) * 6
    u = lt / dur
    if kind in ("hook", "outro"):
        paste_crow(img, cx, 520 * S2 + bob, 1000 * S2, gt, angle=tilt)
        for i, (sx, sy, r) in enumerate([(820, 150, 40), (900, 260, 22), (180, 230, 28)]):
            k = 0.7 + 0.3 * math.sin(gt * 3 + i)
            star(d, sx * S2, sy * S2, r * S2 * k, (255, 214, 102, 230))
    elif kind == "faces":
        paste_crow(img, 330 * S2, 560 * S2 + bob, 720 * S2, gt, angle=tilt * 0.5, angry=True)
        # person face
        fx, fy = 800 * S2, 470 * S2
        R = 150 * S2
        d.ellipse((fx - R, fy - R, fx + R, fy + R), fill=(242, 196, 160))
        d.chord((fx - R, fy - R * 1.05, fx + R, fy + R * 0.2), 180, 360, fill=(70, 46, 36))
        for ex in (-50, 50):
            d.ellipse((fx + ex * S2 - 14 * S2, fy + 10 * S2, fx + ex * S2 + 14 * S2, fy + 38 * S2), fill=(40, 30, 30))
        d.arc((fx - 45 * S2, fy + 70 * S2, fx + 45 * S2, fy + 120 * S2), 200, 340, fill=(120, 60, 60), width=8 * S2)
        # scan reticle
        p = (gt * 1.2) % 1.0
        rr = R * (1.25 + 0.15 * math.sin(gt * 4))
        for a0 in (0, 90, 180, 270):
            d.arc((fx - rr, fy - rr, fx + rr, fy + rr), a0 + 15, a0 + 75, fill=(255, 90, 90, 230), width=10 * S2)
        sy = fy - rr + 2 * rr * p
        d.line([(fx - rr * 0.9, sy), (fx + rr * 0.9, sy)], fill=(255, 90, 90, 150), width=5 * S2)
        # exclamation bubble
        if u > 0.25:
            k = ease_back((u - 0.25) / 0.15)
            bx, by, br = 520 * S2, 200 * S2, 60 * S2 * k
            d.ellipse((bx - br, by - br, bx + br, by + br), fill=(255, 90, 90))
            fb = ImageFont.truetype(F + "InterDisplay-Black.otf", max(1, int(90 * S2 * k)))
            d.text((bx - fb.getlength("!") / 2, by - 62 * S2 * k), "!", font=fb, fill=WHITE)
    elif kind == "tools":
        paste_crow(img, 420 * S2, 560 * S2 + bob, 820 * S2, gt, angle=tilt * 0.4)
        # twig held in beak, hooked end wobbling
        bx, by = (420 + (860 - 560) * 0.759) * S2, (560 + (425 - 560) * 0.759) * S2 + bob
        wob = math.sin(gt * 2.5) * 0.12
        pts = []
        L = 380 * S2
        for k in range(30):
            s = k / 29
            a = 0.55 + wob + (2.6 * max(0, s - 0.8) / 0.2 if s > 0.8 else 0)
            if k == 0: x, y = bx - 20 * S2, by
            else:
                x += math.cos(a) * L / 29; y += math.sin(a) * L / 29
            pts.append((x, y))
        d.line(pts, fill=(140, 96, 58), width=18 * S2, joint="curve")
        d.line(pts, fill=(176, 126, 80), width=8 * S2, joint="curve")
        # grub at the hook
        gx, gy = pts[-1]
        for i in range(4):
            r = (22 - i * 3) * S2
            d.ellipse((gx + i * 26 * S2 - r, gy + 20 * S2 - r, gx + i * 26 * S2 + r, gy + 20 * S2 + r), fill=(240, 220, 160))
    elif kind == "water":
        paste_crow(img, 330 * S2, 560 * S2 + bob, 720 * S2, gt, angle=-4 + tilt * 0.3)
        tx0, tx1, ty0, ty1 = 640 * S2, 900 * S2, 200 * S2, 900 * S2
        lvl = 0.25 + 0.5 * ease_out(min(1, max(0, (u - 0.1) / 0.75)))
        wy = ty1 - (ty1 - ty0) * lvl
        d.rectangle((tx0 + 10 * S2, wy, tx1 - 10 * S2, ty1 - 10 * S2), fill=(80, 150, 255, 170))
        d.line([(tx0 + 10 * S2, wy), (tx1 - 10 * S2, wy)], fill=(180, 220, 255, 220), width=6 * S2)
        # stones settled at bottom
        n_st = int(min(6, max(0, (u - 0.1) / 0.75 * 6)))
        for i in range(n_st):
            sx = tx0 + (45 + (i % 3) * 85) * S2; sy = ty1 - (45 + (i // 3) * 70) * S2
            d.ellipse((sx - 38 * S2, sy - 30 * S2, sx + 38 * S2, sy + 30 * S2), fill=(130, 130, 145))
        # falling stone
        if n_st < 6 and u > 0.1:
            ph = ((u - 0.1) / 0.75 * 6) % 1
            fy2 = ty0 - 120 * S2 + ph * (ty1 - ty0)
            fx2 = (tx0 + tx1) / 2
            d.ellipse((fx2 - 36 * S2, fy2 - 28 * S2, fx2 + 36 * S2, fy2 + 28 * S2), fill=(150, 150, 165))
        # floating treat
        d.ellipse(((tx0 + tx1) / 2 - 40 * S2, wy - 34 * S2, (tx0 + tx1) / 2 + 40 * S2, wy + 6 * S2), fill=(255, 170, 90))
        # glass
        d.rounded_rectangle((tx0, ty0, tx1, ty1), radius=30 * S2, outline=(220, 230, 255, 230), width=10 * S2)
        d.line([(tx0 + 35 * S2, ty0 + 60 * S2), (tx0 + 35 * S2, ty1 - 80 * S2)], fill=(255, 255, 255, 90), width=10 * S2)
    elif kind == "funeral":
        # fallen crow in the center, gathering crows around
        cx0, cy0 = cx, 600 * S2
        paste_crow(img, cx0 + 40 * S2, cy0 + 90 * S2, 420 * S2, gt, angle=95, blink=True, alpha=0.85)
        spots = [(-380, 0, False), (-300, -230, False), (300, -230, True), (380, 0, True), (0, -330, False)]
        for i, (dx, dy, fl) in enumerate(spots):
            k = ease_back((u - 0.05 - i * 0.08) / 0.3)
            if k <= 0: continue
            paste_crow(img, cx0 + dx * S2, cy0 + dy * S2 + math.sin(gt * 2 + i) * 8 * S2,
                       360 * S2 * min(1, k), gt + i * 0.7, angle=math.sin(gt * 1.3 + i) * 6, flip=fl)
        # alarm "caw" marks
        for i in range(3):
            p = (gt * 0.8 + i / 3) % 1
            r = (120 + p * 330) * S2
            d.arc((cx0 - r, cy0 - r * 0.7, cx0 + r, cy0 + r * 0.7), 200, 340, fill=(255, 209, 102, int(160 * (1 - p))), width=6 * S2)
    elif kind == "zero":
        paste_crow(img, 300 * S2, 600 * S2 + bob, 640 * S2, gt, angle=tilt * 0.5)
        # three cards with 2, 1, 0 dots; zero card glows
        cards = [(660, 240, 2), (860, 240, 1), (760, 560, 0)]
        for i, (x, y, n) in enumerate(cards):
            k = ease_back((u - 0.1 - i * 0.12) / 0.3)
            if k <= 0: continue
            w2, h2 = 85 * S2 * k, 110 * S2 * k
            X, Y = x * S2, y * S2
            if n == 0:
                gl = 0.5 + 0.5 * math.sin(gt * 4)
                for rr, al in ((40, 40), (25, 60)):
                    d.rounded_rectangle((X - w2 - rr * S2, Y - h2 - rr * S2, X + w2 + rr * S2, Y + h2 + rr * S2),
                                        radius=40 * S2, fill=(255, 209, 102, int(al * gl)))
            d.rounded_rectangle((X - w2, Y - h2, X + w2, Y + h2), radius=24 * S2, fill=(245, 240, 255))
            for j in range(n):
                dx = (j - (n - 1) / 2) * 70 * S2 * k
                d.ellipse((X + dx - 24 * S2 * k, Y - 24 * S2 * k, X + dx + 24 * S2 * k, Y + 24 * S2 * k), fill=(40, 30, 70))
            if n == 0 and k > 0.6:
                fb = ImageFont.truetype(F + "InterDisplay-Black.otf", int(130 * S2 * min(1, k)))
                d.text((X - fb.getlength("0") / 2, Y + h2 + 10 * S2), "0", font=fb, fill=(255, 209, 102))
    return img.resize((W, LH), Image.LANCZOS)

# ---------- frames ----------
def build_text(sc):
    items = [pill_sprite(sc["label"], f_label, (20, 30, 50), YELLOW)]
    tf = f_title if len(sc["title"]) < 26 else f_title_s
    items.append(text_sprite(sc["title"], tf, WHITE, 940, spacing=1.05))
    if sc["body"]: items.append(text_sprite(sc["body"], f_body, SOFT, 900, spacing=1.3))
    return items

def frame_at(sc, sprites, lt, gt):
    fr = BG.copy(); fr.alpha_composite(rays(gt))
    dur = sc["dur"]; last = sc is SCENES[-1]
    out = 0 if last else ease_out((lt - (dur - 0.35)) / 0.35)
    ill = illustration(sc["kind"], lt, dur, gt)
    p = ease_back(lt / 0.55); a = min(1, lt / 0.3) * (1 - out)
    if p < 0.999: ill = ill.resize((max(1, int(W * p)), max(1, int(LH * p))), Image.BILINEAR)
    fr.alpha_composite(with_alpha(ill, a), (int((W - ill.width) / 2), int(LY + (LH - ill.height) / 2)))
    draw_parts(fr, gt)
    y = 290; gaps = [28, 30]
    for i, sp in enumerate(sprites):
        e = ease_out((lt - 0.08 - i * 0.13) / 0.5)
        al = e * (1 - out); dy = (1 - e) * 70 - out * 40
        if al > 0.01: fr.alpha_composite(with_alpha(sp, al), (70, int(y + dy)))
        y += sp.height + (gaps[i] if i < len(gaps) else 0)
    idx = SCENES.index(sc); d = ImageDraw.Draw(fr)
    if 1 <= idx <= 5:
        for k in range(5):
            x0 = 70 + k * 192
            d.rounded_rectangle((x0, 225, x0 + 176, 233), radius=4, fill=(255, 255, 255, 60))
            fw = 176 if k + 1 < idx else (176 * min(1, lt / dur) if k + 1 == idx else 0)
            if fw > 0: d.rounded_rectangle((x0, 225, x0 + fw, 233), radius=4, fill=YELLOW)
    return fr.convert("RGB")

def starts():
    s, acc = [], 0
    for sc in SCENES: s.append(acc); acc += sc["dur"]
    return s

def render_scene(i, start):
    sc = SCENES[i]; sprites = build_text(sc); n = int(round(sc["dur"] * FPS))
    tmp, final = f"outc/s{i}.tmp.mp4", f"outc/s{i}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                          "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    for f in range(n):
        lt = f / FPS; p.stdin.write(frame_at(sc, sprites, lt, start + lt).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, final)
    else: sys.exit("ffmpeg failed")

if __name__ == "__main__":
    os.makedirs("outc", exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[1] == "durs":
        for sc, d_ in zip(SCENES, [float(x) for x in sys.argv[2].split(",")]): sc["dur"] = d_
        sys.argv = sys.argv[:1] + sys.argv[3:]
    st = starts()
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for i, lt in [(0, 2.0), (1, 2.5), (2, 2.5), (3, 3.0), (4, 2.5), (5, 2.5), (6, 2.0)]:
            ims.append(frame_at(SCENES[i], build_text(SCENES[i]), lt, st[i] + lt).resize((360, 640)))
        sh = Image.new("RGB", (360 * 4, 640 * 2)); [sh.paste(im, ((k % 4) * 360, (k // 4) * 640)) for k, im in enumerate(ims)]
        sh.save("outc/sheet.jpg", quality=85)
    else:
        for i in range(len(SCENES)): render_scene(i, st[i])
