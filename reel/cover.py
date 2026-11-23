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
    # brand pill (top of the 3:4 grid crop, which shows y 240-1680)
    # BIG so a stranger on the grid instantly knows this is about Japan
    f = F(66); s = "Japan by Station"; w = f.getlength(s)
    d.rounded_rectangle((W/2 - w/2 - 44, 262, W/2 + w/2 + 44, 372), radius=55, fill=CREAM + (245,))
    d.text((W/2 - w/2, 272), s, font=f, fill=INK)
    # category pill + title, centred as one block on the middle of the grid crop (y=960)
    lines = title.split("|"); fs = 108
    while max(F(fs).getlength(l) for l in lines) > 940: fs -= 4
    f = F(fs); lh = int(fs * 1.1); gap = 34; ph = 78
    block = ph + gap + lh * len(lines)
    top = 960 - block // 2
    fc = F(44); w = fc.getlength(cat) + 64
    d.rounded_rectangle((W/2 - w/2, top, W/2 + w/2, top + ph), radius=39, fill=INK + (235,))
    d.text((W/2 - (w - 64)/2, top + 9), cat, font=fc, fill=WHITE)
    y = top + ph + gap
    d.rectangle((0, y - 22, W, y + lh * len(lines) + 22), fill=(30, 22, 50, 95))
    for l in lines:
        d.text(((W - f.getlength(l)) / 2, y), l, font=f, fill=WHITE, stroke_width=9, stroke_fill=STROKE)
        y += lh
    # no bottom pill (Ling, 23 Nov): natural sharing, no "DM us" on the cover
    im = im.convert("RGBA"); im.alpha_composite(ov); im.convert("RGB").save(out, quality=90)

if __name__ == "__main__":
    make(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
