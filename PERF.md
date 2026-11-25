# Performance log (what works)
Snapshots: perf/<date>.json (from n8n read-only endpoint http://localhost:5678/webhook/jbs-stats-r2x — NEVER call the jbs-post-now webhook for stats). perf/2026-11-24-0526utc.json = the morning snapshot of the same day.
Rule: patterns need samples. Compare like with like (same format, similar posting slot, similar age ≥ 48 h). Call something a pattern only with ≥ 3 posts on each side; until then write "early signal".

## Status (24 Nov, 20:16 MYT snapshot)
- IG @japanbystation: 7 followers (6 this morning), 10 Reels. FB Page: 1 follower.
- NO post is ≥ 48 h old yet (oldest 43 h) → everything below is an EARLY SIGNAL; there are no patterns yet.
- FB numbers now come from the API: reactions, comments, post_media_view (= views), post_clicks. Not in the JSON: shares and post_total_media_view_unique (reach). We don't change n8n; Ling can ask for them to be added.

## IG Reels (age at snapshot · reach · avg watch · saves · shares · slot MYT · hook type)
| Reel (spec) | age | reach | watch s | saves | shares | slot | hook |
|---|---|---|---|---|---|---|---|
| Not sleeping early in Osaka? (osaka-night-owls) | 33 h | 1,269 | 9.5 | 16 | 9 | 23 Nov 11:01 | situation/problem + "before you book" |
| Staying in Namba? (namba) | 37 h | 401 | 11.5 | 14 | 3 | 23 Nov 07:00 | situation (where you already are) |
| Kuromon too crowded? (osaka-local-markets) | 25 h | 286 | 10.1 | 9 | 2 | 23 Nov 19:32 | problem + local alternative |
| First time in Osaka? (osaka-where-to-stay) | 39 h | 260 | 6.1 | 2 | 1 | 23 Nov 05:01 | generic first-timer |
| Just landed at KIX? (kansai-airport-which-train) | 43 h | 187 | 7.3 | 3 | 0 | 23 Nov 01:10 | situation (arrival) |
| Want local Osaka, not the neon? (osaka-live-like-a-local) | 12 h | 186 | 9.4 | 4 | 0 | 24 Nov 08:01 | contrast |
| Four friends: apartment or two rooms? (osaka-four-friends) | 35 h | 157 | 5.8 | 0 | 0 | 23 Nov 08:59 | A-or-B comparison |
| Solo on ¥5,000 a night? (namba-5000-yen-private-room) | 6 h | 150 | 5.7 | 0 | 0 | 24 Nov 14:14 | budget number |
| Cup Noodles Museum, ¥500 (cup-noodles-museum-ikeda) | 10 h | 134 | 7.0 | 1 | 1 | 24 Nov 10:48 | attraction + price |
| First night in Tokyo? Skip Shibuya Sky (shibuya-crossing-view) | 2 h | 124 | 7.5 | 0 | 0 | 24 Nov 18:08 | contrarian "skip X" (first Tokyo Reel) |

## FB (24 Nov snapshot; views = post_media_view)
- FB Reels: Kuromon 229 · Hotel says "Shinjuku"? (FB only, shinjuku-which-station) 210 · Cup Noodles 205 · Solo ¥5,000 138 · Night owls 112 · Shibuya 54 (2 h) · Tenma 8. Avg watch 3.7–7.1 s (Tenma 10.1 s on 5 plays).
- FB TEXT posts (fb-queue id → views): fb-tenma-1 18 · fb-local-1b 15 · fb-nakazaki-1 5 · fb-market-1 5 · fb-group-1 0 · fb-bullet-1 0 · fb-landing-1 0 (1 h old). 0 reactions and 0 clicks on all of them. A photo/guide share ("Second trip to Osaka?") got 11 views and the only 2 clicks.
- No "style" tags yet (variants start 27 Nov).

## Early signals (n = 10 Reels, none ≥ 48 h old, 7 followers)
1. Watch time and saves move together: the 4 Reels with avg watch ≥ 9.4 s got 4–16 saves; the 4 with ≤ 6.1 s got 0–2. The hooks that name a concrete traveller PROBLEM ("not sleeping early", "too crowded") are in the top group; the generic "first time" opener and the A-or-B comparison are in the bottom group. That's 2 v 2 comparable posts, so it's not a pattern yet.
2. One Reel (night owls) got about 4× the reach of the others. A single outlier is not a pattern, and the 11:00 MYT slot could explain it. Check whether other posts around 11:00 do better.
3. FB: Reels get 50–230 views from non-followers. Text posts get 0–18 views because the Page has 1 follower and text posts are mostly shown to followers. Our own FB text-style test (27–29 Nov) will be underpowered unless text posts reach people (see E3).

## Do more / Do less / Next experiments (read by the Reels and Facebook producers)
LING DECISION (24 Nov evening, permanent): Reels go to FAST + STRONG HOOK v4 (PLAYBOOK 3): 20–30 s, 50–70 words, hook in the first second with the answer, a new shot every 1.5–2.5 s. From 25 Nov this log compares v4 Reels against the older 33–40 s Reels.
Do more
- Problem-first hooks: name one specific annoyance or constraint the viewer has (crowds, late nights, luggage, closing times), then the local alternative.
- Put the practical, save-worthy payoff in the first 3 s (saves > likes on every Reel).
Do less
- Generic "First time in X?" openers, and A-or-B questions that don't tease the answer in the first seconds (both ≤ 6.1 s watch, 0–2 saves). Early signal only: keep about 1 in 5 as a control and don't drop them yet.
Next experiments
- E1 (Reels): a timely "X is back / opens this week" hook (seasonal light-ups, winter events). Tokyo Cheapo's two biggest recent Reels (631K and 499K vs ~70K usual) are a dated seasonal list and an "is back" event. Try 2 timely Reels this week and compare them with problem hooks.
- E2 (Reels): one visually striking single-place Reel near Osaka (Minoh / Katsuo-ji). A 34K account's best recent Reel did about 8× its median with exactly this kind of place.
- E3 (FB): check whether text posts reach anyone beyond followers: compare views on a photo+text post and a plain text post on the same day (the photo share already got the only clicks).
- E4 (FB): one "news you can use" text post (a rule, date or price that changes soon, verified at the official source). The most-shared text posts on 2 pages today were this kind.

## Pinterest (from Ling's screenshot, 25 Nov 15:11, account ~2 days old)
- Total: 75 impressions, 5 engagements, 0 outbound clicks, 0 saves. Top Pin by far: "Tenma, Osaka: where locals actually eat" (75); Hiroshima–Miyajima collage 3; Kyoto first-trip collage 3.
- Early signal only (new account; Pinterest usually takes weeks to start distributing): the one Pin that got shown is a FOOD + "where locals" + city keyword title. Keep practical, keyword-first titles; watch whether food/"where locals" Pins keep leading once there are 20+ Pins ≥ 7 days old.
