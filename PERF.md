# Performance log (what works)
Snapshots: perf/<date>.json (from n8n read-only endpoint http://localhost:5678/webhook/jbs-stats-r2x — NEVER call the jbs-post-now webhook for stats). perf/2026-11-24-0526utc.json = the morning snapshot of the same day.
Rule: patterns need samples. Compare like with like (same format, similar posting slot, similar age ≥ 48 h). Call something a pattern only with ≥ 3 posts on each side; until then write "early signal".

## Goals (updated daily)
- **25 Nov 20:15 MYT: FB Page followers 1 / 5,000 (yesterday 1, +0) · website 87 visits in 24 h / 1,000 (yesterday's 24 h ≈ 69, +26%)** · IG 11 followers (yesterday 7, +4).
- Checkpoint 31 Dec: FB 500 · web 300/day. Needed pace from here: FB ≈ +14/day, web ≈ ×3.5 in 5 weeks. Today: FB is OFF pace (0 new followers in 3 days of posting); web is early but growing.

## Status (25 Nov, 20:15 MYT snapshot perf/2026-11-25.json)
- IG: 16 Reels, 11 followers. FB: 27 items (13 Reels, 14 text/photo posts), 1 follower.
- 6 Reels are now ≥ 48 h old → first like-for-like comparison possible (see Patterns).
- Reel reach is basically final after ~30 h (reach grew +0–17 on Reels older than 48 h, +15–67 on 30–36 h ones). So a Reel's fate is decided in its first day.
- FB API: reactions, comments, post_media_view (views), post_clicks arrive. Shares and post_total_media_view_unique (reach) are STILL not in the JSON (n8n not changed; Ling can add them).
- No FB post has a "style" tag yet (variants start 27 Nov). fb-queue.json has no "type" field; all 14 posted FB text posts so far are PRACTICAL-WITH-LINK (photo + ~1,900 characters + guide link). There have been no place cards, guess-where or no-link deep informative posts yet, so the 70/30 mix is not running yet → we can't compare types for followers.
- Website (Cloudflare, last 24 h, bots excluded): 87 visits, 94 page views. Referrers: direct 35, m.facebook.com 26, www.facebook.com 25, google 1. Top paths: / 14, hakone-big-suitcase-forward-carry-store 13, asakusa-which-station-from-narita 12, shinjuku-five-minutes-with-a-suitcase 6, new-chitose-airport-to-sapporo 6 (= exactly the guides our FB link posts pointed to). Countries: US 43, Malaysia 24, Sweden 12, Ireland 4.
- ⚠ Data conflict: Cloudflare shows 51 visits from facebook.com, but the FB API shows 0 post_clicks on every one of those link posts and 0–5 views. 57 of 87 visits are Windows desktop (unusual for FB traffic, which is mostly phones). Some of these "FB" visits may be Meta's link-preview/scanning or in-app prefetch rather than people. Treat FB→web as UNVERIFIED until GA4 (utm_campaign fb_post) confirms it. GA4 not checked this run.
- Pinterest: no new data this run.

## IG Reels (25 Nov snapshot; reach · avg watch s · saves · shares · posted MYT · hook)
| Reel (spec) | age | reach | watch | saves | shares | posted | hook |
|---|---|---|---|---|---|---|---|
| Not sleeping early in Osaka? (osaka-night-owls) | 57 h | 1,286 | 9.5 | 16 | 9 | 23 Nov 11:01 | problem + "before you book" |
| Staying in Namba? (namba) | 61 h | 404 | 11.6 | 14 | 3 | 23 Nov 07:00 | situation |
| Kuromon too crowded? (osaka-local-markets) | 49 h | 323 | 9.7 | 11 | 2 | 23 Nov 19:32 | problem + local alternative |
| First trip to Sapporo? Sleep in Odori (sapporo-where-to-stay-first-trip) | 19 h | 276 | 9.8 | 6 | 2 | 25 Nov 01:10 | first-timer + answer in hook, winter city |
| First time in Osaka? (osaka-where-to-stay) | 63 h | 260 | 6.1 | 2 | 1 | 23 Nov 05:01 | generic first-timer |
| Want local Osaka, not the neon? (osaka-live-like-a-local) | 36 h | 253 | 10.4 | 7 | 2 | 24 Nov 08:01 | contrast |
| Big suitcase into Sapporo? (new-chitose-airport-to-sapporo-v2, v4) | 6 h | 216 | 6.9 | 2 | 0 | 25 Nov 14:19 | problem + answer, winter city |
| Two of you, one afternoon: Minoh (minoh-falls-autumn-afternoon) | 23 h | 200 | 8.2 | 5 | 0 | 24 Nov 21:40 | situation + scenic place |
| Just landed at KIX? (kansai-airport-which-train) | 67 h | 188 | 7.5 | 4 | 0 | 23 Nov 01:10 | arrival situation |
| Solo on ¥5,000? (namba-5000-yen-private-room) | 30 h | 165 | 5.5 | 0 | 0 | 24 Nov 14:14 | budget number |
| Four friends: apartment or 2 rooms? (osaka-four-friends) | 59 h | 159 | 6.0 | 0 | 0 | 23 Nov 08:59 | A-or-B |
| Skip Shibuya Sky (shibuya-crossing-view) | 26 h | 157 | 7.4 | 1 | 0 | 24 Nov 18:08 | contrarian "skip X" |
| Cup Noodles ¥500 (cup-noodles-museum-ikeda) | 33 h | 141 | 8.2 | 1 | 1 | 24 Nov 10:48 | attraction + price |
| Quiet mornings near Shibuya (shibuya-quiet-base-yoyogi) | 13 h | 128 | 5.8 | 1 | 0 | 25 Nov 07:38 | stay-area |
| A few days in Kyoto? (kyoto-where-to-stay-first-trip) | 16 h | 123 | 4.5 | 1 | 0 | 25 Nov 04:22 | stay-area |
| Skip midday at Senso-ji (sensoji-morning-or-evening-v2, v4) | 2 h | 120 | 3.7 | 0 | 0 | 25 Nov 18:04 | "skip X", too young |

## FB (25 Nov snapshot; views = post_media_view)
- FB Reels: 190–231 views each for every Reel ≥ 12 h old, whatever the topic (Kuromon 231, Kyoto 226, Sapporo Odori 218, Solo ¥5,000 213, Shinjuku 212, Shibuya Sky 207, Shibuya park 207, Cup Noodles 207; Minoh 127, Night owls 112, Tenma 8). Avg watch 3.4–6.3 s. Reactions 0–3. → Facebook seems to give each Reel a fixed ~200-view test and none has broken out yet. Kyoto (3 likes) and Sapporo Odori (2) got the most reactions.
- FB text/photo link posts: 0–18 views, 0 reactions, 0 clicks on all 14. Newest: fb-hakone-2 0 (1 h), fb-hakone-1 5, fb-asakusa-2 2, fb-asakusa-1 3, fb-suitcase-2 0, fb-landing-1 4, fb-bullet-1 2, fb-group-1 3, fb-nakazaki-1 5, fb-tenma-1 18, fb-market-1 5, fb-local-1b 15. Photo share "Second trip to Osaka?" 11 views, 2 clicks (still the only clicks besides 1 on the Minoh Reel).
- New FB followers: 0. No post type has brought a follower yet.

## Patterns (≥ 3 comparable posts per side, ≥ 48 h old)
P1 (25 Nov, IG Reels, old 33–40 s format, n = 3 v 3, weakest possible pattern): Reels whose hook names a SPECIFIC traveller problem/situation (night owls, staying in Namba, Kuromon too crowded) got 323–1,286 reach, 9.5–11.6 s watch, 11–16 saves. The generic first-timer, the A-or-B and the arrival-train Reels got 159–260 reach, 6.0–7.5 s, 0–4 saves. Confounds: all 6 are Osaka and posted 22–23 Nov; the night-owls outlier inflates reach. Saves track watch time on all 16 Reels.

## Early signals (not patterns yet)
1. Winter / Sapporo topics: the two Sapporo Reels are #1 and #3 of the last 2 days by reach (276 in 19 h; 216 in 6 h) while Tokyo/Kyoto stay-area Reels sit at 123–157. n = 2. Matches competitors today (japan_walker_'s Hokkaido winter Reel ≈ 5.5× its usual).
2. "Where to stay in <area>" Reels without a problem in the hook (Kyoto 4.5 s, Shibuya park 5.8 s, Solo ¥5,000 5.5 s) have the lowest watch time. n = 3, all < 30 h old.
3. v4 FAST Reels: only 2 so far (Sapporo airport 6.9 s at 6 h, Senso-ji 3.7 s at 2 h). Too young; compare on 27 Nov.
4. FB: Reels reach non-followers (~200 each); text link posts reach almost nobody (0–18). Same as yesterday, now 14 text posts.

## Do more / Do less / Next experiments (read by the Reels and Facebook producers)
LING DECISION (24 Nov evening, permanent): Reels go to FAST + STRONG HOOK v4 (PLAYBOOK 3): 20–30 s, 50–70 words, hook in the first second with the answer, a new shot every 1.5–2.5 s. From 25 Nov this log compares v4 Reels against the older 33–40 s Reels.
Do more
- Problem-first hooks: name one specific annoyance or constraint the viewer has (crowds, late nights, luggage, closing times), then the local alternative.
- Put the practical, save-worthy payoff in the first 3 s (saves > likes on every Reel).
Do less
- Generic "First time in X?" openers, and A-or-B questions that don't tease the answer in the first seconds (both ≤ 6.1 s watch, 0–2 saves). Early signal only: keep about 1 in 5 as a control and don't drop them yet.
Do more (25 Nov additions)
- Winter / Hokkaido / snow Reels in December (early signal + competitors). Sapporo and Otaru topics first.
- "Crowd problem → quieter alternative" angle on BOTH Reels and FB (our best Reels + JapanTravel's 19.6K-reaction FB post).
Do less (25 Nov additions)
- Plain "where to stay in <area>" Reels with no problem in the hook (lowest watch time, n = 3).
- FB: stop adding more long practical LINK posts until the no-link types run; 14 in a row got 0 reactions.
Next experiments
- E5 (FB, start now, don't wait for 27 Nov): post the first 70% no-link types (PLACE CARD with one stunning photo + one line + an easy question; one "crowd → quieter alternative" deep post with no link) and compare views/reactions/follows with the link posts.
- E6 (Reels): one "Is <premium thing> worth ¥X?" verdict Reel (e.g. Green Car, a rapi:t Super Seat) — Paolo's best organic Reel in 3 months (~3×) was this format.
- E1 (Reels): a timely "X is back / opens this week" hook (seasonal light-ups, winter events). Tokyo Cheapo's two biggest recent Reels (631K and 499K vs ~70K usual) are a dated seasonal list and an "is back" event. Try 2 timely Reels this week and compare them with problem hooks.
- E2 (Reels): one visually striking single-place Reel near Osaka (Minoh / Katsuo-ji). A 34K account's best recent Reel did about 8× its median with exactly this kind of place. Tested 24 Nov (minoh-falls-autumn-afternoon): 200 reach, 8.2 s, 5 saves = mid-pack, n = 1; try one more with a stronger visual first second.
- E3 (FB): check whether text posts reach anyone beyond followers: compare views on a photo+text post and a plain text post on the same day (the photo share already got the only clicks).
- E4 (FB): one "news you can use" text post (a rule, date or price that changes soon, verified at the official source). The most-shared text posts on 2 pages today were this kind.

## Pinterest (from Ling's screenshot, 25 Nov 15:11, account ~2 days old)
- Total: 75 impressions, 5 engagements, 0 outbound clicks, 0 saves. Top Pin by far: "Tenma, Osaka: where locals actually eat" (75); Hiroshima–Miyajima collage 3; Kyoto first-trip collage 3.
- Early signal only (new account; Pinterest usually takes weeks to start distributing): the one Pin that got shown is a FOOD + "where locals" + city keyword title. Keep practical, keyword-first titles; watch whether food/"where locals" Pins keep leading once there are 20+ Pins ≥ 7 days old.


## PACE TEST (A = current style, B = theluns-style pauses + stacked list + "N ways" cover; started 26 Nov)
| topic | variant | posted | reach 24h | watch 24h | saves | shares | reach 48h | watch 48h |
|---|---|---|---|---|---|---|---|---|
| kansai-airport-to-kyoto | A (-pa, "visitors pay less", 68 words) | expected 27 Nov ~01:15 MYT | | | | | | |
| kansai-airport-to-kyoto | B (-pb, "3 ways", 59 words, stack + pauses) | target 29 Nov ~01:15 MYT (held, add on 28 Nov) | | | | | | |


## SPLIT TEST ("Everyone goes to / Go here instead", started 26 Nov; key metric = shares)
| slug | posted | reach 24h | watch 24h | saves | shares | reach 48h | shares 48h | same-day normal Reels avg shares |
|---|---|---|---|---|---|---|---|---|


## ROUTE TEST (route-card carousels, started 26 Nov; key metrics = saves + shares)
| slug | posted | reach 24h | saves | shares | reach 48h | saves 48h | shares 48h | same-day Reels avg saves/shares |
|---|---|---|---|---|---|---|---|---|
