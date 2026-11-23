#!/usr/bin/env python3
"""Build a newspaper-front-page style daily world news image (1024x1024, deterministic)."""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageChops

S = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_CB = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_NARROW_B = "/usr/share/fonts/opentype/urw-base35/NimbusSansNarrow-Bold.otf"

PAPER = (242, 238, 227)
INK = (26, 25, 23)
GREY = (92, 89, 82)
RULE = (40, 38, 34)
RED = (168, 40, 32)
DARK = (34, 45, 56)

# subtler lines get drawn on a 3x supersampled layer then reduced -> clean thin rules
SS = 3

img = Image.new("RGB", (S, S), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_fit(path, txt, max_w, start):
    """Largest font size <= start whose text fits max_w."""
    s = start
    while s > 6:
        f = font(path, s)
        if d.textlength(txt, font=f) <= max_w:
            return f
        s -= 1
    return font(path, 6)


def put(x, y, txt, f, fill=INK, anchor="la", track=0):
    if track == 0:
        d.text((x, y), txt, font=f, fill=fill, anchor=anchor)
        return
    # letter-spaced text
    cx = x
    for ch in txt:
        d.text((cx, y), ch, font=f, fill=fill, anchor="l" + anchor[1:])
        cx += d.textlength(ch, font=f) + track


M = 50  # outer margin

# ---------------- Masthead ----------------
# top hairline bar with tagline
put(M, 30, "THE WORLD DAILY", font(F_NARROW_B, 20), fill=GREY, track=1.2)
tag = "GLOBAL EDITION  ·  NO. 1,127  ·  SUNDAY, 22 NOVEMBER 2026"
ft = font(F_SANS, 19)
d.text((S - M, 30), tag, font=ft, fill=GREY, anchor="ra")

d.line([(M, 64), (S - M, 64)], fill=RULE, width=3)
put(M, 70, "WORLD NEWS  ·  ONE DAY", font(F_NARROW_B, 30), fill=RED, track=1.0)

# ---------------- Block 1: big date + lead ----------------
Y1 = 116
# date block (left): huge day number
fday = font(F_SANS_CB, 150)
d.text((M - 6, Y1 - 26), "22", font=fday, fill=INK)
fnov = font(F_NARROW_B, 62)
d.text((M + 2, Y1 + 122), "NOVEMBER", font=fnov, fill=INK)
fyr = font(F_NARROW_B, 82)
d.text((M + 2, Y1 + 180), "2026", font=fyr, fill=RED)
put(M + 6, Y1 + 240, "SUNDAY", font(F_NARROW_B, 32), fill=GREY, track=3.0)
d.line([(M, Y1 + 290), (640, Y1 + 290)], fill=RULE, width=2)
d.line([(660, Y1 - 6), (660, Y1 + 290)], fill=RULE, width=2)
put(682, Y1 - 6, "THE DAY IN ONE LINE", font(F_NARROW_B, 22), fill=RED, track=0.8)
one = ["A record-long climate summit ends",
       "with no deal, while Iran strikes",
       "Bahrain and a Russian ship is hit",
       "in the Baltic; Vietnam counts",
       "41 dead in floods."]
yy = Y1 + 34
for ln in one:
    f = font(F_SANS, 24)
    while d.textlength(ln, font=f) > (S - M - 682):
        f = font(F_SANS, f.size - 1)
    d.text((682, yy), ln, font=f, fill=INK)
    yy += 34

d.line([(M, Y1 + 308), (S - M, Y1 + 308)], fill=RULE, width=7)

# ---------------- Block 2: top story (left, ~2/3) + map (right) ----------------
Y2 = Y1 + 316
COLW_L = 560
COLX_R = 622  # vertical rule at map panel boundary
put(M, Y2, "TOP STORY  ·  CLIMATE", font(F_NARROW_B, 22), fill=RED, track=1.0)

head = ["COP31 ENDS WITH NO DEAL"]
fh = text_fit(F_SERIF_B, head[0], COLW_L, 50)
d.text((M, Y2 + 26), head[0], font=fh, fill=INK)
d.text((M, Y2 + 26 + fh.size + 2), "AS FOSSIL FUELS GO UNNAMED", font=font(F_SERIF_B, fh.size - 4), fill=INK)

body = [
    ("Antalya talks run two days past schedule, 17 years", INK),
    ("after Copenhagen's failure. 190+ nations leave with", INK),
    ("no pact; EU, Norway, Ireland, Panama and the", INK),
    ("Marshall Islands refuse to sign. Guterres:", INK),
    ("\u201Cdeeply disappointed.\u201D  No new draft from the chair.", RED),
]
yb = Y2 + 26 + fh.size * 2 + 20
for i, (ln, col) in enumerate(body):
    f = font(F_SANS, 21)
    while d.textlength(ln, font=f) > COLW_L:
        f = font(F_SANS, f.size - 1)
    d.text((M, yb), ln, font=f, fill=col)
    yb += f.size + 7

# ---------------- Map panel ----------------
MX0, MY0, MX1, MY1 = 622, Y2 - 10, S - M, Y2 + 196
put(MX0 + 8, MY0 + 8, "WHERE IT HAPPENED", font(F_NARROW_B, 20), fill=RED, track=0.8)
mx0, my0, mx1, my1 = MX0 + 8, MY0 + 34, MX1 - 4, MY1

# simplified invented-free schematic: graticule + abstract continent blobs (no exact geo claims)
g = Image.new("RGB", (mx1 - mx0, my1 - my0), (234, 229, 216))
gd = ImageDraw.Draw(g)
W, H = g.size
for i in range(1, 8):
    x = W * i / 8
    gd.line([(x, 0), (x, H)], fill=(222, 216, 202), width=1)
for i in range(1, 6):
    y = H * i / 6
    gd.line([(0, y), (W, y)], fill=(222, 216, 202), width=1)
LAND = (198, 190, 172)
blobs = [
    # west coast Americas
    [(0.02, 0.02), (0.20, 0.02), (0.24, 0.14), (0.16, 0.30), (0.20, 0.44), (0.14, 0.58),
     (0.18, 0.74), (0.12, 0.94), (0.04, 0.92), (0.06, 0.66), (0.02, 0.46), (0.0, 0.24)],
    # north atlantic edge island
    [(0.30, 0.03), (0.38, 0.06), (0.36, 0.14), (0.29, 0.11)],
    # europe/africa (abstract)
    [(0.44, 0.05), (0.58, 0.05), (0.60, 0.16), (0.52, 0.22), (0.56, 0.34), (0.50, 0.52),
     (0.46, 0.66), (0.40, 0.60), (0.42, 0.42), (0.38, 0.26), (0.40, 0.14)],
    # asia
    [(0.58, 0.04), (0.80, 0.06), (0.90, 0.16), (0.84, 0.30), (0.72, 0.36), (0.62, 0.30), (0.58, 0.16)],
    # south-east asia
    [(0.78, 0.34), (0.88, 0.40), (0.86, 0.54), (0.78, 0.50), (0.74, 0.40)],
    # africa south
    [(0.46, 0.60), (0.56, 0.60), (0.54, 0.86), (0.48, 0.84)],
]
for b in blobs:
    gd.polygon([(x * W, y * H) for x, y in b], fill=LAND, outline=(176, 167, 148))
img.paste(g, (mx0, my0))
d.rectangle([mx0, my0, mx1, my1], outline=RULE, width=2)

marks = [
    (0.53, 0.20, "1"),  # Europe / Turkey
    (0.62, 0.34, "2"),  # Gulf
    (0.80, 0.46, "3"),  # SE Asia
    (0.36, 0.14, "4"),  # Baltic (north)
    (0.84, 0.14, "5"),  # Shenzhen-ish NE
]
lab_w = 20
for (ux, uy, n) in marks:
    cx = mx0 + ux * (mx1 - mx0)
    cy = my0 + uy * (my1 - my0)
    r = 15
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    fn = font(F_SANS_B, 19)
    d.text((cx, cy - 1), n, font=fn, fill=PAPER, anchor="mm")

ky = MY1 + 4
keys = [
    ("1", "Antalya, T\u00FCrkiye"),
    ("2", "Bahrain / Gulf"),
    ("3", "Vietnam floods"),
    ("4", "Gulf of Finland"),
    ("5", "Shenzhen summit"),
]
fkey = font(F_SANS, 16)
for i, (n, name) in enumerate(keys):
    col = i % 2
    row = i // 2
    x = MX0 + 2 + col * 196
    y = ky - 2 + row * 21
    d.text((x, y), n + ".", font=font(F_SANS_B, 16), fill=RED)
    d.text((x + 20, y), name, font=fkey, fill=INK)

# ---------------- Block 3: four story tiles ----------------
Y3 = 748
d.line([(M, Y3 - 22), (S - M, Y3 - 22)], fill=RULE, width=3)
put(M, Y3 - 16, "ALSO ON 22 NOVEMBER", font(F_NARROW_B, 20), fill=RED, track=1.0)

# --- small clean pictograms, drawn at 4x then downsampled ---
IC = 84


def icon_canvas():
    return Image.new("RGBA", (IC * 4, IC * 4), (0, 0, 0, 0))


def icon_down(im):
    return im.resize((IC, IC), Image.LANCZOS)


def ic_missile():
    im = icon_canvas(); x = ImageDraw.Draw(im)
    s = IC * 4
    # missile body diagonal
    x.line([(s*0.12, s*0.88), (s*0.78, s*0.22)], fill=DARK + (255,), width=int(s*0.10))
    x.polygon([(s*0.78, s*0.22), (s*0.92, s*0.10), (s*0.90, s*0.28), (s*0.84, s*0.30)], fill=DARK + (255,))
    # fins
    x.line([(s*0.22, s*0.66), (s*0.12, s*0.66)], fill=DARK + (255,), width=int(s*0.07))
    x.line([(s*0.30, s*0.74), (s*0.30, s*0.86)], fill=DARK + (255,), width=int(s*0.07))
    # smoke puffs
    for (cx, cy, r) in [(0.10, 0.94, 0.09), (0.20, 0.97, 0.08), (0.04, 0.80, 0.07)]:
        x.ellipse([s*(cx-r), s*(cy-r), s*(cx+r), s*(cy+r)], fill=GREY + (255,))
    # impact burst (top right)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        x.line([(s*0.88, s*0.18), (s*0.88 + s*0.11*math.cos(rad), s*0.18 + s*0.11*math.sin(rad))],
               fill=RED + (255,), width=int(s*0.045))
    return icon_down(im)


