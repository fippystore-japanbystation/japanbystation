"""SPLIT Reel: "Everyone goes to X / Go here instead: Y" (26 Nov; idea from a Japan account whose famous-vs-hidden
split-screen carousel got about as many shares as likes: the conflict makes people send it to their travel buddy).
Top half = the famous place, bottom half = our pick. One pair every few seconds, music only, no voice.

python3 splitreel.py specs/<slug>.json [--stills]

Spec:
{"slug": "osaka-famous-vs-local", "format": "split", "keyword": "TENMA", "music": "m_petals.mp3",
 "clipdir": "air/", "outdir": "out/", "tag": "OSAKA",
 "labels": {"top": "Everyone goes to", "bottom": "Go here instead"},      (optional; these are the defaults)
 "hold": 2.8,                                                               (seconds per pair; the last pair holds +2 s)
 "pairs": [{"top": {"media": "a.mp4", "t": 1.0, "place": "Dotonbori"},
            "bottom": {"media": "b.jpg", "place": "Tenma", "note": "2.6 km covered food street"}}, ...],
 "caption": "..."}
Every "note" must be on a guide page (or the logged official source); media: licensed only (PLAYBOOK FOOTAGE)."""
import json, os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, HALF, FPS = 1080, 1920, 960, 30
FD = os.path.join(HERE, "..", "fonts") + "/"
def F(s, w="Bold"): return ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)
INK = (59, 48, 96); CREAM = (255, 250, 243); WHITE = (255, 255, 255); STROKE = (20, 16, 40)
CORAL = (255, 125, 94); SUN = (255, 194, 61); MINT = (51, 195, 161)
IMG = (".jpg", ".jpeg", ".png", ".webp")

def fit(d, text, size, maxw, w="Bold"):
    f = F(size, w)
    while d.textlength(text, font=f) > maxw and size > 30: size -= 2; f = F(size, w)
    return f

def overlay(spec, i, last):
    p = spec["pairs"][i]; lab = {"top": "Everyone goes to", "bottom": "Go here instead", **spec.get("labels", {})}
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for y0, y1 in ((HALF - 330, HALF), (H - 380, H)):                      # soft dark gradient under each text block
        for y in range(y0, y1):
            a = int(150 * (y - y0) / (y1 - y0)); d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    d.line([(0, HALF), (W, HALF)], fill=(255, 255, 255, 230), width=6)       # the split
    def block(yb, small, big, color, note=None):
        fs = fit(d, small, 64, W - 120); fb = fit(d, big, 96, W - 100)
        y = yb - (fb.size + fs.size + 30 + (50 if note else 0))
        d.text(((W - d.textlength(small, font=fs)) / 2, y), small, font=fs, fill=WHITE, stroke_width=7, stroke_fill=STROKE)
        y += fs.size + 14
        d.text(((W - d.textlength(big, font=fb)) / 2, y), big, font=fb, fill=color, stroke_width=9, stroke_fill=STROKE)
        if note:
            fn = fit(d, note, 40, W - 160, "SemiBold") if os.path.exists(FD + "Poppins-SemiBold.ttf") else fit(d, note, 40, W - 160)
            y += fb.size + 18
            d.text(((W - d.textlength(note, font=fn)) / 2, y), note, font=fn, fill=WHITE, stroke_width=6, stroke_fill=STROKE)
    block(HALF - 40, lab["top"], p["top"]["place"], WHITE)
    block(H - (150 if last and spec.get("keyword") else 70), lab["bottom"], p["bottom"]["place"], SUN, p["bottom"].get("note"))
    # brand + tag pill at the very top
    f = F(30); s = "Japan by Station" + (f"  ·  {spec['tag']}" if spec.get("tag") else ""); w = d.textlength(s, font=f)
    d.rounded_rectangle((W/2 - w/2 - 28, 70, W/2 + w/2 + 28, 128), 29, fill=CREAM + (235,)); d.text((W/2 - w/2, 77), s, font=f, fill=INK)
    # pair counter, so people know there's more
    c = f"{i + 1}/{len(spec['pairs'])}"; fc = F(30); cw = d.textlength(c, font=fc)
    d.rounded_rectangle((W - 60 - cw - 36, 70, W - 60, 128), 29, fill=(0, 0, 0, 120)); d.text((W - 60 - cw - 18, 77), c, font=fc, fill=WHITE)
    if last and spec.get("keyword"):                                         # ending: small pill, video stays visible
        f1 = F(40); t1 = f"COMMENT {spec['keyword']}"; f2 = F(30, "Medium"); t2 = "  ·  free guide"
        w1 = d.textlength(t1, font=f1) + 40; w2 = d.textlength(t2, font=f2); ww = w1 + w2 + 36; x0 = W/2 - ww/2; y = H - 120
        d.rounded_rectangle((x0, y, x0 + ww, y + 76), 38, fill=CREAM + (238,))
        d.rounded_rectangle((x0 + 8, y + 8, x0 + 8 + w1, y + 68), 30, fill=CORAL); d.text((x0 + 28, y + 12), t1, font=f1, fill=INK)
        d.text((x0 + 8 + w1 + 14, y + 20), t2, font=f2, fill=INK)
    return im

