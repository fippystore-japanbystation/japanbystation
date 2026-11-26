# Performance log (what works)
Snapshots: perf/<date>.json (from n8n read-only endpoint http://localhost:5678/webhook/jbs-stats-r2x — NEVER call the jbs-post-now webhook for stats). perf/2026-11-24-0526utc.json = the morning snapshot of the same day.
Rule: patterns need samples. Compare like with like (same format, similar posting slot, similar age ≥ 48 h). Call something a pattern only with ≥ 3 posts on each side; until then write "early signal".

## Goals (updated daily)
- **26 Nov 20:17 MYT: FB Page followers 2 / 5,000 (yesterday 1, +1) · website 65 visits in 24 h / 1,000 (yesterday 87, −25%)** · IG 15 followers (yesterday 11, +4).
- 25 Nov: FB 1 · web 87 · IG 11.
- Checkpoint 31 Dec: FB 500 · web 300/day. Needed pace: FB ≈ +14/day (actual +1/day) → OFF pace. Web: OFF pace and probably smaller than it looks (see FB→web below).

## Status (26 Nov, 20:17 MYT snapshot perf/2026-11-26.json)
- IG: 22 Reels, 15 followers. FB: 41 items (19 Reels, 22 text/photo posts), 2 followers.
- FB API now returns reactions, comments, post_media_view (views) and post_clicks; shares and reach (post_total_media_view_unique) are still NOT in the JSON (n8n not changed).
- fb-queue.json still has no "type"/"style" fields. Tagged by hand from the text: on 25–26 Nov the FIRST no-link posts ran (E5): 5 PLACE CARDS (-1 items: fb-odori-1, fb-joya-1, fb-nabana-1, fb-tenshiba-1, fb-gluhwein-1; ~270–380 characters, photo, question or follow line, no link) and 4 PRACTICAL-WITH-LINK (-2 items: fb-gluhwein-2, fb-tenshiba-2, fb-odori-2, fb-joya-2; ~930–1,030 characters + link). No guess-where yet.
- Website (Cloudflare, last 24 h, bots excluded): 65 visits, 69 page views. Referrers: direct 37, www.facebook.com 17, m.facebook.com 10, google 1. Top paths: / 16, kyoto-in-december-2026 8, osaka-christmas-markets-2026 6, tokyo-christmas-markets-2026 5, shinjuku-two-hours-before-dinner 4 (again = exactly the guides our newest FB posts link to). Countries: Malaysia 28, US 25, Ireland 6. Devices: Windows desktop 51 of 65.
- ⚠ FB→web is still UNVERIFIED and now looks mostly non-human: 27 "facebook.com" visits in 24 h, while the FB API shows 0–3 views and 0 clicks on every link post. GA4 (28 days to 25 Nov): 124 sessions; Organic Social 56 sessions with ~1 s average engagement; Organic Search 5 sessions, 10 s. A 1-second "visit" is a link-preview/scan or a bounce, not a reader. Malaysia (28) is probably our own team checking pages. Honest reading: real human visits are a small fraction of 65.
- Pinterest: no new data this run.

## IG Reels (26 Nov snapshot; reach · avg watch s · saves · shares · posted MYT · hook; v4 = FAST format from 25 Nov)
| Reel (spec) | age | reach | watch | saves | shares | posted | hook |
|---|---|---|---|---|---|---|---|
| Not sleeping early in Osaka? (osaka-night-owls) | 81 h | 1,286 | 9.5 | 16 | 9 | 23 Nov 11:01 | problem + "before you book" |
| Christmas markets in Tokyo: free or paid? (tokyo-christmas-markets-2026, v4) | 16 h | 817 | 6.4 | 13 | 9 | 26 Nov 04:25 | TIMELY seasonal + A-or-B with the answer |
| At Sapporo's airport, skip the ticket queue (new-chitose-airport-to-sapporo-v2, v4) | 13 h | 530 | 7.4 | 7 | 5 | 26 Nov 07:31 | "skip X" smart-travel, winter city |
| Staying in Namba? (namba) | 85 h | 406 | 11.7 | 14 | 3 | 23 Nov 07:00 | situation |
| First trip to Sapporo? Sleep in Odori (sapporo-where-to-stay-first-trip) | 43 h | 379 | 10.6 | 8 | 2 | 25 Nov 01:10 | first-timer + answer, winter city |
| Kuromon too crowded? (osaka-local-markets) | 73 h | 326 | 9.8 | 12 | 2 | 23 Nov 19:32 | problem + local alternative |
| Big suitcase into Sapporo? (new-chitose-airport-to-sapporo, v4) | 30 h | 312 | 9.1 | 4 | 1 | 25 Nov 14:19 | problem + answer, winter city |
| First time in Osaka? (osaka-where-to-stay) | 87 h | 260 | 6.1 | 2 | 1 | 23 Nov 05:01 | generic first-timer |
| Want local Osaka, not the neon? (osaka-live-like-a-local) | 60 h | 253 | 10.5 | 7 | 2 | 24 Nov 08:01 | contrast |
| Going to Sapporo before Christmas? (sapporo-in-december-2026, v4) | 23 h | 250 | 9.5 | 1 | 3 | 25 Nov 21:30 | timely seasonal question |
| Two of you, one afternoon: Minoh (minoh-falls-autumn-afternoon) | 47 h | 216 | 7.9 | 6 | 0 | 24 Nov 21:40 | situation + scenic place |
| Just landed at KIX? (kansai-airport-which-train) | 91 h | 188 | 7.5 | 4 | 0 | 23 Nov 01:10 | arrival situation |
| Solo on ¥5,000? (namba-5000-yen-private-room) | 54 h | 165 | 5.5 | 0 | 0 | 24 Nov 14:14 | budget number |
| Four friends: apartment or 2 rooms? (osaka-four-friends) | 83 h | 159 | 6.0 | 0 | 0 | 23 Nov 08:59 | A-or-B |
| Skip Shibuya Sky (shibuya-crossing-view) | 50 h | 158 | 7.5 | 1 | 0 | 24 Nov 18:08 | contrarian "skip X" |
| Skip midday at Senso-ji (sensoji-morning-or-evening, v4) | 26 h | 144 | 4.7 | 0 | 0 | 25 Nov 18:04 | "skip X" |
| Cup Noodles ¥500 (cup-noodles-museum-ikeda) | 57 h | 142 | 8.1 | 1 | 1 | 24 Nov 10:48 | attraction + price |
| Skip midday at Senso-ji, 2nd cut (sensoji-morning-or-evening-v2, v4) | 9 h | 138 | 5.1 | 0 | 0 | 26 Nov 10:48 | "skip X" |
| Quiet mornings near Shibuya (shibuya-quiet-base-yoyogi) | 37 h | 129 | 6.0 | 1 | 0 | 25 Nov 07:38 | stay-area |
| A few days in Kyoto? (kyoto-where-to-stay-first-trip) | 40 h | 124 | 4.7 | 1 | 0 | 25 Nov 04:22 | stay-area |
| Ring a temple bell in Kyoto (kyoto-in-december-2026, v4) | 6 h | 124 | 4.1 | 0 | 2 | 26 Nov 14:15 | timely seasonal, too young |
| Tokyo free city view 202 m (shinjuku-two-hours-before-dinner, v4) | 2 h | 83 | 3.9 | 0 | 0 | 26 Nov 18:06 | free + number, too young |

## FB (26 Nov snapshot; views = post_media_view)
- FB Reels ≥ 12 h old: most still get the ~190–235-view test (Kuromon 234, Kyoto 229, Sapporo Odori 222, Solo 213, Shinjuku 212, Shibuya Sky 209, Cup Noodles 209, Shibuya park 208, Sapporo airport v2 190, Sapporo Christmas 162). Avg watch 3–6 s. Reactions 0–2 (Kyoto 2).
- ⚠ 4 of 19 FB Reels got stuck near zero: Christmas markets 9 (while it is our #2 Reel on IG), Sapporo airport v1 22, Tenma 8, Senso-ji v1 0. No common cause visible in the data (slot, topic and length differ). Possible: FB processing/music/duplicate-content flag. Check in Meta Business Suite whether those Reels show a restriction notice.
- FB text/photo posts (22): 0–18 views, 0 reactions, 0 clicks, link or no link. New no-link PLACE CARDS (E5) got 0–3 views (odori-1 1, joya-1 2, nabana-1 1, tenshiba-1 3, gluhwein-1 0 at 1 h); same-day LINK posts got 0–2 (gluhwein-2 2, tenshiba-2 0, odori-2 2, joya-2 1). → With 2 followers, Facebook shows text/photo posts to almost nobody, whatever the style. The format test can't work until the Page has an audience (see Next experiments E7).
- New FB followers: +1 (2 total). Can't attribute it to a post (no per-post follow data); Reels are the only items that reached non-followers.

## Patterns (≥ 3 comparable posts per side, ≥ 48 h old)
P1 (25 Nov, IG Reels, old 33–40 s format, n = 3 v 3, weakest possible pattern): Reels whose hook names a SPECIFIC traveller problem/situation (night owls, staying in Namba, Kuromon too crowded) got 323–1,286 reach, 9.5–11.6 s watch, 11–16 saves. The generic first-timer, the A-or-B and the arrival-train Reels got 159–260 reach, 6.0–7.5 s, 0–4 saves. Confounds: all 6 are Osaka and posted 22–23 Nov; the night-owls outlier inflates reach. Saves track watch time on all 22 Reels. (26 Nov: numbers final, unchanged.)
P2 (26 Nov, FB, n = 22 text/photo posts v 15 unstuck Reels on the same Page, 23–26 Nov): on our Page, text/photo posts reach almost nobody (0–18 views; 9 new ones 0–3) while Reels get a ~200-view test. Holds for link AND no-link posts. This is a reach problem (2 followers), not a writing problem.

## Early signals (not patterns yet)
1. WINTER / CHRISTMAS / SAPPORO is our strongest topic now: the 5 winter Reels posted 24–26 Nov got 250–817 reach (median 379); the 9 non-winter Reels of the same days (≥ 20 h old) got 124–253 (median 144). Only 1 winter Reel is ≥ 48 h old, so this is still an early signal, but a strong one. Competitors agree (japan_walker_ Hokkaido 5.5×; Tokyo Cheapo dated illumination list).
2. TIMELY hook (E1) first result: "Christmas markets in Tokyo: free or paid?" = 817 reach, 13 saves, 9 shares in 16 h — our best Reel at that age. n = 1.
3. Senso-ji "skip midday" twice (two cuts) = 144 and 138 reach, 4.7–5.1 s, 0 saves. A famous-sight timing tip doesn't hook (n = 2, same topic).
4. "Where to stay in <area>" with no problem in the hook stays lowest on watch time (Kyoto 4.7 s, Shibuya park 6.0 s, Solo ¥5,000 5.5 s). n = 3.
5. v4 FAST format: 8 Reels so far; the 6 that are ≥ 9 h old have median reach ~280 vs ~200 for the 14 older-format Reels, but watch time is lower (4.7–9.5 s vs 5.5–11.7 s) and topics differ (most v4 Reels are winter). Can't separate format from topic yet; compare on 28 Nov.
6. FB Reels: 4 of 19 stuck near 0 views (see FB). Unexplained.

## Do more / Do less / Next experiments (read by the Reels and Facebook producers)
LING DECISION (24 Nov evening, permanent): Reels go to FAST + STRONG HOOK v4 (PLAYBOOK 3): 20–30 s, 50–70 words, hook in the first second with the answer, a new shot every 1.5–2.5 s.
Do more
- Problem-first hooks: name one specific annoyance or constraint (crowds, late nights, luggage, queues, closing times), then the fix (P1).
- Winter / Christmas / Hokkaido Reels through December, with dates and "free or paid?"-style answers in the hook (signals 1–2). Sapporo, Otaru, illuminations, Christmas markets first.
- "Crowd problem → quieter alternative" angle on Reels AND FB: now confirmed on 2 platforms at JapanTravel (FB 22.1K reactions; IG Reel 284K ≈ 16× usual).
- FREE things with a hands-on activity near Osaka/Kyoto (a competitor's free Katsuo-ji daruma stamp rally Reel = 292K, 4.5–16× usual on 2 accounts). We have fb-daruma / Minoh material: make a Reel of it.
- Put the save-worthy payoff in the first 3 s (saves track watch time on every Reel).
Do less
- Famous-sight timing tips with no twist (Senso-ji ×2 at ~140).
- Plain "where to stay in <area>" Reels with no problem in the hook; generic "First time in X?" openers (keep ~1 in 5 as a control).
- FB: more text/photo posts will not grow the Page by themselves while it has 2 followers (P2). Keep the 70/30 queue running for the style test, but the growth lever on FB right now is Reels.
- Selling / sponsored / "comment KEYWORD" / AI-sounding "Unlock the best…" openers: lowest on every account checked (5 accounts now).
Next experiments
- E7 (FB, NEW, start 27 Nov): make FB style variants visible. Since text posts get ~0 views, put the A/B/C text styles into the CAPTIONS of FB Reels (which get ~200 views each) and also judge them on reactions-per-view. Keep the text-post variants running too, but don't expect a verdict from 0–3-view posts.
- E8 (Reels, NEW): one "free + hands-on" Reel near Osaka (Katsuo-ji daruma / Minoh) with "free" and the activity in the first second. Compare reach/saves with the Minoh scenic Reel (216).
- E1 (Reels, running, 1 result = 817): 2 more timely "this December / is back / free or paid" Reels this week (Osaka Christmas markets, Kyoto New Year bells) to see if it repeats.
- E5 (FB, running since 25 Nov): place cards vs link posts — both 0–3 views so far; let it run to 29 Nov but judge it on Reels (E7).
- E6 (Reels): one "Is <premium thing> worth ¥X?" verdict Reel (Green Car, rapi:t Super Seat).
- E2 (Reels): single striking place near Osaka — 1 try (Minoh 216 = mid-pack); fold into E8.
- E3 (FB): photo + text vs plain text — superseded by P2 until the Page has followers.
- E4 (FB): one "news you can use" post (rule/date/price that changes soon). Competitor evidence keeps growing (Tokyo Cheapo "it's back" 111 shares; Japan Travel Tips tax-refund FAQ).
- Check (Ling or next run, read-only): open the 4 stuck FB Reels in Meta Business Suite and look for a restriction or copyright notice.

## Pinterest (from Ling's screenshot, 25 Nov 15:11, account ~2 days old)
- Total: 75 impressions, 5 engagements, 0 outbound clicks, 0 saves. Top Pin by far: "Tenma, Osaka: where locals actually eat" (75); Hiroshima–Miyajima collage 3; Kyoto first-trip collage 3.
- Early signal only (new account; Pinterest usually takes weeks to start distributing): the one Pin that got shown is a FOOD + "where locals" + city keyword title. Keep practical, keyword-first titles; watch whether food/"where locals" Pins keep leading once there are 20+ Pins ≥ 7 days old.


## PACE TEST (A = current style, B = theluns-style pauses + stacked list + "N ways" cover; started 26 Nov)
| topic | variant | posted | reach 24h | watch 24h | saves | shares | reach 48h | watch 48h |
|---|---|---|---|---|---|---|---|---|
| kansai-airport-to-kyoto | A (-pa, "visitors pay less", 68 words) | expected 27 Nov ~01:15 MYT | | | | | | |
| kansai-airport-to-kyoto | B (-pb, "3 ways", 59 words, stack + pauses) | target 29 Nov ~01:15 MYT (held, add on 28 Nov) | | | | | | |
| tokyo-to-kawaguchiko | B (-pb, "2 ways", 60 words, stack + pauses; posts FIRST) | expected 27 Nov ~04:25 MYT | | | | | | |
| tokyo-to-kawaguchiko | A (-pa, "bus for less than half", 68 words) | target 29 Nov ~04:25 MYT (held, add on 28 Nov) | | | | | | |


## SPLIT TEST ("Everyone goes to / Go here instead", started 26 Nov; key metric = shares)
| slug | posted | reach 24h | watch 24h | saves | shares | reach 48h | shares 48h | same-day normal Reels avg shares |
|---|---|---|---|---|---|---|---|---|


## ROUTE TEST (route-card carousels, started 26 Nov; key metrics = saves + shares)
| slug | posted | reach 24h | saves | shares | reach 48h | saves 48h | shares 48h | same-day Reels avg saves/shares |
|---|---|---|---|---|---|---|---|---|
| tokyo-night-walks (4 routes, carousel) | expected 27 Nov ~07:35 MYT | | | | | | | |
