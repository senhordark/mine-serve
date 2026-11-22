import math, colorsys, random, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
F = "/usr/share/fonts/opentype/inter/"
f_title = ImageFont.truetype(F + "InterDisplay-Black.otf", 104)
f_title_s = ImageFont.truetype(F + "InterDisplay-Black.otf", 92)
f_body = ImageFont.truetype(F + "Inter-Medium.otf", 48)
f_label = ImageFont.truetype(F + "Inter-ExtraBold.otf", 36)
f_small = ImageFont.truetype(F + "Inter-Bold.otf", 40)

CORAL = (255, 107, 107)
YELLOW = (255, 209, 102)
WHITE = (255, 255, 255)
SOFT = (200, 225, 245)

SCENES = [
    dict(kind="hook", dur=4.66, label="VOCÊ SABIA?", title="5 fatos incríveis sobre o polvo", body=None),
    dict(kind="hearts", dur=6.69, label="FATO 01 / 05", title="Ele tem 3 corações",
         body="Dois bombeiam sangue para as brânquias e um para o resto do corpo."),
    dict(kind="blood", dur=5.86, label="FATO 02 / 05", title="O sangue dele é azul",
         body="Graças à hemocianina, uma proteína com cobre que transporta oxigênio."),
    dict(kind="brain", dur=5.53, label="FATO 03 / 05", title="Os braços “pensam”",
         body="Cerca de dois terços dos neurônios ficam nos braços, não no cérebro."),
    dict(kind="squeeze", dur=5.71, label="FATO 04 / 05", title="Não tem ossos",
         body="Passa por qualquer fresta maior que o bico, a única parte dura do corpo."),
    dict(kind="color", dur=4.6, label="FATO 05 / 05", title="Mestre do disfarce",
         body="Muda de cor e textura em menos de um segundo para sumir no fundo."),
    dict(kind="outro", dur=5.1, label="E AÍ?", title="Qual fato te surpreendeu mais?",
         body="Comenta aqui e salva pra mostrar pra alguém!"),
]

