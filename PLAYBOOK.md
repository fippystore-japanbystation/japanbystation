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
- NEVER repeat a topic. Before writing anything, read the DONE list in TOPICS.md and the existing site/guides and reel/specs. Add every new guide/Reel to DONE.
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
- Phrase subtitles, outlined text, no background, spoken word bounces in yellow. Small cards in the site palette. Same cover LAYOUT every time (cover.py).
- Real Japan footage WITH PEOPLE, lively, from the right city. No clip used twice in one video (reelkit asserts). Japanese-style music, rotate `m_tokyostroll / m_kyotoriver / m_japansnacks / m_petals`.
- Voiceover 70–95 words (about 35–45 s). Start with the most useful finding. Give exactly three answers (the brief's A, B, C), each with ONE concrete detail and who it suits. Then the verdict: one practical recommendation, and say exactly when it changes (time, price, day of week). Then the CTA scene.
- Spec: `reel/specs/<slug>.json` (copy `reel/specs/osaka-night-owls.json`). Scene 1 = hook, last scene = CTA: "Comment or DM us KEYWORD, and we'll send you the full guide. Follow for more Japan tips." (n8n answers both comments and DMs that contain the keyword.) Middle scenes: the three answers + verdict, each with a card {kicker, title, big number, small}. Cards use only glyphs Poppins has (no №, no arrows; use "No.", "to").
- COVER TEXT (Ling, 23 Nov): titles must be BIG and HIGH so they read on the profile grid (cover.py does this: ONE block centred on the MIDDLE of the photo (grid centre y=960): coral logo-colour "Japan by Station" pill, 108 px white title, place (e.g. "NAMBA, OSAKA") in plain cream text under it; only one pill, NOTHING at the bottom: no "Full guide in DM", no "Comment KEYWORD" on the cover. Ling: covers feel like natural sharing, not a DM ask). Keep cover titles short: 2 lines, about 3 words per line.
- STRANGER TEST (Ling, 23 Nov): assume the viewer is a stranger who has never heard of us. The cover must make it obvious this is about JAPAN: the coral "Japan by Station" pill does that, and the place line always names the place with its city (e.g. "NAMBA, OSAKA", "SHINJUKU, TOKYO", never just "GROUPS"). Where it fits, put the city in the title too ("Out late in Osaka?").
- COVER (first image, Ling's rule): the cover LAYOUT is fixed, but the PHOTO must change every time. Pick a strong, recognisably Japanese frame from that place: street crowds, neon, a temple, a train, food stalls, and seasonal scenes (snow, cherry blossom, autumn leaves) when that place really looks like that. Never reuse a cover clip from the last 12 Reels: check and append to `COVERS.md`. Cover `category` = the PLACE with its city (stranger test); `title` = the brief's question, 2 short lines.
- Caption (`"caption"` in the spec), all relevant to THIS place and question:
  1) hook line + emoji; 2) 3 emoji bullets (the three answers, one concrete detail each); 3) the verdict in one line;
  4) "Comment KEYWORD or DM us KEYWORD, and we'll send you the full guide 📩"; 5) a share line, worded differently every time ("Send this to whoever you're travelling with", "Tag your trip buddy", "Drop this in your group chat");
  6) "Follow @japanbystation for a new Japan tip every day"; 7) 5–8 hashtags last: 2–3 for the exact place (e.g. #kizumarket #namba), 2–3 for the topic (#osakafood #budgethotel), 2 broad (#japantravel #japantrip). No affiliate wording.
- Growth goal from Ling: 400 followers a week. Every Reel must give a real answer, end with the comment-for-DM CTA, a share CTA and a follow CTA.
- Footage (needs Ling's computer, built-in browser): in a Pexels tab (`https://www.pexels.com/search/videos/<query>/?orientation=portrait`), collect slugs, then in ONE javascript call fetch each video page, take the `1080_1920` (or 720_1280) mp4 URL, fetch the blobs, build one bundle `window._jbs = Blob([10-digit header length, JSON index [[name,size],…], …parts])`, click-download it as `jbs_bundle_<x>.bin`. Ling asked: **bundle downloads into one file**, never one popup per clip.
  In device_bash: the download appears in `$HOME/mnt/Downloads` as a `.tmp` and vanishes fast → poll and `cp` the newest `*.tmp` to /tmp until it reaches the full size, split it with python into `$HOME/mnt/Downloads/jbs_media/`, then `device_stage_files` (Windows paths `C:\Users\User\Downloads\jbs_media\…`) and copy from `/mnt/user-data/uploads/Downloads/jbs_media/` into `reel/air/`.
  Look at one frame of each clip before using it (city, people, really Japan?). Pexels titles lie: an "Asian alley" may be Taiwan. Keep `CLIPS.md` updated (good clips and never-use clips).
- Render: `cd reel && python3 reelkit.py specs/<slug>.json --stills` → Read `work/<slug>/sheet.jpg` and check → `python3 reelkit.py specs/<slug>.json` → check `out/<slug>.jpg` cover.
- Queue: `python3 jbs.py add-reel slugA slugB …` (batch 2–4 per call: one media push + one main push).
- Publishing is automatic (n8n on Ling's PC reads reels-queue.json). Never post to Instagram by hand.

## 3b. Briefs (BRIEFS-*.md)
Ling supplies batches of briefs: `BRIEFS-KANSAI-40.md` (01–40), then `BRIEFS-TOKYO-71-80.md`, then `BRIEFS-TOKYO-41-70.md`. Follow the order in TOPICS.md. Work them in number order: the WEBSITE task writes the guide page for a brief first (title = the question, three researched answers A/B/C, the verdict with when it changes, sources and check date), then the REELS task makes the Reel from that live page.
Research rules from the brief: room prices on the same stay dates, occupancy and total-price basis (search Booking.com in the built-in browser for one named weeknight about 4 weeks ahead and state those dates on the page); routes count walk + transfers + waiting + the way back; food spots: check last orders; "quiet hotel": evidence about the actual street or room. If a key detail cannot be verified, do NOT publish it: add the brief to `NEEDS-RESEARCH.md` with what is missing and move on. "Go earlier", "skip the upgrade" or "this budget only buys a capsule on these dates" are valid answers.
Affiliate fit: name the stay/activity/transport that fits the verdict and link it with the approved Booking.com/Klook search links only; leave it out if nothing fits.

## 4. Reporting
End each run by sending Ling a short progress note (what went live, queue depth, anything blocked). Plain, short, no step-by-step recap.

## 5. Known limits
- Meta app "Japan by Station DM" is LIVE since 23 Nov 2026; Ling tested: comment-for-DM reaches everyone. Privacy policy (/privacy) and data deletion page (/data-deletion) must stay online.
- n8n runs in Docker on Ling's PC; if it sleeps nothing posts. Changing n8n needs Ling's login or API key; don't hunt for credentials.
- Posting times (Ling, 23 Nov, to keep the new account safe from spam flags): 5 Reels a day at about 08:00, 11:44, 15:11, 17:40, 22:31 Malaysia time (±10 min), to Instagram AND the Facebook Page (n8n workflow "JbS · Publish Reel (5 a day)": schedule → Random delay Wait node → Run; the Code step must finish within 300 s). Reels producer makes up to 3 per run, twice a day.
- Travelpayouts hotel programs (Booking.com, Agoda, Trip.com…) are pending review by Travelpayouts; links still work, they start earning once matched.

## 6. Interactive pieces (pilot, 23 Nov)
- Night/date comparison (`.compare` with `.nights` buttons and `.night` panels, see site/guides/namba-5000-yen-private-room.html): use only when the guide has researched prices for 2+ specific nights. Show total price, what it buys, private vs shared toilet/shower, the sample dates, occupancy and tax basis. Keep both panels in the HTML (visible without JavaScript). Put the booking CTA right after it. Keep "over budget" and "difference between rooms" as separate numbers.
- Station Tip ticket (`<details class="ticket">`): an inline disclosure next to the paragraph it relates to; only link to a real guide or verified route; "Next tip" only when there is a second tip specific to that article. At most one per guide; never a floating pop-up.
- Home page "Start with your situation" is set in build.py (SITUATIONS); city counts come from the published guides automatically.
