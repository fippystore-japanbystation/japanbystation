"""Japan by Station Pin images v3 (Ling, 25 Nov 19:49: "on the phone grid the text must be bigger and grab attention;
the station Pins can't be read at all").

Rule of thumb: Pinterest shows a Pin at about 1/3 of the phone width, so every word on the image must still read
at ~33% size. That means a title of 2–3 lines with 3–4 words per line, set at 110–150 px on a 1000x1500 canvas.

  cover   : full photo, BIG title (2–3 lines) on a strong dark fade. Start a line with * to colour it yellow.
            python3 pinimg3.py cover <photo> "<l1|*l2|l3>" "<PLACE>" <out> [fx] [fy]
  station : station guide Pin. Photo on top, navy panel with the station name huge, "STATION GUIDE",
            a coral "FREE EXIT MAP" badge, and a tilted preview of the real exit card underneath.
            python3 pinimg3.py station <photo> "<Station name>" "<CITY>" <exitcard.jpg> <out> [fx] [fy]
  collage : 4 photos in a 2x2 grid with big numbered labels, big title below (1–2 lines).
            python3 pinimg3.py collage "<p1,p2,p3,p4>" "<l1|l2|l3|l4>" "<title l1|l2>" "<PLACE>" <out>
"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter
from pinimg2 import F, fit, fade, brand, pill, W, H, CORAL, CREAM, INK, WHITE, TEAL, SUN

NAVY = (27, 42, 74)
STROKE = (18, 12, 32)


def _size_to(lines, maxw, start, lo):
    fs = start
    while fs > lo and max(F(fs).getlength(l.lstrip("*")) for l in lines) > maxw: fs -= 2
    return fs


def cover(src, title, kicker, out, fx=0.5, fy=0.5):
    lines = [l for l in title.split("|") if l][:3]
    can = Image.new("RGBA", (W, H)); can.paste(fit(src, W, H, fx, fy), (0, 0))
    fade(can, 0, 190, 120, 0, top=True)
    fs = _size_to(lines, 900, 150, 96)
    lh = int(fs * 1.06); block = lh * len(lines)
    fade(can, max(0, H - block - 520), H, 0, 238)
    d = ImageDraw.Draw(can); brand(d, size=34)
    y = H - 120 - block
    pill(d, 50, y - 104, kicker, 46, fill=SUN, color=INK)
    for l in lines:
        col = SUN if l.startswith("*") else WHITE
        d.text((48, y), l.lstrip("*"), font=F(fs), fill=col, stroke_width=4, stroke_fill=STROKE); y += lh
    d.text((52, H - 84), "japanbystation.com", font=F(34, "Medium"), fill=CREAM)
    can.convert("RGB").save(out, quality=88)


def station(src, name, city, card, out, fx=0.5, fy=0.5):
    can = Image.new("RGBA", (W, H), NAVY + (255,))
    ph = 560
    can.paste(fit(src, W, ph + 60, fx, fy), (0, 0))
    fade(can, 0, 170, 120, 0, top=True)
    d = ImageDraw.Draw(can)
    d.rounded_rectangle((0, ph, W, H + 60), radius=56, fill=NAVY + (255,))
    brand(d, size=34)
    # city pill sits on the photo edge
    pill(d, 50, ph - 44, city.upper(), 44, fill=SUN, color=INK)
    # station name: as big as it fits on one line
    fs = _size_to([name], 900, 160, 90)
    d.text((46, ph + 50), name, font=F(fs), fill=WHITE)
    y = ph + 50 + int(fs * 1.06)
    d.text((50, y), "STATION GUIDE", font=F(68), fill=SUN); y += 98
    # coral badge
    fb = F(58); t = "FREE EXIT MAP"; bw = fb.getlength(t) + 150
    d.rounded_rectangle((50, y, 50 + bw, y + 104), radius=52, fill=CORAL + (255,))
    d.text((92, y + 16), t, font=fb, fill=WHITE)
    # down arrow
    ax = 50 + bw - 62; d.polygon([(ax - 22, y + 40), (ax + 22, y + 40), (ax, y + 70)], fill=WHITE)
    y += 136
    # tilted preview of the real exit card, running off the bottom edge
    c = Image.open(card).convert("RGB")
    c = c.crop((0, 0, c.width, int(c.height * 0.62)))
    cw = 860; c = c.resize((cw, int(c.height * cw / c.width)), Image.LANCZOS).convert("RGBA")
    rot = c.rotate(-3, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", rot.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), mask=rot.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    x0 = (W - rot.width) // 2 + 40
    can.alpha_composite(sh, (x0 + 10, y + 18)); can.alpha_composite(rot, (x0, y))
    # web address on a strip so it stays readable over the card
    d = ImageDraw.Draw(can)
    d.rounded_rectangle((W - 420, H - 96, W - 30, H - 34), radius=31, fill=NAVY + (235,))
    d.text((W - 396, H - 89), "japanbystation.com", font=F(32, "Medium"), fill=WHITE)
    can.convert("RGB").save(out, quality=88)


def collage(srcs, labels, title, kicker, out):
    GH = 1040; g = 8; cw = (W - g) // 2; ch = (GH - g) // 2
    can = Image.new("RGBA", (W, H), CREAM + (255,))
    for i, (s, lab) in enumerate(zip(srcs, labels)):
        x = (i % 2) * (cw + g); y = (i // 2) * (ch + g)
        can.paste(fit(s, cw, ch), (x, y))
        sh = Image.new("RGBA", (cw, 190), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
        for yy in range(190): sd.line([(0, yy), (cw, yy)], fill=(18, 12, 32, int(200 * (yy / 190) ** 1.4)))
        can.alpha_composite(sh, (x, y + ch - 190))
        d = ImageDraw.Draw(can)
        d.ellipse((x + 18, y + ch - 96, x + 90, y + ch - 24), fill=CORAL + (255,))
        fn = F(44); n = str(i + 1); d.text((x + 54 - fn.getlength(n) / 2, y + ch - 92), n, font=fn, fill=WHITE)
        fl = F(44)
        while fl.getlength(lab) > cw - 120: fl = F(fl.size - 1)
        d.text((x + 104, y + ch - 88), lab, font=fl, fill=WHITE, stroke_width=3, stroke_fill=STROKE)
    d = ImageDraw.Draw(can); brand(d, size=30)
    pill(d, 50, GH + 30, kicker, 40, fill=INK, color=WHITE)
    lines = [l for l in title.split("|") if l][:2]
    fs = _size_to(lines, 900, 104, 64); y = GH + 120
    for l in lines:
        d.text((48, y), l.lstrip("*"), font=F(fs), fill=CORAL if l.startswith("*") else INK); y += int(fs * 1.08)
    d.text((52, H - 76), "japanbystation.com", font=F(32, "Medium"), fill=CORAL)
    can.convert("RGB").save(out, quality=88)


if __name__ == "__main__":
    a = sys.argv; m = a[1]
    if m == "cover": cover(a[2], a[3], a[4], a[5], *(float(x) for x in a[6:8]))
    elif m == "station": station(a[2], a[3], a[4], a[5], a[6], *(float(x) for x in a[7:9]))
    elif m == "collage": collage(a[2].split(","), a[3].split("|"), a[4], a[5], a[6])
