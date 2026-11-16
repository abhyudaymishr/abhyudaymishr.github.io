"""Rebuild original, decorative mathematical SVGs; no external assets or packages."""
from pathlib import Path
import math
import random

OUT = Path(__file__).resolve().parents[1] / 'assets' / 'images'
OUT.mkdir(parents=True, exist_ok=True)

def svg(name, width, height, background, body):
    (OUT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="{background}"/>{body}</svg>\n')

def path(points, color, opacity, width=1):
    data = ' '.join(f'{"M" if i == 0 else "L"}{x:.1f},{y:.1f}' for i, (x, y) in enumerate(points))
    return f'<path d="{data}" fill="none" stroke="{color}" stroke-opacity="{opacity:.2f}" stroke-width="{width}"/>'

def torus(cx, cy, scale, count=66, samples=150):
    body = ''
    for i in range(count):
        phi = 2 * math.pi * i / count
        points=[]
        for j in range(samples + 1):
            t = 2 * math.pi * j / samples
            r = 1.75 + .65 * math.cos(t * 3 + phi)
            x = r * math.cos(t)
            y = r * math.sin(t)
            z = .65 * math.sin(t * 3 + phi)
            rx = x * .92 + z * .38
            rz = -x * .38 + z * .92
            ry = y * .68 - rz * .73
            depth = y * .73 + rz * .68
            p = 4.9 / (4.9 + depth)
            points.append((cx + scale * rx * p, cy + scale * ry * p))
        color = ['#759bff','#bbc4ff','#9381e9','#659ce0'][i % 4]
        body += path(points, color, .25 + .3 * (math.sin(phi) + 1) / 2, .8 if i % 5 else 1.25)
    return body

rng=random.Random(42)
stars=''.join(f'<circle cx="{rng.randrange(610,1600)}" cy="{rng.randrange(50,980)}" r="{rng.choice([.6,.8,1.1])}" fill="#a9bfff" opacity="{rng.uniform(.1,.4):.2f}"/>' for _ in range(95))
svg('structure.svg',1600,1000,'#080c18', '<defs><radialGradient id="h"><stop stop-color="#5262ca" stop-opacity=".18"/><stop offset="1" stop-color="#080c18" stop-opacity="0"/></radialGradient></defs><ellipse cx="1190" cy="520" rx="570" ry="480" fill="url(#h)"/>'+stars+torus(1160,510,178))
svg('quantum.svg',800,560,'#111020',torus(410,285,86,45,110))
body=''
for row in range(47):
    points=[]
    for col in range(100):
        x=col*9-40; y=65+row*10
        bump=90*math.exp(-((x-430)**2/23000+(y-300)**2/16000))
        y+=math.sin(x/70+row/17)*12 + math.sin(x/100-row/7)*bump
        points.append((x,y))
    body+=path(points,['#599be0','#8ab9ea','#c0ddf7'][row%3],.35+row/120,.9)
svg('operators.svg',800,560,'#0d2944',body)
body=''
for y in range(15):
    points=[]
    for x in range(22):
        xx=25+x*37; yy=45+y*34+math.sin(x/3)*30
        xx+=math.sin(y/2.7)*26
        intensity=math.exp(-((xx-475)**2+(yy-260)**2)/26000)
        radius=1.3+intensity*5
        body+=f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{radius:.1f}" fill="{["#dca988","#c57b59","#f4d0b5"][x%3]}" opacity="{.2+intensity*.7:.2f}"/>'
        points.append((xx,yy))
    body+=path(points,'#d7ac98',.13,.6)
svg('oculon.svg',800,560,'#30201f',body)
body=''
for line in range(20):
    points=[]
    for j in range(500):
        t=math.pi*2*j/499
        x=math.sin(t)+2*math.sin(2*t); y=math.cos(t)-2*math.cos(2*t);z=-math.sin(3*t)
        points.append((400+(x+.025*line)*75,270+(y*.68+z*.65+.015*line)*75))
    body+=path(points,['#a1d5ba','#6ea99c','#d3e7c8'][line%3],.65,.9)
svg('topology.svg',800,560,'#142c29',body)
body=''
for row in range(8):
    for col in range(15):
        x=100+col*41; y=125+row*39
        hue=['#b6b3e0','#7c93b6','#d6cce5','#9eacd1'][(row*3+col)%4]
        body+=f'<rect x="{x}" y="{y}" width="27" height="27" rx="5" fill="{hue}" opacity="{.25+.65*rng.random():.2f}"/>'
svg('language.svg',800,560,'#222437',body)
(OUT/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#080c18"/><path d="m24 8 14 8v16l-14 8-14-8V16l14-8Zm0 0v32M10 16l28 16m0-16L10 32" fill="none" stroke="#b6ccff" stroke-width="1.8" stroke-linejoin="round"/></svg>\n')
svg('seo-card.svg',1200,630,'#080c18',torus(990,315,95,36,100)+'<g fill="#fff" font-family="Arial, sans-serif"><text x="75" y="115" font-size="24">ABHYUDAY MISHRA</text><text x="75" y="275" font-size="62">Learning from the</text><text x="75" y="350" font-size="62">structure of things.</text><text x="75" y="480" font-size="22" fill="#bfc9df">Scientific machine learning · Quantum computing</text><text x="75" y="565" font-size="18" fill="#a6b2cd">abhyudaymishr.github.io</text></g>')
print('Generated seven original mathematical visuals and favicon')

# Optional Pillow export for social platforms that do not accept SVG previews.
try:
    from PIL import Image, ImageDraw, ImageFont
    import re
    factor = 2
    canvas = Image.new('RGB', (1200*factor, 630*factor), '#080c18')
    draw = ImageDraw.Draw(canvas)
    for d, color, opacity in re.findall(r'<path d="([^"]+)" fill="none" stroke="([^"]+)" stroke-opacity="([^"]+)"', torus(995, 320, 95, 36, 100)):
        points = [(float(x)*factor, float(y)*factor) for x, y in re.findall(r'[ML]([\d.\-]+),([\d.\-]+)', d)]
        rgb=tuple(int(color[i:i+2],16) for i in (1,3,5)); alpha=float(opacity)
        mixed=tuple(int(a*(alpha+.15)+b*(.85-alpha)) for a,b in zip(rgb,(8,12,24)))
        draw.line(points, fill=mixed, width=2)
    candidates=['/System/Library/Fonts/Helvetica.ttc','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    font_path=next((p for p in candidates if Path(p).exists()),None)
    def text(x,y,value,size,color):
        font=ImageFont.truetype(font_path,size*factor) if font_path else ImageFont.load_default(size=size*factor)
        draw.text((x*factor,y*factor),value,font=font,fill=color)
    text(75,80,'ABHYUDAY MISHRA',24,'#d6dff4')
    text(71,215,'Learning from the',62,'#ffffff')
    text(71,290,'structure of things.',62,'#ffffff')
    text(75,455,'Scientific machine learning · Quantum computing',22,'#bfc9df')
    text(75,550,'abhyudaymishr.github.io',18,'#a6b2cd')
    canvas.resize((1200,630),Image.Resampling.LANCZOS).save(OUT/'seo-card.png',optimize=True)
    print('Exported 1200 × 630 PNG social card')
except ImportError:
    print('PNG export requires Pillow; existing PNG is retained')
