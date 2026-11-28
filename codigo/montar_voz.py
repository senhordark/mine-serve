import subprocess, sys
d = sys.argv[1]; durs = []
for i in range(8):
    post = 1.6 if i == 7 else 0.9
    af = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
          "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,"
          f"adelay=350:all=1,apad=pad_dur={post}")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{d}/voz/v{i}.wav","-af",af,"-ar","44100","-ac","2",f"{d}/p{i}.wav"],check=True)
    durs.append(round(float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{d}/p{i}.wav"])),3))
open(f"{d}/list.txt","w").write("".join(f"file 'p{i}.wav'\n" for i in range(8)))
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-i",f"{d}/list.txt","-c","copy",f"{d}/narr.wav"],check=True)
print(",".join(map(str,durs)), round(sum(durs),2))
