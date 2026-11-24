"""Japan by Station Reel maker. One JSON spec in, one finished Reel + cover out.

python3 reelkit.py spec.json [--stills]

Spec:
{
 "slug": "kansai-airport-which-train", "keyword": "AIRPORT", "music": "m_tokyostroll.mp3",
 "clipdir": "air/", "outdir": "out/",
 "hook": {"tag": "KANSAI AIRPORT TO OSAKA", "lines": ["Which train", "do you take?"]},
 "cta_sub": "every fare & time, in one guide",
 "cover": {"title": "Kansai Airport|to Osaka: which train?", "category": "GETTING THERE", "color": "sky", "clip": "v_namba.mp4", "t": 3},
 "scenes": [
   {"id": "hook", "clip": ["v_hook.mp4", 4.0], "clauses": [["spoken text", "on-screen text"], ...]},
   {"id": "a", "clip": ["file.mp4", 0.0], "card": {"color": "coral", "kicker": "..", "title": "..", "big": "..", "small": ".."}, "clauses": [...]},
   ...
   {"id": "cta", "clip": ["file.mp4", 0.0], "clauses": [...]}
 ]
}
Rules baked in: every clip used once, male voice D (am_puck 0.6 + am_michael 0.4), speed 1.05, outlined
phrase subtitles with the spoken word in yellow, small cards in the site palette."""
import json, re, os, sys, io, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
import os as _os
FD = "/usr/share/fonts/truetype/google-fonts/" if _os.path.exists("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf") else _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "fonts") + "/"
def F(s, w="Bold"): return ImageFont.truetype(FD + f"Poppins-{ {'SemiBold':'Bold','ExtraBold':'Bold'}.get(w, w) }.ttf", s)
INK = (59, 48, 96); CREAM = (255, 250, 243); WHITE = (255, 255, 255); STROKE = (40, 28, 70)
COL = {"coral": (255, 125, 94), "mint": (51, 195, 161), "sky": (90, 174, 255), "sun": (255, 194, 61), "lilac": (168, 139, 255), "pink": (255, 141, 182)}

def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0, min(1, x)); c = 1.6; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def al(c, a): return tuple(c[:3]) + (int(255 * max(0, min(1, a))),)
def rr(d, box, r, fill): d.rounded_rectangle(box, radius=r, fill=fill)
def ctext(d, y, t, f, fill): d.text(((W - f.getlength(t)) / 2, y), t, font=f, fill=fill)
def otext(d, xy, t, f, fill, sw=6): d.text(xy, t, font=f, fill=fill, stroke_width=sw, stroke_fill=STROKE + (fill[3],))
def deep(c): return (214, 150, 0) if c == COL["sun"] else c

