# Draws Kaian's black dragon. Run it again after changing colours:
#   python3 tools/make_dragon.py
from PIL import Image, ImageDraw
import os, math

OUT = os.path.join(os.path.dirname(__file__), "..", "art")

# Kaian's dragon - the black one
HERO = dict(BODY=(54, 60, 80), BELLY=(98, 106, 134), WING=(40, 46, 66),
            EYE=(140, 240, 160), HORN=(240, 238, 230), rider=True)
# the evil ones
EVIL = dict(BODY=(146, 44, 42), BELLY=(206, 118, 74), WING=(104, 28, 30),
            EYE=(255, 214, 80), HORN=(246, 238, 214), rider=False)

BODY = BELLY = WING = EYE = HORN = None

def draw(flap, kit):
    global BODY, BELLY, WING, EYE, HORN
    BODY, BELLY, WING, EYE, HORN = kit['BODY'], kit['BELLY'], kit['WING'], kit['EYE'], kit['HORN']
    """flap 0 = wings up, 1 = level, 2 = wings down"""
    W, H = 620, 430
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 300, 252
    shoulder = (cx + 6, cy - 46)

    lift = [1.0, 0.55, 0.05][flap]
    drop = [0.0, 0.22, 0.5][flap]

    def wing_pts(scale, sweep):
        sx, sy = shoulder
        tips = [(-0.30, -1.00), (-0.72, -0.86), (-1.00, -0.50), (-1.02, -0.12)]
        webs = [(-0.52, -0.52), (-0.80, -0.34), (-0.90, -0.02)]
        def m(p):
            x, y = p
            return (sx + x * scale * sweep, sy + (y * lift + drop) * scale)
        pts = [(sx, sy), m(tips[0]), m(webs[0]), m(tips[1]), m(webs[1]),
               m(tips[2]), m(webs[2]), m(tips[3]), m((-0.34, 0.18))]
        return pts, [m(t) for t in tips]

    far, _ = wing_pts(150, 0.78)
    d.polygon(far, fill=tuple(int(c * 0.55) for c in WING))

    tail = []
    N = 26
    for t in range(N):
        f = t / (N - 1)
        x = cx - 40 - f * 150
        y = cy + 24 + math.sin(f * 2.6) * 52
        tail.append((x, y - (24 * (1 - f) + 3)))
    for t in range(N - 1, -1, -1):
        f = t / (N - 1)
        x = cx - 40 - f * 150
        y = cy + 24 + math.sin(f * 2.6) * 52
        tail.append((x, y + (24 * (1 - f) + 3)))
    d.polygon(tail, fill=BODY)
    fx, fy = cx - 190, cy + 24 + math.sin(2.6) * 52
    d.polygon([(fx + 8, fy - 6), (fx - 52, fy - 42), (fx - 36, fy + 4), (fx - 58, fy + 44)], fill=WING)

    d.ellipse([cx - 86, cy - 56, cx + 86, cy + 72], fill=BODY)
    d.ellipse([cx - 50, cy - 2, cx + 58, cy + 70], fill=BELLY)

    for (sx2, sy2, h) in [(-66, -36, 22), (-34, -50, 28), (2, -56, 30)]:
        d.polygon([(cx + sx2, cy + sy2), (cx + sx2 + 14, cy + sy2 - h), (cx + sx2 + 27, cy + sy2 + 4)], fill=WING)

    d.polygon([(cx + 40, cy - 40), (cx + 92, cy - 116), (cx + 134, cy - 92), (cx + 82, cy - 10)], fill=BODY)
    d.ellipse([cx + 90, cy - 152, cx + 190, cy - 84], fill=BODY)
    d.ellipse([cx + 146, cy - 130, cx + 214, cy - 92], fill=BODY)
    d.polygon([(cx + 196, cy - 124), (cx + 224, cy - 112), (cx + 196, cy - 98)], fill=BODY)
    d.ellipse([cx + 150, cy - 106, cx + 206, cy - 86], fill=BELLY)
    d.polygon([(cx + 108, cy - 140), (cx + 82, cy - 206), (cx + 132, cy - 150)], fill=HORN)
    d.polygon([(cx + 132, cy - 146), (cx + 122, cy - 204), (cx + 154, cy - 144)], fill=HORN)
    d.ellipse([cx + 148, cy - 132, cx + 174, cy - 106], fill=(255, 255, 255))
    d.ellipse([cx + 156, cy - 128, cx + 170, cy - 108], fill=EYE)
    d.ellipse([cx + 161, cy - 126, cx + 167, cy - 110], fill=(16, 16, 20))
    d.ellipse([cx + 204, cy - 116, cx + 213, cy - 108], fill=(18, 18, 28))

    d.rounded_rectangle([cx - 56, cy + 38, cx - 16, cy + 100], radius=16, fill=tuple(int(c * 0.66) for c in BODY))
    d.rounded_rectangle([cx - 4, cy + 44, cx + 40, cy + 112], radius=18, fill=tuple(int(c * 0.82) for c in BODY))
    d.rounded_rectangle([cx + 30, cy + 104, cx + 76, cy + 126], radius=10, fill=tuple(int(c * 0.82) for c in BODY))
    for k in range(3):
        d.polygon([(cx + 70, cy + 106 + k * 7), (cx + 90, cy + 104 + k * 7), (cx + 70, cy + 112 + k * 7)], fill=HORN)


    near, tips = wing_pts(190, 1.0)
    d.polygon(near, fill=WING)
    bone = tuple(int(c * 0.66) for c in WING)
    sx, sy = shoulder
    for t in tips:
        d.line([(sx, sy), t], fill=bone, width=6)
    d.ellipse([sx - 9, sy - 9, sx + 9, sy + 9], fill=bone)

    # --- Hicup, sitting on the dragon's back
    if not kit['rider']:
        return im
    rx, ry = cx + 14, cy - 104
    SKIN, TUNIC, HAIR = (226, 186, 150), (108, 86, 62), (128, 86, 52)
    d.polygon([(rx - 4, ry + 34), (rx + 20, ry + 30), (rx + 34, ry + 58), (rx + 12, ry + 60)], fill=(70, 56, 40))
    d.rounded_rectangle([rx - 10, ry + 6, rx + 22, ry + 42], radius=11, fill=TUNIC)
    d.line([(rx + 16, ry + 16), (rx + 46, ry + 26)], fill=SKIN, width=9)
    d.ellipse([rx - 2, ry - 20, rx + 28, ry + 10], fill=SKIN)
    d.polygon([(rx - 3, ry - 8), (rx + 2, ry - 24), (rx + 27, ry - 20), (rx + 29, ry - 4)], fill=HAIR)
    d.ellipse([rx + 18, ry - 10, rx + 24, ry - 4], fill=(30, 30, 40))

    return im

os.makedirs(OUT, exist_ok=True)
JOBS = [("dragon", HERO), ("evil", EVIL)]
for stem, kit in JOBS:
  for i in range(3):
    im = draw(i, kit)
    im = im.crop(im.getbbox()).resize((248, 0) if False else (248, int(248 * im.crop(im.getbbox()).size[1] / im.crop(im.getbbox()).size[0])), Image.LANCZOS)
    im.save(os.path.join(OUT, f"{stem}_{i+1}.png"))
print("wrote dragon + evil frames")