def ic_ship():
    im = icon_canvas(); x = ImageDraw.Draw(im)
    s = IC * 4
    # waterline waves
    pts = [(0, 0.80), (0.25, 0.73), (0.5, 0.80), (0.75, 0.73), (1.0, 0.80)]
    for k, off in enumerate([0, 0.07]):
        x.line([(s*px, s*(py + off)) for px, py in pts], fill=(70, 96, 122, 255), width=int(s*0.03), joint="curve")
    # hull
    x.polygon([(s*0.16, s*0.52), (s*0.86, s*0.52), (s*0.78, s*0.72), (s*0.24, s*0.72)], fill=DARK + (255,))
    # bridge / containers
    x.rectangle([s*0.30, s*0.36, s*0.46, s*0.52], fill=DARK + (255,))
    for i in range(3):
        x.rectangle([s*(0.52 + i*0.10), s*0.40, s*(0.60 + i*0.10), s*0.52], outline=DARK + (255,), width=int(s*0.02))
    # drone + beam hitting deck
    x.rectangle([s*0.62, s*0.10, s*0.74, s*0.14], fill=RED + (255,))
    for dx in (0.62, 0.66, 0.70, 0.74):
        x.line([(s*dx, s*0.14), (s*(dx - 0.03), s*0.19)], fill=RED + (255,), width=int(s*0.02))
    x.line([(s*0.68, s*0.18), (s*0.62, s*0.38)], fill=RED + (255,), width=int(s*0.025))
    x.ellipse([s*0.55, s*0.34, s*0.69, s*0.44], outline=RED + (255,), width=int(s*0.025))
    return icon_down(im)