# ---------------- voice ----------------
def voice(spec, wd):
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(HERE, "tts/kokoro.onnx"), os.path.join(HERE, "tts/voices-v1.0.bin"))
    v = 0.6 * k.get_voice_style("am_puck") + 0.4 * k.get_voice_style("am_michael")   # Ling 24 Nov: voice D (brighter)
    sr = 24000
    def trim(a, th=0.008):
        i = np.where(np.abs(a) > th)[0]; return a[max(0, i[0] - 360): i[-1] + 900]
    def syl(w):
        w = re.sub(r"[^a-z0-9¥]", "", w.lower()) or "x"
        return 3 if re.match(r"^[¥\d]", w) else max(1, len(re.findall(r"[aeiouy]+", w)))
    # Ling 24 Nov: tone. Speak whole SENTENCES in one go (natural intonation), not clause by clause
    # (that made every fragment restart its pitch: choppy, robotic). Clause timing for subtitles is
    # then split inside the sentence by syllables.
    words, scenes, clauses = [], [], []; ch = [np.zeros(int(0.2 * sr), np.float32)]; t = 0.2
    for sc in spec["scenes"]:
        s0 = t; cl = sc["clauses"]; i = 0
        while i < len(cl):
            j = i
            while j < len(cl) - 1 and cl[j][0].rstrip()[-1:] not in ".?!": j += 1
            grp = cl[i:j + 1]
            a, sr = k.create(" ".join(x[0].strip() for x in grp), voice=v, speed=spec.get("speed", 1.05), lang="en-us")
            a = trim(a.astype(np.float32)); d = len(a) / sr
            sw = [sum(syl(w) for w in x[0].split()) + 0.6 for x in grp]; tot = sum(sw); c0 = t
            for (spoken, shown), x in zip(grp, sw):
                cd_ = d * x / tot
                ws = shown.split(); wt = [syl(w) + 0.4 for w in ws]; wtot = sum(wt); c = c0 + 0.03
                for w, y in zip(ws, wt):
                    dd = (cd_ - 0.06) * y / wtot; words.append(dict(w=w, s=round(c, 3), e=round(c + dd, 3))); c += dd
                clauses.append(dict(text=shown, s=round(c0, 3), e=round(c0 + cd_, 3))); c0 += cd_
            g = 0.3 if j == len(cl) - 1 else 0.2
            ch += [a, np.zeros(int(g * sr), np.float32)]; t += d + g; i = j + 1
        scenes.append(dict(id=sc["id"], start=round(s0, 3), end=round(t, 3)))
    sf.write(wd + "voice_raw.wav", np.concatenate(ch), sr)
    subprocess.run(f"ffmpeg -y -loglevel error -i {wd}voice_raw.wav -af 'highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,loudnorm=I=-15:TP=-1.5,aresample=44100' -ac 2 {wd}voice.wav", shell=True, check=True)
    tj = dict(scenes=scenes, words=words, clauses=clauses, end=round(t, 3))
    json.dump(tj, open(wd + "timing.json", "w"), indent=1); return tj

# ---------------- render ----------------
# ---- sound effects (Ling, 24 Nov: key words get a sound + visual hit). All synthesised here: no licensed audio.
def _sfx_track(path, events, END, sr=44100):
    n = int((END + 1.5) * sr); a = np.zeros(n, dtype=np.float32); rng = np.random.default_rng(7)
    def put(t, x):
        i = int(t * sr); j = min(n, i + len(x))
        if 0 <= i < n: a[i:j] += x[:j - i]
    for t, k in events:
        if k == "impact":      # hook: low thump + short noise burst
            tt = np.arange(int(.45 * sr)) / sr
            x = .55 * np.sin(2 * np.pi * (90 - 50 * tt / .45) * tt) * np.exp(-tt * 9)
            x[:int(.06 * sr)] += .25 * rng.standard_normal(int(.06 * sr)) * np.exp(-np.arange(int(.06 * sr)) / (.012 * sr))
            put(t, x)
        elif k == "whoosh":    # card in: soft filtered-noise swoosh
            L = int(.32 * sr); env = np.sin(np.linspace(0, np.pi, L)) ** 2
            nz = rng.standard_normal(L + 64); x = np.convolve(nz, np.ones(24) / 24, "same")[:L]
            put(t - .18, .16 * x * env / max(1e-6, np.abs(x).max()))
        elif k == "pop":       # card lands
            tt = np.arange(int(.09 * sr)) / sr
            put(t, .30 * np.sin(2 * np.pi * (520 + 900 * tt / .09) * tt) * np.exp(-tt * 38))
        elif k == "tick":      # emphasised word
            tt = np.arange(int(.05 * sr)) / sr
            put(t, .12 * np.sin(2 * np.pi * 1850 * tt) * np.exp(-tt * 70))
        elif k == "ding":      # ending
            tt = np.arange(int(.8 * sr)) / sr
            put(t, (.20 * np.sin(2 * np.pi * 1318 * tt) + .10 * np.sin(2 * np.pi * 1976 * tt)) * np.exp(-tt * 5))
    a = np.clip(a, -0.95, 0.95); sf.write(path, np.stack([a, a], 1), sr)

def _is_emph(w, extra):
    k = re.sub(r"[^\w¥%#'-]", "", w)
    if not k: return False
    if k.lower() in extra: return True
    return bool(re.search(r"\d|¥|%", k)) or (len(k) >= 3 and k.isupper() and k.isalpha())

