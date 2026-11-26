import re, os, html
HERE=os.path.dirname(os.path.abspath(__file__)); SRC=os.path.join(HERE,"site"); OUT=os.path.join(HERE,"live")
P={"hero":28608380,"dotonbori":34729040,"shinsaibashi":32459950,"kuromon":2450697,"yasaka":27516858,"umeda_head":30037377,
   "umeda_sky":39459443,"station_city":20020111,"tennoji_head":34924739,"harukas":30944530,"zoo":32733152,"shinsekai":30999644,
   "glico":35183439,"crab":7631463,"takoyaki":12759815,"kix":32108257,"izumisano":39466513,"tokyo":5905666,"kyoto":40884563,"hokkaido":36595972,"nara":31047839}
def purl(k,w=1200): i=P[k]; return f"https://images.pexels.com/photos/{i}/pexels-photo-{i}.jpeg?auto=compress&cs=tinysrgb&w={w}"
def fiximg(s):
    s=re.sub(r'src="pexels:(\d+)(?::(\d+))?"', lambda m: f'src="https://images.pexels.com/photos/{m.group(1)}/pexels-photo-{m.group(1)}.jpeg?auto=compress&cs=tinysrgb&w={m.group(2) or 1200}"', s)
    s=re.sub(r'src="img/([a-z_]+)\.jpg"', lambda m: f'src="{purl(m.group(1), 1600 if m.group(1) in ("hero","glico","kix") else 1000)}"', s)
    return s
FAV="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='30' fill='%23ff6a4d'/%3E%3Ccircle cx='32' cy='32' r='12' fill='white'/%3E%3C/svg%3E"
NAV_CITIES=[]   # filled after guides are discovered: [(city, slug, count)]
def cslug(c): return re.sub(r"[^a-z0-9]+","-",c.lower()).strip("-")
def nav(active):
    def a(k,u,n): return f'<a href="{u}">{"<b>"+n+"</b>" if k==active else n}</a>'
    links=a("home","index.html","Home")+"".join(a("city-"+sl,sl+".html",c) for c,sl,n in NAV_CITIES)
    links+=a("guides","guides.html","All guides")+a("about","about.html","About")
    return '<nav class="nav" aria-label="Site"><a class="brand" href="index.html" style="text-decoration:none"><img src="/icons/favicon-96.png?v=2" alt="Japan by Station logo" width="34" height="34" class="brand-ic">Japan <i>by</i> Station</a><span class="links">'+links+'</span></nav>'
