// Paste into the built-in browser's javascript tool on a https://www.pinterest.com/japanbystation/ tab.
// Set window.__pinq = [ {id, board_id, image_url, link, title, description, alt_text}, ... ] first (from pin/queue.json, posted:false).
// Ling 24 Nov: no fixed times. Waits a random 0-5 min before the first Pin, then 40-120 s (random) between Pins. Runs in the background; poll window.__pinres / window.__pindone.
window.__pinpost = async function (p) {
  const csrf = document.cookie.match(/csrftoken=([^;]+)/)?.[1]; const { id, ...opts } = p;
  const body = new URLSearchParams({ source_url: '/japanbystation/', data: JSON.stringify({ options: opts, context: {} }) });
  const r = await fetch('/resource/PinResource/create/', { method: 'POST', credentials: 'include', body,
    headers: { 'x-csrftoken': csrf, 'x-requested-with': 'XMLHttpRequest', 'content-type': 'application/x-www-form-urlencoded' } });
  const t = await r.text(); try { const j = JSON.parse(t); return [id, r.status, j.resource_response?.data?.id, j.resource_response?.error?.message]; } catch (e) { return [id, r.status, t.slice(0, 100)]; }
};
window.__pinres = []; window.__pindone = false;
(async () => { await new Promise(r => setTimeout(r, Math.floor(Math.random() * 300000))); for (const p of window.__pinq) { window.__pinres.push(await window.__pinpost(p)); await new Promise(r => setTimeout(r, 40000 + Math.floor(Math.random() * 80000))); } window.__pindone = true; })();
'started ' + window.__pinq.length;
