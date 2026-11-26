"""ROUTE CARDS: "4 night walks, swipe for the routes" (26 Nov; Ling liked a Tokyo carousel of night-walk route
cards: 1.7K likes, 4.2K sends). One cover + one card per route (numbered stops with photos, a schematic route,
walk time, best for) + an ending card. Output: 4:5 slides (carousel / Pinterest / FB) AND a 9:16 Reel.

python3 routecard.py specs/<slug>.json [--stills]

The route drawing is a SCHEMATIC (like a metro diagram), never a fake street map: we don't draw streets we
haven't mapped. Every stop, note, time and "best for" must come from our guide pages (PLAYBOOK 3 ROUTE CARDS).

Spec:
{"slug": "tokyo-night-walks", "format": "routes", "keyword": "TOKYO", "music": "m_tokyostroll.mp3",
 "clipdir": "air/", "outdir": "out/",
 "cover": {"media": "tower.jpg", "lines": ["TOKYO AFTER DARK", "4 NIGHT WALKS"], "small": "SAVE THESE ROUTES"},
 "routes": [{"name": ["ASAKUSA", "BY THE RIVER"], "sub": "Lanterns, river, Skytree", "color": "coral",
             "start": "Asakusa Stn", "end": "Skytree",
             "stops": [{"name": "Kaminarimon", "note": "Start under the big lantern", "media": "a1.jpg"}, ...  (3–4 stops)],
             "time": "45–60 MIN", "best": "Temples, river views, photos"}, ...],
 "ending": {"lines": ["Comment TOKYO", "for our free guides to all 4 walks"]},
 "caption": "..."}"""
import json, os, sys, subprocess, io, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
CW, CH = 1080, 1350           # carousel card 4:5
RW, RH, FPS = 1080, 1920, 30  # reel
FD = os.path.join(HERE, "..", "fonts") + "/"
def F(s, w="Bold"): return ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)
NAVY = (12, 18, 42); PANEL = (20, 28, 60); WHITE = (255, 255, 255); MUTED = (170, 178, 205); CREAM = (255, 250, 243); INK = (22, 30, 58)
COL = {"coral": (255, 107, 84), "mint": (51, 205, 170), "sun": (255, 196, 52), "lilac": (178, 140, 255), "sky": (90, 174, 255), "pink": (255, 120, 170)}

def wrap(d, text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: out.append(cur)
            cur = w
    if cur: out.append(cur)
    return out

def photo(path, w, h):
    im = Image.open(path).convert("RGB"); r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x = (im.width - w) // 2; y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

def rounded(im, r):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width, im.height), r, fill=255)
    o = Image.new("RGBA", im.size); o.paste(im, (0, 0), m); return o

def glow_line(base, pts, color, width=7):
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for a, b in zip(pts, pts[1:]):                      # dotted path
        n = max(2, int(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** .5 / 18))
        for k in range(n):
            t0, t1 = k / n, (k + .55) / n
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=color + (255,), width=width)
    g = lay.filter(ImageFilter.GaussianBlur(9)); base.alpha_composite(g); base.alpha_composite(g); base.alpha_composite(lay)

