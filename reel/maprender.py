"""Real-map route renderer for ROUTE CARDS (26 Nov, Ling: "their cards use a real map with the points connected").

Map data: OpenFreeMap vector tiles (OpenMapTiles schema, built from OpenStreetMap; free incl. commercial use).
Attribution required on every image: "© OpenStreetMap contributors · OpenMapTiles" (drawn by render_map).
The walking route between stops comes from the FOSSGIS OSRM foot router (routing.openstreetmap.de, the walking
router of openstreetmap.org; light use, cached), so the line follows real streets and paths; the walk time shown is
that distance at 75 m/min ("map estimate").

    from maprender import geocode, render_map
    ll = geocode("Kaminarimon, Asakusa, Tokyo")            # Nominatim, cached in reel/geo-cache.json, 1 request/s
    img, pins, meters = render_map([(lat, lon), ...], 560, 1350, color=(255, 107, 84))
"""
import json, math, os, time, urllib.request, urllib.parse, heapq
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "JapanByStation/1.0 (+https://japanbystation.com)"}
Z = 14
CACHE = os.path.join(HERE, "work", "tiles"); os.makedirs(CACHE, exist_ok=True)
FD = os.path.join(HERE, "..", "fonts") + "/"
def F(s, w="Bold"): return ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)

BG = (14, 20, 46); PARK = (22, 74, 62); WATER = (26, 82, 146); WATER_EDGE = (70, 150, 220); BLD = (32, 40, 74)
ROAD = {"motorway": ((120, 92, 190), 5), "trunk": ((104, 100, 190), 5), "primary": ((92, 104, 180), 4.5), "secondary": ((70, 84, 145), 3.5),
        "tertiary": ((80, 92, 150), 3), "minor": ((66, 78, 132), 2.4), "service": ((56, 66, 112), 1.8), "path": ((60, 72, 122), 1.5),
        "track": ((40, 48, 85), 1.2), "rail": ((96, 104, 150), 1.6), "transit": ((96, 104, 150), 1.6)}
WALK = {"primary", "secondary", "tertiary", "minor", "service", "path", "track", "trunk", "pedestrian"}

_tj = None
def _tiles_url():
    global _tj
    if _tj is None:
        _tj = json.loads(urllib.request.urlopen(urllib.request.Request("https://tiles.openfreemap.org/planet", headers=UA), timeout=30).read())
    return _tj["tiles"][0]

def ll2uv(lat, lon):                          # mercator in z14 tile units
    n = 2 ** Z; s = math.sin(math.radians(lat))
    return (lon + 180) / 360 * n, (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n

def tile(x, y):
    p = os.path.join(CACHE, f"{Z}_{x}_{y}.pbf")
    if not os.path.exists(p):
        u = _tiles_url().replace("{z}", str(Z)).replace("{x}", str(x)).replace("{y}", str(y))
        open(p, "wb").write(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read())
    import mapbox_vector_tile
    return mapbox_vector_tile.decode(open(p, "rb").read(), default_options={"y_coord_down": True})

def geocode(q):
    cp = os.path.join(HERE, "geo-cache.json"); c = json.load(open(cp)) if os.path.exists(cp) else {}
    if q in c: return tuple(c[q])
    parts = [p.strip() for p in q.split(",")]
    tries = [q] + ([parts[0] + ", " + parts[-1], parts[0]] if len(parts) > 1 else [])   # "X, area, city" -> "X, city" -> "X"
    r = []
    for t in tries:
        time.sleep(1.1)
        u = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": t, "format": "json", "limit": 1, "accept-language": "en", "countrycodes": "jp"})
        r = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read())
        if r: break
    if not r: raise ValueError("not found: " + q + "  (give the stop an explicit \"ll\": [lat, lon] from the guide's map link)")
    c[q] = [float(r[0]["lat"]), float(r[0]["lon"])]; json.dump(c, open(cp, "w"), indent=0, ensure_ascii=False)
    return tuple(c[q])