FOOT='''<footer>
  <div class="wrap">
    <p><b>Japan by Station</b> · Checked Japan travel answers, quick to read.</p>
    <p>Times are approximate, for the fastest regular train, and don't include waiting or walking inside big stations. We check them against operators and tourism bureaus and re-check every three months.</p>
    <p>Some links earn us a commission if you book, at no extra cost to you. <a href="disclosure.html">How we make money</a> · <a href="about.html">About</a> · <a href="privacy.html">Privacy</a></p>
    <p>Photos: Pexels contributors and Wikimedia Commons / Flickr photographers (CC licences), credited on each page.</p>
  </div>
</footer>
</body>
</html>'''
def head(title,desc):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title if (len(title)+19>65 or "Japan by Station" in title) else title+" | Japan by Station"}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:site_name" content="Japan by Station">
<link rel="icon" href="/favicon.ico?v=2" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="/icons/favicon-192.png?v=2">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png?v=2">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.pexels.com">
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet"></noscript>
<style>@font-face{{font-family:"Nunito Fallback";src:local("Arial");size-adjust:101.5%;ascent-override:99.6%;descent-override:34.8%;line-gap-override:0%}}.hero{{position:relative;overflow:hidden}}.hero>img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}</style>
<link rel="stylesheet" href="style.css?v={CSSV}">
<script nowprocket data-noptimize="1" data-cfasync="false" data-wpfc-render="false" seraph-accel-crit="1" data-no-defer="1" data-cmp-ab="2">
  (function () {{
      function go(){{
      var script = document.createElement("script");
      script.async = 1;
      script.setAttribute("data-cmp-ab","2");
      script.src = 'https://emrldtp.cc/NjA1MTU1.js?t=605155';
      document.head.appendChild(script);
      }}
      function later(){{ if (window.requestIdleCallback) requestIdleCallback(go,{{timeout:2500}}); else setTimeout(go,1200); }}
      if (document.readyState === "complete") later(); else window.addEventListener("load", later);
  }})();
  /* Microsoft Clarity (Ling 25 Nov): heatmaps + session recordings, loaded after the page */
  (function(){{
      function cl(){{ (function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","zj80uizxew"); }}
      if (document.readyState === "complete") setTimeout(cl,800); else window.addEventListener("load", function(){{ setTimeout(cl,800); }});
  }})();
</script>
</head>
<body>
'''
def body_of(fn):
    s=open(f"{SRC}/{fn}").read()
    a=s.index('<header class="hero">'); b=s.index('<footer>')
    return fiximg(s[a:b])
def relink(s):
    return s.replace('href="index.html#','href="osaka-where-to-stay.html#').replace('href="index.html"','href="osaka-where-to-stay.html"')
CSSV = "20"
pages={}
# ---- Osaka where to stay with traveller filter
osaka=relink(body_of("index.html"))
FILTER='''
<section class="wrap finder" aria-labelledby="h-finder">
  <h2 id="h-finder">Who's travelling?</h2>
  <p class="finder-sub">Pick the one that fits. We'll tell you where to stay and what to look for in the room.</p>
  <div class="chips" role="tablist" aria-label="Traveller type">
    <button role="tab" class="chip" data-k="first" aria-selected="true">First time in Japan</button>
    <button role="tab" class="chip" data-k="couple" aria-selected="false">Couple</button>
    <button role="tab" class="chip" data-k="family" aria-selected="false">Family with kids</button>
    <button role="tab" class="chip" data-k="group" aria-selected="false">4 friends</button>
    <button role="tab" class="chip" data-k="solo" aria-selected="false">Solo, on a budget</button>
    <button role="tab" class="chip" data-k="trips" aria-selected="false">Day trips</button>
  </div>
  <div class="answer-card" id="answer" aria-live="polite">
    <div class="ac-top"><span class="ac-eyebrow">Stay in</span><h3 id="ac-area">Namba</h3><p id="ac-why">The airport train ends here and Dotonbori is a 3–5 minute walk. The easiest first base.</p></div>
    <div class="ac-cols">
      <div><h4>Good</h4><ul id="ac-pros"><li>Kansai Airport in 34–39 min, no change</li><li>Food and nightlife on foot</li><li>Lots of hotels at every price</li></ul></div>
      <div><h4>Not so good</h4><ul id="ac-cons"><li>Kyoto day trips need one change</li><li>Busy and loud at night</li></ul></div>
    </div>
    <p class="ac-room"><b>Look for:</b> <span id="ac-room">A hotel within 5 minutes of Namba Station, so luggage day is easy.</span></p>
    <a class="btn ac-btn" id="ac-btn" href="#namba">See where to stay in Namba ↓</a>
  </div>
</section>
<script>
(function(){
var D={
 first:{a:"Namba",h:"#namba",why:"The airport train ends here and Dotonbori is a 3–5 minute walk. The easiest first base.",p:["Kansai Airport in 34–39 min, no change","Food and nightlife on foot","Lots of hotels at every price"],c:["Kyoto day trips need one change","Busy and loud at night"],r:"A hotel within 5 minutes of Namba Station, so luggage day is easy."},
 couple:{a:"Namba",h:"#namba",why:"Evenings are the best part of Osaka, and Namba is where they happen. Walk home from dinner along the canal.",p:["Dotonbori and Hozenji Yokocho on foot","Bars and late food everywhere","Direct airport train"],c:["Crowded on weekends","Rooms are often compact"],r:"A double room on a higher floor, away from the main street, for a quieter night."},
 family:{a:"Tennoji",h:"#tennoji",why:"30 minutes from the airport with no change, a zoo and park next door, and usually lower prices than Namba or Umeda.",p:["Kansai Airport in 30 min, no change","Tennoji Zoo 5–10 min on foot","Abeno Harukas for rainy days"],c:["Kyoto needs a change at Osaka Station","Less nightlife (fine with kids)"],r:"An apartment-style hotel or family room with separate beds, so everyone gets some privacy. Ask about cots before booking."},
 group:{a:"Namba",h:"#namba",why:"Four people can split an apartment-style hotel and still walk to everything. Splitting a bigger room often beats two doubles.",p:["Easy to meet up and split up","Food for every budget","Direct airport train"],c:["Apartment rooms book out early","Weekends are busy"],r:"An apartment hotel with two bedrooms or four real beds, not sofa beds. Check the bed layout in the room photos."},
 solo:{a:"Tennoji",h:"#tennoji",why:"Cheaper rooms, a direct airport train and Namba only 5–6 minutes away by subway when you want the neon.",p:["Usually lower prices","Kansai Airport in 30 min","Nara direct in 30–36 min"],c:["Quieter in the evening","Kyoto needs one change"],r:"A compact single near Tennoji Station. Being close to the station matters more than room size when you're alone."},
 trips:{a:"Umeda",h:"#umeda",why:"JR Osaka Station is here, with direct trains to Kyoto in 29 minutes and Universal Studios in about 15.",p:["Kyoto 29 min, direct","Universal Studios ≈15 min","Airport express stops here"],c:["Dotonbori is a subway ride away","The station is huge"],r:"A hotel on the same side of Osaka Station as the JR gates, so early trains are easy."}
};
var chips=document.querySelectorAll('.finder .chip');
function li(a){return a.map(function(x){return '<li>'+x+'</li>'}).join('')}
function show(k){var d=D[k];if(!d)return;
 chips.forEach(function(c){c.setAttribute('aria-selected',c.dataset.k===k?'true':'false')});
 document.getElementById('ac-area').textContent=d.a;document.getElementById('ac-why').textContent=d.why;
 document.getElementById('ac-pros').innerHTML=li(d.p);document.getElementById('ac-cons').innerHTML=li(d.c);
 document.getElementById('ac-room').textContent=d.r;var b=document.getElementById('ac-btn');b.href=d.h;b.textContent='See where to stay in '+d.a+' ↓';
 document.getElementById('answer').dataset.area=d.a.toLowerCase();}
chips.forEach(function(c){c.addEventListener('click',function(){show(c.dataset.k)})});
var h=(location.hash||'').replace('#for-','');if(D[h]){show(h);setTimeout(function(){document.getElementById('h-finder').scrollIntoView({behavior:'smooth',block:'start'})},150);}
})();
</script>
'''
osaka=osaka.replace('<p class="byline wrap">Times checked 22 November 2026</p>','<p class="byline wrap">Times checked 22 November 2026</p>'+FILTER,1)
osaka=osaka.replace('<span class="kicker">Osaka · Where to stay</span>','<span class="kicker">Osaka · Where to stay</span>')
ONEMORE_OSAKA='<div class="onemore" style="margin:28px auto"><h2 id="h-one" style="margin-top:0;font-size:24px">One more thing: a 1920s street under a skyscraper</h2><p>If you stay in Umeda, go down to the basement of the Umeda Sky Building to <b>Takimi Koji</b>, a food alley built to look like an Osaka street from the early Showa era, with cobblestones, tiled roofs, old posters and a small shrine. Around 20 restaurants serve okonomiyaki, kushikatsu and other Osaka staples, and you can wander it for free after the sunset from the rooftop.</p><p class="small">Takimi Koji, Umeda Sky Building B1F, 1-1-88 Oyodonaka, Kita-ku; about 7–9 min from JR Osaka Station. Hours vary by restaurant. Sources: Osaka Convention &amp; Tourism Bureau (osaka-info.jp), GLTJP. Checked 23 November 2026.</p></div>'
osaka=osaka.replace('<h2 style="margin-top:28px;font-size:26px">Keep planning Osaka',ONEMORE_OSAKA+'<h2 style="margin-top:28px;font-size:26px">Keep planning Osaka',1)
pages["osaka-where-to-stay.html"]=(head("Where to Stay in Osaka: Namba, Umeda or Tennoji","Where to stay in Osaka: Namba, Umeda or Tennoji for first-timers, couples and families, with walking times to the sights and minutes to the airport and Kyoto."),"city-osaka",osaka)
pages["namba.html"]=(head("Things to Do Near Namba Station, Osaka: All Walkable","From Namba Station Exit 14, Dotonbori is 3–5 minutes on foot, Kuromon Market about 8, and the Shinsaibashi-suji arcade starts right at the canal."),"city-osaka",relink(body_of("namba.html")))
pages["kansai-airport-to-osaka.html"]=(head("Kansai Airport to Osaka: Which Train for Your Hotel","Nankai or JR? Kansai Airport to Namba, Tennoji, Osaka Station and Shin-Osaka with travel times and fares, picked by where your hotel is."),"city-osaka",relink(body_of("kansai-airport-to-osaka.html")))
# ---- Home
import re as _re
home=open(os.path.join(HERE,"home.html")).read()
home=_re.sub(r"\{img:([a-z_]+):(\d+)\}", lambda m: purl(m.group(1), int(m.group(2))), home)
pages["index.html"]=(head("Japan by Station: Checked Japan Travel Guides That Save Time","Japan travel answers you can trust: the quick answer first, every time and price checked, plus the local places most lists miss. Stay, eat and get around Japan."),"home",home)
def simple(title,h1,inner):
    return f'''
<main class="wrap doc">
  <h1>{h1}</h1>
  {inner}
</main>
'''
pages["about.html"]=(head("About Japan by Station (japanbystation.com)","Japan by Station is an independent English guide to Japan: quick, carefully checked answers to real trip questions, plus the local places most lists miss."),"about",simple("About","About Japan by Station",'''
  <p><b>Japan by Station</b> (japanbystation.com) is an independent English guide to Japan. We do the checking so you don't have to, and we keep it short, so you can decide in a minute and get back to planning the fun part. We're on Instagram, Facebook and Pinterest as <b>@japanbystation</b>.</p>
  <p>Every guide starts with the quick answer to one real trip question: where to stay, what to eat near the station, which train, what to do with a free afternoon. Then come the details that make it work, and the things most lists miss: the lunch counter locals queue for, the quieter exit, the free view at sunset.</p>
  <h2>How we check our facts</h2>
  <p>Train times come from the operators themselves, the airports and city tourism bureaus wherever they publish them. When we can only find a figure in travel guides, we say so. Each guide shows the date we checked it, and we re-check every three months.</p>
  <p>We have not stayed in every area or hotel we write about, and we don't pretend to. Our guides are built from published timetables, maps and official sources, not from paid stays.</p>
  <h2>Photos</h2>
  <p>Our photos come from Pexels and, for real photos of a specific market, shop or dish, from Wikimedia Commons and Flickr under Creative Commons licences. Each photo is credited to its photographer, with its licence, on the page where it appears.</p>
  <h2>Contact</h2>
  <p>Spotted a wrong time or a closed attraction? Send us a message on Instagram at <b>@japanbystation</b> and we'll fix it.</p>
'''))
pages["disclosure.html"]=(head("How We Make Money","Japan by Station earns commissions from some booking links (Booking.com, Agoda, Klook). How it works, and why it never changes your price or our picks."),"",simple("","How we make money",'''
  <p>Some links on Japan by Station go to booking sites such as Agoda, Booking.com and Klook. If you book through one of those links, we may earn a small commission. You pay the same price either way.</p>
  <p>Commissions never decide which area we recommend. We recommend areas based on train times, walking distances and who is travelling. If an area isn't a good fit for you, we say so, even when it would be easier to sell.</p>
  <p>These commissions pay for keeping our guides checked and up to date.</p>
'''))
pages["privacy.html"]=(head("Privacy Policy","How Japan by Station handles your data on japanbystation.com and on Instagram: site analytics, booking-site cookies, Instagram comments and messages."),"",simple("","Privacy Policy",'''
  <p><i>Last updated 25 November 2026.</i> Japan by Station runs japanbystation.com and the Instagram account <b>@japanbystation</b>. This policy explains what data we handle and why.</p>
  <h2>On this website</h2>
  <p>We don't ask you to create an account, and we don't collect your name or email on this site. We use Cloudflare Web Analytics, which counts visits without cookies and without identifying you, and Google Analytics, which uses cookies to show us anonymous totals such as which countries visitors come from and which pages they read. We don't use it for advertising. We also use Microsoft Clarity to see, without identifying you, how pages are used (where people scroll and tap, and anonymised recordings of visits) so we can make the guides easier to read; Clarity masks text you type and uses cookies. See <a href="https://privacy.microsoft.com/privacystatement" rel="noopener">Microsoft's privacy statement</a>. You can opt out with Google's <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">Analytics opt-out add-on</a> or by blocking cookies in your browser. Our hosting provider, Cloudflare, may log basic technical data such as IP addresses to keep the site secure.</p>
  <p>When you click a booking link, the booking site may set cookies so it can tell that you came from us. That is how affiliate commissions are tracked. Those cookies belong to the booking site and are covered by its own privacy policy.</p>
  <h2>On Instagram (comments and direct messages)</h2>
  <p>Our Reels invite you to comment a keyword, such as AIRPORT, to receive the matching guide. When you do, our app "Japan by Station DM" uses the Instagram API to read comments on our own posts, check whether the comment contains one of our keywords, and send you one direct message with the link to that guide. We may also reply publicly under your comment.</p>
  <p>To do this we process your Instagram username, the comment ID, the comment text and the time it was posted. We keep a record of which comment IDs we have already answered so you don't get the same message twice. We do not sell this data, use it for advertising, or share it with anyone except Meta, which delivers the message. Records of answered comments are deleted automatically when they are no longer needed, and at the latest after 12 months.</p>
  <p>If you reply to our message, we read your reply in our Instagram inbox to answer your question.</p>
  <h2>Deleting your data</h2>
  <p>You can ask us to delete any data we hold about you at any time. See <a href="data-deletion.html">how to request data deletion</a>.</p>
  <h2>Contact</h2>
  <p>Questions about this policy? Send a direct message to <b>@japanbystation</b> on Instagram.</p>
'''))
pages["data-deletion.html"]=(head("Data Deletion Instructions","How to ask Japan by Station to delete the data we hold about you from Instagram comments and messages. We delete it within 7 days and confirm."),"",simple("","Data deletion instructions",'''
  <p>Japan by Station keeps very little data: if you commented a keyword on one of our Instagram posts, we keep your Instagram username and the ID of that comment so we don't message you twice.</p>
  <h2>How to request deletion</h2>
  <ol>
    <li>Send a direct message to <b>@japanbystation</b> on Instagram with the words <b>"Delete my data"</b>.</li>
    <li>We delete every record linked to your Instagram username within 7 days and reply to confirm.</li>
  </ol>
  <p>You can also delete your own comment on our post at any time. Deleting the comment does not delete the message we already sent you; you can delete that conversation in your Instagram inbox.</p>
  <p>See our <a href="privacy.html">privacy policy</a> for details.</p>
'''))

# ---- Auto guides: site/guides/<slug>.html with a <!--meta {json} --> header
import json as _jj, glob as _glob
GMETA={}
for _f in sorted(_glob.glob(f"{SRC}/guides/*.html")):
    _raw=open(_f).read()
    _m=re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*", _raw, re.S)
    if not _m: continue
    _meta=_jj.loads(_m.group(1)); _slug=os.path.basename(_f)
    _meta["slug"]=_slug; GMETA[_slug]=_meta
    _body=fiximg(_raw[_m.end():])
    # GEO (24 Nov, Ling: must not change what readers see): "keyfacts" are NOT shown on the page; they go into the Article JSON-LD "abstract" and llms.txt / llms-full.txt only.
    if _meta.get("faq"):
        _body+='<section class="wrap sec faq" aria-labelledby="h-faq"><h2 id="h-faq">Quick answers</h2>'+''.join(f'<details><summary>{html.escape(q)}</summary><p>{a}</p></details>' for q,a in _meta["faq"])+'</section>'
    if _meta.get("sources"):
        _body+=f'<section class="wrap sec sources"><p class="small">Sources: {_meta["sources"]}</p></section>'
    pages[_slug]=(head(_meta.get("seo_title",_meta["title"]),_meta.get("seo_desc",_meta["desc"])),"city-"+cslug(_meta["city"]),_body)
# ---- Station clusters (Ling 25 Nov: social visitors open station pages; keep them exploring the same station)
try: _ST=_jj.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"stations.json")))
except Exception: _ST={}
_CL={}
for _s,_m in GMETA.items():
    for _st in (_m.get("stations") or _ST.get(_s[:-5]) or []): _CL.setdefault(_st,[]).append(_s)
for _s,_m in GMETA.items():
    _blocks=""
    for _st in (_m.get("stations") or _ST.get(_s[:-5]) or [])[:2]:
        _others=[o for o in _CL.get(_st,[]) if o!=_s][:4]
        if not _others: continue
        _lis="".join(f'<li><a href="{o}"><b>{html.escape(GMETA[o]["title"])}</b><span>{html.escape(GMETA[o].get("card",GMETA[o].get("desc",""))[:110])}</span></a></li>' for o in _others)
        _lab=_st if any(w in _st for w in ("Airport","Station","Day trips")) else _st+" Station"
        _hd=_lab if _lab.startswith("Day trips") else "More around "+_lab
        _blocks+=f'<section class="wrap sec around" aria-label="{html.escape(_hd)}"><h2>{html.escape(_hd)}</h2><ul class="around-list">{_lis}</ul></section>'
    if _blocks:
        _h,_c,_b=pages[_s]
        _i=_b.find('<section class="wrap sec faq"')
        pages[_s]=(_h,_c,(_b[:_i]+_blocks+_b[_i:]) if _i>=0 else _b+_blocks)
# ---- Follow block (Ling 25 Nov: grow FB to 5,000 followers; turn website readers into followers)
_FOLLOW=('<section class="wrap sec follow-us" aria-label="Follow Japan by Station"><p><b>Planning Japan?</b> We share one useful station tip a day, plus December markets and lights. '
         '<a class="fb" href="https://www.facebook.com/1512969825226649" target="_blank" rel="noopener">Follow on Facebook</a> '
         '<a class="ig" href="https://www.instagram.com/japanbystation/" target="_blank" rel="noopener">Instagram</a></p></section>')
for _s in GMETA:
    _h,_c,_b=pages[_s]
    if 'follow-us' in _b: continue
    _i=_b.find('<section class="wrap sec faq"')
    pages[_s]=(_h,_c,(_b[:_i]+_FOLLOW+_b[_i:]) if _i>=0 else _b+_FOLLOW)
# ---- First-screen value + tip toast + scroll tracking (Ling 25 Nov: avg engagement ~1 s from social clicks)
_TTJS='<script>(function(){try{var t=document.getElementById("tiptoast");if(t){var shown=false;function show(){if(shown)return;shown=true;try{if(sessionStorage.getItem("jbs_tt"))return}catch(e){}t.hidden=false;try{sessionStorage.setItem("jbs_tt","1")}catch(e){};if(window.gtag)gtag("event","tip_shown")}setTimeout(function(){if((document.documentElement.scrollTop||0)<200)show()},7000);window.addEventListener("scroll",function(){if(shown&&(document.documentElement.scrollTop||0)>600)t.hidden=true},{passive:true});t.querySelector(".tt-x").onclick=function(){t.hidden=true}}var marks=[25,50,75],done={};window.addEventListener("scroll",function(){var h=document.documentElement,p=(h.scrollTop+innerHeight)/h.scrollHeight*100;marks.forEach(function(m){if(p>=m&&!done[m]){done[m]=1;if(window.gtag)gtag("event","scroll_depth",{percent:m})}})},{passive:true});setTimeout(function(){if(window.gtag)gtag("event","engaged_15s")},15000)}catch(e){}})();</script>'
def _plain(x): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',x))).strip()
def _first_sents(t,n=2,maxc=230):
    ss=re.split(r'(?<=[.!?])\s+',t); out=''
    for x in ss[:n]:
        if len(out)+len(x)>maxc and out: break
        out=(out+' '+x).strip()
    return out
for _s,_m in GMETA.items():
    _h,_c,_b=pages[_s]
    if 'quick-answer' in _b: continue
    _q=''
    _mv=re.search(r'id="h-v".*?class="tipbox"[^>]*>(.*?)</div>',_b,re.S)
    if _mv: _q=re.sub(r'^We suggest:\s*','',_plain(_mv.group(1)))
    if not _q:
        _ml=re.search(r'<p class="lede[^"]*">(.*?)</p>',_b,re.S)
        if _ml: _q=_plain(_ml.group(1))
    _q=_first_sents(_q) if _q else ''
    if _q: _q=_q[0].upper()+_q[1:]
    _tip=''
    _mb=re.search(r'id="h-book".*?<li>(.*?)</li>',_b,re.S)
    if _mb: _tip=_first_sents(_plain(_mb.group(1)),1,170)
    elif _m.get("keyfacts"): _tip=_first_sents(_plain(str(_m["keyfacts"][0])),1,170)
    if len(_tip)>120:   # keep the toast small: cut at a natural break
        _cut=max(_tip.rfind(x,0,118) for x in (': ',', ',' (',' — ',' – '))
        _tip=(_tip[:_cut] if _cut>40 else _tip[:115].rsplit(' ',1)[0]).rstrip(' :,(–—')+'…'
    _tiplink='<a href="#h-book">More ↓</a>' if 'id="h-book"' in _b else ''

    if _q:
        _more='<a href="#h-v">Why we say this ↓</a>' if 'id="h-v"' in _b else ''
        _card=f'<div class="quick-answer"><b>💡 The quick answer</b><p>{html.escape(_q)}</p>{_more}</div>'
        _i=_b.find('</h1>')
        if 0<_i<_b.find('</header>'):
            _b=_b[:_i+5]+_card+_b[_i+5:]
    if _tip:
        _b+=f'<div class="tiptoast" id="tiptoast" hidden><button class="tt-x" aria-label="Close tip" type="button">×</button><b>Good to know</b><span>{html.escape(_tip)} {_tiplink}</span></div>'
    _b+=_TTJS
    pages[_s]=(_h,_c,_b)
# older hand-built guides, so they show in lists
LEGACY=[{"slug":"osaka-where-to-stay.html","title":"Where to stay in Osaka: Namba, Umeda or Tennoji?","card":"Three areas on one red subway line. What's outside each door, and who each one suits.","city":"Osaka","cat":"Where to stay","tag":"coral","hero":30037377,"date":"2026-11-22","keyword":"OSAKA"},
        {"slug":"namba.html","title":"Things to do around Namba, all within a 15-minute walk","card":"The canal, the food streets and the shopping arcades, with walking times from Exit 14.","city":"Osaka","cat":"Things to do","tag":"sun","hero":35183439,"date":"2026-11-22","keyword":"NAMBA"},
        {"slug":"kansai-airport-to-osaka.html","title":"Kansai Airport to Osaka: which train for your hotel","card":"Nankai or JR? Pick the line that stops at your hotel and skip the transfer.","city":"Osaka","cat":"Getting there","tag":"sky","hero":39466513,"date":"2026-11-22","keyword":"AIRPORT"}]
ALLG=sorted(list(GMETA.values())+LEGACY, key=lambda g:(g.get("date",""),g.get("order",0)), reverse=True)
def _card(g):
    img=f'https://images.pexels.com/photos/{g["hero"]}/pexels-photo-{g["hero"]}.jpeg?auto=compress&cs=tinysrgb&w=900'
    d=g.get("date",""); 
    try:
        import datetime as __d; dd=__d.date.fromisoformat(d).strftime("%-d %b %Y")
    except Exception: dd=d
    return (f'<a class="post" href="{g["slug"]}"><div class="post-img"><img src="{img}" alt="{html.escape(g.get("hero_alt",g["title"]))}" loading="lazy"></div>'
            f'<div class="post-tx"><span class="tag tag-{g.get("tag","coral")}">{html.escape(g["cat"])}</span><h3>{html.escape(g["title"])}</h3><p>{html.escape(g["card"])}</p><small>{g["city"]} · checked {dd}</small></div></a>')
# home: "Start with your situation" (3 hand-picked guides) + latest 6 (excluding those 3) + city counts
SITUATIONS=[("namba-5000-yen-private-room.html","I have ¥5,000 a night.",31728406,"A compact hotel room","What ¥5,000 really buys near Namba on a weeknight vs a Saturday."),
            ("osaka-night-owls.html","I want to walk home after midnight.",37619882,"People walking through an Osaka izakaya street at night","Where to sleep so the last train doesn't matter."),
            ("osaka-four-friends.html","There are four of us.",11062799,"Three beds in one apartment room","One apartment or two hotel rooms: how we'd decide.")]
_live=set(GMETA)|{g["slug"] for g in LEGACY}
_sit=[x for x in SITUATIONS if x[0] in _live]
_sith=""
if _sit:
    _sith='<section class="wrap sec" aria-labelledby="h-sit"><div class="sec-h"><span class="tape t-coral">Start here</span><h2 id="h-sit">Start with your situation</h2></div><div class="situations">'
    for slug,q,ph,alt,sub in _sit:
        _sith+=(f'<a class="sit" href="{slug}"><div class="sit-img"><img src="https://images.pexels.com/photos/{ph}/pexels-photo-{ph}.jpeg?auto=compress&cs=tinysrgb&w=700" alt="{html.escape(alt)}" loading="lazy"></div>'
                f'<div class="sit-tx"><q>{html.escape(q)}</q><p>{html.escape(sub)}</p><span class="sit-go">Read the answer →</span></div></a>')
    _sith+='</div></section>'
_used={x[0] for x in _sit}
_latest=[g for g in ALLG if g["slug"] not in _used][:6]
_h=pages["index.html"]
_body=re.sub(r'(<div class="posts">).*?(</div>\s*</section>)', lambda m: m.group(1)+''.join(_card(g) for g in _latest)+m.group(2), _h[2], count=1, flags=re.S)
_body=_body.replace('{{SITUATIONS}}',_sith)
def _cnt(c):
    n=sum(1 for g in ALLG if g["city"]==c); return f"{n} guide{'s' if n!=1 else ''} →"
_cities=[]
for _g in ALLG:
    if _g["city"] not in _cities: _cities.append(_g["city"])
_CITYIMG={"Osaka":"dotonbori","Tokyo":"tokyo","Kyoto":"kyoto","Hokkaido":"hokkaido","Nara":"nara"}
_cc=""
for _c,_sl,_n in sorted([(c,cslug(c),sum(1 for g in ALLG if g["city"]==c)) for c in _cities], key=lambda x:-x[2]):
    _im=purl(_CITYIMG[_c],800) if _c in _CITYIMG else f'https://images.pexels.com/photos/{next(g["hero"] for g in ALLG if g["city"]==_c)}/pexels-photo-{next(g["hero"] for g in ALLG if g["city"]==_c)}.jpeg?auto=compress&cs=tinysrgb&w=800'
    _cc+=f'<a class="city2 live" href="{_sl}.html"><img src="{_im}" alt="Travel guides for {_c}, Japan" loading="lazy"><span><b>{_c}</b><small>{_cnt(_c)}</small></span></a>'
for _c,_lab in (("Kyoto","Up next"),("Hokkaido","On our list")):
    if _c not in _cities: _cc+=f'<div class="city2"><img src="{purl(_CITYIMG[_c],800)}" alt="Travel guides for {_c}, Japan" loading="lazy"><span><b>{_c}</b><small>{_lab}</small></span></div>'
_body=re.sub(r'<div class="cities2">.*?</div>\s*</section>', lambda m:'<div class="cities2">'+_cc+'</div>\n  </section>', _body, count=1, flags=re.S)
_tok=sum(1 for g in ALLG if g["city"]=="Tokyo")
_tc=(f'<a class="city2 live" href="guides.html#tokyo"><img src="{purl("tokyo",800)}" alt="Shibuya Crossing at twilight" loading="lazy"><span><b>Tokyo</b><small>{_cnt("Tokyo")}</small></span></a>' if _tok else
     f'<div class="city2"><img src="{purl("tokyo",800)}" alt="Shibuya Crossing at twilight" loading="lazy"><span><b>Tokyo</b><small>Writing now</small></span></div>')

pages["index.html"]=(_h[0],_h[1],_body)
# all-guides index grouped by city
_cities=[]
for g in ALLG:
    if g["city"] not in _cities: _cities.append(g["city"])
_gi='<header class="hero hero-lite"><div class="wrap"><span class="kicker">All guides</span><h1>Every Japan by Station guide</h1><p>Where to stay, how to get around and what is worth your time, city by city. Newest first.</p></div></header><main>'
for c in _cities:
    _gi+=f'<section class="wrap sec" id="{c.lower()}" aria-labelledby="h-{c.lower()}"><div class="sec-h"><h2 id="h-{c.lower()}">{c}</h2></div><div class="posts">'+''.join(_card(g) for g in ALLG if g["city"]==c)+'</div></section>'
_gi+='</main>'
pages["guides.html"]=(head("All Japan Travel Guides","Japan travel guides by city and station: where to stay in Tokyo, Osaka, Kyoto and Sapporo, airport trains, which exit to use, local food and day trips."),"guides",_gi)

import re as _hre
_CORE=_hre.compile(r"(?i)first trip|which area should you stay|where to stay in|where to stay:|airport to|narita or haneda|getting around|kansai airport")
_AWAY=_hre.compile(r"(?i)hakone|kawaguchi|fuji|minoh|nara|nikko|kamakura|miyajima|otaru")
def _hub_groups(gs):
    core=[g for g in gs if _CORE.search(g["title"]) and "¥" not in g["title"] and g["cat"] in ("Where to stay","Getting there","Getting around")]
    core.sort(key=lambda g:(0 if _hre.search(r"(?i)first trip|which area|namba, umeda or tennoji",g["title"]) else 1 if g["cat"]=="Where to stay" else 2 if g["cat"]=="Getting there" else 3))
    rest=[g for g in gs if g not in core]
    away=[g for g in rest if g["cat"] in ("Day trip","Day trips") or _AWAY.search(g["title"])]
    away.sort(key=lambda g:0 if _hre.search(r"(?i)hakone|fuji|kawaguchi|minoh|nara|cup noodles",g["title"]) else 1)
    rest=[g for g in rest if g not in away]
    eat=[g for g in rest if g["cat"] in ("Food","Local food","Neighbourhood guide","Things to do")]
    rest=[g for g in rest if g not in eat]
    return [("big","Start here","t-coral","The big questions first","Where to stay, how to get in from the airport and how to get around. Read these before anything else.",core),
            ("eat","Eat & explore","t-mint","Eat and explore like a local","Food streets, neighbourhoods and the things worth your time.",eat),
            ("away","Day trips","t-sun","Day trips and nights away","Easy escapes from the city, with the train times worked out.",away),
            ("tips","Small questions","t-lilac","Smart answers for specific situations","Budget, groups, late nights, big suitcases and the little decisions that make a trip smoother.",rest)]
HUBMETA={  # Ling 25 Nov: hub snippets must answer straight away, no "Every Japan by Station guide..."
 "Osaka":("Osaka Travel Guide: Where to Stay, Airport Trains, Food","Where to stay in Osaka (Namba, Umeda, Tennoji or Tenma), which train from Kansai Airport, where locals eat, and easy day trips like Minoh and Nara."),
 "Tokyo":("Tokyo Travel Guide: Where to Stay, Airports, Getting Around","Where to stay in Tokyo on a first trip, Narita or Haneda to your hotel, IC card or subway pass, food halls and quiet neighbourhoods for a half day."),
 "Kyoto":("Kyoto Travel Guide: Where to Stay, Airport, Kyoto Station","Where to stay in Kyoto (station, Gion or Karasuma), Kansai Airport to Kyoto, which Kyoto Station exit, the best time for Fushimi Inari, December events."),
 "Hokkaido":("Sapporo Travel Guide: Where to Stay, Airport Train, Food","Where to stay in Sapporo (station, Odori or Susukino), New Chitose Airport to the city, where locals eat, Otaru, and Sapporo's December lights."),
 "Nara":("Nara Day Trip: Deer, Temples and Trains","Nara from Osaka or Kyoto: day trip or one night, which station to use, and how to see the deer park, Todaiji's Great Buddha and a quiet evening."),
 "Okinawa":("Naha, Okinawa Guide: Where to Stay, Do You Need a Car?","Where to stay in Naha on a first trip to Okinawa (Kokusai-dori, Asahibashi or Omoromachi), how far the Yui Rail monorail gets you, and when you need a car."),
 "Hiroshima":("Hiroshima and Miyajima in One Day: Base, Tram or Train","Hiroshima and Miyajima in one day: where to base yourself, tram or train, and how the tides change your visit to the floating torii."),
 "Nagoya":("Nagoya Day Trips: Nabana no Sato Illumination 2026","Nabana no Sato's 2026–27 winter illumination: open 17 Oct to 31 May, December advance tickets ¥3,000, and the easy day trip from Nagoya or Osaka."),
 "Japan":("Japan Travel Guide: Christmas Food 2026 and Seasonal Tips","Japan-wide tips for any city: Christmas 2026 food (strawberry shortcake, jidori legs, Nagoya wings, shanmeri), konbini cake pick-up 19–25 Dec, where to buy."),
 "Fukuoka":("Fukuoka Travel Guide: Where to Stay, Yatai, Local Food","Where to stay in Fukuoka (Hakata, Tenjin or Nakasu), how the yatai food stalls work, and what to eat beyond tonkotsu ramen."),
}
for _c in _cities:
    _gs=[g for g in ALLG if g["city"]==_c]; _sl=cslug(_c)
    NAV_CITIES.append((_c,_sl,len(_gs)))
    _grp=[x for x in _hub_groups(_gs) if x[5]]
    _jump='<nav class="hubjump" aria-label="Sections">'+''.join(f'<a href="#{k}">{lab}</a>' for k,lab,_t,_h2,_p,_l in _grp)+'</nav>' if len(_grp)>1 else ''
    _secs=''
    for k,lab,tcls,h2,p,lst in _grp:
        _secs+=(f'<section class="wrap sec hubsec hub-{k}" id="{k}" aria-labelledby="h-{k}"><div class="sec-h"><span class="tape {tcls}">{lab}</span><h2 id="h-{k}">{h2}</h2></div>'
                f'<p class="hubsub">{p}</p><div class="posts{" posts-big" if k=="big" else ""}">'+''.join(_card(g) for g in lst)+'</div></section>')
    _hb=(f'<header class="hero hero-lite"><div class="wrap"><span class="kicker">{_c} · {len(_gs)} guide{"s" if len(_gs)!=1 else ""}</span><h1>{_c} travel guides</h1>'
         f'<p>Start with the big questions, then the food, day trips and smaller details. Every time and price is checked, with the date on each guide.</p>{_jump}</div></header>'
         f'<main>{_secs}'
         f'<div class="wrap"><section class="more"><p><a href="guides.html">All guides</a></p></section></div></main>')
    _ht,_hd=HUBMETA.get(_c,(f"{_c} Travel Guide: Where to Stay, Trains, Food", f"{_c} travel guide: "+"; ".join(g["title"] for g in _gs[:3])))
    if len(_hd)>158: _hd=_hd[:155].rsplit(" ",1)[0]+"…"
    pages[_sl+".html"]=(head(_ht,_hd),"city-"+_sl,_hb)
NAV_CITIES.sort(key=lambda x:-x[2])
os.makedirs(OUT,exist_ok=True)
import json as _json, datetime as _dt
SITE="https://japanbystation.com"
OGIMG={"index.html":"glico","osaka-where-to-stay.html":"hero","namba.html":"glico","kansai-airport-to-osaka.html":"kix"}
for _s,_g in GMETA.items(): P["g_"+_s]=_g["hero"]; OGIMG[_s]="g_"+_s
for _fn in list(pages):  # SEO 25 Nov: hubs get their own hero as og:image; about/guides the home photo
    if _fn in OGIMG: continue
    _mm=re.search(r'<img\b[^>]*?(?:pexels:|photos/)(\d+)',pages[_fn][2])
    if _mm and _fn not in ("about.html","guides.html","privacy.html","disclosure.html","data-deletion.html"): P["p_"+_fn]=int(_mm.group(1)); OGIMG[_fn]="p_"+_fn
    elif _fn in ("about.html","guides.html","privacy.html","disclosure.html","data-deletion.html"): OGIMG[_fn]="glico"
GUIDES={"osaka-where-to-stay.html","namba.html","kansai-airport-to-osaka.html"}|set(GMETA)
_MON={m:i+1 for i,m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"])}
def _mod(fn):
    """SEO 24 Nov: last real change = newest 'Checked D Month YYYY' in the sources line, else the publish date."""
    g=GMETA.get(fn,{}); best=g.get("modified") or g.get("date","2026-11-22")
    for d,m,y in _re.findall(r"[Cc]hecked (?:on )?(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December) (20\d\d)", g.get("sources","")):
        iso=f"{y}-{_MON[m]:02d}-{int(d):02d}"
        if iso>best and iso<=_dt.date.today().isoformat(): best=iso
    return best
_HUBS={cslug(c)+".html":c for c in {g["city"] for g in ALLG}}
# IMAGE SEO (25 Nov): real Pexels sizes (pexels-dims.json) -> width/height, og:image size, ImageObject, image sitemap
try: _DIM={k:v for k,v in _jj.load(open(os.path.join(HERE,"pexels-dims.json")))["w1200"].items()}
except Exception: _DIM={}
def _imgh(pid,w=1200):
    d=_DIM.get(str(pid)); return round(w*d[1]/d[0]) if d else None
def _page_imgs(body):
    """[(absolute url, width, height, caption)] for the photos in a page body: Pexels photos + /exitcards cards."""
    out=[]; seen=set()
    caps={}
    for fig in re.findall(r"<figure\b.*?</figure>",body,re.S):
        im=re.search(r'<img\b[^>]*src="([^"]+)"',fig); fc=re.search(r"<figcaption>(.*?)</figcaption>",fig,re.S)
        if im and fc: caps[im.group(1)]=html.unescape(re.sub("<[^>]+>","",fc.group(1))).strip()
    for tag in re.findall(r"<img\b[^>]*>",body):
        sm=re.search(r'src="([^"]+)"',tag); am=re.search(r'alt="([^"]*)"',tag)
        if not sm: continue
        src=sm.group(1); alt=html.unescape(am.group(1)) if am else ""
        pm=re.search(r"images\.pexels\.com/photos/(\d+)/",src)
        if pm:
            pid=pm.group(1); u=f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=1200"; w,h=1200,_imgh(pid)
        elif "exitcards/" in src:
            u=SITE+"/exitcards/"+src.split("exitcards/")[1]; w,h=1080,1440
        elif "carousels/" in src:   # 26 Nov: route-card maps on WALK pages
            u=SITE+"/carousels/"+src.split("carousels/")[1]; w,h=1080,1350
        else: continue
        if u in seen: continue
        seen.add(u); out.append((u,w,h,caps.get(src) or alt))
    return out
def _ldimgs(fn):
    hero=purl(OGIMG.get(fn,"hero"),1200)
    lst=_page_imgs(pages[fn][2]) if fn in pages else []
    lst=[x for x in lst if x[0]==hero]+[x for x in lst if x[0]!=hero]
    if not lst or lst[0][0]!=hero: lst=[(hero,1200,_imgh(P[OGIMG.get(fn,"hero")]),(GMETA.get(fn,{}).get("hero_alt") or ""))]+lst
    return [{"@type":"ImageObject","url":u,"contentUrl":u,"width":w,**({"height":h} if h else {}),**({"caption":c} if c else {})} for u,w,h,c in lst[:12]]
def seo(fn,h):
    url=SITE+"/" if fn=="index.html" else SITE+"/"+fn[:-5]
    title=_re.search(r"<title>(.*?)(?: \| Japan by Station)?</title>",h).group(1)
    desc=_re.search(r'<meta name="description" content="(.*?)">',h).group(1)
    tags=f'<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">\n<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n<meta property="og:type" content="{"article" if fn in GUIDES else "website"}">\n'
    if fn in OGIMG:
        _ou=purl(OGIMG[fn],1200); _oh=_imgh(P[OGIMG[fn]])
        tags+=f'<meta property="og:image" content="{_ou}">\n<meta property="og:image:secure_url" content="{_ou}">\n<meta property="og:image:type" content="image/jpeg">\n<meta property="og:image:width" content="1200">\n'
        if _oh: tags+=f'<meta property="og:image:height" content="{_oh}">\n'
        tags+=f'<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="{_ou}">\n'
    if fn in GMETA and GMETA[fn].get("hero_alt"): tags+=f'<meta property="og:image:alt" content="{html.escape(GMETA[fn]["hero_alt"])}">\n<meta name="twitter:image:alt" content="{html.escape(GMETA[fn]["hero_alt"])}">\n'
    title=html.unescape(title); desc=html.unescape(desc)
    org={"@type":"Organization","@id":SITE+"/#org","name":"Japan by Station","alternateName":["JapanByStation","japanbystation","japanbystation.com"],"url":SITE+"/",
         "logo":{"@type":"ImageObject","url":SITE+"/icons/favicon-512.png","width":512,"height":512},
         "description":"Japan by Station is an independent English guide to Japan: quick, carefully checked answers to real trip questions, plus the local places most lists miss.",
         "sameAs":["https://www.instagram.com/japanbystation/","https://www.facebook.com/1512969825226649","https://www.pinterest.com/japanbystation/"]}
    if fn=="index.html":
        ld={"@context":"https://schema.org","@graph":[{"@type":"WebSite","@id":SITE+"/#website","name":"Japan by Station","alternateName":["JapanByStation","japanbystation.com"],"url":SITE+"/","inLanguage":"en","description":desc,"publisher":{"@id":SITE+"/#org"}},org]}
    elif fn in GUIDES:
        ld={"@context":"https://schema.org","@graph":[
          {"@type":"Article","headline":title,"description":desc,"url":url,"datePublished":GMETA.get(fn,{}).get("date","2026-11-22"),"dateModified":_mod(fn),
           "author":{"@type":"Organization","name":"Japan by Station team","url":SITE+"/about"},"publisher":org,
           "image":_ldimgs(fn),**({"abstract":" ".join(_re.sub("<[^>]+>","",k) for k in GMETA[fn]["keyfacts"])} if GMETA.get(fn,{}).get("keyfacts") else {}),"about":([{"@type":e.get("type","Place"),"name":e["name"],**({"sameAs":e["sameAs"]} if e.get("sameAs") else {})} for e in GMETA[fn]["about"]] if GMETA.get(fn,{}).get("about") else {"@type":"Place","name":GMETA.get(fn,{}).get("city","Osaka")+", Japan"})},
          {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":GMETA.get(fn,{}).get("city","Osaka"),"item":SITE+"/guides#"+GMETA.get(fn,{}).get("city","Osaka").lower()},{"@type":"ListItem","position":3,"name":title,"item":url}]}]}
    elif fn in _HUBS:
        _gs=[g for g in ALLG if g["city"]==_HUBS[fn]]
        ld={"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","name":title,"description":desc,"url":url,"publisher":org,"about":{"@type":"Place","name":_HUBS[fn]+", Japan"}},
            {"@type":"ItemList","name":title,"itemListElement":[{"@type":"ListItem","position":k+1,"url":SITE+"/"+g["slug"].replace(".html",""),"name":g["title"]} for k,g in enumerate(_gs)]}]}
    else:
        ld={"@context":"https://schema.org","@type":"WebPage","name":title,"url":url,"publisher":org}
    if GMETA.get(fn,{}).get("faq"):
        ld.setdefault("@graph",[]).append({"@type":"FAQPage","mainEntity":[{"@type":"Question","name":html.unescape(q),"acceptedAnswer":{"@type":"Answer","text":html.unescape(_re.sub("<[^>]+>","",a))}} for q,a in GMETA[fn]["faq"]]})
    tags+='<script type="application/ld+json">'+_json.dumps(ld,ensure_ascii=False)+'</script>\n'
    return h.replace('<link rel="stylesheet"',tags+'<link rel="stylesheet"',1), url
urls=[]
for fn,(h,active,b) in pages.items():
    h,url=seo(fn,h); urls.append((url,fn))
    _page=h+nav(active)+b+FOOT
    # Clean internal URLs (25 Nov): Cloudflare Pages 308-redirects /x.html -> /x, so link straight to /x (no redirect hop)
    _page=_re.sub(r'href="(?:https://japanbystation\.com/|/)?index\.html(#[^"]*)?"', lambda m: 'href="/'+(m.group(1) or '')+'"', _page)
    _page=_re.sub(r'href="(?:https://japanbystation\.com/|/)?([a-z0-9][a-z0-9-]*)\.html((?:[?#][^"]*)?)"', lambda m: 'href="/'+m.group(1)+m.group(2)+'"', _page)
    _page=_re.sub(r'"([a-z0-9][a-z0-9-]*)\.html(#[^"]*)?"', lambda m: '"/'+m.group(1)+(m.group(2) or '')+'"', _page)   # link targets inside inline scripts
    open(f"{OUT}/{fn}","w").write(_page)
# 404 (26 Nov): without a 404.html, Cloudflare Pages served the home page with HTTP 200 for ANY unknown URL (soft 404s; Cloudflare even pinged bot probes like /backup.tar.gz to Bing). A real 404.html makes Pages answer 404. Not in the sitemap, noindex, absolute asset paths (it is served at any depth).
_h404=head("Page not found","This page doesn't exist on Japan by Station. Try our checked guides instead: where to stay in Tokyo, Osaka and Kyoto, airport trains and food near stations.").replace('<link rel="stylesheet"','<meta name="robots" content="noindex">\n<link rel="stylesheet"',1)
_p404=_h404+nav("")+simple("","Sorry, that page doesn't exist",'''
  <p>The link may be old, or the address has a typo. These are a good place to start:</p>
  <ul><li><a href="index.html">Home</a></li><li><a href="guides.html">All guides</a></li><li><a href="osaka.html">Osaka</a> · <a href="tokyo.html">Tokyo</a> · <a href="kyoto.html">Kyoto</a></li></ul>
''')+FOOT
_p404=_re.sub(r'href="(?:https://japanbystation\.com/|/)?index\.html(#[^"]*)?"', lambda m: 'href="/'+(m.group(1) or '')+'"', _p404)
_p404=_re.sub(r'href="(?:https://japanbystation\.com/|/)?([a-z0-9][a-z0-9-]*)\.html((?:[?#][^"]*)?)"', lambda m: 'href="/'+m.group(1)+m.group(2)+'"', _p404)
_p404=_re.sub(r'(href|src)="(?!https?:|/|#|data:|mailto:)([^"]+)"', lambda m: m.group(1)+'="/'+m.group(2)+'"', _p404)
open(f"{OUT}/404.html","w").write(_p404)
today=_dt.date.today().isoformat()
def _smimg(f):
    if f not in GUIDES: return ""
    return "".join(f'<image:image><image:loc>{html.escape(u)}</image:loc></image:image>' for u,w,h,c in _page_imgs(pages[f][2]))
open(f"{OUT}/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>{_mod(f) if f in GUIDES else today}</lastmod>{_smimg(f)}</url>\n' for u,f in urls)+'</urlset>\n')
# GEO: say plainly that search and AI-answer crawlers are welcome (Ling wants to be cited by ChatGPT, Claude, Perplexity, Gemini)
_bots=["Googlebot","Bingbot","GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-SearchBot","Claude-User","PerplexityBot","Perplexity-User","Google-Extended","Applebot","Applebot-Extended","DuckDuckBot"]
open(f"{OUT}/robots.txt","w").write("".join(f"User-agent: {b}\nAllow: /\n\n" for b in _bots)+"User-agent: *\nAllow: /\n\nSitemap: https://japanbystation.com/sitemap.xml\n")
_ll="# Japan by Station\n\n> Carefully checked English guides to Japan travel, quick answer first: where to stay, what is within walking distance, local markets, nightlife, and how many minutes it takes to reach the airport, day trips and sights. Every time and price is checked against operators, airports and tourism bureaus, with the check date shown on each page.\n"
# GEO (24 Nov): station hubs first, with their key facts, so answer engines find the direct answers
_hubs=[g for g in ALLG if g.get("keyfacts") and "station" in g["slug"]]
if _hubs:
    _ll+="\n## Station guides (start here)\n"+"".join(f"- [{g['title']}](https://japanbystation.com/{g['slug'][:-5]}): {g['card']} Key facts (checked {_mod(g['slug'])}): "+" ".join(re.sub(r'<[^>]+>','',k) for k in g['keyfacts'])+"\n" for g in _hubs)
for _c in _cities:
    _ll+=f"\n## {_c}\n"+"".join(f"- [{g['title']}](https://japanbystation.com/{g['slug'][:-5]}): {g['card']}\n" for g in ALLG if g['city']==_c)
_ll+="\n## About\n- [About and how we check facts](https://japanbystation.com/about)\n- [How we make money](https://japanbystation.com/disclosure)\n- [All guides](https://japanbystation.com/guides)\n"
open(f"{OUT}/llms.txt","w").write(_ll)

css=open(f"{SRC}/style.css").read()
css=_re.sub(r"@media \(prefers-color-scheme: dark\)\{.*?\}\s*\}", "", css, flags=_re.S)
css=_re.sub(r":root\[data-theme=\"dark\"\]\{[^}]*\}", "", css)
css+='''
/* finder */
.finder{margin-top:36px}
.finder h2{font-size:clamp(28px,5vw,36px)}
.finder-sub{color:var(--muted);margin:6px 0 16px}
.chips{display:flex;flex-wrap:wrap;gap:10px}
.chip{font:inherit;font-weight:700;font-size:15.5px;border:2px solid var(--rule);background:var(--bg);color:var(--ink);border-radius:999px;padding:8px 16px;cursor:pointer}
.chip[aria-selected="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.chip:focus-visible{outline:3px solid var(--namba);outline-offset:2px}
.answer-card{margin-top:18px;border-radius:26px;background:var(--soft);padding:24px;border-left:8px solid var(--namba)}
.answer-card[data-area="umeda"]{border-left-color:var(--umeda)} .answer-card[data-area="tennoji"]{border-left-color:var(--tennoji)}
.ac-eyebrow{font-size:13px;font-weight:800;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.ac-top h3{font-size:clamp(36px,7vw,52px);margin-top:2px}
.ac-top p{margin:6px 0 0;font-size:18px;max-width:60ch}
.ac-cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:18px}
.ac-cols h4{margin:0 0 6px;font-size:15px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.ac-cols ul{margin:0;padding-left:20px}
.ac-room{margin:16px 0 0;background:var(--bg);border-radius:16px;padding:12px 16px}
.ac-btn{background:var(--ink);color:var(--bg);display:inline-block;margin-top:18px}
/* home */
.how{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin-top:16px}
.how div{background:var(--soft);border-radius:20px;padding:18px}
.how span{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--namba);color:#2a2730;font-weight:800}
.how h3{font-size:20px;margin-top:10px}
.how p{margin:4px 0 0;color:var(--muted);font-size:15.5px}
.cities{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-top:16px}
.city{position:relative;border-radius:22px;overflow:hidden;min-height:180px;display:flex;align-items:flex-end;text-decoration:none;background:var(--soft)}
.city img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.city.live::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,rgba(0,0,0,.7))}
.city span{position:relative;z-index:1;padding:16px 18px}
.city.live span{color:#fff}
.city b{display:block;font-size:24px}
.city small{color:inherit;opacity:.85}
.city.soon{color:var(--muted)}
/* home hero finder */
.home-hero{min-height:560px}
.quick{margin-top:22px;background:rgba(255,255,255,.95);color:#2a2730;border-radius:22px;padding:16px;display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px;max-width:640px}
.quick label{font-weight:700;font-size:15.5px}
.quick select{font:inherit;font-weight:800;font-size:16px;border:2px solid #e3ddd3;border-radius:12px;padding:8px 10px;background:#fff;color:#2a2730}
.quick .q-go{flex:1 1 100%;margin-top:6px;background:var(--namba);color:#2a2730;border:0;cursor:pointer;font:inherit;font-weight:800;font-size:17px}
.trust{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:20px;position:relative;z-index:2}
@media(min-width:760px){.trust{gap:12px;margin-top:-34px}}
.trust div{background:var(--bg);border:1px solid var(--rule);border-radius:16px;padding:10px 12px;box-shadow:0 8px 24px rgba(0,0,0,.06)}
@media(max-width:520px){.trust b{font-size:14px}.trust span{font-size:12.5px;line-height:1.4;display:block}}
.trust b{display:block;font-size:16.5px}
.trust span{font-size:14.5px;color:var(--muted)}
.tens{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:16px}
.ten{display:flex;flex-direction:column;gap:2px;text-decoration:none;border-radius:22px;padding:18px 20px;color:#2a2730}
.ten small{font-weight:800;font-size:13px;opacity:.75;text-transform:uppercase;letter-spacing:.05em}
.ten b{font-size:34px;line-height:1.1;margin:2px 0 8px}
.ten span{font-size:16px}
.ten em{font-style:normal;font-weight:800}
.t-namba{background:var(--namba)} .t-umeda{background:var(--umeda)} .t-tennoji{background:var(--tennoji)}
.soon-img img{filter:grayscale(.35) brightness(.8)}
/* docs */
.doc{max-width:720px;padding-top:40px}
.doc h1{font-size:clamp(34px,6vw,46px)}
.doc h2{font-size:24px;margin-top:30px}
.doc p{max-width:64ch}
footer a{color:var(--muted)}
/* image SEO 25 Nov: width/height attributes only reserve the ratio */
img{height:auto}
'''
css+=open(os.path.join(HERE,"theme.css")).read()
open(f"{OUT}/style.css","w").write(css)
for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(f"{OUT}/{f}"))

# keywords.json for the Instagram comment -> DM workflow (one unique keyword per guide)
_kw={}
for g in sorted(ALLG,key=lambda g:g.get("date","")):
    k=g.get("keyword")
    if not k: continue
    assert k not in _kw, f"duplicate keyword {k}"
    _kw[k]={"url":"https://japanbystation.com/"+g["slug"][:-5],"title":g["title"]}
    for _al in (g.get("keyword_aliases") or []):   # Ling 25 Nov: area words like SHIBUYA can also trigger the guide
        assert _al not in _kw, f"duplicate keyword alias {_al}"
        _kw[_al]=_kw[k]
# City hubs (26 Nov, route-card carousels: "Comment TOKYO for our free guides to all 4 walks" -> the city's hub page with
# every guide). Only where the city word isn't already a guide keyword (OSAKA/KYOTO stay on their guides).
for _hub in ("tokyo","osaka","kyoto","hokkaido","fukuoka","nara","okinawa","hiroshima","nagoya"):
    _K=_hub.upper()
    if _K not in _kw and os.path.exists(f"{OUT}/{_hub}.html"):
        _kw[_K]={"url":"https://japanbystation.com/"+_hub,"title":f"All our {_hub.capitalize()} guides"}
open(f"{OUT}/keywords.json","w").write(_json.dumps(_kw,ensure_ascii=False,indent=1))
print("keywords:",len(_kw))

# designed Facebook images (fbimg.py) are published at /fbimg/<id>.jpg
import shutil as _sh
if os.path.isdir(os.path.join(SRC,"fbimg")): _sh.copytree(os.path.join(SRC,"fbimg"), os.path.join(OUT,"fbimg"), dirs_exist_ok=True)
if os.path.isdir(os.path.join(SRC,"pinimg")): _sh.copytree(os.path.join(SRC,"pinimg"), os.path.join(OUT,"pinimg"), dirs_exist_ok=True)
if os.path.isdir(os.path.join(SRC,"icons")):
    _sh.copytree(os.path.join(SRC,"icons"), os.path.join(OUT,"icons"), dirs_exist_ok=True); _sh.copy(os.path.join(SRC,"icons","favicon.ico"), os.path.join(OUT,"favicon.ico"))
if os.path.isdir(os.path.join(SRC,"exitcards")): _sh.copytree(os.path.join(SRC,"exitcards"), os.path.join(OUT,"exitcards"), dirs_exist_ok=True)  # Ling 25 Nov: saveable "Which exit?" cheat sheets
# fb-queue.json for the Facebook text-post workflow (site/fbposts/*.json, posted in "order")
_fb=[]
for _f in sorted(os.listdir(os.path.join(SRC,"fbposts"))) if os.path.isdir(os.path.join(SRC,"fbposts")) else []:
    if _f.endswith(".json"):
        _p=_json.load(open(os.path.join(SRC,"fbposts",_f)))
        if _p.get("skip") or _p.get("rewrite"): continue  # Ling 24 Nov: retired posts (e.g. hotel/booking) stay on disk but never post
        _fbtxt=re.sub(r'(https://japanbystation\.com/[A-Za-z0-9\-./]*)(?=[\s)\]]|$)', lambda m: m.group(1)+("&" if "?" in m.group(1) else "?")+"utm_source=facebook&utm_medium=social&utm_campaign=fb_post", _p["text"])  # Ling 25 Nov: tell FB visits apart
        _fb.append({"id":_p["id"],"order":_p.get("order",999),"guide":_p["guide"],"text":_fbtxt,
                    "photo_url":(SITE+"/"+_p["image"]) if _p.get("image") else f"https://images.pexels.com/photos/{_p['photo']}/pexels-photo-{_p['photo']}.jpeg?auto=compress&cs=tinysrgb&w=1600"})
_fb.sort(key=lambda x:(x["order"],x["id"]))
open(f"{OUT}/fb-queue.json","w").write(_json.dumps({"items":_fb},ensure_ascii=False,indent=1))

# Pinterest website claim (p:domain_verify) on every page's <head>
_PIN='<meta name="p:domain_verify" content="eb3483b0c99319fb04a7c61ccba32038"/>'
for _r,_d,_fs in os.walk(OUT):
    for _f in _fs:
        if _f.endswith(".html"):
            _pth=os.path.join(_r,_f); _t=open(_pth,encoding="utf-8").read()
            if "p:domain_verify" not in _t and "<head>" in _t:
                open(_pth,"w",encoding="utf-8").write(_t.replace("<head>","<head>\n"+_PIN,1))

# Ling 24 Nov: early Pins linked to /guides/<slug>.html, but pages live at /<slug>.html, so those links fell back to the
# home page. Cloudflare Pages redirect keeps every old link landing on the right guide.
open(os.path.join(OUT, "_redirects"), "w").write("/guides/:slug /:slug 301\n/guides/:slug.html /:slug.html 301\n/hakone-ropeway-closed-plan-b /gora-to-lake-ashi-bus-or-ropeway 301\n/hakone-ropeway-closed-plan-b.html /gora-to-lake-ashi-bus-or-ropeway.html 301\n")

# Google Analytics 4 (Ling, 24 Nov; property "Japan by Station", same Google account as Search Console) on every page
_GA='<script async src="https://www.googletagmanager.com/gtag/js?id=G-G13XXKV55G"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-G13XXKV55G");</script>'
for _r,_d,_fs in os.walk(OUT):
    for _f in _fs:
        if _f.endswith(".html"):
            _pth=os.path.join(_r,_f); _t=open(_pth,encoding="utf-8").read()
            if "G-G13XXKV55G" not in _t and "<head>" in _t:
                open(_pth,"w",encoding="utf-8").write(_t.replace("<head>","<head>\n"+_GA,1))


# SEO/GEO pass (24 Nov): faster first image (Core Web Vitals LCP p90 was ~7.8 s), responsive Pexels images,
# a full-text llms-full.txt for AI answer engines, and an IndexNow key so Bing (which feeds ChatGPT search) can be pinged.
_IDX="6c1f0b2e9a7d4c58b3e1f2a0d9c8b7a6"
open(os.path.join(OUT, _IDX+".txt"),"w").write(_IDX)
def _srcset(m):
    tag=m.group(0)
    if "srcset=" in tag or "images.pexels.com/photos/" not in tag: return tag
    u=re.search(r'src="(https://images\.pexels\.com/photos/\d+/pexels-photo-\d+\.jpeg\?auto=compress&cs=tinysrgb)&w=\d+"',tag)
    if not u: return tag
    b=u.group(1)
    return tag.replace(" src=", f' srcset="{b}&w=640 640w, {b}&w=1000 1000w, {b}&w=1600 1600w" sizes="(max-width: 700px) 100vw, 1100px" src=',1)
def _wh(m):
    """IMAGE SEO 25 Nov: explicit width/height (real ratio) so the browser reserves space; CSS keeps height:auto."""
    tag=m.group(0)
    if re.search(r"\swidth=",tag): return tag
    u=re.search(r'src="https://images\.pexels\.com/photos/(\d+)/[^"]*?&w=(\d+)"',tag)
    if not u: return tag
    h=_imgh(u.group(1),int(u.group(2)))
    return tag.replace("<img ",f'<img width="{u.group(2)}" height="{h}" ',1) if h else tag
for _r,_d,_fs in os.walk(OUT):
    for _f in _fs:
        if not _f.endswith(".html"): continue
        _pth=os.path.join(_r,_f); _t=open(_pth,encoding="utf-8").read(); _o=_t
        _t=re.sub(r'<img\b[^>]*>', _srcset, _t)
        _t=re.sub(r'<img\b[^>]*>', _wh, _t)
        _t=re.sub(r'(<header class="hero">\s*<img)(?![^>]*fetchpriority)', r'\1 fetchpriority="high" decoding="async"', _t, count=1)
        if _t!=_o: open(_pth,"w",encoding="utf-8").write(_t)
_full=["# Japan by Station: full text of every guide","","> Carefully checked English Japan travel guides, quick answer first. Each guide shows the date its facts were checked. Source: https://japanbystation.com",""]
for g in ALLG:
    _fp=os.path.join(OUT, g["slug"])
    if not os.path.exists(_fp): continue
    _t=open(_fp,encoding="utf-8").read()
    _m=re.search(r"<main>(.*?)</main>",_t,re.S)
    if not _m: continue
    _x=re.sub(r"<(script|style)[^>]*>.*?</\1>","",_m.group(1),flags=re.S)
    _x=re.sub(r"</(p|li|h2|h3|h4|figcaption|div|section)>","\n",_x); _x=re.sub(r"<[^>]+>","",_x)
    _x="\n".join(l.strip() for l in html.unescape(_x).splitlines() if l.strip())
    _kfl=["Key facts:"]+["- "+re.sub(r"<[^>]+>","",k) for k in g.get("keyfacts",[])]+[""] if g.get("keyfacts") else []
    _full+=[f"## {g['title']}", f"URL: {SITE}/{g['slug'].replace('.html','')}", f"City: {g['city']} · Facts checked: {_mod(g['slug'])}", ""]+_kfl+[_x, ""]
open(os.path.join(OUT,"llms-full.txt"),"w",encoding="utf-8").write("\n".join(_full))


# SEO lint (24 Nov): written to SEO-LINT.txt in the studio folder (not published) for the SEO task to work through.
_lint=[]
for _f in sorted(os.listdir(OUT)):
    if not _f.endswith(".html"): continue
    _t=open(os.path.join(OUT,_f),encoding="utf-8").read()
    _ti=html.unescape((re.search(r"<title>(.*?)</title>",_t) or [None,""])[1]); _de=html.unescape((re.search(r'<meta name="description" content="(.*?)">',_t) or [None,""])[1])
    if len(_ti)>65: _lint.append(f"{_f}\ttitle {len(_ti)} chars (aim <=60; add \"seo_title\" to the guide meta)")
    if not 110<=len(_de)<=160: _lint.append(f"{_f}\tdescription {len(_de)} chars (aim 120-160; add \"seo_desc\")")
    for _im in re.findall(r"<img\b[^>]*>",_t):
        if 'aria-hidden' in _t[max(0,_t.find(_im)-1200):_t.find(_im)]: continue
        _a=re.search(r'alt="([^"]*)"',_im)
        if not _a or len(_a.group(1).strip())<10: _lint.append(f"{_f}\timage alt missing/short: {_im[-120:]}")
    if _t.count("<h1")!=1: _lint.append(f"{_f}\th1 count {_t.count('<h1')}")
open(os.path.join(HERE,"SEO-LINT.txt"),"w").write("\n".join(_lint)+"\n")
print("seo lint:", len(_lint), "items -> SEO-LINT.txt")
