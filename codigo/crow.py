import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
S=1080; K=3; W=S*K
def P(x,y): return (x*K, y*K)
def ell(d,cx,cy,rx,ry,fill): d.ellipse((K*(cx-rx),K*(cy-ry),K*(cx+rx),K*(cy+ry)),fill=fill)
def poly(d,pts,fill): d.polygon([P(*p) for p in pts],fill=fill)
def star(d,cx,cy,r,fill):
    pts=[]
    for i in range(8):
        a=i*math.pi/4; rr=r if i%2==0 else r*0.28
        pts.append((cx+rr*math.sin(a), cy-rr*math.cos(a)))
    poly(d,pts,fill)
# background radial gradient
yy,xx=np.mgrid[0:S,0:S]/S
r=np.sqrt((xx-0.5)**2+(yy-0.45)**2)/0.7
inner=np.array([108,72,170]); outer=np.array([18,14,42])
t=np.clip(r,0,1)[...,None]**0.9
bg=(inner*(1-t)+outer*t).astype(np.uint8)
img=Image.fromarray(bg).convert("RGBA").resize((W,W),Image.BILINEAR)
d=ImageDraw.Draw(img,"RGBA")
# glow behind
glow=Image.new("RGBA",(W,W),(0,0,0,0)); gd=ImageDraw.Draw(glow)
gd.ellipse(P(250,230)+P(830,810),fill=(255,190,90,70)); glow=glow.filter(ImageFilter.GaussianBlur(60*K))
img.alpha_composite(glow); d=ImageDraw.Draw(img,"RGBA")
BODY=(30,30,48); DARK=(18,18,30); SHEEN=(92,104,190)
# tail
poly(d,[(420,700),(300,900),(360,915),(410,880),(440,930),(500,780)],DARK)
# feet
for fx in (500,590):
    d.line([P(fx,820),P(fx-8,900)],fill=(60,60,72),width=14*K)
    for dx in (-30,0,26): d.line([P(fx-8,900),P(fx-8+dx,925)],fill=(60,60,72),width=11*K)
# body
ell(d,540,640,215,235,BODY)
# belly sheen
d.arc(P(360,430)+P(720,860),200,250,fill=SHEEN,width=16*K)
# wing
d.chord(P(330,520)+P(590,860),200,420,fill=DARK)
poly(d,[(345,760),(300,850),(380,800)],DARK)
for a in (0,1,2):
    d.arc(P(350+a*20,560+a*40)+P(570-a*10,840),95,160,fill=(52,52,82),width=7*K)
# head (tilted)
ell(d,600,390,165,155,BODY)
d.arc(P(460,250)+P(740,530),200,260,fill=SHEEN,width=14*K)
# head feather tuft
poly(d,[(560,245),(590,190),(605,245)],BODY); poly(d,[(600,240),(650,200),(640,255)],BODY)
# beak
poly(d,[(720,380),(860,425),(720,460)],(70,72,88))
poly(d,[(720,380),(860,425),(725,418)],(110,112,130))
# eye
ell(d,650,365,58,62,(255,255,255))
ell(d,660,372,36,38,(255,186,40))
ell(d,664,376,19,21,(15,12,25))
ell(d,672,360,9,9,(255,255,255))
ell(d,650,378,4,4,(255,255,255,200))
# brow (curious)
d.line([P(595,290),P(700,300)],fill=DARK,width=12*K)
# cheek blush
ell(d,640,448,28,14,(255,120,150,110))
# sparkles (curiosity)
star(d,820,250,46,(255,214,102)); star(d,890,340,22,(255,236,170)); star(d,250,300,28,(200,180,255,200))
img=img.resize((S,S),Image.LANCZOS).convert("RGB")
img.save("out/foto_perfil_corvo.png")
m=Image.new("L",(S,S),0); ImageDraw.Draw(m).ellipse((0,0,S,S),fill=255)
pv=Image.new("RGB",(S,S),"white"); pv.paste(img,(0,0),m); pv.resize((420,420)).save("out/corvo_preview.jpg")
