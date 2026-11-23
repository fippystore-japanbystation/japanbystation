"""Japan by Station Reel cover: same layout every time.
usage: python3 cover.py <video> <time> "<title line 1>|<line 2>" "<CATEGORY>" <color> <KEYWORD> <out.jpg>
Safe zone: everything important sits inside the centre 1080x1440 (profile grid crop is 3:4)."""
import sys, subprocess, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
W, H = 1080, 1920
import os as _os
FD = "/usr/share/fonts/truetype/google-fonts/" if _os.path.exists("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf") else _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "fonts") + "/"
def F(s, w="Bold"): return ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)
INK = (59, 48, 96); CREAM = (255, 250, 243); WHITE = (255, 255, 255); STROKE = (40, 28, 70)
COL = {"coral": (255, 125, 94), "mint": (51, 195, 161), "sky": (90, 174, 255), "sun": (255, 194, 61), "lilac": (168, 139, 255), "pink": (255, 141, 182)}

def make(video, t, title, cat, color, kw, out):
    b = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t), "-i", video, "-frames:v", "1", "-vf",
                        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920", "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True, check=True).stdout
    im = Image.open(io.BytesIO(b)).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.15)
    ov = Image.new("RGBA", (W, H), (30, 22, 50, 70)); d = ImageDraw.Draw(ov)
    c = COL[color]
    # ONE centred block on the middle of the grid crop (y=960), logo colours, one pill only:
    #   coral "Japan by Station" pill  ->  title  ->  place in plain white text
    lines = title.split("|"); fs = 108
    while max(F(fs).getlength(l) for l in lines) > 940: fs -= 4
    f = F(fs); lh = int(fs * 1.1)
    fb = F(54); bs = "Japan by Station"; bw = fb.getlength(bs); bh = 92
    fc = F(46); cw = fc.getlength(cat)
    g1, g2, ch = 30, 30, 60
    block = bh + g1 + lh * len(lines) + g2 + ch
    top = 960 - block // 2
    CORAL = (255, 125, 94)
    d.rounded_rectangle((W/2 - bw/2 - 40, top, W/2 + bw/2 + 40, top + bh), radius=46, fill=CORAL + (255,))
    d.text((W/2 - bw/2, top + 10), bs, font=fb, fill=CREAM)
    y = top + bh + g1
    d.rectangle((0, y - 20, W, y + lh * len(lines) + g2 + ch + 16), fill=(30, 22, 50, 95))
    for l in lines:
        d.text(((W - f.getlength(l)) / 2, y), l, font=f, fill=WHITE, stroke_width=9, stroke_fill=STROKE)
        y += lh
    y += g2
    d.text(((W - cw) / 2, y), cat, font=fc, fill=CREAM, stroke_width=5, stroke_fill=STROKE)
    # no bottom pill (Ling, 23 Nov): natural sharing, no "DM us" on the cover
    im = im.convert("RGBA"); im.alpha_composite(ov); im.convert("RGB").save(out, quality=90)

if __name__ == "__main__":
    make(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
