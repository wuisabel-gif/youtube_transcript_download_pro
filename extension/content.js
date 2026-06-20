// Bridge between the popup and the YouTube page. The popup cannot read the page's
// JS, so it asks this content script, which (a) injects inject.js into the main
// world to read the caption track list, and (b) fetches a chosen track's text
// (same-origin, so the user's own cookies/IP are used — no proxy needed).

function getTracksFromPage() {
  return new Promise(function (resolve) {
    function onMsg(ev) {
      if (ev.source !== window) return;
      const d = ev.data;
      if (d && d.source === "tubescribe-inject") {
        window.removeEventListener("message", onMsg);
        resolve(d);
      }
    }
    window.addEventListener("message", onMsg);

    const s = document.createElement("script");
    s.src = chrome.runtime.getURL("inject.js");
    s.onload = function () { s.remove(); };
    (document.head || document.documentElement).appendChild(s);

    // Safety net if the page never responds.
    setTimeout(function () {
      window.removeEventListener("message", onMsg);
      resolve({ source: "tubescribe-inject", ok: false });
    }, 4000);
  });
}

async function fetchSegments(baseUrl) {
  // json3 is the easiest caption format to parse: events[].segs[].utf8 + timings.
  const url = baseUrl + (baseUrl.indexOf("?") >= 0 ? "&" : "?") + "fmt=json3";
  const res = await fetch(url, { credentials: "include" });
  if (!res.ok) throw new Error("Caption fetch failed (HTTP " + res.status + ")");
  const data = await res.json();
  const segments = [];
  for (const ev of data.events || []) {
    if (!ev.segs) continue;
    const text = ev.segs
      .map(function (s) { return s.utf8 || ""; })
      .join("")
      .replace(/\s+/g, " ")
      .trim();
    if (!text) continue;
    segments.push({
      start: (ev.tStartMs || 0) / 1000,
      dur: (ev.dDurationMs || 0) / 1000,
      text: text
    });
  }
  return segments;
}

chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
  if (msg && msg.type === "GET_TRACKS") {
    getTracksFromPage().then(sendResponse);
    return true; // async response
  }
  if (msg && msg.type === "GET_TRANSCRIPT") {
    fetchSegments(msg.baseUrl)
      .then(function (segments) { sendResponse({ ok: true, segments: segments }); })
      .catch(function (e) { sendResponse({ ok: false, error: e.message }); });
    return true; // async response
  }
});