# ---------- helpers ----------
def ease_out(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def ease_back(x):
    x = min(max(x, 0), 1); c = 1.6; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def text_sprite(text, font, fill, maxw, spacing=1.12, align="left"):
    lines = wrap(text, font, maxw)
    asc, desc = font.getmetrics(); lh = int((asc + desc) * spacing)
    w = int(max(font.getlength(l) for l in lines)) + 8
    img = Image.new("RGBA", (w, lh * len(lines) + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        x = (w - font.getlength(l)) / 2 if align == "center" else 0
        d.text((x, i * lh), l, font=font, fill=fill)
    return img

def pill_sprite(text, font, fg, bg):
    tw = font.getlength(text); asc, desc = font.getmetrics()
    w, h = int(tw + 52), asc + desc + 26
    img = Image.new("RGBA", (w * 2, h * 2), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), radius=h, fill=bg)
    img = img.resize((w, h), Image.LANCZOS)
    ImageDraw.Draw(img).text((26, 12), text, font=font, fill=fg)
    return img

def with_alpha(img, a):
    if a >= 0.999: return img
    out = img.copy(); out.putalpha(img.getchannel("A").point(lambda v: int(v * a))); return out

# ---------- background ----------
yy = np.linspace(0, 1, H)[:, None]
top, bot = np.array([14, 52, 92]), np.array([3, 10, 26])
grad = (top * (1 - yy ** 0.8) + bot * yy ** 0.8)[:, None, :].repeat(W, 1)[:, :, 0, :] if False else None
g = np.zeros((H, W, 3), np.float32)
for c in range(3): g[:, :, c] = top[c] * (1 - yy ** 0.8) + bot[c] * yy ** 0.8
xx = np.linspace(-1, 1, W)[None, :]
glow = np.exp(-((xx) ** 2 * 2.2 + ((np.linspace(0, 1, H)[:, None] - 0.62) ** 2) * 9))
g += glow[:, :, None] * np.array([10, 40, 60])
BG = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

def rays(gt):
    lw, lh = 270, 480
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for i in range(5):
        cx = 30 + i * 55 + math.sin(gt * 0.35 + i * 1.7) * 20
        spread = 18 + 10 * math.sin(gt * 0.5 + i)
        a = int(16 + 10 * math.sin(gt * 0.8 + i * 2.1))
        d.polygon([(cx - 6, -5), (cx + 6, -5), (cx + spread + 40, lh), (cx - spread + 20, lh)], fill=(170, 230, 255, a))
    return img.filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR)

def bubble_sprite(r):
    s = 4; R = r * s
    img = Image.new("RGBA", (2 * R + 8, 2 * R + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.ellipse((4, 4, 4 + 2 * R, 4 + 2 * R), fill=(190, 235, 255, 30), outline=(210, 245, 255, 150), width=max(2, s * 2))
    d.ellipse((4 + R * 0.45, 4 + R * 0.4, 4 + R * 0.85, 4 + R * 0.8), fill=(255, 255, 255, 170))
    return img.resize((img.width // s, img.height // s), Image.LANCZOS)

rng = random.Random(7)
BUBBLES = []
for i in range(26):
    r = rng.choice([6, 8, 10, 13, 17, 22])
    BUBBLES.append(dict(x=rng.uniform(40, W - 40), y0=rng.uniform(0, H + 200), sp=rng.uniform(60, 150) * (0.6 + r / 30),
                        ph=rng.uniform(0, 6.28), spr=bubble_sprite(r)))

def draw_bubbles(frame, gt):
    for b in BUBBLES:
        y = (b["y0"] - b["sp"] * gt) % (H + 250) - 120
        x = b["x"] + math.sin(gt * 1.3 + b["ph"]) * 18
        frame.alpha_composite(b["spr"], (int(x), int(y)))

# ---------- illustration (drawn at 2x) ----------
LY, LH = 760, 1060  # layer position / height in final coords
S2 = 2

def octopus(d, cx, cy, s, t, color, sx=1.0, dots=False, spots=0.0):
    dark = tuple(int(c * 0.78) for c in color)
    light = tuple(min(255, int(c + (255 - c) * 0.35)) for c in color)
    # tentacles
    for i in range(8):
        base_x = cx + (-105 + i * 30) * s * sx
        base_y = cy + 80 * s
        ang0 = (-1.15 + i * (2.3 / 7))
        side = 1 if ang0 >= 0 else -1
        x, y, ang = base_x, base_y, ang0
        N, L = 34, 420 * s
        pts = []
        for k in range(N + 1):
            u = k / N
            a = ang0 * (0.9 + 0.5 * u) + math.sin(t * 2.4 + i * 0.9 - u * 4.5) * 0.55 * u + side * u * u * 1.1
            pts.append((x, y, u))
            x += math.sin(a) * L / N * sx
            y += math.cos(a) * L / N
        col = dark if i % 2 else color
        for (px, py, u) in pts:
            r = 36 * s * (1 - u * 0.86)
            d.ellipse((px - r, py - r, px + r, py + r), fill=col)
        for (px, py, u) in pts[3:-4:3]:
            r = 9 * s * (1 - u * 0.8)
            d.ellipse((px - r, py - r, px + r, py + r), fill=light)
        if dots:
            for off in (0.0, 0.5):
                u = (t * 0.7 + i * 0.137 + off) % 1.0
                k = int(u * N); px, py, _ = pts[k]
                for rr, al in ((34, 60), (22, 120), (12, 255)):
                    r = rr * s
                    d.ellipse((px - r, py - r, px + r, py + r), fill=(255, 230, 120, al))
    # head
    hw, hh = 150 * s * sx, 175 * s
    d.ellipse((cx - hw, cy - hh * 1.25, cx + hw, cy + hh * 0.75), fill=color)
    d.ellipse((cx - hw * 0.55, cy - hh * 1.1, cx - hw * 0.05, cy - hh * 0.6), fill=light)
    if spots > 0:
        for (ox, oy, rr) in [(-60, -150, 18), (50, -170, 14), (80, -90, 20), (-90, -60, 12), (10, -110, 10), (-30, -200, 11)]:
            r = rr * s * spots
            d.ellipse((cx + ox * s * sx - r, cy + oy * s - r, cx + ox * s * sx + r, cy + oy * s + r), fill=dark)
    # eyes
    blink = 0.12 if (t % 3.1) < 0.12 else 1.0
    for ex in (-58, 58):
        exx, eyy = cx + ex * s * sx, cy + 10 * s
        rw, rh = 36 * s * sx, 40 * s * blink
        d.ellipse((exx - rw, eyy - rh, exx + rw, eyy + rh), fill=WHITE)
        if blink > 0.5:
            pr = 19 * s
            d.ellipse((exx - pr * sx + 4 * s, eyy - pr + 5 * s, exx + pr * sx + 4 * s, eyy + pr + 5 * s), fill=(20, 24, 40))
            d.ellipse((exx + 2 * s, eyy - 4 * s, exx + 10 * s, eyy + 4 * s), fill=WHITE)
    # cheeks + smile
    for ex in (-95, 95):
        r = 16 * s
        d.ellipse((cx + ex * s * sx - r * 1.3, cy + 52 * s - r, cx + ex * s * sx + r * 1.3, cy + 52 * s + r), fill=(255, 150, 160))
    d.arc((cx - 26 * s * sx, cy + 40 * s, cx + 26 * s * sx, cy + 76 * s), 20, 160, fill=(90, 30, 40), width=int(7 * s))

def heart(d, cx, cy, size, fill):
    pts = []
    for k in range(80):
        a = k / 80 * 2 * math.pi
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + x * size, cy + y * size))
    d.polygon(pts, fill=fill)
    d.ellipse((cx - 9 * size, cy - 9 * size, cx - 4 * size, cy - 4 * size), fill=(255, 190, 200, 255))

def illustration(kind, lt, dur, gt):
    lw, lh = W * S2, LH * S2
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(img, "RGBA")
    cx = lw / 2; bob = math.sin(gt * 1.6) * 18 * S2
    if kind in ("hook", "brain", "outro"):
        octopus(d, cx, 470 * S2 + bob, 1.05 * S2, gt, CORAL, dots=(kind == "brain"))
    elif kind == "hearts":
        beat = lambda ph: 1 + 0.12 * max(0, math.sin((gt * 2.6 + ph) * math.pi)) ** 6
        heart(d, cx - 340 * S2, 470 * S2, 6.5 * S2 * beat(0.35), (255, 128, 150, 255))
        heart(d, cx + 340 * S2, 470 * S2, 6.5 * S2 * beat(0.35), (255, 128, 150, 255))
        heart(d, cx, 440 * S2 + bob * 0.3, 11.5 * S2 * beat(0.0), (255, 72, 98, 255))
        for i, (x, lab) in enumerate([(-340, "brânquias"), (0, "corpo"), (340, "brânquias")]):
            tx = cx + x * S2; ty = (600 if i != 1 else 650) * S2
            tw = f_small.getlength(lab) * S2
            fbig = ImageFont.truetype(F + "Inter-Bold.otf", 40 * S2)
            d.text((tx - fbig.getlength(lab) / 2, ty), lab, font=fbig, fill=(200, 225, 245, 230))
    elif kind == "blood":
        sc = 1 + 0.04 * math.sin(gt * 3)
        cy = 450 * S2 + bob * 0.5
        r = 200 * S2 * sc
        pts = [(cx, cy - r * 1.75)]
        for k in range(0, 61):
            a = math.pi * (1.2 - 1.4 * k / 60) - math.pi / 2 + math.pi / 2
            a = math.radians(-30 + 240 * k / 60)
            pts.append((cx + r * math.cos(math.radians(-30) - math.radians(240 * k / 60) + math.pi) * -1, 0))
        # simple droplet: circle + triangle
        d.polygon([(cx, cy - r * 1.8), (cx - r * 0.86, cy - r * 0.5), (cx + r * 0.86, cy - r * 0.5)], fill=(60, 130, 255))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(60, 130, 255))
        d.ellipse((cx - r * 0.62, cy - r * 0.55, cx - r * 0.25, cy - r * 0.05), fill=(170, 210, 255, 200))
        fb = ImageFont.truetype(F + "InterDisplay-Black.otf", 120 * S2)
        d.text((cx - fb.getlength("Cu") / 2, cy - 75 * S2), "Cu", font=fb, fill=WHITE)
        for k in range(6):
            a = gt * 0.8 + k * math.pi / 3
            ox, oy = cx + math.cos(a) * 330 * S2, cy + math.sin(a) * 330 * S2 * 0.55
            rr = 26 * S2
            d.ellipse((ox - rr, oy - rr, ox + rr, oy + rr), fill=(140, 200, 255, 160))
            fo = ImageFont.truetype(F + "Inter-ExtraBold.otf", 26 * S2)
            d.text((ox - fo.getlength("O₂") / 2 if False else ox - 14 * S2, oy - 16 * S2), "O", font=fo, fill=(20, 50, 110))
    elif kind == "squeeze":
        u = (lt / dur)
        k = math.sin(min(1, max(0, (u - 0.15) / 0.7)) * math.pi)
        sx = 1 - 0.55 * k
        oy = 560 * S2 - 220 * S2 * ease_out((u - 0.1) / 0.8)
        octopus(d, cx, oy, 0.95 * S2, gt, CORAL, sx=sx)
        rock = (88, 104, 128)
        for side in (-1, 1):
            x0 = cx + side * 150 * S2
            box = (x0, 330 * S2, x0 + side * 700 * S2, 720 * S2)
            d.rounded_rectangle((min(box[0], box[2]), box[1], max(box[0], box[2]), box[3]), radius=150 * S2, fill=rock)
            d.rounded_rectangle((min(box[0], box[2]) + 30 * S2, box[1] + 30 * S2, max(box[0], box[2]) - 30 * S2, box[1] + 90 * S2),
                                radius=40 * S2, fill=(110, 128, 152))
    elif kind == "color":
        h = (gt * 0.45) % 1.0
        r, g, b = colorsys.hsv_to_rgb(h, 0.62, 1.0)
        octopus(d, cx, 470 * S2 + bob, 1.05 * S2, gt, (int(r * 255), int(g * 255), int(b * 255)),
                spots=0.6 + 0.4 * math.sin(gt * 3))
    return img.resize((W, LH), Image.LANCZOS)

# ---------- scene renderer ----------
def build_text(sc):
    items = []
    lab = pill_sprite(sc["label"], f_label, (20, 30, 50), YELLOW)
    items.append(lab)
    tf = f_title if len(sc["title"]) < 26 else f_title_s
    items.append(text_sprite(sc["title"], tf, WHITE, 940, spacing=1.05))
    if sc["body"]:
        items.append(text_sprite(sc["body"], f_body, SOFT, 900, spacing=1.3))
    return items

def frame_at(sc, sprites, lt, gt):
    fr = BG.copy()
    fr.alpha_composite(rays(gt))
    dur = sc["dur"]
    out = ease_out((lt - (dur - 0.35)) / 0.35) if sc is not SCENES[-1] else 0
    # illustration
    ill = illustration(sc["kind"], lt, dur, gt)
    p = ease_back(lt / 0.55)
    a = min(1, lt / 0.3) * (1 - out)
    if p < 0.999:
        sz = max(1, int(W * p)), max(1, int(LH * p))
        ill = ill.resize(sz, Image.BILINEAR)
    fr.alpha_composite(with_alpha(ill, a), (int((W - ill.width) / 2), int(LY + (LH - ill.height) / 2)))
    draw_bubbles(fr, gt)
    # text
    y = 290
    gaps = [28, 30]
    for i, sp in enumerate(sprites):
        e = ease_out((lt - 0.08 - i * 0.13) / 0.5)
        al = e * (1 - out)
        dy = (1 - e) * 70 - out * 40
        if al > 0.01:
            fr.alpha_composite(with_alpha(sp, al), (70, int(y + dy)))
        y += sp.height + (gaps[i] if i < len(gaps) else 0)
    # progress bar
    idx = SCENES.index(sc)
    d = ImageDraw.Draw(fr)
    if 1 <= idx <= 5:
        for k in range(5):
            x0 = 70 + k * 192
            d.rounded_rectangle((x0, 225, x0 + 176, 233), radius=4, fill=(255, 255, 255, 60))
            fillw = 176 if k + 1 < idx else (176 * min(1, lt / dur) if k + 1 == idx else 0)
            if fillw > 0:
                d.rounded_rectangle((x0, 225, x0 + fillw, 233), radius=4, fill=YELLOW)
    return fr.convert("RGB")

def render_scene(i, start):
    sc = SCENES[i]
    sprites = build_text(sc)
    n = int(round(sc["dur"] * FPS))
    tmp, final = f"out/s{i}.tmp.mp4", f"out/s{i}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                          "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    for f in range(n):
        lt = f / FPS
        p.stdin.write(frame_at(sc, sprites, lt, start + lt).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, final)
    else: sys.exit("ffmpeg failed")

starts = []
acc = 0
for sc in SCENES: starts.append(acc); acc += sc["dur"]

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    if sys.argv[1] == "preview":
        for i, lt in [(0, 1.5), (1, 2.0), (2, 2.0), (3, 2.0), (4, 2.2), (5, 2.0), (6, 2.0)]:
            sc = SCENES[i]
            frame_at(sc, build_text(sc), lt, starts[i] + lt).save(f"out/prev{i}.jpg", quality=85)
    else:
        idxs = [int(a) for a in sys.argv[2:]] if len(sys.argv) > 2 else range(len(SCENES))
        for i in idxs: render_scene(i, starts[i])
