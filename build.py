#!/usr/bin/env python3
"""Deterministic newspaper-front-page world-news image for 22 Nov 2026.

Renders a 1024x1024 PNG (<=1 MiB) that mirrors the leaderboard-top meta
template: big date, 5-number stats strip, 7-region legend with counts,
3 hero stories, a 12-tile grid, a 21-story 'ALSO' list beside a dot-matrix
world map, a DATE-CHECK block, and a status-tag legend footer.

Two runs must write byte-identical PNGs; no network, no time, no random.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

S = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_CB = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_NARROW_B = "/usr/share/fonts/opentype/urw-base35/NimbusSansNarrow-Bold.otf"
F_NARROW = "/usr/share/fonts/opentype/urw-base35/NimbusSansNarrow-Regular.otf"

PAPER = (243, 239, 228)
INK = (26, 25, 23)
GREY = (94, 90, 82)
RULE = (40, 38, 34)
RED = (168, 40, 32)
FAINT = (120, 116, 106)

# ---- status tag colours -------------------------------------------------
ST_COLOR = {
    "CONFIRMED": (45, 108, 60),
    "REPORTED": (150, 108, 34),
    "CLAIM": (168, 40, 32),
    "PENDING": (96, 92, 84),
}

# ---- 7 regions, each with its count and a distinct hue -----------------
REGION = {
    "GLOBAL/CLIMATE": ((60, 126, 128), "G"),
    "MIDDLE EAST":    ((184, 78, 40), "ME"),
    "EUROPE":         ((62, 92, 150), "EU"),
    "AMERICAS":       ((120, 78, 150), "AM"),
    "ASIA-PACIFIC":   ((66, 128, 70), "AP"),
    "AFRICA":         ((190, 148, 40), "AF"),
    "CONFLICT-AT-SEA":((40, 58, 88), "CS"),
}
REGION_ORDER = ["GLOBAL/CLIMATE", "MIDDLE EAST", "EUROPE", "AMERICAS",
                "ASIA-PACIFIC", "AFRICA", "CONFLICT-AT-SEA"]

img = Image.new("RGB", (S, S), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_fit(path, txt, max_w, start):
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


# =========================================================================
# STORY DATA  (36 items).  Every source is named in the source briefing;
# status is CONFIRMED / REPORTED / CLAIM / PENDING.
# fields: n, region, headline, detail, source, status, (lat, lon)
# =========================================================================
STORIES = [
 (1,  "GLOBAL/CLIMATE", "COP31 ENDS WITH NO DEAL",
     "First no-deal in 17 yrs; Guterres 'deeply disappointed'", "Reuters · The Guardian · BBC", "CONFIRMED", 36.9, 30.7),
 (2,  "MIDDLE EAST", "IRAN STRIKES REPORTED ON 2 BASES",
     "Bahrain industrial site fire, 2 hurt; 2 Hormuz supertankers out", "Fars · Dawn", "CLAIM", 26.0, 50.6),
 (3,  "EUROPE", "RUSSIA FIRES 186 DRONES ON UKRAINE",
     "161 downed; Dymer block hit, 2+ dead, 14 missing", "Ukrainian Air Force", "CONFIRMED", 50.4, 30.5),
 # ---- 12 tiles ----
 (4,  "MIDDLE EAST", "GAZA TOLL REACHES 74,742",
     "2 killed in dawn strike; meningitis surge warned", "Wafa · Palestine Chronicle", "CONFIRMED", 31.4, 34.3),
 (5,  "EUROPE", "UKRAINE: 5 REGIONS CUT OFF POWER",
     "Odesa plant damage on video; grid strained", "DTEK · Ukrenergo", "CONFIRMED", 46.5, 30.7),
 (6,  "MIDDLE EAST", "SETTLERS TORCH WEST BANK VILLAGES",
     "4 villages hit; Eisenkot: 'Jewish terrorism'", "Reuters · Al Arabiya", "REPORTED", 32.0, 35.2),
 (7,  "AMERICAS", "DEMOCRATS TAKE HOUSE CONTROL",
     "Jeffries to lead as first Black Speaker", "AP · NPR · Reuters", "CONFIRMED", 38.9, -77.0),
 (8,  "AMERICAS", "ARMY GRABS FBI'S #1 FUGITIVE",
     "Meza Flores in Sinaloa raid, 10+ yrs on the run", "Reuters", "CONFIRMED", 24.9, -108.7),
 (9,  "ASIA-PACIFIC", "JAVA FACTORY FIRE: 3 DEAD, 36 MISSING",
     "Confectionery plant; rescue crews still searching", "Pajhwok", "REPORTED", -7.0, 110.0),
 (10, "ASIA-PACIFIC", "CONGRESS VOWS MORE PROTESTS VS META",
     "After clashes with police", "Reuters", "CONFIRMED", 28.6, 77.2),
 (11, "ASIA-PACIFIC", "TAIPEI 'SUPER SUNDAY' MAYORAL RUSH",
     "Rivals stage motorcade, street festival", "Focus Taiwan · Taiwan News", "CONFIRMED", 25.0, 121.5),
 (12, "AFRICA", "SUDAN: DRONES TEAR THROUGH THIS WEEK",
     "UN says ~3/4 of war deaths by drone; 'killing hundreds'", "Reuters", "REPORTED", 15.6, 32.5),
 (13, "AFRICA", "SISI PUSHES FINANCIAL-SYSTEM REFORM",
     "Aswan forum: Red Sea trilateral with Sudan, Eritrea", "Ahram Online", "CONFIRMED", 24.0, 32.9),
 # ---- ALSO 21 (14..34 are also-list; 35,36 below) ----
 (14, "AFRICA", "SOUTH SUDAN CREDITORS HEAD TO KENYA COURTS",
     "Debt distress; legal move east", "The EastAfrican", "CONFIRMED", 4.85, 31.6),
 (15, "AFRICA", "MLAMBO-NgcUKA DIES, 71",
     "South Africa's first woman deputy president", "UN · allAfrica", "CONFIRMED", -33.9, 18.4),
 (16, "MIDDLE EAST", "US DENIES IRAN'S F-16 CLAIM",
     "Iran says a missile hit the jet; Pentagon denies", "Arab News", "CLAIM", 26.7, 56.3),
 (17, "MIDDLE EAST", "TRUMP WANTS 'PERMANENT' IRAN DEAL",
     "Says Iranian officials 'very, very difficult'", "Fox News", "CONFIRMED", 38.9, -77.0),
 (18, "MIDDLE EAST", "QATAR MEDIATES; ARAFCHI: DIPLOMACY GOES ON",
     "'The path of diplomacy continues'", "IRNA · Al Arabiya", "REPORTED", 25.3, 51.2),
 (19, "MIDDLE EAST", "YEMEN: ~10 KILLED IN LAHJ HEALTH-CENTER STRIKE",
     "Houthis designated a terrorist org", "Soth24", "REPORTED", 15.0, 44.5),
 (20, "MIDDLE EAST", "LEBANON: AOUN DEMANDS ISRAELI WITHDRAWAL",
     "Trump writes Aoun to 'seize the opportunity'", "Naharnet", "REPORTED", 33.9, 35.5),
 (21, "MIDDLE EAST", "JORDAN–EU SIGN STRATEGIC INVESTMENT PACT",
     "60+ European firms interested", "Jordan Times", "CONFIRMED", 31.9, 35.9),
 (22, "ASIA-PACIFIC", "PAKISTAN'S FIRST ASTRONAUT TO BEIJING",
     "Launch ceremony; historic space program", "APP", "CONFIRMED", 39.9, 116.4),
 (23, "ASIA-PACIFIC", "HONG KONG ELECTION COMMITTEE: RECORD VOTING",
     "Turnout best ever; CFA Li congratulates", "China Daily · 中新社", "CONFIRMED", 22.3, 114.2),
 (24, "ASIA-PACIFIC", "MYANMAR JUNTA: ASEAN CALL 'UNFAIR'",
     "Condemns 'imbalanced' decision", "Reuters", "REPORTED", 19.7, 96.1),
 (25, "ASIA-PACIFIC", "AFGHANISTAN: WHO SEES 50 POLIO CASES",
     "Ministry disputes findings", "TOLOnews", "REPORTED", 34.5, 65.9),
 (26, "EUROPE", "FINLAND: RUSSIAN CARGO SHIP ON FIRE",
     "Gulf of Finland; towed; drone strike suspected", "Reuters", "REPORTED", 60.0, 29.0),
 (27, "EUROPE", "FRENCH SENATE PASSES POLICE-SHOOTINGS LAW",
     "Doubted 'licence to kill'", "Reuters", "CONFIRMED", 48.9, 2.3),
 (28, "EUROPE", "RUSSIA: FRENCH TROOPS IN UKRAINE = WAR",
     "'Direct participation', Moscow warns", "Naharnet", "REPORTED", 55.8, 37.6),
 (29, "EUROPE", "GREECE–ISRAEL ~€3BN AIR-DEFENCE TALKS",
     "Elbit training centre expansion", "Naharnet", "REPORTED", 37.9, 23.7),
 (30, "EUROPE", "TÜRKİYE EXPANDS NATO ROLE; STARLIFT IN IZMIR",
     "Multinational logistics initiative", "Hürriyet Daily", "CONFIRMED", 38.4, 27.1),
 (31, "EUROPE", "EX-ITALY POLICE CHIEF FOUND DEAD",
     "De Gennaro suicide amid mafia probe", "Reuters", "CONFIRMED", 41.9, 12.5),
 (32, "AMERICAS", "US SUGGESTS GUYANA CEDe ESSEQUIBO",
     "To Venezuela; Machado unveils transition plan", "Efecto Cocuyo · Reuters", "REPORTED", 5.0, -58.8),
 (33, "AMERICAS", "RECORD BLACK DEMOCRATS JOIN CONGRESS",
     "Most in decades set to sway policy", "Reuters", "CONFIRMED", 38.9, -77.0),
 (34, "CONFLICT-AT-SEA", "OFF BENGHAZI: MALTESE SHIP HIT BY SEA DRONE",
     "Russian corvette Merkury ablaze; 12+ boats; Ascalon hit", "Reuters · Al Jazeera", "CLAIM", 32.1, 20.1),
 (35, "GLOBAL/CLIMATE", "GryNSPAN VETOED AS UN CHIEF",
     "Costa Rica's pick blocked by 2 of 5 powers", "Reuters", "REPORTED", 40.7, -74.0),
 (36, "GLOBAL/CLIMATE", "UN'S WFP: NEEDS $12.1BN IN 2027",
     "To aid 91m people as hunger deepens", "UN · APP", "CONFIRMED", 40.7, -74.0),
]

TOP = [1, 2, 3]
TILES = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
ALSO = [n for n in range(16, 37)]  # 16..36  -> 21 items

M = 30  # outer margin


def region_count(name):
    return sum(1 for s in STORIES if s[1] == name)


# =========================================================================
# MASTHEAD dark bar
# =========================================================================
d.rectangle([0, 0, S, 56], fill=(24, 26, 33))
put(M, 16, "THE WORLD IN ONE DAY", font(F_NARROW_B, 21), fill=(243, 239, 228), track=1.6)
d.text((S - M, 18), "36 STORIES · 7 REGIONS · SUN 22 NOV 2026",
       font=font(F_SANS_B, 15), fill=(198, 194, 182), anchor="ra")

# =========================================================================
# BIG DATE (fit to width so '2026' is never clipped)
# =========================================================================
d.line([(M, 62), (S - M, 62)], fill=RULE, width=2)
fd = text_fit(F_SERIF_B, "Sunday 22 November 2026", S - 2 * M, 96)
d.text((M - 4, 66), "Sunday 22 November 2026", font=fd, fill=INK)
d.line([(M, 156), (S - M, 156)], fill=RULE, width=2)

# standfirst
put(M, 164, "COP31 ends without a deal  ·  Strikes on two US bases reported  ·  186 drones over Ukraine  ·  74,742 in Gaza",
    text_fit(F_SERIF, "COP31 ends without a deal  ·  Strikes on two US bases reported  ·  186 drones over Ukraine  ·  74,742 in Gaza", S - 2 * M, 20),
    fill=RED, anchor="la")

# =========================================================================
# STATS strip  (5 big numbers)
# =========================================================================
STATS = [
    ("186", "drones on Ukraine overnight", "161 downed"),
    ("0",   "deals at COP31", "first in 17 yrs"),
    ("74,742", "dead in Gaza, cumulative", "per Health Ministry"),
    ("$12.1bn", "WFP asks for 2027", "91m people"),
    ("36 / 7", "stories / regions", "all dated 22 Nov"),
]
SY = 196
d.rectangle([M, SY, S - M, SY + 52], fill=(236, 232, 220))
d.line([(M, SY), (S - M, SY)], fill=RULE, width=2)
cell_w = (S - 2 * M) // 5
for i, (big, lab1, lab2) in enumerate(STATS):
    x0 = M + i * cell_w
    cx = x0 + cell_w // 2
    if i:
        d.line([(x0, SY + 8), (x0, SY + 44)], fill=(150, 145, 132), width=1)
    d.text((cx, SY + 4), big, font=font(F_SANS_CB, 30), fill=RED if i in (0, 1) else INK, anchor="ma")
    d.text((cx, SY + 34), lab1, font=font(F_SANS, 11), fill=GREY, anchor="ma")
    d.text((cx, SY + 45), lab2, font=font(F_SANS, 9), fill=FAINT, anchor="ma")

# =========================================================================
# REGION LEGEND bar (7 chips with counts) — short labels, fit to width
# =========================================================================
REGION_SHORT = {
    "GLOBAL/CLIMATE": "CLIMATE", "MIDDLE EAST": "MID-EST", "EUROPE": "EUROPE",
    "AMERICAS": "AMER", "ASIA-PACIFIC": "ASIA-PAC", "AFRICA": "AFRICA",
    "CONFLICT-AT-SEA": "AT-SEA",
}
LY = 258
put(M, LY, "BY REGION", font(F_NARROW_B, 14), fill=GREY, track=0.8)
rx = M + 92
# precompute each chip width so the row is centred / always fits
chips = []
for name in REGION_ORDER:
    col, code = REGION[name]
    cnt = region_count(name)
    lab = REGION_SHORT[name] + "  " + str(cnt)
    f = font(F_SANS_B, 13)
    w = int(d.textlength(lab, font=f)) + 30
    chips.append((col, code, lab, f, w))
total_w = sum(c[4] for c in chips) + 12 * (len(chips) - 1)
if total_w > S - 2 * M:  # safety: never overflow
    f = font(F_SANS_B, 11)
    chips = []
    for name in REGION_ORDER:
        col, code = REGION[name]
        lab = REGION_SHORT[name] + " " + str(region_count(name))
        w = int(d.textlength(lab, font=f)) + 26
        chips.append((col, code, lab, f, w))
    total_w = sum(c[4] for c in chips) + 12 * (len(chips) - 1)
rx = M + 92
for col, code, lab, f, w in chips:
    d.rectangle([rx, LY - 2, rx + w, LY + 22], outline=col, width=1)
    d.rectangle([rx, LY - 2, rx + 22, LY + 22], fill=col)
    d.text((rx + 11, LY + 10), code, font=font(F_SANS_B, 10), fill=(243, 239, 228), anchor="mm")
    d.text((rx + 26, LY + 9), lab, font=f, fill=INK)
    rx += w + 12

# =========================================================================
# 3 HERO story panels
# =========================================================================
HY = 292
HH = 150
gw = (S - 2 * M - 2 * 12) // 3
for i, n in enumerate(TOP):
    s = next(x for x in STORIES if x[0] == n)
    _, region, head, detail, src, status, lat, lon = s
    col, code = REGION[region]
    x0 = M + i * (gw + 12)
    d.rectangle([x0, HY, x0 + gw, HY + HH], outline=(90, 86, 78), width=1)
    d.rectangle([x0, HY, x0 + gw, HY + 24], fill=(30, 30, 30))
    d.ellipse([x0 + 8, HY + 4, x0 + 24, HY + 20], fill=col)
    d.text((x0 + 16, HY + 12), str(n), font=font(F_SANS_B, 13), fill=(243, 239, 228), anchor="mm")
    d.text((x0 + 30, HY + 12), region, font=font(F_SANS_B, 10), fill=(220, 216, 204), anchor="lm")
    sf = font(F_SANS_B, 10)
    sw = int(d.textlength(status, font=sf)) + 14
    d.rectangle([x0 + gw - sw - 8, HY + 5, x0 + gw - 8, HY + 19], outline=ST_COLOR[status], width=1)
    d.text((x0 + gw - sw - 1, HY + 12), status, font=sf, fill=ST_COLOR[status], anchor="rm")
    hh = text_fit(F_SERIF_B, head, gw - 18, 28)
    d.text((x0 + 9, HY + 34), head, font=hh, fill=INK)
    hy2 = HY + 34 + hh.size + 4
    df = text_fit(F_SANS, detail, gw - 18, 14)
    d.text((x0 + 9, hy2), detail, font=df, fill=(56, 54, 49))
    hy3 = hy2 + df.size + 7
    d.line([(x0 + 9, hy3 - 3), (x0 + gw - 9, hy3 - 3)], fill=(180, 176, 164), width=1)
    d.text((x0 + 9, hy3 + 3), "Sources: " + src, font=font(F_SANS, 11), fill=GREY)
    d.text((x0 + gw - 9, hy3 + 3), f"#{n}", font=font(F_SANS_CB, 11), fill=FAINT, anchor="ra")

# =========================================================================
# SECTION: THE STORIES THAT MOVED THE WORLD  (12 tiles, 4x3, 3-part)
# =========================================================================
TY0 = HY + HH + 14   # section title baseline
put(M, TY0, "THE STORIES THAT MOVED THE WORLD", font(F_NARROW_B, 17), fill=RED, track=0.8)
d.line([(M, TY0 + 16), (S - M, TY0 + 16)], fill=RULE, width=1)

tgw = (S - 2 * M - 3 * 8) // 4
tgh = 52
TY1 = TY0 + 26
for idx, n in enumerate(TILES):
    r, c = divmod(idx, 4)
    s = next(x for x in STORIES if x[0] == n)
    _, region, head, detail, src, status, lat, lon = s
    col, code = REGION[region]
    x0 = M + c * (tgw + 8)
    y0 = TY1 + r * (tgh + 8)
    d.rectangle([x0, y0, x0 + tgw, y0 + tgh], outline=(150, 146, 134), width=1)
    d.rectangle([x0, y0, x0 + 3, y0 + tgh], fill=col)
    d.text((x0 + 8, y0 + 4), str(n), font=font(F_SANS_CB, 13), fill=col)
    hf = text_fit(F_SANS_B, head, tgw - 24, 13)
    d.text((x0 + 26, y0 + 4), head, font=hf, fill=INK)
    d.text((x0 + 26, y0 + 20), detail, font=text_fit(F_SANS, detail, tgw - 30, 11), fill=(80, 78, 70))
    d.text((x0 + 8, y0 + tgh - 15), "Src " + src, font=text_fit(F_SANS, "Src " + src, tgw - 40, 10), fill=GREY)
    d.text((x0 + tgw - 5, y0 + tgh - 15), status, font=font(F_SANS_B, 9), fill=ST_COLOR[status], anchor="ra")
TY_BOTTOM = TY1 + 3 * (tgh + 8)  # bottom of the 3 tile rows

# =========================================================================
# ALSO band:  left = region-grouped number index, right = 21-item list
# =========================================================================
AY0 = TY_BOTTOM + 26
put(M, AY0, "ALSO ON 22 NOVEMBER  ·  21 MORE STORIES", font(F_NARROW_B, 17), fill=RED, track=0.8)
d.line([(M, AY0 + 16), (S - M, AY0 + 16)], fill=RULE, width=1)

# --- region index (left): 7 boxes, each listing its story numbers + a
# --- short place hint, so the numbering is traceable without a map ---
MAP_X, MAP_Y = M, AY0 + 22
MAP_W, MAP_H = 224, 164
d.text((S - M, AY0), "WHERE IT HAPPENED — # = story, grouped by region", font=font(F_NARROW_B, 13), fill=GREY, anchor="ra", track=0.4)

PLACE = {
    "GLOBAL/CLIMATE": "UN/COP · New York, Baku",
    "MIDDLE EAST": "Gulf · Levant · Iran",
    "EUROPE": "Ukraine · EU · Balkans",
    "AMERICAS": "US · Mexico · Guyana",
    "ASIA-PACIFIC": "S. Asia · E. Asia",
    "AFRICA": "Sahel · Horn · Egypt",
    "CONFLICT-AT-SEA": "Medoff Benghazi · Hormuz",
}
IDX_GAP = 4
box_h = (MAP_H - 3 * IDX_GAP) // 4          # 4 rows per column
fn_h  = font(F_SANS_B, 9)                    # region name
fn_pl = font(F_SANS, 7)                      # place hint
fn_n  = font(F_SANS_CB, 9)                   # story number

def draw_idx_box(x0, y0, w, h, name):
    col, code = REGION[name]
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 234, 222), outline=(170, 166, 154), width=1)
    d.rectangle([x0, y0, x0 + 4, y0 + h], fill=col)
    d.text((x0 + 9, y0 + 5), REGION_SHORT[name], font=fn_h, fill=col)
    nums = sorted(s[0] for s in STORIES if s[1] == name)
    d.text((x0 + w - 6, y0 + 5), "· " + str(len(nums)),
           font=font(F_SANS_B, 9), fill=col, anchor="ra")
    d.text((x0 + 9, y0 + 17), PLACE[name], font=fn_pl, fill=GREY)
    # story numbers: one line if they fit, else wrap to a 2nd line — never clip
    avail = w - 14
    parts, cur = [], ""
    for n in nums:
        piece = ("#" + str(n)) + "  "
        if int(d.textlength(cur + piece, font=fn_n)) > avail and cur:
            parts.append(cur); cur = ""
        cur += piece
    if cur:
        parts.append(cur)
    ytxt = y0 + 28 if len(parts) > 1 else y0 + 27
    for li, ln in enumerate(parts[:2]):
        d.text((x0 + 9, ytxt + li * 10), ln.rstrip(), font=fn_n, fill=INK)

col_w = (MAP_W - 8) // 2
# left column: 4 regions, right column: 3 regions (evenly spaced in column)
pad_v = 2
rh = (MAP_H - pad_v * 2) // 4
for i, name in enumerate(REGION_ORDER[:4]):
    draw_idx_box(MAP_X, MAP_Y + pad_v + i * rh, col_w, rh - 2, name)
for i, name in enumerate(REGION_ORDER[4:]):
    draw_idx_box(MAP_X + col_w + 8, MAP_Y + pad_v + i * rh, col_w, rh - 2, name)

# --- 21-item two-column list, FIXED 3 tracks: number+title | source | status
# FIXED 3 tracks, one row per story: [## | title (1 line, auto-fit) |
# source | status].  Track origins are computed once and asserted to fit, so
# no glyph of one track can ever be painted into a neighbour's space.
LX = M + 232
LW = S - M - LX
NUM_W = 20                       # number gutter
PAD   = 6                        # space between tracks
SRC_W = 72                       # source track (truncated with ellipsis)
STATUS_W = 62                    # widest tag "CONFIRMED" @8px = 55
colw = (LW - 14) // 2            # 14 = gap between the two columns
TITLE_W = colw - NUM_W - SRC_W - STATUS_W - 2 * PAD
lrows = [ALSO[:len(ALSO) // 2], ALSO[len(ALSO) // 2:]]
rows = max(len(c) for c in lrows)
list_top = MAP_Y
row_h = int(MAP_H / rows)
TRUNC = "…"

def fit_one(path, txt, w, start):
    """Largest font whose width fits; if even 'start' overflows, clip + ellipsis."""
    s = start
    while s >= 6:
        f = font(path, s)
        if d.textlength(txt, font=f) <= w:
            return f, txt
        s -= 1
    f = font(path, 6)
    t = txt
    while t and d.textlength(t + TRUNC, font=f) > w:
        t = t[:-1]
    return f, (t.rstrip(TRUNC).rstrip() + TRUNC if t else TRUNC)

def wrap_two(path, size, txt, w):
    """Return (font, [line1, line2]) — at most 2 lines, each width-checked;
    if a head cannot fit in 2 lines it is re-fitted one size down."""
    for sz in (size, size - 1, size - 2):
        f = font(path, sz)
        words, lines, cur = txt.split(" "), [], ""
        overflow = False
        for wd in words:
            trial = (cur + " " + wd).strip()
            if d.textlength(trial, font=f) <= w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                    cur = wd
                else:                      # single word wider than track
                    cur = ""
                if len(lines) == 2:
                    overflow = True
                    break
        if not overflow and cur and len(lines) < 2:
            if d.textlength(cur, font=f) <= w:
                lines.append(cur)
            else:
                overflow = True
        elif not overflow and cur:         # 2 lines already full
            overflow = True
        if not overflow and lines and all(d.textlength(l, font=f) <= w for l in lines):
            return f, lines
    # last resort: 2 hard-clipped lines with ellipsis on the tail
    f = font(path, size - 2)
    words = txt.split(" ")
    l1 = ""
    i = 0
    while i < len(words) and d.textlength((l1 + " " + words[i]).strip(), font=f) <= w:
        l1 = (l1 + " " + words[i]).strip(); i += 1
    rest = " ".join(words[i:])
    _, l2 = fit_one(path, rest, w, size - 2) if rest else (f, "")
    return f, [l1] + ([l2] if l2 else [])

for ci, col_items in enumerate(lrows):
    x0 = LX + ci * (colw + 14)
    tcol = x0 + NUM_W
    scol = tcol + TITLE_W + PAD
    stcol = scol + SRC_W + PAD
    assert stcol + STATUS_W <= x0 + colw, "3-track layout overflows column"
    y = list_top + 3
    for n in col_items:
        s = next(x for x in STORIES if x[0] == n)
        _, region, head, detail, src, status, lat, lon = s
        col, code = REGION[region]
        # one text line per row, vertically centred; titles auto-fit their track
        base = y + (row_h - 12) // 2
        d.text((x0, base - 9), str(n), font=font(F_SANS_CB, 11), fill=col)
        hf, htxt = fit_one(F_SANS_B, head, TITLE_W, 9)
        d.text((tcol, base - hf.size), htxt, font=hf, fill=INK)
        sf, stxt = fit_one(F_SANS, src, SRC_W, 8)
        d.text((scol, base - sf.size), stxt, font=sf, fill=GREY)
        tf, ttxt = fit_one(F_SANS_B, status, STATUS_W, 8)
        d.text((stcol, base - tf.size), ttxt, font=tf, fill=ST_COLOR[status])
        y += row_h
        if n != col_items[-1]:
            d.line([(x0, y - 1), (x0 + colw, y - 1)], fill=(224, 220, 208), width=1)

ALSO_BOTTOM = list_top + 4 + rows * row_h

# =========================================================================
# DATE CHECK block
# =========================================================================
DCKY = MAP_Y + MAP_H + 16
d.line([(M, DCKY - 5), (S - M, DCKY - 5)], fill=RED, width=1)
put(M, DCKY, "DATE CHECK", font(F_NARROW_B, 15), fill=RED, track=0.6)
d.text((M + 120, DCKY), "left out as earlier days’ news", font=font(F_SERIF, 14), fill=GREY)
DATECHECK = [
    "Shenzhen Xi–Putin–Trump trilateral summit (19 Nov) · France's 6th straight cost-of-living march (Sat 21 Nov)",
    "Moscow's 400-drone barrage + 2 missiles into Poland (Fri 20 Nov) · Russia's '165 missiles in a week' (thru 21 Nov) · Bayelsa boat toll 29 (Fri 20 Nov)",
]
yy = DCKY + 20
for ln in DATECHECK:
    f = text_fit(F_SANS, ln, S - 2 * M - 150, 12)
    d.text((M + 150, yy), ln, font=f, fill=INK)
    yy += 18

# =========================================================================
# FOOTER: status-tag legend + sourcing + code note  (chained after DATE CHECK)
# =========================================================================
FY = yy + 12
d.line([(M, FY - 8), (S - M, FY - 8)], fill=RULE, width=2)
put(M, FY, "TAGS", font(F_NARROW_B, 13), fill=GREY, track=0.8)
tagx = M + 60
for st in ["CONFIRMED", "REPORTED", "CLAIM", "PENDING"]:
    f = font(F_SANS_B, 11)
    d.text((tagx, FY + 1), st, font=f, fill=ST_COLOR[st])
    tagx += int(d.textlength(st, font=f)) + 16
put(S - M, FY, "every story dated Sun 22 Nov 2026 (UTC day) · sources named beside each · scenes drawn in code",
    font(F_SANS, 12), fill=GREY, anchor="ra")
d.line([(M, FY + 24), (S - M, FY + 24)], fill=RULE, width=2)
put(M, FY + 32, "SUNDAY 22 NOVEMBER 2026  ·  THE WORLD IN ONE DAY", font(F_SANS_B, 16), fill=INK, track=0.5)
put(S - M, FY + 32, "36 stories · 7 regions · all checkable", font(F_SANS, 13), fill=FAINT, anchor="ra")

# =========================================================================
# SAVE
# =========================================================================
img.save(OUT, format="PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), img.size)

PREV = os.path.join(HERE, "preview-300.png")
img.resize((300, 300), Image.LANCZOS).save(PREV, format="PNG", optimize=True)
print("wrote", PREV, os.path.getsize(PREV))
