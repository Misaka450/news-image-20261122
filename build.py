#!/usr/bin/env python3
"""Build a newspaper-front-page style daily world news image (1024x1024, deterministic)."""
import math, os
from PIL import Image, ImageDraw, ImageFont

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
    cx = x
    for ch in txt:
        d.text((cx, y), ch, font=f, fill=fill, anchor="l" + anchor[1:])
        cx += d.textlength(ch, font=f) + track


M = 60  # outer margin (breathing room around the whole page)

# ---------------- Masthead ----------------
put(M, 34, "THE WORLD DAILY", font(F_NARROW_B, 20), fill=GREY, track=1.2)
tag = "GLOBAL EDITION  ·  NO. 1,127  ·  SUNDAY, 22 NOVEMBER 2026"
d.text((S - M, 34), tag, font=font(F_SANS, 19), fill=GREY, anchor="ra")

d.line([(M, 66), (S - M, 66)], fill=RULE, width=3)
put(M, 74, "WORLD NEWS  ·  ONE DAY", font(F_NARROW_B, 30), fill=RED, track=1.0)

# ---------------- Block 1: big date + standfirst ----------------
Y1 = 116
fday = font(F_SANS_CB, 130)
d.text((M - 6, Y1 - 26), "22", font=fday, fill=INK)
d.text((M + 2, Y1 + 104), "NOVEMBER", font=font(F_NARROW_B, 58), fill=INK)
d.text((M + 2, Y1 + 158), "2026", font=font(F_NARROW_B, 72), fill=RED)
put(M + 6, Y1 + 214, "SUNDAY", font(F_NARROW_B, 32), fill=GREY, track=3.0)
d.line([(M, Y1 + 262), (640, Y1 + 262)], fill=RULE, width=2)
d.line([(660, Y1 - 6), (660, Y1 + 262)], fill=RULE, width=2)
put(682, Y1 - 6, "THE DAY IN ONE LINE", font(F_NARROW_B, 22), fill=RED, track=0.8)
# trimmed to three sentences so it stays comfortable at 300 px
one = ["A record-long climate summit ends",
       "with no deal. Iran strikes Bahrain;",
       "Vietnam floods kill 41."]
yy = Y1 + 44
for ln in one:
    f = font(F_SANS, 26)
    while d.textlength(ln, font=f) > (S - M - 682):
        f = font(F_SANS, f.size - 1)
    d.text((682, yy), ln, font=f, fill=INK)
    yy += 46

d.line([(M, Y1 + 280), (S - M, Y1 + 280)], fill=RULE, width=7)

# ---------------- Block 2: top story (left) + numbered story list (right) ----------------
Y2 = Y1 + 290
COLW_L = 520
COLX_R = 610  # column divider
put(M, Y2, "TOP STORY  ·  CLIMATE", font(F_NARROW_B, 22), fill=RED, track=1.0)

head1 = "COP31 ENDS WITH NO DEAL"
fh = text_fit(F_SERIF_B, head1, COLW_L, 46)
d.text((M, Y2 + 26), head1, font=fh, fill=INK)
fh2 = text_fit(F_SERIF_B, "AS FOSSIL FUELS GO UNNAMED", COLW_L, fh.size - 4)
d.text((M, Y2 + 26 + fh.size + 2), "AS FOSSIL FUELS GO UNNAMED", font=fh2, fill=INK)

body = [
    ("Antalya talks run two days past schedule, 17 years", INK),
    ("after Copenhagen's failure. 190+ nations leave with", INK),
    ("no pact; EU, Norway, Ireland, Panama and the", INK),
    ("Marshall Islands refuse to sign. Guterres:", INK),
    ("\u201Cdeeply disappointed.\u201D  No new draft from the chair.", RED),
]
yb = Y2 + 26 + fh.size + 2 + fh2.size + 24
for i, (ln, col) in enumerate(body):
    f = font(F_SANS, 21)
    while d.textlength(ln, font=f) > COLW_L:
        f = font(F_SANS, f.size - 1)
    d.text((M, yb), ln, font=f, fill=col)
    yb += f.size + 11

# ---------------- Right panel: five stories, numbered, vertical list ----------------
d.line([(COLX_R - 16, Y2 - 4), (COLX_R - 16, yb - 8)], fill=(150, 144, 131), width=2)
put(COLX_R, Y2, "THE FIVE STORIES", font(F_NARROW_B, 22), fill=RED, track=0.8)
d.line([(COLX_R, Y2 + 32), (S - M, Y2 + 32)], fill=RULE, width=2)

