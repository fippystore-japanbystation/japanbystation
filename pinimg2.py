"""Japan by Station Pin images v2 (Ling, 24 Nov: photo first, smaller title, multi-photo).
1000x1500 (2:3). Three layouts:

  cover   : the photo fills the whole Pin, a small title sits on a soft dark fade at the bottom.
            python3 pinimg2.py cover <photo> "<title l1|l2>" "<KICKER>" <out> [fx] [fy]
  collage : 4 photos in a 2x2 grid, each numbered with a short label, slim title strip below.
            python3 pinimg2.py collage "<p1,p2,p3,p4>" "<l1|l2|l3|l4>" "<title>" "<KICKER>" <out>
  page    : one carousel page: full photo, small card at the bottom with #n, a head line and 1-2 lines.
            python3 pinimg2.py page <photo> <n> "<head>" "<body>" <out> [fx] [fy]
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W, H = 1000, 1500
HERE = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/truetype/google-fonts/" if os.path.exists("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf") else os.path.join(HERE, "fonts") + "/"
def F(s, w="Bold"):
    p = FD + f"Poppins-{w}.ttf"
    return ImageFont.truetype(p if os.path.exists(p) else FD + "Poppins-Bold.ttf", s)
CORAL = (255, 125, 94); CREAM = (255, 250, 243); INK = (59, 48, 96); WHITE = (255, 255, 255); TEAL = (49, 196, 160); SUN = (255, 196, 61)


def fit(src, w, h, fx=0.5, fy=0.5):
    im = Image.open(src).convert("RGB"); r = w / h
    if im.width / im.height > r:
        nw = int(im.height * r); x0 = int((im.width - nw) * fx); im = im.crop((x0, 0, x0 + nw, im.height))
    else:
        nh = int(im.width / r); y0 = int((im.height - nh) * fy); im = im.crop((0, y0, im.width, y0 + nh))
    im = im.resize((w, h), Image.LANCZOS)
    return ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.12)).enhance(1.04)


def fade(can, y0, y1, a0, a1, top=False):
    g = Image.new("RGBA", (W, y1 - y0), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    for y in range(y1 - y0):
        t = y / (y1 - y0); a = a0 + (a1 - a0) * (t ** 1.6 if not top else t)
        d.line([(0, y), (W, y)], fill=(18, 12, 32, int(a)))
    can.alpha_composite(g, (0, y0))


def brand(d, x=36, y=36, size=30):
    f = F(size); s = "Japan by Station"; w = f.getlength(s)
    d.rounded_rectangle((x, y, x + w + 48, y + size + 26), radius=(size + 26) // 2, fill=CORAL + (255,))
    d.text((x + 24, y + 6), s, font=f, fill=CREAM)


def pill(d, x, y, text, size=28, fill=INK, color=WHITE):
    f = F(size); w = f.getlength(text)
    d.rounded_rectangle((x, y, x + w + 44, y + size + 24), radius=(size + 24) // 2, fill=fill + (255,))
    d.text((x + 22, y + 7 + max(0, size - 28) // 4), text, font=f, fill=color); return w + 44


def chips(d, y, items, size=30):
    """Highlight keywords as coloured tags (Ling 24 Nov: show WHAT the highlights are at a glance)."""
    fc = F(size, "SemiBold"); x = 50; rows = 1
    for k, c in enumerate(items):
        cw = fc.getlength(c) + 36
        if x + cw > W - 50 and x > 50: x = 50; y += size + 30; rows += 1
        col = (CORAL, TEAL, SUN)[k % 3]
        d.rounded_rectangle((x, y, x + cw, y + size + 18), radius=(size + 18) // 2, fill=col + (255,))
        d.text((x + 18, y + 5), c, font=fc, fill=INK if col == SUN else WHITE); x += cw + 12
    return rows


def cover(src, title, kicker, out, fx=0.5, fy=0.5, hl=None):
    lines = [l for l in title.split("|") if l][:2]
    items = [c.strip() for c in (hl or "").split(";") if c.strip()][:3]
    if items:  # measure how many chip rows we need
        fc = F(30, "SemiBold"); x = 50; nrows = 1
        for c in items:
            cw = fc.getlength(c) + 36
            if x + cw > W - 50 and x > 50: x = 50; nrows += 1
            x += cw + 12
        extra = 20 + nrows * 60
    else: extra = 0
    can = Image.new("RGBA", (W, H)); can.paste(fit(src, W, H, fx, fy), (0, 0))
    fade(can, 0, 170, 110, 0, top=True)
    fade(can, H - 560, H, 0, 215)
    d = ImageDraw.Draw(can); brand(d)
    fs = 74
    while max(F(fs).getlength(l) for l in lines) > 900: fs -= 2
    lh = int(fs * 1.12); y = H - 110 - lh * len(lines) - extra
    pill(d, 50, y - 96, kicker, 40, fill=CREAM, color=INK)  # Ling 24 Nov: place label bigger
    for l in lines:
        d.text((50, y), l, font=F(fs), fill=WHITE, stroke_width=2, stroke_fill=(18, 12, 32)); y += lh
    if items: chips(d, y + 14, items)
    d.text((52, H - 78), "japanbystation.com", font=F(30, "SemiBold"), fill=SUN)
    can.convert("RGB").save(out, quality=88)


def collage(srcs, labels, title, kicker, out):
    GH = 1160; g = 8; cw = (W - g) // 2; ch = (GH - g) // 2
    can = Image.new("RGBA", (W, H), CREAM + (255,))
    for i, (s, lab) in enumerate(zip(srcs, labels)):
        x = (i % 2) * (cw + g); y = (i // 2) * (ch + g)
        can.paste(fit(s, cw, ch), (x, y))
        sh = Image.new("RGBA", (cw, 150), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
        for yy in range(150): sd.line([(0, yy), (cw, yy)], fill=(18, 12, 32, int(170 * (yy / 150) ** 1.5)))
        can.alpha_composite(sh, (x, y + ch - 150))
        d = ImageDraw.Draw(can)
        d.ellipse((x + 18, y + ch - 78, x + 74, y + ch - 22), fill=CORAL + (255,))
        fn = F(32); n = str(i + 1); d.text((x + 46 - fn.getlength(n) / 2, y + ch - 73), n, font=fn, fill=WHITE)
        fl = F(30)
        while fl.getlength(lab) > cw - 110: fl = F(fl.size - 1)
        d.text((x + 88, y + ch - 70), lab, font=fl, fill=WHITE, stroke_width=2, stroke_fill=(18, 12, 32))
    d = ImageDraw.Draw(can); brand(d, size=26)
    pill(d, 50, GH + 30, kicker, 32)
    fs = 62
    while F(fs).getlength(title) > 900: fs -= 2
    d.text((50, GH + 106), title, font=F(fs), fill=INK)
    d.text((52, H - 82), "japanbystation.com", font=F(30, "SemiBold"), fill=CORAL)
    for i, c in enumerate((CORAL, TEAL, SUN)):
        cx = W - 150 + i * 40; d.ellipse((cx, H - 68, cx + 22, H - 46), fill=c)
    can.convert("RGB").save(out, quality=88)


def page(src, n, head, body, out, fx=0.5, fy=0.5):
    can = Image.new("RGBA", (W, H)); can.paste(fit(src, W, H, fx, fy), (0, 0))
    fade(can, 0, 170, 110, 0, top=True)
    d = ImageDraw.Draw(can); brand(d)
    fb = F(32, "Medium"); rows = [""]
    for wd in body.split():
        t = (rows[-1] + " " + wd).strip()
        if fb.getlength(t) > 820 and rows[-1]: rows.append(wd)
        else: rows[-1] = t
    rows = rows[:3]
    fh = 54
    while F(fh).getlength(head) > 820: fh -= 2
    ch = 60 + int(fh * 1.15) + 46 * len(rows) + 50
    y0 = H - 50 - ch
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((40, y0, W - 40, H - 50), radius=36, fill=CREAM + (242,))
    can.alpha_composite(card); d = ImageDraw.Draw(can)
    d.ellipse((76, y0 - 40, 156, y0 + 40), fill=CORAL + (255,))
    fn = F(44); d.text((116 - fn.getlength(str(n)) / 2, y0 - 31), str(n), font=fn, fill=WHITE)
    y = y0 + 58; d.text((80, y), head, font=F(fh), fill=INK); y += int(fh * 1.15) + 8
    for r in rows: d.text((80, y), r, font=fb, fill=(95, 86, 125)); y += 46
    can.convert("RGB").save(out, quality=88)


if __name__ == "__main__":
    a = sys.argv; m = a[1]
    if m == "cover":
        hl = None
        if "--hl" in a: i = a.index("--hl"); hl = a[i + 1]; a = a[:i] + a[i + 2:]
        cover(a[2], a[3], a[4], a[5], *(float(x) for x in a[6:8]), hl=hl)
    elif m == "collage": collage(a[2].split(","), a[3].split("|"), a[4], a[5], a[6])
    elif m == "page": page(a[2], int(a[3]), a[4], a[5], a[6], *(float(x) for x in a[7:9]))
