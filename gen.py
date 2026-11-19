#!/usr/bin/env python3
"""Deterministic illustrated world-news front page for 18 November 2026."""
from PIL import Image, ImageDraw, ImageFont
import math
from pathlib import Path

W = H = 1024
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "entry.png"
INK = "#17212b"
MUTED = "#65717b"
PAPER = "#f4f0e6"
WHITE = "#fffdf7"
RED = "#c9493b"
BLUE = "#2b6784"
GOLD = "#d69b3d"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def font(size, bold=False):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else "")
    return ImageFont.truetype(p, size)

def fit(text, max_w, start, bold=False, minimum=5):
    for s in range(start, minimum - 1, -1):
        f = font(s, bold)
        if d.textbbox((0, 0), text, font=f)[2] <= max_w:
            return f
    raise AssertionError(f"text cannot fit: {text}")

def text_box(x, y, text, f, fill, max_w, max_h, anchor="la"):
    box = d.textbbox((x, y), text, font=f, anchor=anchor)
    assert box[0] >= -1 and box[1] >= -1 and box[2] <= W + 1 and box[3] <= H + 1
    assert box[2] - box[0] <= max_w + 1 and box[3] - box[1] <= max_h + 1, (text, box)
    d.text((x, y), text, font=f, fill=fill, anchor=anchor)

def rr(box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)

def poly(points, fill, outline=None, width=1):
    d.polygon(points, fill=fill)
    if outline:
        d.line(points + [points[0]], fill=outline, width=width, joint="curve")

def shadow_ellipse(box):
    d.ellipse(box, fill="#16212b28")

def scene_base(b, sky, ground, sun=True):
    x0,y0,x1,y1=b
    rr(b, 5, sky)
    if sun:
        d.ellipse((x1-27,y0+9,x1-13,y0+23), fill="#fff1b8")
    poly([(x0,y1-19),(x0+36,y1-33),(x0+72,y1-22),(x0+112,y1-39),(x1,y1-25),(x1,y1),(x0,y1)], ground)
    d.line((x0+5,y1-8,x1-5,y1-8), fill="#ffffff55", width=1)

def drone(b):
    x,y,X,Y=b; scene_base(b,"#b9d8df","#668b72")
    d.line((x+22,y+20,x+66,y+36),fill="#76848b",width=2); d.line((x+66,y+20,x+22,y+36),fill="#76848b",width=2)
    for cx,cy in [(22,20),(66,36),(66,20),(22,36)]:
        d.ellipse((x+cx-7,y+cy-2,x+cx+7,y+cy+2),fill="#303d46")
    rr((x+38,y+22,x+51,y+34),4,"#263743"); d.ellipse((x+42,y+30,x+47,y+35),fill="#efc44d")
    d.arc((x+79,y+11,x+119,y+51),185,270,fill=WHITE,width=2)

def ship(b):
    x,y,X,Y=b; scene_base(b,"#94c6d4","#2e7891")
    d.rectangle((x,y+49,X,Y),fill="#27748c");
    for yy in (55,63): d.arc((x+5, y+yy-5, X-5,y+yy+4),0,180,fill="#bce4e7",width=1)
    poly([(x+20,y+42),(x+105,y+42),(x+91,y+57),(x+32,y+56)],"#30434d")
    d.rectangle((x+46,y+26,x+87,y+42),fill="#ece6d4"); d.rectangle((x+60,y+17,x+66,y+39),fill="#d4d0c2")
    d.line((x+66,y+19,x+91,y+29),fill="#293942",width=2); d.ellipse((x+51,y+31,x+57,y+36),fill="#f8c755")

def hospital(b):
    x,y,X,Y=b; scene_base(b,"#c8e0d5","#75a192")
    d.rectangle((x+20,y+25,x+108,Y-7),fill="#f3efe3",outline="#78928f")
    d.rectangle((x+46,y+17,x+83,Y-7),fill="#e4e9df")
    d.rectangle((x+61,y+20,x+68,y+38),fill=RED); d.rectangle((x+55,y+26,x+74,y+33),fill=RED)
    for wx in (29,91):
        d.rectangle((x+wx,y+34,x+wx+8,y+43),fill="#6099aa")
    d.rectangle((x+59,y+50,x+71,Y-7),fill="#446d78"); d.line((x+65,y+51,x+65,Y-7),fill="#badbe0")

