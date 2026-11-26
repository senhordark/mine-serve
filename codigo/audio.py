import numpy as np, wave
SR = 44100
durs = [11.708, 13.817, 9.564, 11.122, 9.904, 8.361, 13.728, 8.115]
T = sum(durs)
n = int(T * SR); t = np.arange(n) / SR
out = np.zeros(n)

def hz(m): return 440 * 2 ** ((m - 69) / 12)
# Am F C G (midi)
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
bar = T / 8
for b in range(8):
    ch = chords[b % 4]
    s, e = int(b * bar * SR), min(n, int((b + 1) * bar * SR + 1.2 * SR))
    tt = t[s:e] - b * bar
    env = np.minimum(1, tt / 0.9) * np.exp(-np.maximum(0, tt - bar) * 2.5)
    pad = sum(np.sin(2 * np.pi * hz(m) * tt * d) for m in ch for d in (0.997, 1.003)) / 6
    bass = np.sin(2 * np.pi * hz(ch[0] - 12) * tt) * 0.6
    out[s:e] += (pad * 0.35 + bass * 0.25) * env * (0.85 + 0.15 * np.sin(2 * np.pi * 0.5 * tt))
    # arpeggio plucks (8ths)
    step = bar / 8
    seq = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 24, ch[2] + 12, ch[1] + 12, ch[0] + 24, ch[2] + 12]
    for k, m in enumerate(seq):
        ps = int((b * bar + k * step) * SR); pe = min(n, ps + int(0.9 * SR))
        pt = t[ps:pe] - t[ps]
        tone = np.sin(2 * np.pi * hz(m) * pt) + 0.3 * np.sin(4 * np.pi * hz(m) * pt)
        out[ps:pe] += tone * np.exp(-pt * 5) * 0.09 * np.minimum(1, pt / 0.005)

# bubble "bloops" at each scene start
acc = 0
for dd in durs:
    for j, off in enumerate((0.0, 0.09, 0.17)):
        ps = int((acc + off) * SR); pe = min(n, ps + int(0.18 * SR))
        pt = t[ps:pe] - t[ps]
        f = 300 + 1400 * pt / 0.18 + j * 120
        ph = 2 * np.pi * np.cumsum(f) / SR
        out[ps:pe] += np.sin(ph) * np.exp(-pt * 22) * 0.22
    acc += dd

out /= np.max(np.abs(out)) * 1.12
fade = int(1.5 * SR); out[-fade:] *= np.linspace(1, 0, fade)
out[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))
st = np.stack([out, np.roll(out, 300) * 0.96], 1)
with wave.open("out/music.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
