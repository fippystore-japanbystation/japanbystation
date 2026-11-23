# Japan by Station: production playbook

Ling runs **Japan by Station**: japanbystation.com (Japan-only English travel guides) and Instagram **@japanbystation**.
Each Reel answers ONE traveler question and gives the solution. Viewers comment a KEYWORD and n8n DMs them the guide page.
**The guide page must be live (and its keyword in keywords.json) before its Reel is queued.**

## 0. Session setup (every fresh session)
```
git clone -q -b studio https://github.com/fippystore-japanbystation/japanbystation.git ~/jbs/studio   # add_repo first if git is refused
cd ~/jbs/studio && python3 jbs.py setup      # clones main + media into ~/jbs, downloads the Kokoro voice model
python3 jbs.py status                        # what's queued, which keywords exist
```
Always finish with `python3 jbs.py save "what you did"` so the next session has your new sources (no Cloudflare build).

## 1. Voice and facts (non-negotiable)
- Professional team voice: "we suggest", "we'd take", "our pick". Never "Honestly?", no overly friendly AI phrasing, no hype.
- Never invent team names, credentials or personal stays. We build guides from official sources.
- Every time, price, opening day and distance comes from a source you found this session (operator, airport, city tourism bureau such as osaka-info.jp / kyoto.travel, the venue itself). If only blogs say it, write "about" or leave it out. Put sources in the guide's `sources` field with the check date.
- Explain WHY (minutes saved, price, fewer changes, who it suits). Say who it does NOT suit.
- No affiliate or commission wording inside videos or captions. No fake urgency.

## 2. Website guides
One file per guide: `site/guides/<slug>.html`. The build picks it up automatically (home "Latest posts", /guides index, sitemap, llms.txt, JSON-LD Article + Breadcrumb + FAQPage, keywords.json).
Header block (JSON, must parse):
```
<!--meta
{"title":"…","desc":"meta description, ~150 chars","city":"Kyoto","cat":"Where to stay","tag":"coral|mint|sky|sun|lilac|pink",
 "hero":PEXELS_PHOTO_ID,"hero_alt":"…","card":"one-line summary for cards","date":"YYYY-MM-DD","keyword":"UNIQUEWORD","order":0,
 "faq":[["question","answer"],…],"sources":"… Checked D Month YYYY."}
-->
```
Body: copy the structure of an existing guide (e.g. `site/guides/osaka-local-markets.html`): hero → lede (answer first) → byline with check date → `band` sections (`band plain|namba|umeda|tennoji`) with `card noimg` fact cards → `tipbox` "Our suggestion" → booking CTA → "Keep planning" links.
- Images: `src="pexels:ID:WIDTH"` (Pexels photo id). Pick photos that really show that place; Tokyo photos never on Osaka pages.
- Affiliate links only inside content, `rel="sponsored noopener" target="_blank"`: Booking.com search `https://www.booking.com/searchresults.html?ss=<Area>%2C+<City>` (Travelpayouts Drive script converts it), Klook search `https://www.klook.com/search/result/?query=…` for tours/passes/transfers. A page with no affiliate link is fine.
- Keyword: one short UPPERCASE word, unique (build asserts). It is what viewers comment.
- SEO/GEO: answer in the first paragraph, 3–4 FAQ entries with direct answers, real numbers, internal links to related guides.
- Deploy: `python3 jbs.py deploy-site "Add <slug>"` (builds, copies to main, pushes → live in ~1 min). **Batch several guides per deploy** (Cloudflare free plan ≈500 builds/month; budget ≤4 site deploys/day).
- Verify one new page in the browser after deploy.

## 3. Reels (approved style; do not change without Ling)
- Mature male voice with intonation, slow pace (Kokoro blend am_michael 0.65 + am_fenrir 0.35, speed 1.0, built into reelkit).
- Phrase subtitles, outlined text, no background, spoken word bounces in yellow. Small cards in the site palette. Same cover layout every time (cover.py).
- Real Japan footage WITH PEOPLE, lively, from the right city. No clip used twice in one video (reelkit asserts). Japanese-style music, rotate `m_tokyostroll / m_kyotoriver / m_japansnacks / m_petals`.
- 40–50 s. Scene 1 = hook (a traveler question), last scene = CTA "Comment KEYWORD, and we'll send you our guide." In between 3–5 scenes, each with a card {kicker, title, big number, small} and the WHY.
- Spec: `reel/specs/<slug>.json` (copy `reel/specs/namba.json`). Add `"caption"`:
  hook line + emoji / 3–4 emoji fact bullets / one summary line / "Comment KEYWORD and we'll DM you the full guide." / a share line worded differently each time ("📌 Save this and send it to whoever you're travelling with", "Tag your travel buddy", "Share it with your trip group chat") / 5–8 hashtags last.
- Footage (needs Ling's computer, built-in browser): in a Pexels tab (`https://www.pexels.com/search/videos/<query>/?orientation=portrait`), collect slugs, then in ONE javascript call fetch each video page, take the `1080_1920` (or 720_1280) mp4 URL, fetch the blobs, build one bundle `window._jbs = Blob([10-digit header length, JSON index [[name,size],…], …parts])`, click-download it as `jbs_bundle_<x>.bin`. Ling asked: **bundle downloads into one file**, never one popup per clip.
  In device_bash: the download appears in `$HOME/mnt/Downloads` as a `.tmp` and vanishes fast → poll and `cp` the newest `*.tmp` of the right size to /tmp, split it with python into `$HOME/mnt/Downloads/jbs_media/`, then `device_stage_files` (Windows paths `C:\Users\User\Downloads\jbs_media\…`) and copy from `/mnt/user-data/uploads/Downloads/jbs_media/` into `reel/air/`.
  Look at one frame of each clip before using it (city/people check). Keep `CLIPS.md` updated with good clip ids.
- Render: `cd reel && python3 reelkit.py specs/<slug>.json --stills` → Read `work/<slug>/sheet.jpg` and check → `python3 reelkit.py specs/<slug>.json` → check `out/<slug>.jpg` cover.
- Queue: `python3 jbs.py add-reel slugA slugB …` (batch 2–4 per call: one media push + one main push).
- Publishing is automatic (n8n on Ling's PC reads reels-queue.json). Never post to Instagram by hand.

## 4. Reporting
End each run by sending Ling a short progress note (what went live, queue depth, anything blocked). Plain, short, no step-by-step recap.

## 5. Known limits
- Instagram DMs to the public need Meta App Review (app is in development mode). Until approved only app-role testers get DMs.
- n8n runs in Docker on Ling's PC; if it sleeps nothing posts. Changing n8n needs Ling's login or API key; don't hunt for credentials.
- Travelpayouts hotel programs (Booking.com, Agoda, Trip.com…) are pending review by Travelpayouts; links still work, they start earning once matched.
