"""Japan by Station "Which exit?" cheat sheet v2: a saveable JPEG for a station page (Ling, 25 Nov).
Design: station-sign look. Big yellow exit badges (like Japanese subway exit signs), each row a white card,
line names as coloured chips in the line's official colour, one font family with 3 weights only.
usage: python3 exitcard.py cards/<slug>.json site/exitcards/<slug>.jpg
JSON: {"station": "Asakusa Station", "city": "Tokyo", "subtitle": "...",
       "rows": [{"to": "Kaminarimon Gate", "sub": "Senso-ji", "line": "Ginza Line", "line_color": "#F39700",
                 "exit": "1", "note": "1 min · lift"}], "tips": ["..."], "checked": "25 Nov 2026"}
Every row must come from the guide page or an official station map checked this run (PLAYBOOK 2d)."""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1440
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"
def F(s, w="Bold"): return ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)
NAVY = (22, 30, 58); BG = (240, 242, 247); WHITE = (255, 255, 255); INK = (22, 30, 58); MUTED = (96, 104, 128)
YELLOW = (255, 210, 0); CORAL = (255, 107, 84)

def hexc(h, default=(90, 100, 130)):
    try: h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except Exception: return default

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def make(spec, out):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    # header: navy block, brand pill, big station name, city
    d.rectangle([0, 0, W, 250], fill=NAVY)
    pill = "JAPAN BY STATION"; pw = d.textlength(pill, font=F(24)) + 40
    d.rounded_rectangle([64, 36, 64 + pw, 80], 22, fill=CORAL); d.text((84, 41), pill, font=F(24), fill=WHITE)
    name = spec["station"]; size = 70
    while d.textlength(name, font=F(size)) > W - 128 and size > 50: size -= 2
    d.text((64, 92), name, font=F(size), fill=WHITE)
    d.text((66, 96 + size + 4), spec["city"].upper(), font=F(28, "Medium"), fill=(170, 180, 210))
    # yellow strip
    d.rectangle([0, 250, W, 326], fill=YELLOW)
    d.text((64, 262), "WHICH EXIT?", font=F(40), fill=NAVY)
    if spec.get("subtitle"):
        st = spec["subtitle"]; f = F(24, "Medium")
        d.text((W - 64 - d.textlength(st, font=f), 274), st, font=f, fill=NAVY)
    # rows as white cards
    y = 344; bx = 64; badge = 116; tx = bx + 22 + badge + 28; maxw = W - 64 - 28 - tx
    for r in spec["rows"]:
        tl = wrap(d, r["to"], F(36), maxw)
        h = 22 + len(tl) * 46 + (34 if r.get("sub") else 0) + 52 + 12
        h = max(h, badge + 28)
        d.rounded_rectangle([bx, y, W - 64, y + h], 22, fill=WHITE)
        by = y + (h - badge) // 2
        d.rounded_rectangle([bx + 22, by, bx + 22 + badge, by + badge], 18, fill=YELLOW)
        cx = bx + 22 + badge / 2
        d.text((cx, by + 28), "EXIT", font=F(22), fill=NAVY, anchor="mm")
        num = str(r["exit"]).replace("Exit ", ""); fs = 54 if len(num) <= 2 else 44
        parts = num.split(" ") if (" " in num and d.textlength(num, font=F(30)) > badge - 14) else [num]
        if len(parts) == 1:
            while fs > 22 and d.textlength(num, font=F(fs)) > badge - 14: fs -= 2   # long exit names (e.g. "Hachijo") shrink to fit
            d.text((cx, by + 80), num, font=F(fs), fill=NAVY, anchor="mm")
        else:
            fs = 30
            while fs > 18 and max(d.textlength(x, font=F(fs)) for x in parts) > badge - 14: fs -= 2
            for k, x in enumerate(parts[:2]): d.text((cx, by + 66 + k * (fs + 4)), x, font=F(fs), fill=NAVY, anchor="mm")
        yy = y + 20
        for t in tl: d.text((tx, yy), t, font=F(36), fill=INK); yy += 46
        if r.get("sub"): d.text((tx, yy - 4), r["sub"], font=F(26, "Regular"), fill=MUTED); yy += 34
        lc = hexc(r.get("line_color", "#5A6482")); lf = F(24, "Medium"); lw = d.textlength(r["line"], font=lf) + 36
        d.rounded_rectangle([tx, yy + 4, tx + lw, yy + 44], 20, fill=lc)
        d.text((tx + 18, yy + 8), r["line"], font=lf, fill=WHITE)
        if r.get("note"): d.text((tx + lw + 18, yy + 8), r["note"], font=F(25, "Regular"), fill=MUTED)
        y += h + 12
    # tips box
    tips = spec.get("tips", [])
    if tips:
        lines = [wrap(d, t, F(26, "Regular"), W - 64 * 2 - 110) for t in tips]
        th = 24 + sum(len(l) * 36 + 10 for l in lines) + 14
        d.rounded_rectangle([64, y + 2, W - 64, y + 2 + th], 22, fill=(255, 244, 196))
        d.ellipse([88, y + 26, 124, y + 62], fill=YELLOW); d.text((106, y + 44), "!", font=F(26), fill=NAVY, anchor="mm")
        yy = y + 24
        for l in lines:
            for ln in l: d.text((144, yy), ln, font=F(26, "Regular"), fill=INK); yy += 36
            yy += 10
        y += th + 6
    # footer
    d.rectangle([0, H - 90, W, H], fill=NAVY)
    d.text((64, H - 64), "Save this  ·  japanbystation.com", font=F(28), fill=WHITE)
    ck = f"Checked {spec.get('checked', '')}"; f = F(22, "Regular")
    d.text((W - 64 - d.textlength(ck, font=f), H - 58), ck, font=f, fill=(170, 180, 210))
    if y > H - 100: print("WARNING: content overflows the card; cut rows or tips", file=sys.stderr)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    im.save(out, "JPEG", quality=92)

if __name__ == "__main__":
    make(json.load(open(sys.argv[1])), sys.argv[2])
