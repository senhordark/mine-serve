#!/bin/bash
# uso: finalizar.sh <pasta> <durs csv> <saida.mp4>
set -e
D=$1; DURS=$2; OUT=$3
cd $D
mkdir -p out
sed -e "s/^durs = .*/durs = [$DURS]/" /home/claude/reels/codigo/audio.py > audio_local.py
python3 audio_local.py
printf "file 'outc/s%d.mp4'\n" 0 1 2 3 4 5 6 7 > scenes.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i scenes.txt -c copy video.mp4
ffmpeg -y -loglevel error -i video.mp4 -i narr.wav -i out/music.wav -filter_complex \
 "[1:a]volume=2.2,asplit=2[v][key];[2:a]volume=0.35[m];[m][key]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[md];[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $OUT
ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT
