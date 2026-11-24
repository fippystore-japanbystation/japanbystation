# SEO / GEO log
Newest first. One block per run: queries seen, pages changed, new guides, indexing status, GEO checks.

## 2026-11-24 (scheduled SEO run 1)
- Search Console 28 days: still 0 in the 28-day view (data lag); last 24 h: 5 impressions, 0 clicks. Query: "station" "osaka" — 4 impressions, avg position 8.3. Pages: / (3), /osaka-live-like-a-local (1), /sakai-watch-knife-making (1).
- Page indexing: still "Processing data, check again in a day". Sitemap: Success, 65 discovered (66 after this deploy).
- NEW GUIDE (station hub #1): /osaka-station-vs-umeda "Osaka Station vs Umeda: Same Place? Which Side for Your Hotel" (keyword UMEDA): six stations explained, destination-first sides (West Gate for HARUKA platforms 21/24, Central Gate for Granvia, 3F bridge for RESPIRE, Hankyu Sanbangai airport bus ¥1,800 ≈60 min), one hotel per traveller, Hanshin ikayaki + Kushikatsu Matsuba, late-night bus, FAQ x4. Facts from kate.co.jp, hankyu.co.jp, osakastation-hotel.jp, osaka-info.jp, skybldg.co.jp (checked 24 Nov). Not verified (left out): JR gate for Hankyu/Metro by name, walk minutes to Higashi/Nishi-Umeda, Shin-Umeda Shokudogai opening year, ikayaki price.
- Hub linked from: nakazakicho-vs-umeda-hotel, osaka-hotels-by-budget, osaka-live-like-a-local, osaka-night-owls, tenma, osaka-four-friends, itami-sky-park, nifrel, minoh-falls (Keep planning), kansai-airport-to-osaka (Haruka card), osaka-where-to-stay (Umeda section).
- LINT: seo_title/seo_desc added to 14 guides; SEO-LINT 65 → 48 lines.
- Technical: 0 broken internal links; all images load on the new page, /, /guides, /osaka. IndexNow pinged 18 URLs. URL inspection → Request indexing for /osaka-station-vs-umeda.
- GEO: WebSearch "is Osaka Station the same as Umeda Station" and "Nakazakicho vs Umeda hotel cheaper walk Osaka Station" — japanbystation.com not in results (Wikipedia, japan-experience, gltjp, livejapan, explore.osaka rank). New hub answers in sentence 1 with checked numbers + FAQ.
- GEO follow-up (Ling asked "GEO 部分需要多improve", same day, 2nd deploy on his request):
  - Cloudflare AI Crawl Control, last 7 days: 571 AI-crawler requests, all allowed, 0 blocked. Meta-ExternalAgent 199, ClaudeBot (+2) 194, Googlebot (+1) 151, GPTBot (+2) 15, Applebot 5, BingBot 4, archive.org 3, PerplexityBot 0, CCBot 0. robots.txt allows every AI bot (no Cloudflare block prepended).
  - Gap: Bing crawled only 4 times, and a `site:japanbystation.com` web search returns nothing. ChatGPT search and Copilot lean on Bing → Ling should add the site to Bing Webmaster Tools (import from Search Console). That is his account, so we did not do it.
  - Built (then made invisible on Ling's request "不要影响到视觉": the box is no longer rendered; key facts now live only in JSON-LD "abstract" + llms.txt/llms-full.txt): "keyfacts" meta → a "Key facts" box right after the byline (quotable lines with numbers + check dates); "about" meta → TrainStation/Place entities with Wikipedia sameAs in the Article JSON-LD; llms.txt now opens with "Station guides (start here)" including their key facts.
  - Key facts added to: osaka-station-vs-umeda, nakazakicho-vs-umeda-hotel, tenma-tenjinbashisuji-local-guide. IndexNow pinged these + llms.txt/llms-full.txt.
  - Extra GEO check: "HARUKA platform Osaka Station underground West Gate which hotel closest" → not cited (osakastation-hotel.jp, Wikipedia, trip.com).
- NEXT: hub #2 Namba Station (which Namba: Nankai / Osaka Metro / Kintetsu-JR Namba, side for your hotel), then Shin-Osaka, Tennoji. Keep fixing lint (48 left: Tokyo/Hakone/Kawaguchiko titles, about/privacy descriptions). Recheck Page indexing.

## 2026-11-24 (setup, main session)
- Search Console: sitemap re-read 24 Nov, 65 URLs discovered; Page indexing still "processing". First query seen: "station" "osaka" — 4 impressions, avg position 8.3, 0 clicks.
- GA4 property "Japan by Station" (G-G13XXKV55G) live on every page, linked to Search Console.
- Built: dateModified from check dates, real sitemap lastmod, hub CollectionPage + ItemList, Pinterest in sameAs, srcset + fetchpriority hero (LCP p90 was 7.8 s), llms-full.txt, IndexNow key + all 65 URLs pinged.
- Cloudflare 7 days: 138 visits (MY 60 incl. our own checks, US 55, SE 8, UK 3, CA 3); referrers: direct 93, Facebook 43.
- TODO next run: guide for "station osaka" (Osaka Station vs Umeda), check Page indexing.
