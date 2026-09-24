# Draws the sky + islands behind the dragon. Tiles left-right so it can scroll.
from PIL import Image, ImageDraw, ImageFilter
import os, math, random

OUT = os.path.join(os.path.dirname(__file__), "..", "art")
W, H = 2560, 720

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def sky():
    top, mid, low = (22, 28, 56), (86, 66, 118), (232, 132, 96)
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        c = lerp(top, mid, t / 0.62) if t < 0.62 else lerp(mid, low, (t - 0.62) / 0.38)
        d.line([(0, y), (W, y)], fill=c)
    return im

def stars(im):
    d = ImageDraw.Draw(im)
    rnd = random.Random(7)
    for _ in range(260):
        x, y = rnd.randrange(W), rnd.randrange(int(H * 0.5))
        r = rnd.choice([0, 0, 1])
        b = rnd.randint(150, 255)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(b, b, min(255, b + 20)))

def sun(im):
    g = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(g)
    cx, cy, r = 1900, 470, 150
    for i in range(70, 0, -1):
        f = i / 70
        rr = int(r + f * 320)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=lerp((0, 0, 0), (120, 60, 30), (1 - f) ** 2))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 150))
    g = g.filter(ImageFilter.GaussianBlur(14))
    return Image.blend(im, Image.blend(im, g, 0.0), 0.0) if False else Image.composite(
        Image.new("RGB", (W, H), (255, 255, 255)), im, Image.new("L", (W, H), 0)) if False else _screen(im, g)

def _screen(a, b):
    pa, pb = a.load(), b.load()
    out = Image.new("RGB", (W, H))
    po = out.load()
    for y in range(H):
        for x in range(W):
            r1, g1, b1 = pa[x, y]; r2, g2, b2 = pb[x, y]
            po[x, y] = (255 - (255 - r1) * (255 - r2) // 255,
                        255 - (255 - g1) * (255 - g2) // 255,
                        255 - (255 - b1) * (255 - b2) // 255)
    return out

def islands(im, y0, colour, count, seed, scale):
    """Sea stacks like the ones round Berk. Wraps at the edges."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rnd = random.Random(seed)
    for i in range(count):
        x = int(i * (W / count) + rnd.randint(-60, 60))
        w = int(rnd.randint(90, 220) * scale)
        h = int(rnd.randint(120, 300) * scale)
        top = y0 - h
        d.polygon([(x - w, y0 + 40), (x - int(w * 0.72), top + int(h * 0.30)),
                   (x - int(w * 0.30), top), (x + int(w * 0.24), top + int(h * 0.12)),
                   (x + int(w * 0.70), top + int(h * 0.42)), (x + w, y0 + 40)], fill=colour)
        if x - w < 0:
            d.polygon([(x - w + W, y0 + 40), (x - int(w * 0.72) + W, top + int(h * 0.30)),
                       (x - int(w * 0.30) + W, top), (x + int(w * 0.24) + W, top + int(h * 0.12)),
                       (x + int(w * 0.70) + W, top + int(h * 0.42)), (x + w + W, y0 + 40)], fill=colour)
    im.paste(layer, (0, 0), layer)

def clouds(im, y, colour, seed, n, scale):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rnd = random.Random(seed)
    for _ in range(n):
        cx = rnd.randrange(W); cy = y + rnd.randint(-70, 70)
        for k in range(rnd.randint(4, 7)):
            rx = int(rnd.randint(60, 150) * scale); ry = int(rx * rnd.uniform(0.22, 0.34))
            ox = rnd.randint(-160, 160); oy = rnd.randint(-14, 14)
            d.ellipse([cx + ox - rx, cy + oy - ry, cx + ox + rx, cy + oy + ry], fill=colour)
    layer = layer.filter(ImageFilter.GaussianBlur(3))
    im.paste(layer, (0, 0), layer)

im = sky()
stars(im)
im = sun(im)
clouds(im, 300, (150, 110, 150, 70), 3, 14, 1.3)
islands(im, 660, (58, 44, 86), 7, 11, 1.0)
clouds(im, 520, (226, 150, 130, 80), 5, 10, 1.0)
islands(im, 720, (32, 24, 52), 6, 22, 1.4)
os.makedirs(OUT, exist_ok=True)
im.save(os.path.join(OUT, "sky.png"))
print("wrote sky.png")