def _lines(geom):
    t = geom["type"]; co = geom["coordinates"]
    if t == "LineString": return [co]
    if t == "MultiLineString": return co
    return []

def _polys(geom):
    t = geom["type"]; co = geom["coordinates"]
    if t == "Polygon": return [co]
    if t == "MultiPolygon": return co
    return []

def render_map(stops, W, H, color=(255, 107, 84), pad=0.14, labels=True, box=None, max_scale=2600):
    """box = (x0, y0, x1, y1): the part of the W x H image the stops must fit in (the rest is still real map)."""
    uv = [ll2uv(a, b) for a, b in stops]
    u0, u1 = min(p[0] for p in uv), max(p[0] for p in uv); v0, v1 = min(p[1] for p in uv), max(p[1] for p in uv)
    du, dv = max(u1 - u0, 0.02), max(v1 - v0, 0.02)
    bx0, by0, bx1, by1 = box or (0, 0, W, H)
    S = min((bx1 - bx0) * (1 - 2 * pad) / du, (by1 - by0) * (1 - 2 * pad) / dv, max_scale)   # px per z14 tile unit
    cu, cv = (u0 + u1) / 2, (v0 + v1) / 2
    U0, V0 = cu - (bx0 + bx1) / 2 / S, cv - (by0 + by1) / 2 / S
    P = lambda u, v: ((u - U0) * S, (v - V0) * S)
    lat_c = stops[0][0]; m_per_unit = 40075016.686 * math.cos(math.radians(lat_c)) / 2 ** Z
    im = Image.new("RGBA", (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    feats = {}
    for tx in range(int(U0) - 0, int(U0 + W / S) + 1):
        for ty in range(int(V0) - 0, int(V0 + H / S) + 1):
            try: t = tile(tx, ty)
            except Exception: continue
            for layer, v in t.items():
                ext = v.get("extent", 4096)
                for f in v["features"]:
                    feats.setdefault(layer, []).append((tx, ty, ext, f))
    def pts(tx, ty, ext, ring): return [P(tx + x / ext, ty + y / ext) for x, y in ring]
    for layer, fill in (("landcover", PARK), ("park", PARK), ("water", WATER), ("building", BLD)):
        for tx, ty, ext, f in feats.get(layer, []):
            if layer == "landcover" and f["properties"].get("class") not in ("grass", "wood", "park"): continue
            for poly in _polys(f["geometry"]):
                if poly and len(poly[0]) > 2:
                    d.polygon(pts(tx, ty, ext, poly[0]), fill=fill)
                    if layer == "water": d.line(pts(tx, ty, ext, poly[0]) + [pts(tx, ty, ext, poly[0])[0]], fill=WATER_EDGE, width=2)
    order = ["path", "track", "service", "minor", "tertiary", "secondary", "primary", "trunk", "motorway", "rail", "transit"]
    tr = feats.get("transportation", [])
    for cls in order:
        col, w = ROAD.get(cls, ((40, 48, 85), 1))
        for tx, ty, ext, f in tr:
            if f["properties"].get("class") != cls: continue
            for ln in _lines(f["geometry"]):
                if len(ln) > 1: d.line(pts(tx, ty, ext, ln), fill=col, width=max(1, int(round(w * min(2.2, max(0.6, S / 1400))))), joint="curve")
    # walking route: FOSSGIS OSRM foot router (the one openstreetmap.org uses for walking directions), cached
    legs, meters = [], 0.0
    def walk(a, b):
        k = f"{a[0]:.6f},{a[1]:.6f}>{b[0]:.6f},{b[1]:.6f}"
        cp = os.path.join(HERE, "route-cache.json"); c = json.load(open(cp)) if os.path.exists(cp) else {}
        if k not in c:
            time.sleep(1.0)
            u = f"https://routing.openstreetmap.de/routed-foot/route/v1/driving/{a[1]},{a[0]};{b[1]},{b[0]}?overview=full&geometries=geojson"
            r = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read())
            if r.get("code") != "Ok": return None
            c[k] = {"m": r["routes"][0]["distance"], "ll": r["routes"][0]["geometry"]["coordinates"]}
            json.dump(c, open(cp, "w"))
        return c[k]
    for i in range(len(stops) - 1):
        try: w = walk(stops[i], stops[i + 1])
        except Exception: w = None
        if w:
            meters += w["m"]; legs.append([P(*ll2uv(la, lo)) for lo, la in w["ll"]])
        else:
            meters += math.dist(uv[i], uv[i + 1]) * m_per_unit * 1.3; legs.append([P(*uv[i]), P(*uv[i + 1])])
    # neon route: glow + core + white dashes
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    for leg in legs: g.line(leg, fill=color + (255,), width=16, joint="curve")
    glow = glow.filter(ImageFilter.GaussianBlur(10)); im.alpha_composite(glow); im.alpha_composite(glow)
    d = ImageDraw.Draw(im)
    for leg in legs: d.line(leg, fill=color + (255,), width=7, joint="curve")
    for leg in legs:                                     # small white dashes on the line
        acc = 0
        for a, b in zip(leg, leg[1:]):
            L = math.dist(a, b); s = 0
            while s < L:
                if int((acc + s) // 14) % 2 == 0:
                    t0, t1 = s / L, min(L, s + 7) / L
                    d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=(255, 255, 255, 200), width=2)
                s += 7
            acc += L
    if labels:   # water names and train stations, in English, like a real map
        seen = set(); nst = [0]; pinpx = [P(u, v) for u, v in uv]
        for tx, ty, ext, f in feats.get("water_name", []):
            n = f["properties"].get("name:en") or f["properties"].get("name_en")
            if not n or n in seen or f["geometry"]["type"] not in ("Point", "LineString", "MultiLineString"): continue
            c = f["geometry"]["coordinates"]; c = c if f["geometry"]["type"] == "Point" else (c[len(c) // 2] if f["geometry"]["type"] == "LineString" else c[0][len(c[0]) // 2])
            x, y = P(tx + c[0] / ext, ty + c[1] / ext)
            if "river" not in n.lower() or len(seen) >= 2: continue      # big rivers only, they orient the reader
            if bx0 + 10 < x < W - 220 and 30 < y < H - 30 and min(math.dist((x, y), q) for q in pinpx) < 420: d.text((x, y), n, font=F(26, "Medium"), fill=(150, 200, 250)); seen.add(n)
        for tx, ty, ext, f in feats.get("poi", []):
            pr = f["properties"]
            if pr.get("class") != "railway" or pr.get("subclass") not in ("station", "subway", "halt"): continue
            n = pr.get("name:en") or pr.get("name_en")
            if not n or n.lower() in seen or not n.isascii() or nst[0] >= 4: continue
            c = f["geometry"]["coordinates"]; x, y = P(tx + c[0] / ext, ty + c[1] / ext)
            if not (bx0 + 10 < x < W - 150 and 20 < y < H - 30): continue
            if min(math.dist((x, y), q) for q in pinpx) > 260: continue
            seen.add(n.lower()); nst[0] += 1; fs = F(20, "Medium"); n = n if n.lower().endswith("station") else n + " Stn"
            d.rounded_rectangle((x - 13, y - 13, x + 13, y + 13), 7, fill=(235, 238, 255)); d.text((x, y), "▣" if False else "T", font=F(18), fill=BG, anchor="mm")
            d.text((x + 18, y - 12), n, font=fs, fill=(215, 222, 245))
    d.text((W - 10, H - 10), "© OpenStreetMap contributors · OpenMapTiles", font=F(15, "Regular"), fill=(150, 158, 190), anchor="rd")
    return im, [P(u, v) for u, v in uv], meters
