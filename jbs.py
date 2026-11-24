#!/usr/bin/env python3
"""Japan by Station studio helper.

  python3 jbs.py setup                 # clone main + media checkouts, download TTS model
  python3 jbs.py deploy-site "message" # build site, copy into main checkout, push (auto-deploys)
  python3 jbs.py add-reel SLUG [SLUG…]  # encode reel/out/SLUG.mp4 for IG; ONE push to media, ONE push to main
                                       # (cover + queue entry, caption from the spec). Batch reels: each push = 1 Cloudflare build.
  python3 jbs.py save "message"        # commit this studio folder to the studio branch (no Cloudflare build)
  python3 jbs.py status                # queue depth, keywords, guide count
"""
import json, os, subprocess, sys, datetime, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.expanduser("~/jbs")              # checkouts live here
MAIN = os.path.join(WORK, "main")
MEDIA = os.path.join(WORK, "media")
REPO = "https://github.com/fippystore-japanbystation/japanbystation.git"
ATTR = ("\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")


def sh(cmd, cwd=None, check=True):
    print("+", cmd if isinstance(cmd, str) else " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), check=check, text=True,
                          capture_output=False)


def pull(path, branch):
    if not os.path.isdir(os.path.join(path, ".git")):
        os.makedirs(WORK, exist_ok=True)
        sh(["git", "clone", "-q", "--single-branch", "-b", branch, REPO, path])
    else:
        sh(["git", "fetch", "-q", "origin", branch], cwd=path)
        sh(["git", "reset", "-q", "--hard", "origin/" + branch], cwd=path)


def commit_push(path, msg, branch):
    sh(["git", "add", "-A"], cwd=path)
    r = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=path)
    if r.returncode == 0:
        print("nothing to commit"); return
    sh(["git", "commit", "-qm", msg + ATTR], cwd=path)
    for _ in range(3):
        if subprocess.run(["git", "push", "-q", "origin", "HEAD:" + branch], cwd=path).returncode == 0:
            return
        sh(["git", "pull", "-q", "--rebase", "origin", branch], cwd=path, check=False)
    raise SystemExit("push failed")


def setup():
    pull(MAIN, "main"); pull(MEDIA, "media")
    tts = os.path.join(HERE, "reel", "tts"); os.makedirs(tts, exist_ok=True)
    base = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
    for src, dst in [("kokoro-v1.0.fp16.onnx", "kokoro.onnx"), ("voices-v1.0.bin", "voices-v1.0.bin")]:
        if not os.path.exists(os.path.join(tts, dst)):
            sh(["curl", "-sL", "-o", os.path.join(tts, dst), base + src])
    sh("pip install -q --break-system-packages kokoro-onnx soundfile pillow numpy 2>/dev/null || true")
    print("setup done")


def deploy_site(msg):
    # always build from the newest studio sources, so parallel runs never deploy an older home page / keywords.json
    subprocess.run(["git", "pull", "-q", "--rebase", "--autostash", "origin", "studio"], cwd=HERE)
    pull(MAIN, "main")
    live = os.path.join(HERE, "live")
    shutil.rmtree(live, ignore_errors=True)
    sh([sys.executable, os.path.join(HERE, "build.py")])
    for f in os.listdir(live):
        src = os.path.join(live, f)
        if os.path.isdir(src): shutil.copytree(src, os.path.join(MAIN, f), dirs_exist_ok=True)
        else: shutil.copy(src, os.path.join(MAIN, f))
    commit_push(MAIN, msg, "main")


def encode(slug):
    out = os.path.join(HERE, "reel", "out")
    src, ig = os.path.join(out, slug + ".mp4"), os.path.join(out, slug + "_ig.mp4")
    for crf, mr in (("23", "4M"), ("26", "3M"), ("28", "2500k")):
        sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-c:v", "libx264", "-preset", "veryfast", "-crf", crf,
            "-maxrate", mr, "-bufsize", "8M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart", ig])
        if os.path.getsize(ig) < 24 * 1024 * 1024: return ig
    raise SystemExit("video too big for Pages")


def add_reel(slugs):
    out = os.path.join(HERE, "reel", "out")
    specs = {s: json.load(open(os.path.join(HERE, "reel", "specs", s + ".json"))) for s in slugs}
    pull(MAIN, "main")
    keys = json.load(open(os.path.join(MAIN, "keywords.json")))
    for s, sp in specs.items():
        assert sp["keyword"] in keys, f"keyword {sp['keyword']} missing from keywords.json - deploy the page first"
        assert sp.get("caption"), f"{s}: spec needs a caption"
    igs = {s: encode(s) for s in slugs}
    qp = os.path.join(MAIN, "reels-queue.json"); q = json.load(open(qp))
    for s, sp in specs.items():
        shutil.copy(os.path.join(out, s + ".jpg"), os.path.join(MAIN, "covers", s + ".jpg"))
        for i in q["items"]:
            if i["slug"] == s: i["caption"] = sp["caption"]   # re-cut of a queued Reel: new video + new caption
        if not any(i["slug"] == s for i in q["items"]):
            q["items"].append({"slug": s, "keyword": sp["keyword"],
                               "video_url": f"https://media.japanbystation-web.pages.dev/{s}.mp4",
                               "cover_url": f"https://japanbystation.com/covers/{s}.jpg", "caption": sp["caption"]})
    keep = [i["slug"] for i in q["items"][-45:]]
    # media branch: rebuilt as a single orphan commit holding only recent videos (no git bloat)
    pull(MEDIA, "media")
    for s, ig in igs.items(): shutil.copy(ig, os.path.join(MEDIA, s + ".mp4"))
    for f in os.listdir(MEDIA):
        if f.endswith(".mp4") and f[:-4] not in keep: os.remove(os.path.join(MEDIA, f))
    sh("git checkout -q --orphan tmp && git add -A && git commit -qm 'Reel media (recent only)' && "
       "git branch -D media -q 2>/dev/null; git branch -m media && git push -q -f origin media", cwd=MEDIA)
    q["updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(q, open(qp, "w"), ensure_ascii=False, indent=1)
    commit_push(MAIN, "Queue reels: " + ", ".join(slugs), "main")


def pull_reel(slugs):
    """Take unposted Reels out of the queue (e.g. to re-cut them). Re-add later with add-reel."""
    pull(MAIN, "main")
    qp = os.path.join(MAIN, "reels-queue.json"); q = json.load(open(qp))
    before = len(q["items"]); q["items"] = [i for i in q["items"] if i["slug"] not in slugs]
    q["updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(q, open(qp, "w"), ensure_ascii=False, indent=1)
    print("removed", before - len(q["items"]))
    commit_push(MAIN, "Pull reels for re-cut: " + ", ".join(slugs), "main")


def save(msg):
    commit_push(HERE, msg + " [CF-Pages-Skip]", "studio")


def status():
    pull(MAIN, "main")
    q = json.load(open(os.path.join(MAIN, "reels-queue.json")))
    k = json.load(open(os.path.join(MAIN, "keywords.json")))
    print("queue items:", [i["slug"] for i in q["items"]])
    print("keywords:", list(k))
    print("guides in studio:", len(os.listdir(os.path.join(HERE, "site", "guides"))))


if __name__ == "__main__":
    a = sys.argv[1:] or ["status"]
    {"setup": lambda: setup(), "deploy-site": lambda: deploy_site(a[1] if len(a) > 1 else "Site update"),
     "add-reel": lambda: add_reel(a[1:]), "pull-reel": lambda: pull_reel(a[1:]), "save": lambda: save(a[1] if len(a) > 1 else "Studio update"), "status": lambda: status()}[a[0]]()