def ic_flood():
    im = icon_canvas(); x = ImageDraw.Draw(im)
    s = IC * 4
    for k, y in enumerate([0.52, 0.64, 0.76, 0.88]):
        pts = [(0, y), (0.25, y - 0.05), (0.5, y), (0.75, y - 0.05), (1.0, y)]
        x.line([(s*px, s*py) for px, py in pts], fill=DARK + (255,), width=int(s*0.035), joint="curve")
    # house half sunk
    x.rectangle([s*0.30, s*0.20, s*0.64, s*0.52], fill=(230, 222, 205, 255), outline=DARK + (255,), width=int(s*0.025))
    x.polygon([(s*0.24, s*0.20), (s*0.47, s*0.04), (s*0.70, s*0.20)], fill=RED + (255,))
    x.rectangle([s*0.42, s*0.34, s*0.52, s*0.46], fill=DARK + (255,))
    return icon_down(im)


def ic_handshake():
    im = icon_canvas(); x = ImageDraw.Draw(im)
    s = IC * 4
    # three abstract figures in a triangle
    heads = [(0.50, 0.16), (0.22, 0.62), (0.78, 0.62)]
    for hx, hy in heads:
        x.ellipse([s*(hx-0.075), s*(hy-0.075), s*(hx+0.075), s*(hy+0.075)], fill=DARK + (255,))
        x.polygon([(s*(hx-0.16), s*(hy+0.36)), (s*(hx+0.16), s*(hy+0.36)), (s*(hx+0.07), s*(hy+0.10)),
                   (s*(hx-0.07), s*(hy+0.10))], fill=DARK + (255,))
    for a, b in [(0, 1), (1, 2), (2, 0)]:
        x.line([(s*(heads[a][0]+0.0), s*(heads[a][1]+0.28)), (s*(heads[b][0]), s*(heads[b][1]+0.28))],
               fill=RED + (255,), width=int(s*0.045))
    return icon_down(im)


