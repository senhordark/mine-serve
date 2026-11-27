import subprocess
END=75.885
segs=[(0.0,9.53),(9.94,20.44),(20.85,31.61),(31.95,40.89),(41.22,49.81),(50.09,57.84),(58.14,69.49),(69.78,END)]
durs=[]
for i,(a,b) in enumerate(segs):
    a=max(0,a-0.05); b=min(END,b+0.1); post=1.6 if i==7 else 0.9
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i","dl/voz.mp3","-af",f"atrim={a}:{b},asetpts=PTS-STARTPTS,adelay=350:all=1,apad=pad_dur={post}","-ar","44100","-ac","2",f"p{i}.wav"],check=True)
    d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"p{i}.wav"]))
    durs.append(round(d,3))
open("list.txt","w").write("".join(f"file 'p{i}.wav'\n" for i in range(8)))
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-i","list.txt","-c","copy","narr.wav"],check=True)
print(",".join(map(str,durs)), sum(durs))
