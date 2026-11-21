#!/usr/bin/env python3
"""Generate the front-page image for news-image-20261120.

A one-image newspaper front page summing up world news of
Friday, 20 November 2026. All artwork is drawn with PIL shapes;
all text uses fonts bundled on the machine. No network, no photos,
no downloaded assets. Deterministic: same input -> same bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)   # warm off-white newsprint
INK = (17, 17, 17)        # near-black
RED = (166, 30, 30)       # accent red
NAVY = (27, 42, 74)       # dark navy for graphics
SKY = (22, 35, 63)        # night sky in the lead illustration
RIVER = (42, 74, 107)     # Dnipro river band
TINT = (238, 232, 219)    # light panel tint for icons
GREY = (90, 90, 90)       # secondary grey

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = os.path.join(FONT_DIR, "dejavu/DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "dejavu/DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "dejavu/DejaVuSans.ttf")
SANS_I = os.path.join(FONT_DIR, "dejavu/DejaVuSans-Oblique.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_tracked(draw, cx, y, text, fnt, fill, tracking=3):
    """Draw text centred on cx with extra tracking between characters."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def draw_lead_art(d, x0, y0, x1, y1):
    """Stylised night scene over Kyiv: skyline, bridges over the river,
    missile trails and impact glow. All fixed coordinates (deterministic)."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    # stars (fixed positions)
    for sx, sy, r in [(18, 14, 2), (70, 30, 1), (120, 10, 2), (170, 26, 1),
                      (215, 12, 2), (260, 34, 1), (300, 16, 2), (340, 28, 1),
                      (45, 48, 1), (150, 52, 1), (235, 46, 2), (315, 50, 1)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                  fill=(255, 255, 255))
    # missile trails (orange streaks with bright heads)
    for (ax, ay, bx, by) in [(40, 108, 130, 62), (210, 112, 285, 66),
                             (300, 106, 352, 70)]:
        d.line([x0 + ax, y0 + ay, x0 + bx, y0 + by], fill=(255, 170, 60),
               width=3)
        d.ellipse([x0 + bx - 4, y0 + by - 4, x0 + bx + 4, y0 + by + 4],
                  fill=(255, 210, 90))
    # impact glow
    d.ellipse([x0 + 96, y0 + 96, x0 + 128, y0 + 128], fill=(255, 120, 40))
    d.ellipse([x0 + 104, y0 + 104, x0 + 120, y0 + 120], fill=(255, 200, 90))
    # skyline silhouettes
    base = y1 - 34
    buildings = [(0, 46, 34), (38, 70, 30), (72, 52, 36), (112, 84, 30),
                 (146, 60, 34), (184, 78, 30), (218, 54, 36), (258, 72, 32),
                 (292, 58, 34), (330, 66, 34)]
    for bx, bh, bw in buildings:
        d.rectangle([x0 + bx, base - bh, x0 + bx + bw, base],
                    fill=(10, 16, 34))
    # river band
    d.rectangle([x0, base, x1, y1], fill=RIVER)
    # three bridges: arches rising above the river deck line
    for cx, span in [(62, 52), (182, 56), (302, 52)]:
        d.arc([x0 + cx - span // 2, base - 18, x0 + cx + span // 2, base + 10],
              start=180, end=360, fill=(150, 185, 220), width=3)
        d.line([x0 + cx - span // 2, base + 4, x0 + cx + span // 2, base + 4],
               fill=(150, 185, 220), width=2)
    # label
    d.text((x0 + 8, y0 + 6), "KYIV", font=font(SANS_B, 15), fill=(255, 255, 255))


def icon_jet(d, x0, y0, s):
    """Fighter jet silhouette + red blip."""
    d.rectangle([x0, y0, x0 + s, y0 + s], fill=TINT)
    pts = [(x0 + 12, y0 + 52), (x0 + 30, y0 + 30), (x0 + 44, y0 + 30),
           (x0 + 68, y0 + 52), (x0 + 52, y0 + 58), (x0 + 44, y0 + 66),
           (x0 + 36, y0 + 58)]
    d.polygon(pts, fill=NAVY)
    d.ellipse([x0 + 62, y0 + 14, x0 + 70, y0 + 22], fill=RED)


def icon_scales(d, x0, y0, s):
    """Scales of justice."""
    d.rectangle([x0, y0, x0 + s, y0 + s], fill=TINT)
    d.line([x0 + 40, y0 + 12, x0 + 40, y0 + 66], fill=NAVY, width=4)
    d.line([x0 + 16, y0 + 22, x0 + 64, y0 + 22], fill=NAVY, width=4)
    d.line([x0 + 40, y0 + 66, x0 + 28, y0 + 66], fill=NAVY, width=4)
    d.line([x0 + 40, y0 + 66, x0 + 52, y0 + 66], fill=NAVY, width=4)
    for cx in (16, 64):
        d.line([x0 + cx, y0 + 22, x0 + cx, y0 + 38], fill=NAVY, width=2)
        d.polygon([(x0 + cx - 10, y0 + 38), (x0 + cx + 10, y0 + 38),
                   (x0 + cx, y0 + 50)], fill=NAVY)


def icon_globe(d, x0, y0, s):
    """Globe with three dots (three-way summit)."""
    d.rectangle([x0, y0, x0 + s, y0 + s], fill=TINT)
    d.ellipse([x0 + 16, y0 + 16, x0 + 64, y0 + 64], outline=NAVY, width=3)
    d.ellipse([x0 + 30, y0 + 16, x0 + 50, y0 + 64], outline=NAVY, width=2)
    d.line([x0 + 16, y0 + 40, x0 + 64, y0 + 40], fill=NAVY, width=2)
    for cx in (28, 40, 52):
        d.ellipse([x0 + cx - 3, y0 + 8 - 3, x0 + cx + 3, y0 + 8 + 3], fill=RED)


def icon_chart_down(d, x0, y0, s):
    """Falling market chart."""
    d.rectangle([x0, y0, x0 + s, y0 + s], fill=TINT)
    d.line([x0 + 12, y0 + 14, x0 + 12, y0 + 66], fill=NAVY, width=3)
    d.line([x0 + 12, y0 + 66, x0 + 68, y0 + 66], fill=NAVY, width=3)
    pts = [(14, 26), (28, 34), (40, 30), (54, 52), (66, 62)]
    pts = [(x0 + px, y0 + py) for px, py in pts]
    d.line(pts, fill=RED, width=4, joint="curve")
    d.polygon([(x0 + 66, y0 + 62), (x0 + 58, y0 + 58), (x0 + 60, y0 + 66)],
              fill=RED)


def icon_tower(d, x0, y0, s):
    """Skyscraper with impact burst."""
    d.rectangle([x0, y0, x0 + s, y0 + s], fill=TINT)
    d.rectangle([x0 + 30, y0 + 20, x0 + 50, y0 + 68], fill=NAVY)
    for wy in (28, 38, 48, 58):
        for wx in (34, 42):
            d.rectangle([x0 + wx, y0 + wy, x0 + wx + 4, y0 + wy + 4],
                        fill=(255, 210, 90))
    d.polygon([(x0 + 58, y0 + 14), (x0 + 62, y0 + 22), (x0 + 70, y0 + 22),
               (x0 + 64, y0 + 27), (x0 + 66, y0 + 35), (x0 + 58, y0 + 30),
               (x0 + 50, y0 + 35), (x0 + 52, y0 + 27), (x0 + 46, y0 + 22),
               (x0 + 54, y0 + 22)], fill=RED)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40  # margin
    CW = W - 2 * M  # content width 944

    # outer frame
    d.rectangle([20, 20, W - 20, H - 20], outline=INK, width=3)

    # ---- masthead ----
    mast = font(SERIF_B, 100)
    d.text((W // 2, 34), "THE WORLD", font=mast, fill=INK, anchor="ma")
    date_f = font(SANS_B, 33)
    draw_tracked(d, W // 2, 148, "FRIDAY, 20 NOVEMBER 2026", date_f, INK,
                 tracking=2)
    d.line([M, 192, W - M, 192], fill=INK, width=4)
    d.line([M, 200, W - M, 200], fill=INK, width=1)

    # ---- lead story ----
    kick = font(SANS_B, 21)
    d.text((M, 214), "UKRAINE WAR", font=kick, fill=RED)
    head = font(SANS_B, 46)
    lead_head = "Russia launches huge missile and drone attack on Kyiv"
    lines = wrap(d, lead_head, head, CW)
    y = draw_lines(d, M, 244, lines, head, INK, 56)
    # summary (left) + illustration (right)
    body = font(SANS, 23)
    summary = ("More than 100 missiles and 400 drones struck Ukraine. "
               "Eight killed, 28 injured. Bridges across the Dnipro were "
               "hit as Russia targeted the energy grid.")
    draw_lines(d, M, 372, wrap(d, summary, body, 560), body, INK, 30)
    draw_lead_art(d, 620, 368, 984, 536)
    d.rectangle([620, 368, 984, 536], outline=INK, width=2)

    # divider
    d.line([M, 556, W - M, 556], fill=INK, width=2)

    # ---- secondary grid: 2 cols x 3 rows ----
    rows = [
        ("POLAND", "NATO jets scramble as Russian missiles enter Poland",
         "Tusk calls it an \u2018intentional provocation\u2019.",
         icon_jet),
        ("WORLD COURT", "Court rules Myanmar committed genocide",
         "9\u20136 ruling for the Rohingya \u2014 a first for a state.",
         icon_scales),
        ("DIPLOMACY", "Trump, Xi and Putin: \u2018A nuclear war cannot be won\u2019",
         "First three-way summit in Shenzhen; no Ukraine breakthrough.",
         icon_globe),
        ("MARKETS", "Stocks fall a fifth day; Nikkei drops 4.8%",
         "US shares slide again as Japan\u2019s market sinks.",
         icon_chart_down),
        ("MIDDLE EAST", "Houthi missile damages Riyadh tower",
         "Saudi defences stop another missile and five drones.",
         icon_tower),
        None,  # also-in-the-news cell
    ]
    col_x = [M, 522]
    row_y = [570, 708, 846]
    cell_w, cell_h = 462, 130
    kf = font(SANS_B, 16)
    hf = font(SANS_B, 21)
    df = font(SANS, 18)
    for i, item in enumerate(rows):
        cx = col_x[i % 2]
        cy = row_y[i // 2]
        if item is None:
            d.text((cx, cy), "ALSO IN THE NEWS", font=kf, fill=RED)
            af = font(SANS_B, 19)
            bf = font(SANS, 19)
            y2 = cy + 24
            for tag, txt in [("ESTONIA", "Border with Russia to close for at least six months."),
                             ("TECH", "Anthropic debuts on Nasdaq; shares close up 17% at $97.")]:
                d.text((cx, y2), "\u2022 " + tag + " \u2014 ", font=af, fill=INK)
                tw = d.textlength("\u2022 " + tag + " \u2014 ", font=af)
                # wrap the rest under the same left edge
                rest = wrap(d, txt, bf, cell_w - tw)
                d.text((cx + tw, y2), rest[0], font=bf, fill=INK)
                y2 += 24
                for extra in rest[1:]:
                    d.text((cx + 14, y2), extra, font=bf, fill=INK)
                    y2 += 24
                y2 += 4
            continue
        kicker, headline, deck, icon = item
        icon(d, cx, cy + 4, 80)
        tx = cx + 96
        tw = cell_w - 96
        d.text((tx, cy), kicker, font=kf, fill=RED)
        hl = wrap(d, headline, hf, tw)
        y2 = draw_lines(d, tx, cy + 23, hl, hf, INK, 26)
        draw_lines(d, tx, y2 + 2, wrap(d, deck, df, tw), df, GREY, 22)

    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, optimize=True)
    print("saved", out, img.size, os.path.getsize(out), "bytes")