def render(spec, tj, wd, stills=False):
    cd = spec["clipdir"]; END = round(tj["end"] + 1.0, 2)
    S = {s["id"]: s for s in spec["scenes"]}; order = [s["id"] for s in spec["scenes"]]
    B = {}
    for i, x in enumerate(tj["scenes"]):
        a = 0 if i == 0 else x["start"] - 0.1
        b = END if i == len(order) - 1 else tj["scenes"][i + 1]["start"] - 0.1
        B[x["id"]] = (round(a, 3), round(b, 3))
    MAXSHOT = 4.0   # Ling, 23 Nov: a new shot at least every 4 s
    IMG = (".jpg", ".jpeg", ".png", ".webp")
    segs = []       # (file, start, duration)
    for i in order:
        d = B[i][1] - B[i][0]
        clips = S[i].get("clips") or [S[i]["clip"]]
        nseg = max(1, -(-d // MAXSHOT))
        nseg = int(max(nseg, 1))
        assert len(clips) >= nseg, f"scene '{i}' lasts {d:.1f}s: it needs {nseg} different clips/photos in \"clips\" (max {MAXSHOT:.0f}s per shot), it has {len(clips)}"
        use = clips[:max(nseg, min(len(clips), int(-(-d // 2.5))))]   # use extra clips if given, aiming ~2.5-4 s per shot
        for c in use:
            segs.append((c[0], c[1] if len(c) > 1 else 0.0, d / len(use)))
    files = [x[0] for x in segs]
    assert len(files) == len(set(files)), "a clip or photo is used twice"
    assert all(x[2] <= MAXSHOT + 0.01 for x in segs)
    inputs, flt = [], []
    for n, (f, st, d) in enumerate(segs):
        if f.lower().endswith(IMG):    # still photo: slow push-in (Ken Burns)
            N = max(1, int(round(d * 30)))
            inputs += ["-i", cd + f]
            flt.append(f"[{n}:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='1+0.10*on/{N}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={N}:s=1080x1920:fps=30,setsar=1,trim=duration={d:.3f},setpts=PTS-STARTPTS[v{n}]")
            continue
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", cd + f],
                                   capture_output=True, text=True).stdout.strip() or 0)
        avail = max(0.5, dur - st)
        k = 1.0 if avail >= d else min(d / avail, 1.6)       # short clip: slow it down a little, then loop if still short
        inputs += ["-stream_loop", "-1", "-ss", str(st), "-i", cd + f]
        flt.append(f"[{n}:v]setpts={k:.4f}*(PTS-STARTPTS),scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,trim=duration={d:.3f},setpts=PTS-STARTPTS[v{n}]")
    flt.append("".join(f"[v{n}]" for n in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0,eq=saturation=1.12:contrast=1.03[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(flt), "-map", "[out]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", wd + "base.mp4"], check=True)

    EMPH = {x.lower() for x in spec.get("emph", [])}
    ev = [(0.02, "impact")]
    for k in order[1:]:
        if S[k].get("card"): ev += [(B[k][0], "whoosh"), (B[k][0] + .05, "pop")]
    ev.append((B[order[-1]][0] + .2, "ding"))
    last = -9
    for wd_ in tj["words"]:
        if _is_emph(wd_["w"] if "w" in wd_ else wd_.get("text", ""), EMPH) and wd_["s"] - last > 1.5 and wd_["s"] > 1.0:
            ev.append((wd_["s"], "tick")); last = wd_["s"]
    _sfx_track(wd + "sfx.wav", ev, END)
    def brand(d):
        f = F(30); s = "Japan by Station"; w = f.getlength(s)
        rr(d, (W/2 - w/2 - 28, 120, W/2 + w/2 + 28, 178), 29, al(CREAM, .92)); d.text((W/2 - w/2, 127), s, font=f, fill=INK)
    def card(d, lt, c):
        color = COL[c["color"]]; big = c.get("big"); small = c.get("small")
        s = back(lt / .45); a = ease(lt / .25)
        if a <= 0: return
        cw = 640; chh = 128 + (110 if big else 0) + (56 if small else 0)
        x0 = W/2 - cw/2; y0 = 300 + (1 - s) * 50
        rr(d, (x0 + 6, y0 + 10, x0 + cw + 6, y0 + chh + 10), 36, al((40, 30, 70), .16 * a))
        rr(d, (x0, y0, x0 + cw, y0 + chh), 36, al(CREAM, .97 * a)); rr(d, (x0, y0, x0 + cw, y0 + 16), 8, al(color, a))
        fk = F(24); kw = fk.getlength(c["kicker"]) + 36
        rr(d, (W/2 - kw/2, y0 + 34, W/2 + kw/2, y0 + 74), 20, al(color, a)); ctext(d, y0 + 40, c["kicker"], fk, al(INK, a))
        ft = F(38);
        while ft.getlength(c["title"]) > cw - 40: ft = F(ft.size - 2)
        ctext(d, y0 + 84, c["title"], ft, al(INK, a)); yy = y0 + 134
        if big: ctext(d, yy, big, F(72), al(deep(color), a)); yy += 106
        if small: ctext(d, yy + 4, small, F(28, "Medium"), al((124, 115, 152), a))
    def caption(d, t):
        for c in tj["clauses"]:
            if c["s"] - 0.05 <= t < c["e"] + 0.12:
                a = ease((t - c["s"] + .05) / .16); f = F(58)
                words = c["text"].split(); ws = [w for w in tj["words"] if c["s"] - 0.01 <= w["s"] <= c["e"] + 0.01]
                if len(ws) != len(words): ws = [None] * len(words)
                lines, cur, cw = [], [], 0; sp = f.getlength(" ")
                for i, w in enumerate(words):
                    wl = f.getlength(w)
                    if cur and cw + sp + wl > 900: lines.append(cur); cur, cw = [], 0
                    cur.append(i); cw += (sp if len(cur) > 1 else 0) + wl
                lines.append(cur); lh = 78; y0 = 1470 - (lh * len(lines)) / 2 + (1 - a) * 14
                for li, idxs in enumerate(lines):
                    tw = sum(f.getlength(words[i]) for i in idxs) + sp * (len(idxs) - 1); x = (W - tw) / 2
                    for i in idxs:
                        w = words[i]; wt = ws[i]; wl = f.getlength(w)
                        em = _is_emph(w, EMPH)
                        if wt is not None and wt["s"] - 0.02 <= t < wt["e"] + 0.04:
                            p = (t - wt["s"] + 0.02) / max(0.12, wt["e"] - wt["s"]); lift = (-26 if em else -14) * (1 - abs(1 - min(2, p * 6)))
                            otext(d, (x, y0 + li * lh + lift), w, f, al(COL["coral"] if em else COL["sun"], a), sw=8 if em else 7)
                        else: otext(d, (x, y0 + li * lh), w, f, al(COL["sun"] if em else WHITE, a))
                        x += wl + sp
                return
    def frame(t):
        s = next((k for k in order if B[k][0] <= t < B[k][1]), order[-1]); lt = t - B[s][0]
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        edge = s == order[0]
        d.rectangle((0, 0, W, H), fill=(30, 22, 50, 70 if edge else 30)); brand(d)
        if s == order[0]:
            a = 1.0; hk = spec["hook"]   # Ling 24 Nov: hook on screen from frame 1 (strong hook + FB thumbnail)
            fk = F(30); kw = fk.getlength(hk["tag"]) + 44
            rr(d, (W/2 - kw/2, 420, W/2 + kw/2, 472), 26, al(COL["sun"], a)); ctext(d, 427, hk["tag"], fk, al(INK, a))
            f = F(140)
            while max(f.getlength(l) for l in hk["lines"]) > 1000: f = F(f.size - 4)
            for i, l in enumerate(hk["lines"]):
                r = back((lt + .45 - i * .12) / .45) if lt < 1.2 else 1.0
                otext(d, ((W - f.getlength(l)) / 2, 500 + i * int(f.size * 1.12) + (1 - r) * 40), l, f, al(WHITE, min(1, r * 1.2)), sw=10)
        elif s == order[-1]:
            # Ling 24 Nov: no big box over the footage at the end. One small pill at the bottom, video stays visible.
            a = ease(lt / .3); K = spec["keyword"]
            f1 = F(40); t1 = f"DM {K}"; f2 = F(30, "Medium"); t2 = "  ·  link in bio"
            w1 = f1.getlength(t1) + 40; w2 = f2.getlength(t2); w = w1 + w2 + 36; x0 = W/2 - w/2; y = 1690 + (1 - a) * 24
            rr(d, (x0, y, x0 + w, y + 76), 38, al(CREAM, .93 * a))
            rr(d, (x0 + 8, y + 8, x0 + 8 + w1, y + 68), 30, al(COL["coral"], a)); d.text((x0 + 28, y + 12), t1, font=f1, fill=al(INK, a))
            d.text((x0 + 8 + w1 + 14, y + 20), t2, font=f2, fill=al(INK, a))
        elif S[s].get("card"): card(d, lt, S[s]["card"])
        if s != order[0] and lt < 0.12: d.rectangle((0, 0, W, H), fill=(255, 255, 255, int(70 * (1 - lt / 0.12))))   # quick flash on every new part
        caption(d, t)
        fade = min(1, (END - t) / .35)   # Ling 24 Nov: no fade-in, so the first frame (FB thumbnail) is never black
        if fade < 1: d.rectangle((0, 0, W, H), fill=(0, 0, 0, int(255 * (1 - max(0, fade)))))
        return ov
    if stills:
        outs = []
        for x in tj["scenes"]:
            tt = round((x["start"] + x["end"]) / 2, 2)
            bg = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(tt), "-i", wd + "base.mp4", "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            im = Image.open(io.BytesIO(bg)).convert("RGBA"); im.alpha_composite(frame(tt)); outs.append(im.convert("RGB").resize((300, 533)))
        sheet = Image.new("RGB", (310 * len(outs), 533), "white")
        for i, im in enumerate(outs): sheet.paste(im, (i * 310, 0))
        sheet.save(wd + "sheet.jpg", quality=85); return wd + "sheet.jpg"
    out = os.path.join(spec.get("outdir", "out/"), spec["slug"] + ".mp4"); os.makedirs(os.path.dirname(out), exist_ok=True)
    music = os.path.join(HERE, "music", spec.get("music", "m_tokyostroll.mp3"))
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-i", wd + "base.mp4",
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wd + "voice.wav", "-stream_loop", "-1", "-i", music, "-i", wd + "sfx.wav",
        "-filter_complex",
        f"[0:v][1:v]overlay=0:0:format=auto[v];[3:a]volume=0.32,afade=t=in:d=0.6,afade=t=out:st={END-1.4}:d=1.4[m];"
        f"[2:a]asplit=2[vo][sc];[m][sc]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=350[md];[4:a]volume=0.9[fx];[vo][md][fx]amix=inputs=3:duration=first:normalize=0,apad[a]",
        "-map", "[v]", "-map", "[a]", "-t", str(END), "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-maxrate", "8M", "-bufsize", "16M",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    for i in range(int(END * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    if p.returncode != 0: raise SystemExit("ffmpeg failed")
    os.replace(out + ".tmp.mp4", out)
    # cover in the shared style
    sys.path.insert(0, HERE); import cover
    cv = spec["cover"]; cover.make(cd + cv["clip"], cv.get("t", 2), cv["title"], cv["category"], cv["color"], spec["keyword"], out[:-4] + ".jpg")
    return out

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1])); wd = os.path.join("work", spec["slug"]) + "/"; os.makedirs(wd, exist_ok=True)
    tj = voice(spec, wd)
    print(render(spec, tj, wd, stills="--stills" in sys.argv), tj["end"])
