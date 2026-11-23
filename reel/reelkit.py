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
Rules baked in: every clip used once, male voice (am_michael+am_fenrir), speed 1.0, outlined
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
    v = 0.65 * k.get_voice_style("am_michael") + 0.35 * k.get_voice_style("am_fenrir")
    sr = 24000
    def trim(a, th=0.008):
        i = np.where(np.abs(a) > th)[0]; return a[max(0, i[0] - 360): i[-1] + 900]
    def syl(w):
        w = re.sub(r"[^a-z0-9¥]", "", w.lower()) or "x"
        return 3 if re.match(r"^[¥\d]", w) else max(1, len(re.findall(r"[aeiouy]+", w)))
    words, scenes, clauses = [], [], []; ch = [np.zeros(int(0.2 * sr), np.float32)]; t = 0.2
    for sc in spec["scenes"]:
        s0 = t
        for ci, (spoken, shown) in enumerate(sc["clauses"]):
            a, sr = k.create(spoken, voice=v, speed=spec.get("speed", 1.0), lang="en-us"); a = trim(a.astype(np.float32)); d = len(a) / sr
            ws = shown.split(); wt = [syl(w) + 0.4 for w in ws]; tot = sum(wt); c = t + 0.05
            for w, x in zip(ws, wt):
                dd = (d - 0.12) * x / tot; words.append(dict(w=w, s=round(c, 3), e=round(c + dd, 3))); c += dd
            clauses.append(dict(text=shown, s=round(t, 3), e=round(t + d, 3)))
            last = ci == len(sc["clauses"]) - 1
            g = 0.3 if last else (0.16 if spoken.rstrip()[-1] in ".?!" else 0.07)
            ch += [a, np.zeros(int(g * sr), np.float32)]; t += d + g
        scenes.append(dict(id=sc["id"], start=round(s0, 3), end=round(t, 3)))
    sf.write(wd + "voice_raw.wav", np.concatenate(ch), sr)
    subprocess.run(f"ffmpeg -y -loglevel error -i {wd}voice_raw.wav -af 'highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,loudnorm=I=-15:TP=-1.5,aresample=44100' -ac 2 {wd}voice.wav", shell=True, check=True)
    tj = dict(scenes=scenes, words=words, clauses=clauses, end=round(t, 3))
    json.dump(tj, open(wd + "timing.json", "w"), indent=1); return tj

# ---------------- render ----------------
def render(spec, tj, wd, stills=False):
    cd = spec["clipdir"]; END = round(tj["end"] + 1.0, 2)
    S = {s["id"]: s for s in spec["scenes"]}; order = [s["id"] for s in spec["scenes"]]
    B = {}
    for i, x in enumerate(tj["scenes"]):
        a = 0 if i == 0 else x["start"] - 0.1
        b = END if i == len(order) - 1 else tj["scenes"][i + 1]["start"] - 0.1
        B[x["id"]] = (round(a, 3), round(b, 3))
    files = [S[i]["clip"][0] for i in order]
    assert len(files) == len(set(files)), "a clip is used twice"
    inputs, flt = [], []
    for n, i in enumerate(order):
        f, st = S[i]["clip"]; d = B[i][1] - B[i][0]
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", cd + f],
                                   capture_output=True, text=True).stdout.strip() or 0)
        avail = max(0.5, dur - st)
        k = 1.0 if avail >= d else min(d / avail, 1.6)       # short clip: slow it down a little, then loop if still short
        inputs += ["-stream_loop", "-1", "-ss", str(st), "-i", cd + f]
        flt.append(f"[{n}:v]setpts={k:.4f}*(PTS-STARTPTS),scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,trim=duration={d:.3f},setpts=PTS-STARTPTS[v{n}]")
    flt.append("".join(f"[v{n}]" for n in range(len(order))) + f"concat=n={len(order)}:v=1:a=0,eq=saturation=1.12:contrast=1.03[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(flt), "-map", "[out]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", wd + "base.mp4"], check=True)

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
                        if wt is not None and wt["s"] - 0.02 <= t < wt["e"] + 0.04:
                            p = (t - wt["s"] + 0.02) / max(0.12, wt["e"] - wt["s"]); lift = -14 * (1 - abs(1 - min(2, p * 6)))
                            otext(d, (x, y0 + li * lh + lift), w, f, al(COL["sun"], a), sw=7)
                        else: otext(d, (x, y0 + li * lh), w, f, al(WHITE, a))
                        x += wl + sp
                return
    def frame(t):
        s = next((k for k in order if B[k][0] <= t < B[k][1]), order[-1]); lt = t - B[s][0]
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        edge = s in (order[0], order[-1])
        d.rectangle((0, 0, W, H), fill=(30, 22, 50, 70 if edge else 30)); brand(d)
        if s == order[0]:
            a = ease(lt / .35); hk = spec["hook"]
            fk = F(30); kw = fk.getlength(hk["tag"]) + 44
            rr(d, (W/2 - kw/2, 520, W/2 + kw/2, 572), 26, al(COL["sun"], a)); ctext(d, 527, hk["tag"], fk, al(INK, a))
            f = F(96)
            while max(f.getlength(l) for l in hk["lines"]) > 960: f = F(f.size - 4)
            for i, l in enumerate(hk["lines"]):
                r = back((lt - .15 - i * .12) / .45)
                otext(d, ((W - f.getlength(l)) / 2, 600 + i * int(f.size * 1.2) + (1 - r) * 40), l, f, al(WHITE, min(1, r * 1.2)), sw=7)
        elif s == order[-1]:
            a = ease(lt / .3); K = spec["keyword"]
            rr(d, (150, 450 + (1 - a) * 30, W - 150, 850 + (1 - a) * 30), 46, al(CREAM, .95 * a))
            ctext(d, 490 + (1 - a) * 30, "Comment", F(56), al(INK, a))
            r = back((lt - .2) / .45); fw = F(92)
            while fw.getlength(K) > 640: fw = F(fw.size - 4)
            w = fw.getlength(K) + 90; y = 570 + (1 - r) * 40
            rr(d, (W/2 - w/2, y, W/2 + w/2, y + 130), 65, al(COL["coral"], min(1, r))); ctext(d, y + 10, K, fw, al(INK, min(1, r)))
            b = ease((lt - .6) / .35)
            ctext(d, 730, spec.get("cta_sub", "the full guide, free"), F(32, "Medium"), al(INK, b))
            ctext(d, 778, "japanbystation.com", F(32), al(COL["coral"], b))
        elif S[s].get("card"): card(d, lt, S[s]["card"])
        caption(d, t)
        fade = min(1, t / .25, (END - t) / .35)
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
        "-i", wd + "voice.wav", "-stream_loop", "-1", "-i", music,
        "-filter_complex",
        f"[0:v][1:v]overlay=0:0:format=auto[v];[3:a]volume=0.32,afade=t=in:d=0.6,afade=t=out:st={END-1.4}:d=1.4[m];"
        f"[2:a]asplit=2[vo][sc];[m][sc]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=350[md];[vo][md]amix=inputs=2:duration=first:normalize=0,apad[a]",
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
