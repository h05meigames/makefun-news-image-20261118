#!/usr/bin/env python3
"""Render the news-image-20261118 front page: a 1024x1024 newspaper page
summing up Wednesday 18 November 2026, drawn with PIL (no network, no
randomness — the same script always writes the same bytes)."""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 234)
INK = (17, 17, 17)
RED = (166, 25, 46)
BLUE = (28, 78, 122)
SAND = (217, 196, 143)
GRAY = (90, 90, 90)

F = "/usr/share/fonts/truetype/liberation/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
SERIF_I = lambda s: font("LiberationSerif-Italic.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)
SANS = lambda s: font("LiberationSans-Regular.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(text, f, x, y, maxw, leading, fill=INK):
    for line in wrap(text, f, maxw):
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y

def rule(x0, y, x1, w=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)

def burst(cx, cy, r, cols):
    for (dx, dy, rr, c) in cols:
        d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=c)

MX = 36
RX = W - MX

# ---------- masthead ----------
d.text((W // 2, 18), "THE WORLD", font=SERIF_B(84), fill=INK, anchor="ma")
d.text((W // 2, 104), "The day's news in one page", font=SERIF_I(19), fill=GRAY, anchor="ma")
rule(MX, 134, RX, 3)
rule(MX, 139, RX, 1)
d.text((MX, 146), "WEDNESDAY, 18 NOVEMBER 2026", font=SANS_B(18), fill=RED)
d.text((RX, 146), "WORLD NEWS  •  ONE IMAGE", font=SANS_B(18), fill=INK, anchor="ra")
rule(MX, 172, RX, 1)

# ---------- lead story: the Gulf ----------
y = 184
d.text((MX, y), "THE GULF  —  WAR WIDENS", font=SANS_B(19), fill=RED)
y = 208
y = para("Iran strikes U.S. bases in Kuwait and Bahrain after America hits Qeshm",
         SERIF_B(44), MX, y, RX - MX, 50)
y += 2
y = para("Tehran launches drones at Ali Al Salem Air Base and targets in Bahrain, "
         "hours after U.S. warplanes struck a missile site on Qeshm Island.",
         SERIF_I(20), MX, y, RX - MX, 26, fill=(60, 60, 60))
y += 6
PX, PY, PW, PH = MX, y, RX - MX, 126
d.rectangle([PX, PY, PX + PW, PY + PH], fill=BLUE)
# land masses: Arabia below-left, Iran above-right
d.polygon([(PX, PY), (PX + 560, PY), (PX + 520, PY + 34), (PX + 300, PY + 26),
           (PX + 120, PY + 40), (PX, PY + 30)], fill=SAND)
d.polygon([(PX, PY + PH), (PX + PW, PY + PH), (PX + PW, PY + PH - 30),
           (PX + 700, PY + PH - 46), (PX + 420, PY + PH - 28),
           (PX + 180, PY + PH - 40), (PX, PY + PH - 26)], fill=SAND)
# gulf water line
d.line([(PX + 60, PY + 84), (PX + 880, PY + 66)], fill=(120, 170, 210), width=3)
# Kuwait marker (top-left) and Bahrain (centre)
KX, KY = PX + 150, PY + 58
d.ellipse([KX - 5, KY - 5, KX + 5, KY + 5], fill=(255, 255, 255))
d.text((KX + 10, KY - 9), "KUWAIT", font=SANS_B(14), fill=(255, 255, 255))
BX2, BY2 = PX + 470, PY + 76
d.ellipse([BX2 - 5, BY2 - 5, BX2 + 5, BY2 + 5], fill=(255, 255, 255))
d.text((BX2 + 10, BY2 - 9), "BAHRAIN", font=SANS_B(14), fill=(255, 255, 255))
# Qeshm island + explosion (right)
QX, QY = PX + 740, PY + 52
d.polygon([(QX - 60, QY + 6), (QX + 60, QY), (QX + 52, QY + 14), (QX - 52, QY + 18)],
          fill=(196, 172, 118))
d.text((QX - 30, QY + 20), "QESHM I.", font=SANS_B(13), fill=(255, 255, 255))
burst(QX, QY - 22, 0, [(0, 0, 20, (255, 140, 0)), (-12, 7, 12, (255, 190, 0)),
                        (12, 7, 12, (255, 190, 0)), (0, -12, 11, (255, 210, 60)),
                        (-8, -6, 8, (255, 220, 90)), (9, -6, 8, (255, 220, 90))])
for (dx, dy, r) in [(-26, -40, 8), (-12, -48, 11), (4, -44, 9), (18, -52, 7)]:
    d.ellipse([QX + dx - r, QY - 22 + dy - r, QX + dx + r, QY - 22 + dy + r],
              fill=(120, 120, 120))
# drone arcs from Iran (right) toward Kuwait and Bahrain
for (x0, y0, x1, y1) in [(QX - 40, QY + 8, KX + 20, KY - 8),
                         (QX - 40, QY + 12, BX2 + 20, BY2 - 8)]:
    for i in range(15):
        t = i / 14
        x = x0 + (x1 - x0) * t
        yy = y0 + (y1 - y0) * t - 26 * 4 * t * (1 - t)
        d.ellipse([x - 2, yy - 2, x + 2, yy + 2], fill=(255, 80, 60))
d.text((PX + 14, PY + 6), "IRAN", font=SANS_B(16), fill=(90, 60, 20))
d.text((PX + 330, PY + 104), "THE GULF", font=SANS_B(16), fill=(255, 255, 255))
d.text((PX + 14, PY + PH - 24), "SAUDI ARABIA", font=SANS_B(16), fill=(90, 60, 20))
d.text((PX + PW - 14, PY + PH - 24), "U.S. STRIKE  •  IRAN RETALIATES",
       font=SANS_B(13), fill=(255, 210, 90), anchor="ra")
y = PY + PH + 8
y = para("Bahrain says it intercepted several attacks before dawn and published no "
         "damage assessment; Kuwait says it engaged drones over Ali Al Salem. "
         "U.S. officials say American aircraft struck the launch site in reply.",
         SERIF(18), MX, y, RX - MX, 24)
y += 4
rule(MX, y, RX, 1)
y += 8

# ---------- row 2: two columns ----------
COLW = 464
CY = y
# left: summit
x = MX
d.text((x, CY), "SHENZHEN  —  THE SUMMIT", font=SANS_B(15), fill=RED)
yy = para("Xi and Putin meet ahead of three-way talks with Trump", SERIF_B(28),
          x, CY + 22, COLW, 32)
yy += 4
FX, FY, FW, FH = x, yy, COLW, 74
d.rectangle([FX, FY, FX + FW, FY + FH], fill=(232, 226, 208))
random.seed(7)
bx = FX + 8
while bx < FX + FW - 30:
    bw = random.randint(18, 34)
    bh = random.randint(16, 36)
    d.rectangle([bx, FY + FH - bh, bx + bw, FY + FH], fill=(70, 70, 78))
    bx += bw + 4
def flag_cn(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(222, 41, 16))
    d.text((x0 + 5, y0 + 2), "\u2605", font=SANS_B(16), fill=(255, 220, 0))
    for (dx, dy) in [(26, 4), (32, 10), (30, 18), (22, 18)]:
        d.text((x0 + dx, y0 + dy), "\u2605", font=SANS_B(9), fill=(255, 220, 0))
def flag_ru(x0, y0, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x0, y0 + i * h // 3, x0 + w, y0 + (i + 1) * h // 3], fill=c)
def flag_us(x0, y0, w, h):
    for i in range(7):
        d.rectangle([x0, y0 + i * h // 7, x0 + w, y0 + (i + 1) * h // 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x0, y0, x0 + w * 0.42, y0 + h * 0.55], fill=(30, 50, 110))
    for r in range(3):
        for c in range(4):
            d.ellipse([x0 + 4 + c * 9, y0 + 4 + r * 8, x0 + 8 + c * 9, y0 + 8 + r * 8],
                      fill=(255, 255, 255))
flag_cn(FX + 16, FY + 6, 86, 32)
flag_ru(FX + 118, FY + 6, 86, 32)
flag_us(FX + 220, FY + 6, 86, 32)
d.text((FX + 322, FY + 8), "APEC", font=SANS_B(15), fill=INK)
d.text((FX + 322, FY + 28), "SHENZHEN", font=SANS_B(12), fill=GRAY)
yy = FY + FH + 6
y_left = para("Xi vows to stand against protectionism and Putin denounces Western "
              "sanctions as APEC opens; the trilateral with Trump is set for "
              "Thursday, with no agenda published.", SERIF(17), x, yy, COLW, 22)
# right: Alaska
x = RX - COLW
d.text((x, CY), "WASHINGTON  —  THE SENATE", font=SANS_B(15), fill=RED)
yy = para("Peltola wins Alaska; Democrats take a 56–44 Senate", SERIF_B(28),
          x, CY + 22, COLW, 32)
yy += 4
BX, BY, BW, BH = x, yy, COLW, 74
d.rectangle([BX, BY, BX + BW, BY + BH], fill=(232, 226, 208))
# hemicycle of 100 seats: 56 blue, 44 red
random.seed(11)
seats = [(28, 78, 122)] * 56 + [(166, 25, 46)] * 44
random.shuffle(seats)
idx = 0
for row in range(4):
    n = 16 + row * 6
    r = 62 - row * 11
    for i in range(n):
        if idx >= 100:
            break
        ang = math.pi * (0.08 + 0.84 * i / max(n - 1, 1))
        cx = BX + BW // 2 + r * 2.6 * math.cos(ang)
        cy = BY + BH - 8 - r * 0.9 * math.sin(ang)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=seats[idx])
        idx += 1
d.text((BX + 12, BY + 5), "56 DEM", font=SANS_B(14), fill=(28, 78, 122))
d.text((BX + BW - 12, BY + 5), "44 REP", font=SANS_B(14), fill=(166, 25, 46), anchor="ra")
yy = BY + BH + 6
y_right = para("Democrat Mary Peltola defeats Republican Dan Sullivan in Alaska — "
               "her party's ninth Senate flip of the midterms, its largest "
               "majority since 2009.", SERIF(17), x, yy, COLW, 22)
y = max(y_left, y_right) + 6
rule(MX, y, RX, 1)
y += 8

# ---------- row 3: two short items ----------
def icon_probe(cx, cy):
    # deep-space probe: dish arc + mast + body, kept inside the icon column
    d.arc([cx - 13, cy - 13, cx + 13, cy + 13], 200, 340, fill=(90, 90, 100), width=3)
    d.line([(cx, cy), (cx + 8, cy + 8)], fill=(90, 90, 100), width=3)
    d.rectangle([cx + 6, cy + 6, cx + 14, cy + 14], fill=(90, 90, 100))
    for (sx, sy) in [(-12, -10), (2, -14), (13, -4)]:
        d.ellipse([cx + sx - 1, cy + sy - 1, cx + sx + 1, cy + sy + 1], fill=(150, 150, 160))
def icon_virus(cx, cy):
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=RED)
    for a in range(8):
        ang = a * math.pi / 4
        x1, y1 = cx + 11 * math.cos(ang), cy + 11 * math.sin(ang)
        x2, y2 = cx + 17 * math.cos(ang), cy + 17 * math.sin(ang)
        d.line([(x1, y1), (x2, y2)], fill=RED, width=3)
        d.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=RED)

def short_item(x, kicker, head, body, icon):
    d.text((x + 44, y), kicker, font=SANS_B(13), fill=RED)
    yy = para(head, SANS_B(19), x + 44, y + 16, COLW - 44, 23)
    icon(x + 20, y + 26)
    return para(body, SERIF(16), x + 44, yy + 2, COLW - 44, 21)

y2 = short_item(MX, "SPACE", "Voyager 1 passes one light-day from Earth",
                "Sixteen billion miles out, the 1977 probe crosses a distance no "
                "human-made object has reached — light itself needs a full day "
                "to cover it.", icon_probe)
y3 = short_item(RX - COLW, "HEALTH", "Ebola in Congo passes 11,000 cases",
                "The outbreak has more than doubled in three months and is now "
                "the second-largest on record; children bear the heaviest toll.",
                icon_virus)
y = max(y2, y3) + 6
rule(MX, y, RX, 1)
y += 6
# ---------- also today strip ----------
d.text((MX, y), "ALSO TODAY", font=SANS_B(15), fill=RED)
y = para("Cyclone Xavier, a Category 5, hits the Northern Cook Islands  ·  "
         "Russian military plane crashes in Siberia, 19 dead  ·  Trump's Board "
         "of Peace says Israel and Hamas are failing the ceasefire  ·  Israel "
         "elects Matan Kahana speaker  ·  Nvidia revenue doubles to $115.8bn  ·  "
         "Ukraine hits the Kerch Bridge a second day  ·  Houthis fire drones "
         "at a Saudi pipeline",
         SANS(15), MX + 118, y, RX - MX - 118, 20, fill=(60, 60, 60))
y += 4
rule(MX, y, RX, 1)
d.text((W // 2, y + 5), "Compiled from the day's reporting  •  18 November 2026",
       font=SANS(13), fill=GRAY, anchor="ma")

img.save("entry.png")
print("saved; final y =", y)
