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
    f = F(34); s = "Japan by Station"; w = f.getlength(s)
    d.rounded_rectangle((W/2 - w/2 - 30, 290, W/2 + w/2 + 30, 354), radius=32, fill=CREAM + (240,))
    d.text((W/2 - w/2, 297), s, font=f, fill=INK)
    # category tag
    f = F(44); w = f.getlength(cat) + 64
    d.rounded_rectangle((W/2 - w/2, 420, W/2 + w/2, 498), radius=39, fill=c + (255,))
    d.text((W/2 - (w - 64)/2, 429), cat, font=f, fill=INK)
    # title: BIG, outlined, max 2 lines, high up so it reads on the profile grid
    lines = title.split("|"); fs = 158
    while max(F(fs).getlength(l) for l in lines) > 1010: fs -= 4
    f = F(fs); lh = int(fs * 1.08); y = 530
    band = (0, y - 24, W, y + lh * len(lines) + 30)
    d.rectangle(band, fill=(30, 22, 50, 95))
    for l in lines:
        d.text(((W - f.getlength(l)) / 2, y), l, font=f, fill=WHITE, stroke_width=11, stroke_fill=STROKE)
        y += lh
    # bottom pill: the guide comes by DM (keyword is in the video and caption)
    f = F(58); s = "Full guide in DM"
    tw = f.getlength(s) + 90; y2 = 1420
    d.rounded_rectangle((W/2 - tw/2, y2, W/2 + tw/2, y2 + 110), radius=55, fill=CREAM + (245,))
    d.text((W/2 - f.getlength(s)/2, y2 + 18), s, font=f, fill=c if color not in ("sun",) else (214, 150, 0))
    im = im.convert("RGBA"); im.alpha_composite(ov); im.convert("RGB").save(out, quality=90)

if __name__ == "__main__":
    make(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
