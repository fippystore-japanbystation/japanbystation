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
- NOT ALWAYS DOTONBORI / NAMBA (Ling, 23 Nov; guides AND Reels). Too many Osaka pieces end with "stay in Namba, walk to Dotonbori". Every Osaka piece must include at least one less obvious area as a real option, framed as "besides Namba / Dotonbori, consider X, because …" with 1–2 researched whys (e.g. Tenma, Kitashinchi, Nakazakicho, Tanimachi, Kyobashi, Fukushima, Bentencho, Shin-Osaka, Kitahama), matched to who it suits. Do not use Dotonbori as the reference point in more than one answer per piece. Same idea in Tokyo: not every answer is Shinjuku or Shibuya.

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
- More approved programs (Ling, 23 Nov; already active on Travelpayouts, the Drive script converts plain official links): Airalo / Yesim (Japan eSIM — https://www.airalo.com/japan-esim , https://yesim.app/), Welcome Pickups / Kiwitaxi (airport transfers — https://www.welcomepickups.com/ , https://kiwitaxi.com/), Radical Storage (luggage storage — https://radicalstorage.com/), Go City (https://gocity.com/), Tiqets (https://www.tiqets.com/). Put ONE where the reader is deciding that exact thing (eSIM in arrival guides, transfer in airport guides, storage in early-arrival / last-day guides). Booking.com, Agoda, Trip.com etc. are still under review: keep the Booking.com search links (they start earning once approved).
- HONESTY about affiliate links: they do NOT make anything cheaper for the reader (same price as booking direct). Never write "cheaper/best price/save" for a link unless the guide shows a same-date price comparison proving it. Frame them as convenience (book in English, pay in your currency, skip the ticket queue, free cancellation where the page says so).
- Keyword: one short UPPERCASE word, unique (build asserts). It is what viewers comment.
- SEO/GEO: answer in the first paragraph, 3–4 FAQ entries with direct answers, real numbers, internal links to related guides.
- Deploy: `python3 jbs.py deploy-site "Add <slug>"` (builds, copies to main, pushes → live in ~1 min). **Batch several guides per deploy** (Cloudflare free plan ≈500 builds/month; budget ≤4 site deploys/day).
- Verify one new page in the browser after deploy.

## 2b. Facebook text posts (Ling, 23 Nov — test)
For EVERY new guide, also write TWO Facebook posts as `site/fbposts/<id>.json` → `{"id":"fb-<keyword-lower>-1","guide":"<slug>","photo":<pexels id that shows that place>,"order":<next number>,"text":"…"}` (second one `-2`). build.py turns them into fb-queue.json; n8n posts the next one at about 10:00 and 20:30 Malaysia time with the photo.
- Same topic and facts as the guide, but its own angle. Ling (23 Nov): detailed (250–400 words), English, a small team that knows the place ("we'd", "our take"), warm, specific, never salesy.
- HOOK = the first 1–2 sentences, ONE paragraph, 150–250 characters, no line break inside it. Facebook only shows this before "See more", so it must carry the payoff (a number, a surprising fact, a clear benefit) and end with 👇. Bad: "Second trip to Osaka? Stay where Osaka actually lives." Good: "We priced the same three nights on both sides of Osaka Station. Walking 12 minutes saved ¥9,474. Here's when that walk is worth it, and when it isn't 👇"
- LAYOUT: a BLANK LINE between every paragraph and every point (no stacked bullets). Section headers as one line "🚇 HOW TO GET THERE" (emoji + CAPS), no ━━━ lines. Each point = its own 1–2 sentence paragraph, starting with an emoji or 1️⃣. Link on its own line after "👉 …:". Example: site/fbposts/fb-nakazaki-1.json.
- Post 1 = MINI-GUIDE: situation hook → 2–3 options, each = decision + 1–2 researched whys (numbers from the guide only) → "Our take" → guide link → one easy question.
- Post 2 = one of: INSIDER TIP / MISTAKE TO AVOID (one thing first-timers get wrong + the fix), SAVE-THIS CHECKLIST (3–5 steps), or A-or-B QUESTION. Rotate.
- Insider, lesser-known first: lead with the places and habits regulars know. Dotonbori / Namba / Shibuya crossing / Kabukicho only as a reference point and at most once in any 3 posts; never "the best / must-see" hype.
- Every post ends with the full guide URL (https://japanbystation.com/<slug>) and a question or "save this". No affiliate links, no "cheaper/best price", emojis as bullets only. End with 3–5 relevant hashtags (place, topic, #japantravel).
- Photo (Ling, 23 Nov): an eye-catching, clearly Japanese Pexels photo that LOOKS at you (colour, lanterns, food, people, a famous station); it may differ from the exact place, but stay in the same region (Kansai photo for Kansai, Tokyo for Tokyo; never Mount Fuji on an Osaka post). Look at it before using it.
- Emotion: a line or two of feeling (why this moment is worth it), but never claim a stay or visit we didn't make.

## 3. Reels (approved style; do not change without Ling)
- Mature male voice with intonation, slow pace (Kokoro blend am_michael 0.65 + am_fenrir 0.35, speed 1.0, built into reelkit).
- Phrase subtitles, outlined text, no background, spoken word bounces in yellow. Small cards in the site palette. Same cover LAYOUT every time (cover.py).
- Real Japan footage WITH PEOPLE, lively, from the right city. No clip used twice in one video (reelkit asserts). Japanese-style music, rotate `m_tokyostroll / m_kyotoriver / m_japansnacks / m_petals`.
- REEL VARIETY (Ling, 23 Nov): in any 3 Reels in a row, "Dotonbori" or "Namba" may appear (voice, cards, cover, caption) in AT MOST ONE. Before writing a spec, read the specs/captions of the last 2 items in reels-queue.json; if either mentions Dotonbori or Namba, this Reel must not. Same for the over-used Tokyo spots (Shibuya crossing, Shinjuku Kabukicho): max once in 3. Lead with places most visitors have not heard of, with a researched why.
- HOOK BY SITUATION, NOT BY PLACE (data, 23 Nov): "Where to stay in Osaka?" / "What's near Namba?" got few views; "Out late in Osaka? Stay here" got 401 viewers + 6 saves + 4 sends. Hooks name the traveller's situation or mistake, then answer at once. Hook styles to rotate: SITUATION ("Landing at 11 pm?", "Out late?", "With a toddler?"), MISTAKE ("Don't book 'near Umeda' before you check the exit"), CONTRAST ("Skip X, do Y instead"), MONEY ("What ¥5,000 really gets you"), TIME ("Only 3 hours in Kyoto?"), LOCAL ("Where Osaka office workers actually eat"). Never two Reels in a row with the same hook style.
- RETENTION RULES (Ling, 23 Nov; every new Reel). Night-owls Reel: 401 viewers, 6 saves + 4 sends (strong topic) but average watch 7 s, because the first answer (Namba) only came at ~12 s after a set-up about last trains. Length 33–40 s is FINE (voiceover 70–95 words); the problem is ORDER. Rules:
  1. ANSWER FIRST, THEN WHY. Open with the recommendation in the first 2 seconds, voice and text together ("Out late in Osaka? Book Namba."), first card already on screen. Never build up to it ("because trains stop at midnight, so book here" is wrong; "Book Namba — you can walk home from Dotonbori in 5 minutes" is right).
  2. SKIP WHAT EVERYONE KNOWS (e.g. "last trains are around midnight"): only say it if it is the reason behind a specific answer, and then after the answer.
  3. THREE ANSWERS, EACH = decision + 1–2 WHYs. Each why is one concrete, researched detail from the guide (minutes on foot, price on a date, last order, which exit). At least one why, at most two, so it is clear we did the research.
  4. Verdict at the end = which one to pick and exactly when the answer changes.
  5. CUT EVERY 2–3 SECONDS: new clip or new card at least every 3 s.
  6. KEYWORD EARLY: say the keyword once around 8–10 s in passing ("…the full list is in the guide, comment NIGHT") and again at the end. Cover stays clean (Ling's rule).
  7. Every clip: look at a frame for station names / signs (Tokyo signs never in Kansai Reels).
- Voiceover 70–95 words (about 33–40 s). Start with the most useful finding. Give exactly three answers (the brief's A, B, C), each = the decision first, then 1–2 whys (concrete researched details) and who it suits. Then the verdict: one practical recommendation, and say exactly when it changes (time, price, day of week). Then the CTA scene.
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