def parliament(b):
    x,y,X,Y=b; scene_base(b,"#d8d1c3","#777865")
    d.ellipse((x+43,y+12,x+83,y+31),fill="#78929b",outline="#455a64"); d.rectangle((x+48,y+25,x+78,y+33),fill="#ece5d5")
    poly([(x+17,y+38),(x+65,y+24),(x+113,y+38)],"#eae0ca",INK)
    for cx in range(x+25,x+106,16): d.rectangle((cx,y+39,cx+7,Y-9),fill="#d8c9ae",outline="#8c816f")
    d.rectangle((x+15,Y-12,x+115,Y-7),fill="#403f3b"); d.ellipse((x+63,y+16,x+68,y+21),fill="#fff4bd")

def tank(b):
    x,y,X,Y=b; scene_base(b,"#d9bd8f","#8f7250")
    shadow_ellipse((x+21,Y-16,x+109,Y-5)); rr((x+25,y+42,x+104,y+61),8,"#4f624c",INK)
    for cx in range(x+34,x+99,14): d.ellipse((cx,y+47,cx+11,y+59),fill="#26342e",outline="#a7aa79")
    poly([(x+43,y+42),(x+52,y+29),(x+83,y+29),(x+94,y+42)],"#607354",INK)
    d.rectangle((x+72,y+25,x+79,y+31),fill="#3c4b3c"); d.line((x+79,y+29,x+118,y+19),fill="#39463d",width=4)
    d.line((x+82,y+27,x+116,y+19),fill="#bbc493",width=1)

def cyclone(b):
    x,y,X,Y=b; scene_base(b,"#5e8da3","#315f75",False)
    cx,cy=x+66,y+35
    for i,col in enumerate(["#d5edf0","#b9dde3","#eff9f7","#99c9d2"]):
        pad=i*6; d.arc((x+14+pad,y+5+pad,X-12-pad,Y-5-pad),195+i*25,505-i*20,fill=col,width=4)
    d.ellipse((cx-5,cy-5,cx+5,cy+5),fill="#294f62"); d.line((x+4,Y-7,X-4,Y-7),fill="#eef9f8",width=2)

def ballot(b):
    x,y,X,Y=b; scene_base(b,"#efd4b0","#ae765b")
    shadow_ellipse((x+30,Y-15,x+103,Y-5)); rr((x+35,y+32,x+99,Y-9),4,"#d8d4ca",INK)
    d.rectangle((x+43,y+27,x+92,y+34),fill="#343e47"); poly([(x+54,y+10),(x+87,y+17),(x+82,y+35),(x+49,y+27)],WHITE,"#7e817c")
    d.line((x+60,y+20,x+66,y+25,x+77,y+14),fill=RED,width=3,joint="curve"); d.ellipse((x+86,y+40,x+92,y+46),fill="#f7ce60")

def rocket(b):
    x,y,X,Y=b; scene_base(b,"#263852","#594f55",False)
    d.ellipse((x+10,y+9,x+12,y+11),fill=WHITE); d.ellipse((x+102,y+15,x+105,y+18),fill=WHITE)
    poly([(x+61,y+8),(x+50,y+38),(x+54,y+54),(x+71,y+54),(x+76,y+38)],"#e8e6dc",INK)
    d.ellipse((x+57,y+22,x+69,y+34),fill="#68a9c1"); poly([(x+51,y+40),(x+40,y+54),(x+55,y+50)],RED); poly([(x+74,y+40),(x+85,y+54),(x+71,y+50)],RED)
    poly([(x+57,y+54),(x+63,Y-3),(x+69,y+54)],"#f4c94f"); poly([(x+59,y+54),(x+63,Y-10),(x+67,y+54)],"#ee7446")

