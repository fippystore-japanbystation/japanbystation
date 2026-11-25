"""Japan by Station "Which exit?" cheat sheet: a saveable JPEG for a station page (Ling, 25 Nov).
usage: python3 exitcard.py cards/<slug>.json site/exitcards/<slug>.jpg
JSON: {"station": "Asakusa Station", "city": "Tokyo", "subtitle": "4 stations, 1 name: use the right exit",
       "rows": [{"to": "Kaminarimon Gate (Senso-ji)", "line": "Ginza Line", "exit": "Exit 1", "note": "~1 min · lift"}, ...],
       "tips": ["...", "..."], "checked": "25 Nov 2026", "color": "coral"}
Every row must come from the guide page or an official station map checked this run (PLAYBOOK 2d)."""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1440
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"
def F(s, w="Bold"): return ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)
INK = (40, 32, 70); CREAM = (255, 250, 243); WHITE = (255, 255, 255); MUTED = (110, 100, 140); LINE = (230, 222, 240)
COL = {"coral": (255, 125, 94), "mint": (51, 195, 161), "sky": (90, 174, 255), "sun": (255, 194, 61), "lilac": (168, 139, 255), "pink": (255, 141, 182)}

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def make(spec, out):
    c = COL.get(spec.get("color", "coral"), COL["coral"])
    im = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(im)
    # header band
    d.rectangle([0, 0, W, 300], fill=INK)
    d.rounded_rectangle([60, 52, 60 + d.textlength("JAPAN BY STATION", font=F(26)) + 44, 98], 23, fill=c)
    d.text((82, 57), "JAPAN BY STATION", font=F(26), fill=WHITE)
    d.text((60, 118), f"{spec['station']}, {spec['city']}", font=F(54), fill=WHITE)
    d.text((60, 192), "Which exit?", font=F(46, "Medium"), fill=c)
    if spec.get("subtitle"): d.text((60, 250), spec["subtitle"], font=F(26, "Regular"), fill=(220, 214, 240))
    # table header
    y = 340; x1, x2, x3 = 60, 560, 800
    for x, t in ((x1, "GOING TO"), (x2, "LINE"), (x3, "EXIT")):
        d.text((x, y), t, font=F(24), fill=MUTED)
    y += 46
    for r in spec["rows"]:
        to_lines = wrap(d, r["to"], F(32), x2 - x1 - 24)
        line_lines = wrap(d, r["line"], F(26, "Medium"), x3 - x2 - 20)
        rh = max(len(to_lines) * 42, len(line_lines) * 34) + (38 if r.get("note") else 0) + 30
        d.line([60, y, W - 60, y], fill=LINE, width=3)
        yy = y + 18
        for t in to_lines: d.text((x1, yy), t, font=F(32), fill=INK); yy += 42
        if r.get("note"): d.text((x1, yy + 2), r["note"], font=F(24, "Regular"), fill=MUTED)
        ly = y + 22
        for t in line_lines: d.text((x2, ly), t, font=F(26, "Medium"), fill=INK); ly += 34
        ew = d.textlength(r["exit"], font=F(34)) + 36
        d.rounded_rectangle([x3, y + 14, x3 + ew, y + 66], 26, fill=c)
        d.text((x3 + 18, y + 18), r["exit"], font=F(34), fill=WHITE)
        y += rh
    d.line([60, y, W - 60, y], fill=LINE, width=3)
    # tips
    y += 30
    for t in spec.get("tips", []):
        for i, ln in enumerate(wrap(d, t, F(26, "Regular"), W - 160)):
            if i == 0: d.ellipse([62, y + 12, 76, y + 26], fill=c)
            d.text((96, y), ln, font=F(26, "Regular"), fill=INK); y += 36
        y += 10
    # footer
    d.rectangle([0, H - 90, W, H], fill=INK)
    d.text((60, H - 64), "Save this · japanbystation.com", font=F(28), fill=WHITE)
    ck = f"Checked {spec.get('checked', '')}"
    d.text((W - 60 - d.textlength(ck, font=F(22, 'Regular')), H - 58), ck, font=F(22, "Regular"), fill=(200, 192, 225))
    if y > H - 110: print("WARNING: content overflows the card; cut rows or tips", file=sys.stderr)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    im.save(out, "JPEG", quality=90)

if __name__ == "__main__":
    make(json.load(open(sys.argv[1])), sys.argv[2])
