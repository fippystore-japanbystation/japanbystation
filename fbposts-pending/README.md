# FB posts waiting for their designed images (23 Nov 2026 run)
These six posts (briefs 44, 45, 47) are finished but NOT in site/fbposts yet, because this run could not reach Ling's Downloads folder to fetch the Pexels photos (folder access was not granted in the unattended run), and PLAYBOOK 2b says never post a plain photo.
To publish: for each JSON, get its `photo` (Pexels id) as described in PLAYBOOK 2b, run
`python3 fbimg.py <photo.jpg> "<image_title>" "<PLACE, TOKYO>" site/fbimg/<id>.jpg`, look at it, remove the `image_title` key, and move the JSON into site/fbposts/.
Places: quiet = "SHIBUYA, TOKYO"; asakusa = "ASAKUSA, TOKYO"; nippori = "NIPPORI, TOKYO".
A bundle with these photos (jbs_bundle_fb44.bin) was downloaded to Ling's Downloads by the built-in browser. Photo 8394475 (fb-nippori-2) is a Tokyo train with Skytree; check it reads as Tokyo before use.