stories = [
    ("1", "Antalya, T\u00FCrkiye", "COP31 closes with no deal."),
    ("2", "Bahrain / Gulf", "Iranian missiles, drones hit industrial site."),
    ("3", "Vietnam", "Central floods kill 41."),
    ("4", "Gulf of Finland", "Drone hits Russian ship; 2nd in a week."),
    ("5", "Shenzhen, China", "Xi, Putin, Trump sign joint statement."),
]
f_num = font(F_SANS_CB, 24)
f_place = font(F_SANS_B, 20)
f_line = font(F_SANS, 19)
PY = Y2 + 42
PW = S - M - COLX_R
for k, (n, place, line) in enumerate(stories):
    fpl = text_fit(F_SANS_B, place.upper(), PW - 46, 20)
    d.text((COLX_R + 2, PY), n, font=f_num, fill=RED)
    d.text((COLX_R + 44, PY + 1), place.upper(), font=fpl, fill=INK)
    fl = text_fit(F_SANS, line, PW - 44, 19)
    d.text((COLX_R + 46, PY + fpl.size + 7), line, font=fl, fill=(56, 54, 49))
    bh = fpl.size + 7 + fl.size
    PY += bh + 15
    if k < len(stories) - 1:
        d.line([(COLX_R + 44, PY - 7), (S - M, PY - 7)], fill=(206, 200, 186), width=1)

# ---------------- Block 3: five story tiles ----------------
Y3 = 756
d.line([(M, Y3 - 22), (S - M, Y3 - 22)], fill=RULE, width=3)
put(M, Y3 - 16, "ALSO ON 22 NOVEMBER", font(F_NARROW_B, 20), fill=RED, track=1.0)

# --- small clean pictograms, drawn at 4x then downsampled ---
IC = 58


def icon_canvas():
    return Image.new("RGBA", (IC * 4, IC * 4), (0, 0, 0, 0))


def icon_down(im):
    return im.resize((IC, IC), Image.LANCZOS)


def ic_missile():
    im = icon_canvas(); x = ImageDraw.Draw(im)
    s = IC * 4
    x.line([(s*0.12, s*0.88), (s*0.78, s*0.22)], fill=DARK + (255,), width=int(s*0.10))
    x.polygon([(s*0.78, s*0.22), (s*0.92, s*0.10), (s*0.90, s*0.28), (s*0.84, s*0.30)], fill=DARK + (255,))
    x.line([(s*0.22, s*0.66), (s*0.12, s*0.66)], fill=DARK + (255,), width=int(s*0.07))
    x.line([(s*0.30, s*0.74), (s*0.30, s*0.86)], fill=DARK + (255,), width=int(s*0.07))
    for (cx, cy, r) in [(0.10, 0.94, 0.09), (0.20, 0.97, 0.08), (0.04, 0.80, 0.07)]:
        x.ellipse([s*(cx-r), s*(cy-r), s*(cx+r), s*(cy+r)], fill=GREY + (255,))
    for a in range(0, 360, 45):
        rad = math.radians(a)
        x.line([(s*0.88, s*0.18), (s*0.88 + s*0.11*math.cos(rad), s*0.18 + s*0.11*math.sin(rad))],
               fill=RED + (255,), width=int(s*0.045))
    return icon_down(im)


def ic_ship():
    im = icon_canvas(); x = ImageDraw.Draw(im)
    s = IC * 4
    pts = [(0, 0.80), (0.25, 0.73), (0.5, 0.80), (0.75, 0.73), (1.0, 0.80)]
    for k, off in enumerate([0, 0.07]):
        x.line([(s*px, s*(py + off)) for px, py in pts], fill=(70, 96, 122, 255), width=int(s*0.03), joint="curve")
    x.polygon([(s*0.16, s*0.52), (s*0.86, s*0.52), (s*0.78, s*0.72), (s*0.24, s*0.72)], fill=DARK + (255,))
    x.rectangle([s*0.30, s*0.36, s*0.46, s*0.52], fill=DARK + (255,))
    for i in range(3):
        x.rectangle([s*(0.52 + i*0.10), s*0.40, s*(0.60 + i*0.10), s*0.52], outline=DARK + (255,), width=int(s*0.02))
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
    x.rectangle([s*0.30, s*0.20, s*0.64, s*0.52], fill=(230, 222, 205, 255), outline=DARK + (255,), width=int(s*0.025))
    x.polygon([(s*0.24, s*0.20), (s*0.47, s*0.04), (s*0.70, s*0.20)], fill=RED + (255,))
    x.rectangle([s*0.42, s*0.34, s*0.52, s*0.46], fill=DARK + (255,))
    return icon_down(im)


