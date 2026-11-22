# Pipeline de Reels/Shorts — @jonas.ia_6 / canal Jonas.ia-

- make_corvo.py: modelo principal (mascote corvo, fundo roxo, texto no topo, ilustração por fato, barra de progresso).
  Uso: `python3 make_corvo.py durs d0,d1,...,d6` renderiza cenas em outc/ (1080x1920, 30fps).
- make.py: funções compartilhadas (fontes Inter, text_sprite, pill_sprite, easing) — make_corvo importa dele.
- audio.py: trilha sintetizada (Am-F-C-G + arpejo + bolhas). Ajustar `durs` e o caminho de saída.
- voice.py: narração reserva com Kokoro (voz pm_alex, pt-br) caso o ElevenLabs falhe.
- Ritmo aprovado: narração com atempo 0.92, 0.35s antes de cada fala e 1.15s de pausa depois de cada fato.
- Voz principal: ElevenLabs, voz "Fernando Borges" (voice_id 6pQlwCgfwffNdI3jjzM6), modelo eleven_v4.