def route_card(spec, ri):
    """v2 (Ling, 26 Nov 15:31: "use a real map with the points connected, more colour"): the whole card is a real
    dark map (maprender.py, OpenStreetMap data) with the walking route in neon; the text column sits on the left."""
    sys.path.insert(0, HERE); from maprender import geocode, render_map
    r = spec["routes"][ri]; c = COL[r.get("color", "coral")]; cd = os.path.join(HERE, spec.get("clipdir", "air/"))
    stops = r["stops"][:4]; city = spec.get("city", "")
    ll = [tuple(s["ll"]) if s.get("ll") else geocode(s.get("q") or f"{s['name']}, {city}") for s in stops]
    im, pins, meters = render_map(ll, CW, CH, color=c, box=(600, 150, CW - 30, CH - 250), max_scale=7000)
    d = ImageDraw.Draw(im)
    # left text column: dark, fading into the map
    fade = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); fd = ImageDraw.Draw(fade)
    for x in range(0, 700):
        a = 238 if x < 560 else int(238 * (700 - x) / 140); fd.line([(x, 0), (x, CH)], fill=NAVY + (a,))
    for y in range(CH - 240, CH):
        fd.line([(0, y), (CW, y)], fill=NAVY + (int(230 * (y - (CH - 240)) / 240),))
    im.alpha_composite(fade); d = ImageDraw.Draw(im)
    # pins + labels on the map (labels avoid each other and the pins)
    placed = [(x - 34, y - 34, x + 34, y + 34) for x, y in pins]
    for k, ((x, y), st) in enumerate(zip(pins, stops)):
        gl = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse((x - 40, y - 40, x + 40, y + 40), fill=c + (190,))
        im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(12))); d = ImageDraw.Draw(im)
        d.ellipse((x - 30, y - 30, x + 30, y + 30), fill=c, outline=WHITE, width=4); d.text((x, y), str(k + 1), font=F(32), fill=WHITE, anchor="mm")
        lab = st["name"]; fl = F(26)
        while d.textlength(lab, font=fl) > 300 and fl.size > 18: fl = F(fl.size - 1)
        tw = d.textlength(lab, font=fl); bw, bh = tw + 26, 46
        cands = [(x + 40, y - 23), (x - 40 - bw, y - 23), (x - bw / 2, y - 40 - bh), (x - bw / 2, y + 40), (x + 40, y - 23 - 56), (x + 40, y - 23 + 56), (x - 40 - bw, y - 23 - 56), (x - 40 - bw, y - 23 + 56)]
        def free(r):
            if r[0] < 560 or r[2] > CW - 8 or r[1] < 8 or r[3] > CH - 230: return False
            return all(r[2] < q[0] or r[0] > q[2] or r[3] < q[1] or r[1] > q[3] for q in placed)
        pick = next((cc for cc in cands if free((cc[0], cc[1], cc[0] + bw, cc[1] + bh))), cands[0])
        lx, ly = pick; placed.append((lx - 4, ly - 4, lx + bw + 4, ly + bh + 4))
        d.rounded_rectangle((lx, ly, lx + bw, ly + bh), 12, fill=(8, 12, 30, 235), outline=c, width=3)
        d.text((lx + 13, ly + 6), lab, font=fl, fill=WHITE)
    # header
    lab = f"ROUTE {ri + 1}"; f = F(34); w = d.textlength(lab, font=f) + 56
    d.rounded_rectangle((48, 44, 48 + w, 104), 30, fill=c); d.text((76, 50), lab, font=f, fill=NAVY)
    y = 124
    for k, line in enumerate(r["name"][:2]):
        f = F(92)
        while d.textlength(line, font=f) > 500 and f.size > 46: f = F(f.size - 4)
        if k == 1:
            gl = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); ImageDraw.Draw(gl).text((48, y), line, font=f, fill=c + (255,))
            im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10))); d = ImageDraw.Draw(im)
        d.text((48, y), line, font=f, fill=WHITE if k == 0 else c); y += int(f.size * 1.05)
    y += 18; d.text((50, y), r.get("sub", ""), font=F(30, "Medium"), fill=(205, 212, 235)); y += 52
    d.line([(50, y), (520, y)], fill=c, width=4); y += 26
    # stops (left)
    rowh = (CH - 260 - y) // len(stops)
    for k, s_ in enumerate(stops):
        yy = y + k * rowh; th = min(rowh - 24, 150)
        try: im.alpha_composite(rounded(photo(cd + s_["media"], 200, th), 18), (48, yy))
        except Exception: d.rounded_rectangle((48, yy, 248, yy + th), 18, fill=PANEL)
        d = ImageDraw.Draw(im); d.rounded_rectangle((48, yy, 248, yy + th), 18, outline=c, width=4)
        d.ellipse((30, yy - 16, 82, yy + 36), fill=c, outline=WHITE, width=3); d.text((56, yy + 10), str(k + 1), font=F(30), fill=WHITE, anchor="mm")
        fn = F(36); ty = yy
        for ln in wrap(d, s_["name"], fn, 290)[:2]: d.text((268, ty), ln, font=fn, fill=WHITE); ty += 42
        for ln in wrap(d, s_.get("note", ""), F(25, "Regular"), 290)[:3]: d.text((268, ty + 4), ln, font=F(25, "Regular"), fill=(200, 206, 230)); ty += 31
    # bottom boxes (full width)
    by = CH - 200
    mins = int(math.ceil(meters / 75 / 5.0) * 5) if meters else 0
    tt = r.get("time") or (f"ABOUT {mins} MIN" if mins else ""); tl = r.get("time_label") or ("WALK · MAP ESTIMATE" if not r.get("time") else "APPROX. WALK")
    for bx0, bx1 in ((48, 520), (540, CW - 40)):
        d.rounded_rectangle((bx0, by, bx1, by + 150), 22, fill=(10, 14, 34, 225), outline=c, width=3)
    d.text((78, by + 20), tt, font=fit(d, tt, 58, 420), fill=WHITE); d.text((80, by + 94), tl, font=F(25, "Medium"), fill=c)
    d.text((572, by + 18), "BEST FOR", font=F(34), fill=c)
    for k, ln in enumerate(wrap(d, r.get("best", ""), F(27, "Regular"), CW - 40 - 600)[:2]): d.text((572, by + 64 + k * 34), ln, font=F(27, "Regular"), fill=WHITE)
    d.text((48, CH - 38), "Japan by Station · japanbystation.com", font=F(22, "Medium"), fill=(170, 178, 205))
    return im.convert("RGB")