def half_input(cd, m, dur, n):
    """ffmpeg input args + filter for one half (1080x960)."""
    src = cd + m["media"]
    if m["media"].lower().endswith(IMG):
        N = max(1, int(round(dur * FPS)))
        return (["-loop", "1", "-t", f"{dur:.3f}", "-i", src],
                f"[{n}:v]scale=2160:1920:force_original_aspect_ratio=increase,crop=2160:1920,zoompan=z='1+0.08*on/{N}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={N}:s={W}x{HALF}:fps={FPS},setsar=1,trim=duration={dur:.3f},setpts=PTS-STARTPTS[h{n}]")
    return (["-stream_loop", "-1", "-ss", str(m.get("t", 0)), "-i", src],
            f"[{n}:v]scale={W}:{HALF}:force_original_aspect_ratio=increase,crop={W}:{HALF},fps={FPS},setsar=1,trim=duration={dur:.3f},setpts=PTS-STARTPTS[h{n}]")

def render(spec, stills=False):
    cd = os.path.join(HERE, spec.get("clipdir", "air/")); out = os.path.join(HERE, spec.get("outdir", "out/")); os.makedirs(out, exist_ok=True)
    wd = os.path.join(HERE, "work", spec["slug"]) + "/"; os.makedirs(wd, exist_ok=True)
    media = [p[k]["media"] for p in spec["pairs"] for k in ("top", "bottom")]
    assert len(media) == len(set(media)), "a clip or photo is used twice"
    hold = spec.get("hold", 2.8); n = len(spec["pairs"]); parts = []
    for i, p in enumerate(spec["pairs"]):
        last = i == n - 1; dur = hold + (2.0 if last else 0)
        ov = overlay(spec, i, last); ov.save(wd + f"ov{i}.png")
        a1, f1 = half_input(cd, p["top"], dur, 0); a2, f2 = half_input(cd, p["bottom"], dur, 1)
        flt = f"{f1};{f2};[h0][h1]vstack=inputs=2[b];[b][2:v]overlay=0:0,eq=saturation=1.12:contrast=1.03[v]"
        seg = wd + f"seg{i}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a1, *a2, "-i", wd + f"ov{i}.png", "-filter_complex", flt, "-map", "[v]",
                        "-t", f"{dur:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", seg + ".tmp.mp4"], check=True)
        os.replace(seg + ".tmp.mp4", seg); parts.append(seg)
    if stills:
        ims = []
        for s in parts:
            png = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", "1.0", "-i", s, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            import io; ims.append(Image.open(io.BytesIO(png)).convert("RGB").resize((300, 533)))
        sheet = Image.new("RGB", (310 * len(ims), 533), "white")
        for i, im in enumerate(ims): sheet.paste(im, (i * 310, 0))
        sheet.save(wd + "sheet.jpg", quality=85); return wd + "sheet.jpg"
    open(wd + "list.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
    END = hold * n + 2.0; music = os.path.join(HERE, "music", spec.get("music", "m_tokyostroll.mp3"))
    dst = out + spec["slug"] + ".mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", wd + "list.txt", "-stream_loop", "-1", "-i", music,
                    "-filter_complex", f"[1:a]volume=0.55,afade=t=in:d=0.3,afade=t=out:st={END - 1.5}:d=1.5[a]", "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-t", f"{END:.2f}", "-movflags", "+faststart", dst + ".tmp.mp4"], check=True)
    os.replace(dst + ".tmp.mp4", dst)
    # cover = first pair's frame (the conflict is the hook)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.0", "-i", parts[0], "-frames:v", "1", "-q:v", "3", out + spec["slug"] + ".jpg"], check=True)
    return dst

if __name__ == "__main__":
    print(render(json.load(open(sys.argv[1])), stills="--stills" in sys.argv))