def ic_quake():
    """Cracked ground + seismic zig-zag."""
    im = icon_canvas(); x = ImageDraw.Draw(im)
    s = IC * 4
    # seismic trace
    pts = [(0.04, 0.30), (0.24, 0.30), (0.32, 0.10), (0.42, 0.52), (0.50, 0.06),
           (0.58, 0.44), (0.66, 0.30), (0.96, 0.30)]
    x.line([(s*px, s*py) for px, py in pts], fill=RED + (255,), width=int(s*0.045), joint="curve")
    # ground line with a shifted fault block
    x.line([(s*0.02, s*0.72), (s*0.44, s*0.72)], fill=DARK + (255,), width=int(s*0.05))
    x.line([(s*0.56, s*0.84), (s*0.98, s*0.84)], fill=DARK + (255,), width=int(s*0.05))
    # crack between blocks
    x.line([(s*0.46, s*0.60), (s*0.52, s*0.94)], fill=DARK + (255,), width=int(s*0.035))
    x.polygon([(s*0.30, s*0.72), (s*0.44, s*0.72), (s*0.40, s*0.94), (s*0.26, s*0.94)], fill=(198, 190, 172, 255))
    x.line([(s*0.30, s*0.72), (s*0.44, s*0.72)], fill=DARK + (255,), width=int(s*0.05))
    return icon_down(im)


def ic_handshake():
    im = icon_canvas(); x = ImageDraw.Draw(im)
    s = IC * 4
    heads = [(0.50, 0.16), (0.22, 0.62), (0.78, 0.62)]
    for hx, hy in heads:
        x.ellipse([s*(hx-0.075), s*(hy-0.075), s*(hx+0.075), s*(hy+0.075)], fill=DARK + (255,))
        x.polygon([(s*(hx-0.16), s*(hy+0.36)), (s*(hx+0.16), s*(hy+0.36)), (s*(hx+0.07), s*(hy+0.10)),
                   (s*(hx-0.07), s*(hy+0.10))], fill=DARK + (255,))
    for a, b in [(0, 1), (1, 2), (2, 0)]:
        x.line([(s*(heads[a][0]+0.0), s*(heads[a][1]+0.28)), (s*(heads[b][0]), s*(heads[b][1]+0.28))],
               fill=RED + (255,), width=int(s*0.045))
    return icon_down(im)


TILE_Y = Y3 + 8
TILE_H = 154
NT = 5
GAP = 16
TILE_W = (S - 2 * M - (NT - 1) * GAP) // NT
tiles = [
    ("MIDDLE EAST", ["IRAN STRIKES", "BAHRAIN"], ["IRGC missiles & drones;", "fire at industrial site."], ic_missile()),
    ("EUROPE", ["DRONE HITS", "RUSSIAN SHIP"], ["Gulf of Finland, 2nd", "attack in a week."], ic_ship()),
    ("VIETNAM", ["FLOODS:", "41 DEAD"], ["Days of rain in", "central Vietnam."], ic_flood()),
    ("BANGLADESH", ["QUAKE:", "6 DEAD"], ["Tremor felt in", "Kolkata, India."], ic_quake()),
    ("GREAT POWER", ["3-WAY SUMMIT", "SHENZHEN"], ["Xi, Putin, Trump:", "joint statement."], ic_handshake()),
]

TX = M
for (reg, hl, sub, ic) in tiles:
    # region label, icon, headline stack, then one short fact line
    d.text((TX + 2, TILE_Y - 2), reg, font=font(F_NARROW_B, 18), fill=RED)
    img.paste(ic, (TX + 2, TILE_Y + 18), ic)
    yy = TILE_Y + 18 + IC + 6
    for ln in hl:
        f = text_fit(F_SANS_CB, ln, TILE_W - 6, 27)
        d.text((TX + 2, yy), ln, font=f, fill=INK)
        yy += f.size + 3
    yy += 5
    for ln in sub:
        f = text_fit(F_SANS, ln, TILE_W - 8, 17)
        d.text((TX + 2, yy), ln, font=f, fill=(56, 54, 49))
        yy += f.size + 2
    TX += TILE_W + GAP

for i in range(1, NT):
    xx = M + i * (TILE_W + GAP) - GAP // 2 - 1
    d.line([(xx, TILE_Y + 2), (xx, TILE_Y + TILE_H)], fill=(150, 144, 131), width=1)

# ---------------- Source strip + footer (well clear of the bottom edge) ----------------
KY = 960
d.line([(M, KY), (S - M, KY)], fill=RULE, width=3)
put(M, KY + 4, "SOURCE", font(F_NARROW_B, 16), fill=RED, track=0.8)
d.text((M + 78, KY + 4), "CNN · Politico · The Independent · Reuters · AP  |  As reported on 22 November 2026",
       font=font(F_SANS, 15), fill=GREY)

FY = 986
d.line([(M, FY), (S - M, FY)], fill=RULE, width=3)
put(M, FY + 7, "SUNDAY 22 NOVEMBER 2026", font(F_SANS_B, 21), fill=INK, track=0.5)
d.text((S - M, FY + 8), "A single day, five regions  ·  The World Daily", font=font(F_SANS, 19), fill=GREY, anchor="ra")

img.save(OUT, format="PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), img.size)

# ---------------- 300px preview thumbnail ----------------
PREV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preview-300.png")
img.resize((300, 300), Image.LANCZOS).save(PREV, format="PNG", optimize=True)
print("wrote", PREV, os.path.getsize(PREV))