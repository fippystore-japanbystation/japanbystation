"""Japan by Station: Pinterest Pin image (1000x1500, 2:3).
usage: python3 pinimg.py <photo.jpg> "<title l1|l2|l3>" "<KICKER e.g. TENMA, OSAKA>" "<sub line>" <out.jpg> [focus_x 0-1] [focus_y 0-1]
Photo fills the top ~60%, a cream panel holds the kicker, the big title and one short sub line,
with the brand pill on the photo and the site at the foot."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W, H = 1000, 1500
HERE = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/truetype/google-fonts/" if os.path.exists("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf") else os.path.join(HERE, "fonts") + "/"
def F(s, w="Bold"):
    p = FD + f"Poppins-{w}.ttf"
    return ImageFont.truetype(p if os.path.exists(p) else FD + "Poppins-Bold.ttf", s)
CORAL = (255, 125, 94); CREAM = (255, 250, 243); INK = (59, 48, 96); WHITE = (255, 255, 255); TEAL = (49, 196, 160); SUN = (255, 196, 61)


def make(src, title, kicker, sub, out, fx=0.5, fy=0.5):
    lines = [l for l in title.split("|") if l]
    fs = 96
    while max(F(fs).getlength(l) for l in lines) > 880: fs -= 3
    fsb = F(36, "Medium"); rows = [""]
    for wd in sub.split():
        t = (rows[-1] + " " + wd).strip()
        if fsb.getlength(t) > 880 and rows[-1]: rows.append(wd)
        else: rows[-1] = t
    rows = rows[:2]
    panel = 92 + int(fs * 1.1) * len(lines) + 14 + 50 * len(rows) + 130
    PH = max(700, min(920, H - panel))
    im = Image.open(src).convert("RGB")
    r = W / PH
    if im.width / im.height > r:
        nw = int(im.height * r); x0 = int((im.width - nw) * fx); im = im.crop((x0, 0, x0 + nw, im.height))
    else:
        nh = int(im.width / r); y0 = int((im.height - nh) * fy); im = im.crop((0, y0, im.width, y0 + nh))
    im = im.resize((W, PH), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.15); im = ImageEnhance.Contrast(im).enhance(1.05)
    can = Image.new("RGBA", (W, H), CREAM + (255,))
    can.paste(im, (0, 0))
    d = ImageDraw.Draw(can)
    # top shade for the pill
    sh = Image.new("RGBA", (W, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for y in range(200): sd.line([(0, y), (W, y)], fill=(20, 14, 35, int(110 * (1 - y / 200))))
    can.alpha_composite(sh, (0, 0))
    f = F(38); s = "Japan by Station"; w = f.getlength(s)
    d.rounded_rectangle((40, 40, 40 + w + 64, 40 + 72), radius=36, fill=CORAL + (255,))
    d.text((72, 46), s, font=f, fill=CREAM)
    # panel: rounded top edge overlapping the photo
    d.rounded_rectangle((0, PH - 50, W, H + 60), radius=50, fill=CREAM + (255,))
    # kicker pill
    fk = F(34); kw = fk.getlength(kicker)
    d.rounded_rectangle((60, PH, 60 + kw + 56, PH + 62), radius=31, fill=INK + (255,))
    d.text((88, PH + 8), kicker, font=fk, fill=WHITE)
    # title
    ft = F(fs); lh = int(fs * 1.1)
    y = PH + 92
    for l in lines:
        d.text((60, y), l, font=ft, fill=INK); y += lh
    # sub line (wraps to 2 lines max)
    y += 14
    for rw in rows:
        d.text((60, y), rw, font=fsb, fill=(110, 100, 140)); y += 50
    # footer
    fu = F(34, "SemiBold"); u = "japanbystation.com"
    d.text((60, H - 84), u, font=fu, fill=CORAL)
    for i, c in enumerate((CORAL, TEAL, SUN)):
        cx = W - 150 + i * 40; d.ellipse((cx, H - 70, cx + 22, H - 48), fill=c)
    assert y < H - 100, f"text overflows panel ({y})"
    can.convert("RGB").save(out, quality=88)


if __name__ == "__main__":
    a = sys.argv
    make(a[1], a[2], a[3], a[4], a[5], float(a[6]) if len(a) > 6 else 0.5, float(a[7]) if len(a) > 7 else 0.5)