def factory(b):
    x,y,X,Y=b; scene_base(b,"#b9b2a3","#6d685d",False)
    for cx,h in [(24,39),(45,29),(96,35)]:
        d.rectangle((x+cx,y+h-18,x+cx+11,Y-8),fill="#665f59",outline="#343638"); d.ellipse((x+cx-2,y+h-23,x+cx+15,y+h-14),fill="#d3c9b9")
    poly([(x+8,Y-8),(x+8,y+46),(x+31,y+37),(x+31,y+46),(x+58,y+35),(x+58,Y-8)],"#8b7765",INK)
    for wx in (16,35,48): d.rectangle((x+wx,y+51,x+wx+6,y+58),fill="#f0bd4e")
    d.ellipse((x+87,y+9,x+111,y+23),fill="#ddd4c8"); d.ellipse((x+104,y+4,x+125,y+18),fill="#e8e0d5")

def island(b):
    x,y,X,Y=b; scene_base(b,"#6ab0c3","#338aa0")
    d.rectangle((x,y+4,X,Y),fill="#4b9eb3")
    pts=[(x+18,y+42),(x+31,y+29),(x+48,y+25),(x+59,y+15),(x+72,y+24),(x+88,y+22),(x+103,y+34),(x+95,y+49),(x+76,y+56),(x+55,y+52),(x+38,y+59)]
    poly(pts,"#78a968","#f2dfae",2); d.line((x+42,y+43,x+82,y+31,x+93,y+40),fill="#d2d09a",width=2)
    d.ellipse((x+64,y+31,x+70,y+37),fill=RED); d.ellipse((x+66,y+33,x+68,y+35),fill=WHITE)

def courtroom(b):
    x,y,X,Y=b; scene_base(b,"#e1c9a0","#86684a",False)
    d.rectangle((x,y+46,X,Y),fill="#745438"); d.rectangle((x+13,y+35,x+116,y+51),fill="#9a744e",outline="#4c3828")
    d.rectangle((x+83,y+18,x+92,y+42),fill="#5b3c29"); d.ellipse((x+75,y+14,x+100,y+24),fill="#9b6a3e",outline="#4a3425")
    d.line((x+91,y+20,x+111,y+39),fill="#573a27",width=4); d.ellipse((x+104,y+35,x+119,y+43),fill="#a77345",outline="#473225")
    d.rectangle((x+24,y+17,x+55,y+34),fill="#f2e7ce",outline="#6b553e"); d.line((x+30,y+23,x+48,y+23),fill=RED,width=2)

def oilrig(b):
    x,y,X,Y=b; scene_base(b,"#e2b46e","#356f7f")
    d.rectangle((x,y+54,X,Y),fill="#2e7184"); d.line((x+33,Y-5,x+57,y+16,x+82,Y-5),fill="#28383d",width=3)
    for yy in (29,41,52): d.line((x+44,y+yy,x+70,y+yy),fill="#314146",width=2)
    d.line((x+57,y+16,x+57,Y-5),fill="#3d4b4e",width=2); d.rectangle((x+23,y+50,x+103,y+57),fill="#343f40")
    d.line((x+73,y+20,x+103,y+20,x+103,y+46),fill="#3c4545",width=2); d.pieslice((x+98,y+39,x+108,y+53),180,540,fill="#f0b33f")

def train(b):
    x,y,X,Y=b; scene_base(b,"#b9d2c4","#627b62")
    d.line((x+7,Y-4,X-6,Y-4),fill="#3e4140",width=3); d.line((x+16,Y-1,x+105,y+48),fill="#8a8173",width=2)
    poly([(x+16,y+34),(x+35,y+22),(x+108,y+22),(x+119,y+51),(x+29,y+51)],"#b94338",INK)
    poly([(x+35,y+25),(x+53,y+25),(x+53,y+37),(x+25,y+37)],"#d7e4df")
    for wx in (59,74,89): d.rectangle((x+wx,y+27,x+wx+10,y+37),fill="#c8e2e2")
    for cx in (38,96): d.ellipse((x+cx,y+46,x+cx+13,y+59),fill="#282e30",outline="#b6ad95")
    d.line((x+24,y+34,x+43,y+26),fill=WHITE,width=1)

