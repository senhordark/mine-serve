import subprocess
segs=[(0.0,9.00),(9.39,18.37),(18.75,25.51),(25.86,31.42),(31.78,38.91),(39.22,46.47),(46.79,55.90),(56.24,62.43)]
durs=[];parts=[]
for i,(a,b) in enumerate(segs):
    a=max(0,a-0.05); b=min(62.43,b+0.1); post=1.6 if i==7 else 0.9
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i","dl/voz.mp3","-af",f"atrim={a}:{b},asetpts=PTS-STARTPTS,adelay=350:all=1,apad=pad_dur={post}","-ar","44100","-ac","2",f"p{i}.wav"],check=True)
    d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"p{i}.wav"]))
    durs.append(round(d,3))
open("list.txt","w").write("".join(f"file 'p{i}.wav'\n" for i in range(8)))
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-i","list.txt","-c","copy","narr.wav"],check=True)
print(",".join(map(str,durs)), sum(durs))
