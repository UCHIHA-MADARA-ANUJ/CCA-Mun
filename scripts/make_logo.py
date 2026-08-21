#!/usr/bin/env python3
"""
VANGUARD bloc logo — pure-Pillow rebuild of the hand-coded vector design.
Roster v3 (11 members, confirmed 20 Aug 2026): Japan, Canada, India, Kazakhstan,
Barbados, Philippines, Iran, Egypt, Switzerland, South Africa, Mexico.
  Japan (top, larger) · rest clockwise at 32.73° spacing · ring radius 430
Output: assets/vanguard_logo_final.png"""
import math
from PIL import Image, ImageDraw, ImageFont

S = 2.0  # supersample (svg 1200 -> 2400 px)
W, H = int(1200 * S), int(1200 * S)
NAVY = (11, 30, 58)        # #0B1E3A
GOLD = (201, 162, 39)      # #C9A227
GLOBE = (232, 238, 247)    # #E8EEF7
MERID = (124, 147, 181)    # #7C93B5
GREEN = (31, 160, 90)      # #1FA05A
WHITE = (255, 255, 255)

def s(v):
    return v * S

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

CX, CY = s(600), s(600)

# ---- outer navy disc + gold trim ----
d.ellipse([CX - s(560), CY - s(560), CX + s(560), CY + s(560)], fill=NAVY)
d.ellipse([CX - s(560), CY - s(560), CX + s(560), CY + s(560)],
          outline=GOLD, width=max(1, int(s(6))))
=======
# inner navy disc + gold trim
>>>>>>> 1c79f21891be7c5397724507400d7c22beef5a93
d.ellipse([CX - s(330), CY - s(330), CX + s(330), CY + s(330)], fill=NAVY)
d.ellipse([CX - s(330), CY - s(330), CX + s(330), CY + s(330)],
          outline=GOLD, width=max(1, int(s(4))))

<<<<<<< HEAD
# ---- badge machinery ----
def badge(cx, cy, r, draw_fn):
    rad = int(s(r))
    layer = Image.new("RGB", (rad * 2, rad * 2), NAVY)
    draw_fn(ImageDraw.Draw(layer), rad)
    mask = Image.new("L", (rad * 2, rad * 2), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, rad * 2 - 1, rad * 2 - 1], fill=255)
    img.paste(layer, (int(cx * S) - rad, int(cy * S) - rad), mask)
    d.ellipse([cx * S - rad, cy * S - rad, cx * S + rad, cy * S + rad],
              outline=GOLD, width=max(1, int(s(4))))

def bar(ld, r, color, x0, y0, x1, y1):
    ld.rectangle([x0, y0, x1, y1], fill=color)

# ---- flags ----def japan(ld, r):
    ld.ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=WHITE)
    cr = r * 0.58
    ld.ellipse([r - cr, r - cr, r + cr, r + cr], fill=(188, 0, 45))

def canada(ld, r):
    w = 2 * r
    third = w / 3
    red = (213, 43, 30)
    bar(ld, r, red, 0, 0, third, w)
    bar(ld, r, WHITE, third, 0, 2 * third, w)
    bar(ld, r, red, 2 * third, 0, w, w)    ld.polygon([(r, r * 0.28), (r + r * 0.24, r * 0.52), (r + r * 0.12, r * 0.58),
                (r + r * 0.20, r * 0.78), (r + r * 0.05, r * 0.68),
                (r + r * 0.02, r * 0.95), (r - r * 0.02, r * 0.95),
                (r - r * 0.05, r * 0.68), (r - r * 0.20, r * 0.78),
                (r - r * 0.12, r * 0.58), (r - r * 0.24, r * 0.52)],
               fill=red)
def india(ld, r):
    w = 2 * r
    hh = w / 3
    bar(ld, r, (255, 153, 51), 0, 0, w, hh)
    bar(ld, r, WHITE, 0, hh, w, 2 * hh)
    bar(ld, r, (19, 136, 8), 0, 2 * hh, w, w)
    cr = r * 0.24
    ld.ellipse([r - cr, r - cr, r + cr, r + cr], outline=(0, 0, 128), width=max(1, int(r * 0.06)))

def kazakhstan(ld, r):
    w = 2 * r
    bar(ld, r, (0, 175, 202), 0, 0, w, w)  # #00AFCA
    sun = r * 0.34
    ld.ellipse([r - sun, r - sun, r + sun, r + sun], fill=(254, 196, 11))  # #FEC40B
def barbados(ld, r):
    w = 2 * r
    third = w / 3
    blue = (0, 38, 127)
    yellow = (255, 199, 38)
    bar(ld, r, blue, 0, 0, third, w)
    bar(ld, r, yellow, third, 0, 2 * third, w)
    bar(ld, r, blue, 2 * third, 0, w, w)
=======
    # trident
>>>>>>> 1c79f21891be7c5397724507400d7c22beef5a93
    black = (0, 0, 0)
    shaft_w = max(2, int(r * 0.09))
    ld.rectangle([r - shaft_w / 2, r * 0.30, r + shaft_w / 2, r * 1.85], fill=black)
    ld.rectangle([r - r * 0.55, r * 0.24, r + r * 0.55, r * 0.24 + shaft_w * 1.4], fill=black)
    prong_w = max(2, int(r * 0.10))
    ld.rectangle([r - r * 0.55, r * 0.06, r - r * 0.55 + prong_w, r * 0.28], fill=black)
    ld.rectangle([r - prong_w / 2, r * 0.02, r + prong_w / 2, r * 0.28], fill=black)
    ld.rectangle([r + r * 0.55 - prong_w, r * 0.06, r + r * 0.55, r * 0.28], fill=black)