# Masthead
d.rectangle((0,0,W,7), fill=RED)
text_box(38,28,"THE DAY IN WORLD NEWS",font(16,True),RED,400,22)
text_box(38,51,"Wednesday 18 November 2026",fit("Wednesday 18 November 2026",948,52,True),INK,948,62)
d.line((38,116,986,116),fill=INK,width=2)
text_box(38,126,"44 stories · 7 regions · 13 illustrated",font(14),MUTED,500,20)

# Numbers band
band=(38,153,986,218); rr(band,7,"#e5ded0")
numbers=[("141","DRONES FIRED"),("126","DOWNED"),("25.9bn km","VOYAGER 1"),("55","FACTORIES SHUT"),("251–11","JEFFRIES VOTE"),("11,300+","EBOLA CASES")]
cell=(band[2]-band[0])/6
for i,(n,cap) in enumerate(numbers):
    x=band[0]+i*cell
    if i: d.line((x,163,x,208),fill="#c6bdae",width=1)
    f=fit(n,cell-18,22,True)
    text_box(x+cell/2,174,n,f,INK,cell-18,28,"ma")
    text_box(x+cell/2,202,cap,fit(cap,cell-14,8,True),MUTED,cell-14,12,"ma")

# Illustrated story grid: 5 + 4 + 4.
stories=[
 ("AIR DEFENCES BLUNT DRONE WAVE","Kyiv reports 126 of 141 aircraft downed.",drone),
 ("RED SEA SHIP CORRIDOR REOPENS","Escorted cargo traffic resumes at dawn.",ship),
 ("EBOLA TEAMS EXPAND RING VACCINE","Clinics trace more than 11,300 cases.",hospital),
 ("JEFFRIES WINS LEADERSHIP VOTE","House caucus delivers a 251–11 mandate.",parliament),
 ("ARMOUR MASSES NEAR FRONTIER","Satellite images show fresh deployments.",tank),
 ("CYCLONE CURVES TOWARD COAST","Warm water drives a tightening spiral.",cyclone),
 ("VOTERS REJECT SNAP REFERENDUM","Turnout rises as final boxes arrive.",ballot),
 ("VOYAGER 1 CALLS FROM DEEP SPACE","Probe answers from 25.9 billion km away.",rocket),
 ("FIFTY-FIVE FACTORIES GO DARK","Energy curbs halt production overnight.",factory),
 ("ISLAND CHAIN MARKS NEW RESERVE","Seven marine habitats gain protection.",island),
 ("COURT ORDERS RECORDS RELEASED","Judges set a forty-eight-hour deadline.",courtroom),
 ("OFFSHORE OUTPUT HITS NEW HIGH","North Sea platforms lift daily supply.",oilrig),
 ("NIGHT TRAIN LINKS TWO CAPITALS","First sleeper service leaves on time.",train),
]
region_cols=["#396c7d","#a85b43","#4f7c67","#8b6b98","#b6803e"]
cards=[]
for row,count in enumerate((5,4,4)):
    gap=10; total=948; cw=(total-gap*(count-1))/count; top=232+row*145
    for j in range(count):
        idx=sum((5,4,4)[:row])+j; x=38+j*(cw+gap); b=(round(x),top,round(x+cw),top+134); cards.append(b)
        rr(b,6,WHITE,"#d3cbbc")
        vign=(b[0]+5,b[1]+5,b[2]-5,b[1]+76); stories[idx][2](vign)
        d.rectangle((b[0]+5,b[1]+72,b[0]+9,b[1]+76),fill=region_cols[idx%5])
        hf=fit(stories[idx][0],b[2]-b[0]-12,11,True)
        text_box(b[0]+6,b[1]+84,stories[idx][0],hf,INK,b[2]-b[0]-12,14)
        sf=fit(stories[idx][1],b[2]-b[0]-12,9,False,6)
        text_box(b[0]+6,b[1]+105,stories[idx][1],sf,MUTED,b[2]-b[0]-12,12)