def fit(d, text, size, maxw, w="Bold"):
    f = F(size, w)
    while d.textlength(text, font=f) > maxw and size > 24: size -= 2; f = F(size, w)
    return f

def pill_lines(d, lines, cx, y, sizes, fills):
    for ln, sz, fl in zip(lines, sizes, fills):
        f = F(sz)
        while d.textlength(ln, font=f) > 900 and f.size > 40: f = F(f.size - 4)
        w = d.textlength(ln, font=f); h = int(f.size * 1.25)
        d.rounded_rectangle((cx - w / 2 - 36, y, cx + w / 2 + 36, y + h + 12), (h + 12) // 2, fill=(5, 8, 18, 235))
        d.text((cx - w / 2, y + 2), ln, font=f, fill=fl); y += h + 30
    return y

def cover_card(spec):
    cv = spec["cover"]; cd = os.path.join(HERE, spec.get("clipdir", "air/"))
    im = photo(cd + cv["media"], CW, CH).convert("RGBA")
    im.alpha_composite(Image.new("RGBA", (CW, CH), (0, 0, 0, 70))); d = ImageDraw.Draw(im)
    lines = cv["lines"] + ([cv["small"]] if cv.get("small") else [])
    sizes = [96, 84, 54][:len(lines)]; fills = [COL["sun"], WHITE, WHITE][:len(lines)]
    pill_lines(d, lines, CW / 2, CH * 0.42, sizes, fills)
    f = F(28); s = "Japan by Station"; w = d.textlength(s, font=f)
    d.rounded_rectangle((CW / 2 - w / 2 - 26, 50, CW / 2 + w / 2 + 26, 104), 27, fill=CREAM + (235,)); d.text((CW / 2 - w / 2, 56), s, font=f, fill=INK)
    return im.convert("RGB")

def end_card(spec):
    cd = os.path.join(HERE, spec.get("clipdir", "air/"))
    im = photo(cd + spec["cover"]["media"], CW, CH).filter(ImageFilter.GaussianBlur(14)).convert("RGBA")
    im.alpha_composite(Image.new("RGBA", (CW, CH), (8, 12, 30, 170))); d = ImageDraw.Draw(im)
    e = spec.get("ending", {}); lines = e.get("lines", [f"Comment {spec.get('keyword', '')}", "for our free guide"])
    y = CH * 0.36
    f1 = F(84); t1 = lines[0]; w1 = d.textlength(t1, font=f1)
    d.rounded_rectangle((CW / 2 - w1 / 2 - 40, y, CW / 2 + w1 / 2 + 40, y + 124), 62, fill=COL["coral"]); d.text((CW / 2 - w1 / 2, y + 10), t1, font=f1, fill=INK)
    y += 170
    for ln in lines[1:]:
        for sub in wrap(d, ln, F(48, "Medium"), 900): d.text(((CW - d.textlength(sub, font=F(48, "Medium"))) / 2, y), sub, font=F(48, "Medium"), fill=WHITE); y += 64
    t = "Save this for your trip  ·  send it to your travel buddy"; f = F(30, "Regular")
    d.text(((CW - d.textlength(t, font=f)) / 2, CH - 160), t, font=f, fill=MUTED)
    return im.convert("RGB")

def render(spec, stills=False):
    out = os.path.join(HERE, spec.get("outdir", "out/")); os.makedirs(out, exist_ok=True)
    wd = os.path.join(HERE, "work", spec["slug"]) + "/"; os.makedirs(wd, exist_ok=True)
    meds = [s["media"] for r in spec["routes"] for s in r["stops"]]
    assert len(meds) == len(set(meds)), "a photo is used twice"
    cards = [cover_card(spec)] + [route_card(spec, i) for i in range(len(spec["routes"]))] + [end_card(spec)]
    cdir = out + spec["slug"] + "-cards/"; os.makedirs(cdir, exist_ok=True)
    for i, c in enumerate(cards): c.save(cdir + f"{i + 1:02d}.jpg", quality=92)
    if stills:
        sheet = Image.new("RGB", (330 * len(cards), 412), "white")
        for i, c in enumerate(cards): sheet.paste(c.resize((320, 400)), (i * 330, 6))
        sheet.save(wd + "sheet.jpg", quality=85); return wd + "sheet.jpg"
    # Reel: each card centred on a blurred copy of itself; cover 2.5 s, routes 4.5 s, ending 3 s
    durs = [2.5] + [4.5] * len(spec["routes"]) + [3.0]; parts = []
    for i, (c, du) in enumerate(zip(cards, durs)):
        bg = c.resize((RW, int(RW * CH / CW))).resize((RW, RH)).filter(ImageFilter.GaussianBlur(30))
        bg = Image.blend(bg, Image.new("RGB", (RW, RH), NAVY), .45); bg.paste(c, (0, (RH - CH) // 2))
        p = wd + f"f{i}.png"; bg.save(p); s = wd + f"s{i}.mp4"
        N = int(du * FPS)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", p, "-vf",
                        f"format=yuv420p,loop=-1:1,trim=duration={du},zoompan=z='1+0.025*on/{N}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={RW}x{RH}:fps={FPS}",
                        "-t", str(du), "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", s + ".tmp.mp4"], check=True)
        os.replace(s + ".tmp.mp4", s); parts.append(s)
    open(wd + "list.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
    END = sum(durs); music = os.path.join(HERE, "music", spec.get("music", "m_tokyostroll.mp3")); dst = out + spec["slug"] + ".mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", wd + "list.txt", "-stream_loop", "-1", "-i", music,
                    "-filter_complex", f"[1:a]volume=0.55,afade=t=in:d=0.3,afade=t=out:st={END - 1.5}:d=1.5[a]", "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-t", f"{END:.2f}", "-movflags", "+faststart", dst + ".tmp.mp4"], check=True)
    os.replace(dst + ".tmp.mp4", dst)
    cards[0].resize((RW, int(RW * CH / CW))).save(out + spec["slug"] + ".jpg", quality=90)
    return dst

if __name__ == "__main__":
    print(render(json.load(open(sys.argv[1])), stills="--stills" in sys.argv))