<<<<<<< HEAD
def philippines(ld, r):
    w = 2 * r
    bar(ld, r, (0, 56, 168), 0, 0, w, r)
    bar(ld, r, (206, 17, 38), 0, r, w, w)
    ld.polygon([(0, 0), (0, w), (w * 0.62, r)], fill=WHITE)
def iran(ld, r):
    w = 2 * r
    hh = w / 3
    bar(ld, r, (35, 159, 64), 0, 0, w, hh)
    bar(ld, r, WHITE, 0, hh, w, 2 * hh)
    bar(ld, r, (218, 0, 0), 0, 2 * hh, w, w)
def egypt(ld, r):
    w = 2 * r
    hh = w / 3
    bar(ld, r, (206, 17, 38), 0, 0, w, hh)
    bar(ld, r, WHITE, 0, hh, w, 2 * hh)
    bar(ld, r, (0, 0, 0), 0, 2 * hh, w, w)
def switzerland(ld, r):
    w = 2 * r
    bar(ld, r, (213, 43, 30), 0, 0, w, w)
    cw = r * 0.62
    th = max(2, int(r * 0.12))
    bar(ld, r, WHITE, r - cw / 2, r - th / 2, r + cw / 2, r + th / 2)
    bar(ld, r, WHITE, r - th / 2, r - cw / 2, r + th / 2, r + cw / 2)
def southafrica(ld, r):
    w = 2 * r
    bar(ld, r, (224, 60, 49), 0, 0, w, r)
    bar(ld, r, (0, 20, 137), 0, r, w, w)
    ld.polygon([(0, 0), (0, w), (w * 0.78, r)], fill=(0, 0, 0))
    ld.polygon([(0, r * 0.25), (0, r * 1.75), (w * 0.95, r)], fill=(255, 182, 18))
    bar(ld, r, (0, 122, 77), 0, r * 0.40, w, r * 1.60)
def mexico(ld, r):
    w = 2 * r
    third = w / 3
    bar(ld, r, (0, 104, 71), 0, 0, third, w)
    bar(ld, r, WHITE, third, 0, 2 * third, w)
    bar(ld, r, (206, 17, 38), 2 * third, 0, w, w)
    cr = r * 0.16
    ld.ellipse([r - cr, r * 0.45, r + cr, r * 0.45 + 2 * cr], fill=(141, 101, 32))

# ---- ring layout: 11 badges, 32.73° clockwise from top ----
RING = 430.0
BIG = 92.0
SMALL = 62.0
members = [
    ("japan", 0.0, japan, BIG),
    ("canada", 32.73, canada, SMALL),
    ("india", 65.45, india, SMALL),
    ("kazakhstan", 98.18, kazakhstan, SMALL),
    ("barbados", 130.91, barbados, SMALL),
    ("philippines", 163.64, philippines, SMALL),
    ("iran", 196.36, iran, SMALL),
    ("egypt", 229.09, egypt, SMALL),
    ("switzerland", 261.82, switzerland, SMALL),
    ("southafrica", 294.55, southafrica, SMALL),
    ("mexico", 327.27, mexico, SMALL),
]
for name, ang, fn, rad in members:
    a = math.radians(ang)
    cx = 600 + RING * math.sin(a)
    cy = 600 - RING * math.cos(a)
    badge(cx, cy, rad, fn)
# ---- globe ----
GCX, GCY = s(600), s(580)
GR = s(170)
d.ellipse([GCX - GR, GCY - GR, GCX + GR, GCY + GR], fill=GLOBE)
for rx in (s(42.5), s(85.0), s(127.5)):
    d.ellipse([GCX - rx, GCY - GR, GCX + rx, GCY + GR], outline=MERID, width=max(1, int(s(3))))
for ly in (s(495), s(580), s(665)):
    d.line([s(430), ly, s(770), ly], fill=MERID, width=max(1, int(s(3))))

# ---- orbit + leaf ----
orbit = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(orbit)
od.ellipse([GCX - s(215), GCY - s(78), GCX + s(215), GCY + s(78)], outline=GREEN, width=max(2, int(s(9))))
orbit = orbit.rotate(-18, center=(GCX, GCY), resample=Image.BICUBIC)
img = Image.alpha_composite(img.convert("RGBA"), orbit).convert("RGB")
d = ImageDraw.Draw(img)
leaf = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(leaf)
lcx, lcy = s(800), s(578)
ld.ellipse([lcx - s(26), lcy - s(46), lcx + s(26), lcy + s(46)], fill=GREEN)
leaf = leaf.rotate(-40, center=(lcx, lcy), resample=Image.BICUBIC)
img = Image.alpha_composite(img.convert("RGBA"), leaf).convert("RGB")
d = ImageDraw.Draw(img)

# ---- wordmark ----
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(s(62)))word = "VANGUARD"
spacing = s(10)
widths = [d.textlength(ch, font=font) for ch in word]
total = sum(widths) + spacing * (len(word) - 1)
x = CX - total / 2
y = s(825) - font.getbbox(word)[3] / 2
for ch, cw in zip(word, widths):
    d.text((x, y), ch, font=font, fill=WHITE)
    x += cw + spacing

img.save("assets/vanguard_logo_final.png", "PNG")
print("saved assets/vanguard_logo_final.png", img.size)

def px(x, y):
    return img.getpixel((int(x * S), int(y * S)))

print("japan top          :", px(600, 170), "expect white")
print("kazakhstan 98.2°   :", px(1025.6, 661.2), "expect light blue (0,175,202)")
print("barbados 130.9°    :", px(924.8, 881.8), "expect yellow (255,199,38)")
print("mexico 327.3°      :", px(367.5, 238.2), "expect white (255,255,255)")