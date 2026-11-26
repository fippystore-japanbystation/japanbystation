"""Japanese names for the English voice (Ling, 26 Nov: the voice says "Chitose" wrong).

espeak (Kokoro's English phonemizer) reads romaji as English: Chitose -> "CHIT-ohs", Umeda -> "YOU-meh-da",
Kobe -> "kohb", Gion -> "jun". Here every word listed in pronounce.json (plus a spec's "pronounce" list) is
converted from romaji to IPA by rule (romaji is regular), with optional manual overrides, and the rest of the
sentence is phonemized normally. reelkit then feeds the phonemes to Kokoro (is_phonemes=True).
Subtitles are untouched: they use the "shown" text.

Add every new Japanese name a Reel says to pronounce.json ("words"). Test:  python3 pronounce.py "New Chitose Airport"
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
V = {"a": "ɑː", "i": "i", "u": "u", "e": "ɛ", "o": "oʊ"}
LONG = {"aa": "ɑː", "ii": "iː", "uu": "uː", "ou": "oʊ", "oo": "oʊ", "ei": "eɪ", "ee": "eɪ"}
C = {"k": "k", "s": "s", "t": "t", "n": "n", "h": "h", "m": "m", "y": "j", "r": "ɾ", "w": "w", "g": "ɡ",
     "z": "z", "d": "d", "b": "b", "p": "p", "f": "f", "j": "dʒ", "v": "v"}
SPECIAL = [("sh", "ʃ"), ("ch", "tʃ"), ("ts", "ts")]

def syllables(word):
    """romaji word -> list of IPA syllables (no stress yet)."""
    w = word.lower().replace("ō", "ou").replace("ū", "uu").replace("ā", "aa")
    out, i = [], 0
    while i < len(w):
        c = w[i]
        if not c.isalpha(): i += 1; continue
        # geminate consonant (kk, tt, pp, ss, cch): drop the first one
        if i + 1 < len(w) and c == w[i + 1] and c not in "aiueon": i += 1; continue
        if c == "c" and w[i:i + 3] == "cch": i += 1; continue
        # syllabic n: before a consonant (not y) or at the end
        if c == "n" and (i + 1 == len(w) or (w[i + 1] not in "aiueoy")):
            if out: out[-1] += "n"
            else: out.append("n")
            i += 1 + (1 if i + 1 < len(w) and w[i + 1] == "'" else 0); continue
        onset = ""
        for s, ipa in SPECIAL:
            if w.startswith(s, i): onset, i = ipa, i + 2; break
        else:
            if c in C:
                onset = C[c]; i += 1
                if i < len(w) and w[i] == "y" and c != "y": onset += "j"; i += 1   # kya, ryo, nyu …
        if i < len(w) and w[i] in V:
            two = w[i:i + 2]
            if two in LONG: out.append(onset + LONG[two]); i += 2
            else: out.append(onset + V[w[i]]); i += 1
        elif onset:                      # stray consonant (the m in "Namba"): coda of the previous syllable
            if out: out[-1] += onset
            else: out.append(onset)
        else:
            i += 1
    return out

def romaji_ipa(word):
    parts = [p for p in re.split(r"[-\s]+", word) if p]
    res = []
    for p in parts:
        sy = syllables(p)
        if not sy: continue
        k = len(sy) - 2 if len(sy) >= 3 else 0          # stress the second-to-last syllable (English ears expect it)
        sy[k] = "ˈ" + sy[k]
        res.append("".join(sy))
    return " ".join(res)

def load(extra=None):
    d = json.load(open(os.path.join(HERE, "pronounce.json")))
    lex = {w.lower(): None for w in d.get("words", [])}
    lex.update({k.lower(): v for k, v in d.get("override", {}).items()})
    for w in (extra or []):
        if isinstance(w, str): lex.setdefault(w.lower(), None)
    if isinstance(extra, dict): lex.update({k.lower(): v for k, v in extra.items()})
    return lex

def to_phonemes(text, lex, tok=None):
    """Phonemize a sentence: lexicon words by romaji rule / override, the rest with espeak."""
    if tok is None:
        from kokoro_onnx.tokenizer import Tokenizer
        tok = Tokenizer()
    keys = sorted(lex, key=len, reverse=True)
    if not keys: return tok.phonemize(text, "en-us")
    rx = re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(k) for k in keys) + r")(?![A-Za-z])", re.I)
    out, pos = [], 0
    for m in rx.finditer(text):
        if m.start() > pos: out.append(tok.phonemize(text[pos:m.start()], "en-us"))
        w = m.group(1); out.append(lex[w.lower()] or romaji_ipa(w)); pos = m.end()
    if pos < len(text): out.append(tok.phonemize(text[pos:], "en-us"))
    s = " ".join(x.strip() for x in out if x.strip())
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    return s

if __name__ == "__main__":
    lex = load()
    for t in sys.argv[1:] or ["We landed at New Chitose Airport and took the train to Sapporo, then Otaru."]:
        print(t); print("  ", to_phonemes(t, lex))