def ic_broken_table():
    im = icon_canvas(); x = ImageDraw.Draw(im)
    s = IC * 4
    # empty chairs (four) around a cracked table
    x.rectangle([s*0.18, s*0.52, s*0.82, s*0.60], fill=DARK + (255,))
    x.polygon([(s*0.52, s*0.52), (s*0.58, s*0.60), (s*0.46, s*0.60)], fill=PAPER)
    x.line([(s*0.26, s*0.60), (s*0.26, s*0.80)], fill=DARK + (255,), width=int(s*0.04))
    x.line([(s*0.74, s*0.60), (s*0.74, s*0.80)], fill=DARK + (255,), width=int(s*0.04))
    for cx in (0.16, 0.38, 0.62, 0.84):
        x.rectangle([s*(cx-0.07), s*0.80, s*(cx+0.07), s*0.86], fill=RED + (255,))
    x.line([(s*0.30, s*0.52), (s*0.30, s*0.36)], fill=RED + (255,), width=int(s*0.035))
    x.line([(s*0.70, s*0.52), (s*0.70, s*0.36)], fill=RED + (255,), width=int(s*0.035))
    return icon_down(im)


TILE_Y = Y3 + 12
TILE_H = 214
TILE_W = (S - 2*M - 3*16) // 4
tiles = [
    # (region label, headline lines, sub lines, icon, accent-icon?)
    ("MIDDLE EAST", ["IRAN STRIKES", "BAHRAIN ON 22 NOV"], ["IRGC missiles & drones;", "fire at industrial site.", "Saudi Arabia condemns."], ic_missile()),
    ("EUROPE / BALTIC", ["DRONE HITS", "RUSSIAN SHIP"], ["Attack in Gulf of Finland,", "2nd in a week. Russian", "missile debris in Poland."], ic_ship()),
    ("ASIA / DISASTERS", ["VIETNAM FLOODS:", "41 DEAD"], ["Days of rain in central", "Vietnam. Quake kills 6,", "felt in Kolkata."], ic_flood()),
    ("GREAT POWER", ["3-WAY SUMMIT", "SHENZHEN, 19 NOV"], ["Xi, Putin, Trump: first", "joint statement on nuclear", "war & UN reform."], ic_handshake()),
]

TX = M
for (reg, hl, sub, ic) in tiles:
    # icon (left) + headline (right)
    img.paste(ic, (TX + 4, TILE_Y + 2), ic)
    hx = TX + IC + 14
    hw = TILE_W - IC - 14
    yy = TILE_Y + 4
    fr = font(F_NARROW_B, 18)
    d.text((hx, yy), reg, font=fr, fill=RED)
    yy += 24
    for ln in hl:
        f = text_fit(F_SANS_CB, ln, hw, 34)
        d.text((hx, yy), ln, font=f, fill=INK)
        yy += f.size + 1
    # sub lines under, full tile width
    yy = TILE_Y + IC + 14
    for ln in sub:
        f = text_fit(F_SANS, ln, TILE_W - 8, 19)
        d.text((TX + 2, yy), ln, font=f, fill=(56, 54, 49))
        yy += f.size + 5
    TX += TILE_W + 16

# tile separators
for i in range(1, 4):
    xx = M + i * (TILE_W + 16) - 8
    d.line([(xx, TILE_Y), (xx, TILE_Y + TILE_H)], fill=(150, 144, 131), width=1)

# ---------------- Kicker strip above footer ----------------
KY = 976
d.line([(M, KY), (S - M, KY)], fill=RULE, width=3)
put(M, KY + 3, "SOURCE", font(F_NARROW_B, 16), fill=RED, track=0.8)
d.text((M + 78, KY + 3), "CNN · Politico · The Independent · Reuters · AP  |  As reported on 22 November 2026",
       font=font(F_SANS, 15), fill=GREY)

# ---------------- Footer ----------------
FY = 1000
d.line([(M, FY - 4), (S - M, FY - 4)], fill=RULE, width=3)
put(M, FY + 2, "SUNDAY 22 NOVEMBER 2026", font(F_SANS_B, 21), fill=INK, track=0.5)
d.text((S - M, FY + 3), "A single day, five regions  ·  The World Daily", font=font(F_SANS, 19), fill=GREY, anchor="ra")

img.save(OUT, format="PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), img.size)