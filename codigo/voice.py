import soundfile as sf, numpy as np, sys, json
from kokoro_onnx import Kokoro
k = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
lines = [
 "Você sabia? Aqui vão cinco fatos incríveis sobre o polvo.",
 "Um: ele tem três corações. Dois bombeiam sangue para as brânquias, e um, para o resto do corpo.",
 "Dois: o sangue dele é azul, por causa da hemocianina, uma proteína com cobre.",
 "Três: cerca de dois terços dos neurônios ficam nos braços, e não no cérebro.",
 "Quatro: ele não tem ossos, e passa por qualquer fresta maior que o próprio bico.",
 "Cinco: ele muda de cor e de textura em menos de um segundo.",
 "E aí, qual desses fatos te surpreendeu mais? Comenta aqui!",
]
voice = sys.argv[1]
lens = []
for i, l in enumerate(lines):
    s, sr = k.create(l, voice=voice, speed=1.08, lang="pt-br")
    sf.write(f"v{i}.wav", s, sr); lens.append(round(len(s) / sr, 2))
print(sr, lens)