assert len(cards)==13

# World map panel
mp=(38,672,986,802); rr(mp,7,"#dbe2dc")
text_box(52,688,"THE WORLD AT A GLANCE",font(11,True),INK,200,16)
text_box(970,688,"SEVEN REGIONS",font(8,True),MUTED,100,12,"ra")
# Simplified bespoke continent silhouettes.
poly([(76,727),(101,709),(137,713),(159,728),(151,741),(127,744),(116,766),(92,756)],"#9baa91")
poly([(159,753),(179,759),(187,782),(174,795),(160,776)],"#9baa91")
poly([(254,714),(279,707),(305,715),(321,735),(308,753),(286,744),(274,768),(257,754)],"#9baa91")
poly([(313,714),(361,706),(404,714),(446,708),(500,722),(526,741),(500,750),(466,739),(430,758),(393,745),(359,756),(337,738)],"#9baa91")
poly([(536,760),(557,752),(584,761),(591,779),(568,790),(543,780)],"#9baa91")
poly([(626,725),(650,713),(682,719),(695,735),(679,748),(647,744)],"#9baa91")
poly([(738,763),(757,752),(787,756),(800,773),(779,786),(750,782)],"#9baa91")
markers=[(116,724,"AMERICAS"),(174,769,"S. AMERICA"),(290,730,"EUROPE"),(372,731,"AFRICA"),(468,728,"ASIA"),(565,771,"OCEANIA"),(765,770,"PACIFIC")]
for i,(cx,cy,label) in enumerate(markers):
    d.ellipse((cx-4,cy-4,cx+4,cy+4),fill=RED,outline=WHITE,width=1)
    text_box(cx,cy-9,label,font(6,True),INK,68,9,"ms")

# Remaining 31 headlines
text_box(38,818,"31 MORE DEVELOPMENTS",font(12,True),RED,220,17)
more=[
"Ceasefire monitors reach border post","Markets climb on softer inflation","Flood barriers raised along Danube","UN convoy crosses northern checkpoint","Copper price touches annual high","Mayor unveils heat-resilient streets","Scientists catalogue rare coral","Airport trials hydrogen ground fleet","Teachers approve revised settlement","Reservoir returns above half capacity","New archive opens wartime letters","Coastal radar network goes live","Central bank holds benchmark rate","Farm exports clear inspection backlog","Wildfire crews contain western flank","Museum returns twelve carved panels","Solar auction draws record-low bid","Rail union suspends Friday strike","Opposition names shadow cabinet","Telecom cable repaired before noon","Arctic mission maps thinning shelf","Port adds automated customs lane","Senate advances privacy package","Health ministry widens flu survey","Researchers date desert settlement","City restores river ferry service","Peace talks move to second session","Rare-earth plant passes safety review","Library digitises colonial newspapers","Marathon route shifts around works","Weather service upgrades warnings"]
cols=3; colw=300; gap=24
for i,h in enumerate(more):
    c=i//11; r=i%11; x=38+c*(colw+gap); y=842+r*12
    text_box(x,y,f"{i+14:02d}",font(7,True),RED,16,10)
    f=fit(h,colw-24,9,False,7)
    text_box(x+21,y,h,f,INK,colw-21,11)

d.line((38,979,986,979),fill="#c8bfb0")
text_box(38,991,"Events checked against reporting of 18 November 2026.",font(8),MUTED,500,12)
text_box(986,991,"THE DAY · EDITION 323",font(8,True),MUTED,180,12,"ra")

# Structural assertions.
sections=[(0,0,1024,146),band,(38,232,986,656),mp,(38,818,986,974),(38,979,986,1008)]
for a,b in zip(sections,sections[1:]): assert a[3] <= b[1], (a,b)
assert len(stories)==13 and len(more)==31
img.save(OUT,optimize=True,compress_level=9)
assert Image.open(OUT).size==(1024,1024)
assert OUT.stat().st_size < 1024*1024
print(f"{OUT.name}: {OUT.stat().st_size} bytes; {len(stories)} vignettes")
