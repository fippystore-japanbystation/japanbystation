"""Japan by Station: Facebook post image (1080x1350, 4:5) with a big centred title.
usage: python3 fbimg.py <photo.jpg> "<title line 1>|<line 2>|<line 3>" "<KICKER e.g. KIZU MARKET, OSAKA>" <out.jpg> [focus_x 0-1]
The photo is cropped to 4:5 around focus_x (default 0.5), darkened a little, and gets:
coral "Japan by Station" pill at the top, a place pill and the title in the middle, the site at the bottom."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/truetype/google-fonts/" if os.path.exists("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf") else os.path.join(HERE, "fonts") + "/"
def F(s, w="Bold"): return ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)
CORAL = (255, 125, 94); CREAM = (255, 250, 243); INK = (59, 48, 96); WHITE = (255, 255, 255); STROKE = (30, 22, 50)


def make(src, title, kicker, out, fx=0.5):
    im = Image.open(src).convert("RGB")
    # crop to 4:5 around focus_x
    r = W / H
    if im.width / im.height > r:
        nw = int(im.height * r); x0 = int((im.width - nw) * fx); im = im.crop((x0, 0, x0 + nw, im.height))
    else:
        nh = int(im.width / r); y0 = (im.height - nh) // 2; im = im.crop((0, y0, im.width, y0 + nh))
    im = im.resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.18)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    # soft vertical shade so white text always reads
    for y in range(H):
        a = int(70 + 60 * (abs(y - H * 0.5) / (H * 0.5)) ** 1.5)
        d.line([(0, y), (W, y)], fill=(20, 14, 35, a))
    # brand pill
    f = F(46); s = "Japan by Station"; w = f.getlength(s)
    d.rounded_rectangle((W/2 - w/2 - 40, 70, W/2 + w/2 + 40, 70 + 84), radius=42, fill=CORAL + (255,))
    d.text((W/2 - w/2, 79), s, font=f, fill=CREAM)
    # title block, centred
    lines = [l for l in title.split("|") if l]
    fs = 112
    while max(F(fs).getlength(l) for l in lines) > 960: fs -= 4
    ft = F(fs); lh = int(fs * 1.12)
    fk = F(40); kw = fk.getlength(kicker) + 60; kh = 68
    block = kh + 36 + lh * len(lines)
    top = int(H * 0.5 - block / 2)
    d.rounded_rectangle((W/2 - kw/2, top, W/2 + kw/2, top + kh), radius=34, fill=INK + (235,))
    d.text((W/2 - (kw - 60)/2, top + 9), kicker, font=fk, fill=WHITE)
    y = top + kh + 36
    for l in lines:
        d.text(((W - ft.getlength(l)) / 2, y), l, font=ft, fill=WHITE, stroke_width=10, stroke_fill=STROKE)
        y += lh
    # site line
    fu = F(38, "SemiBold") if os.path.exists(FD + "Poppins-SemiBold.ttf") else F(38)
    u = "Full guide on japanbystation.com"
    d.text(((W - fu.getlength(u)) / 2, H - 110), u, font=fu, fill=CREAM, stroke_width=4, stroke_fill=STROKE)
    im = im.convert("RGBA"); im.alpha_composite(ov)
    im.convert("RGB").save(out, quality=88)


if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]) if len(sys.argv) > 5 else 0.5)
