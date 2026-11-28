# Voz reserva: Supertonic 3 (sherpa-onnx), voz "masc1" = sid 5, escolhida pelo dono em 28/11/2026.
# Usar SÓ quando o ElevenLabs falhar ou estiver sem crédito. Geração simples (sem truques de emoção),
# speed 1.0, num_steps 10, lang "pt".
#
# Preparo (uma vez por sessão):
#   pip install "sherpa-onnx==2.0.3" soundfile --break-system-packages -q
#   curl -sSLO https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/sherpa-onnx-supertonic-3-tts-int8-2026-05-11.tar.bz2
#   tar xjf sherpa-onnx-supertonic-3-tts-int8-2026-05-11.tar.bz2
#
# Uso: python3 voice_supertonic.py <pasta_do_modelo> <roteiro.txt> <pasta_saida>
#   roteiro.txt: uma fala por linha (8 linhas: gancho, Um..Seis, final).
#   Gera v0.wav..v7.wav (24 kHz) e imprime as durações de cada fala.
import sys, os, json
import sherpa_onnx, soundfile as sf

D, roteiro, out = sys.argv[1].rstrip("/") + "/", sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    supertonic=sherpa_onnx.OfflineTtsSupertonicModelConfig(
        duration_predictor=D + "duration_predictor.int8.onnx",
        text_encoder=D + "text_encoder.int8.onnx",
        vector_estimator=D + "vector_estimator.int8.onnx",
        vocoder=D + "vocoder.int8.onnx",
        tts_json=D + "tts.json",
        unicode_indexer=D + "unicode_indexer.bin",
        voice_style=D + "voice.bin"),
    num_threads=2, provider="cpu"))
tts = sherpa_onnx.OfflineTts(cfg)
lines = [l.strip() for l in open(roteiro, encoding="utf-8") if l.strip()]
lens = []
for i, t in enumerate(lines):
    g = sherpa_onnx.GenerationConfig()
    g.sid = 5
    g.num_steps = 10
    g.speed = 1.0
    g.extra["lang"] = "pt"
    a = tts.generate(t, g)
    sf.write(f"{out}/v{i}.wav", a.samples, samplerate=a.sample_rate)
    lens.append(round(len(a.samples) / a.sample_rate, 2))
print(json.dumps(lens))
