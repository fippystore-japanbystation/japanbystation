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
    # brand pill
    f = F(34); s = "Japan by Station"; w = f.getlength(s)
    d.rounded_rectangle((W/2 - w/2 - 30, 300, W/2 + w/2 + 30, 364), radius=32, fill=CREAM + (240,))
    d.text((W/2 - w/2, 307), s, font=f, fill=INK)
    # category tag
    f = F(38); w = f.getlength(cat) + 56
    d.rounded_rectangle((W/2 - w/2, 640, W/2 + w/2, 708), radius=34, fill=c + (255,))
    d.text((W/2 - (w - 56)/2, 648), cat, font=f, fill=INK)
    # title, outlined, max 2 lines
    lines = title.split("|"); fs = 104
    while max(F(fs).getlength(l) for l in lines) > 940: fs -= 4
    f = F(fs); y = 740
    for l in lines:
        d.text(((W - f.getlength(l)) / 2, y), l, font=f, fill=WHITE, stroke_width=8, stroke_fill=STROKE)
        y += int(fs * 1.12)
    # keyword
    f = F(40, "Medium"); s = "Comment"; fk = F(56); k = kw
    tw = f.getlength(s) + 18 + fk.getlength(k) + 70
    y2 = 1500
    d.rounded_rectangle((W/2 - tw/2, y2, W/2 + tw/2, y2 + 96), radius=48, fill=CREAM + (245,))
    x = W/2 - tw/2 + 35
    d.text((x, y2 + 22), s, font=f, fill=INK); x += f.getlength(s) + 18
    d.text((x, y2 + 10), k, font=fk, fill=c if color not in ("sun",) else (214, 150, 0))
    im = im.convert("RGBA"); im.alpha_composite(ov); im.convert("RGB").save(out, quality=90)

if __name__ == "__main__":
    make(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
