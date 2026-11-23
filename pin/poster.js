// Paste into the built-in browser's javascript tool on a https://www.pinterest.com/japanbystation/ tab.
// Set window.__pinq = [ {id, board_id, image_url, link, title, description, alt_text}, ... ] first (from pin/queue.json, posted:false).
// Posts one Pin every 35 s in the background; read window.__pinres / window.__pindone afterwards.
window.__pinpost = async function (p) {
  const csrf = document.cookie.match(/csrftoken=([^;]+)/)?.[1]; const { id, ...opts } = p;
  const body = new URLSearchParams({ source_url: '/japanbystation/', data: JSON.stringify({ options: opts, context: {} }) });
  const r = await fetch('/resource/PinResource/create/', { method: 'POST', credentials: 'include', body,
    headers: { 'x-csrftoken': csrf, 'x-requested-with': 'XMLHttpRequest', 'content-type': 'application/x-www-form-urlencoded' } });
  const t = await r.text(); try { const j = JSON.parse(t); return [id, r.status, j.resource_response?.data?.id, j.resource_response?.error?.message]; } catch (e) { return [id, r.status, t.slice(0, 100)]; }
};
window.__pinres = []; window.__pindone = false;
(async () => { for (const p of window.__pinq) { window.__pinres.push(await window.__pinpost(p)); await new Promise(r => setTimeout(r, 35000)); } window.__pindone = true; })();
'started ' + window.__pinq.length;
