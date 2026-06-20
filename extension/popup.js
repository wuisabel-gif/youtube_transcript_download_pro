// Popup UI: ask the content script for caption tracks, let the user pick a
// language + format, then fetch and download the transcript.

const $ = function (id) { return document.getElementById(id); };
const langSel = $("lang");
const fmtSel = $("fmt");
const tsBox = $("ts");
const dlBtn = $("dl");
const statusEl = $("status");
const titleEl = $("title");

let state = { tabId: null, videoId: null, title: null, tracks: [] };

function setStatus(msg, kind) {
  statusEl.textContent = msg || "";
  statusEl.className = "status" + (kind ? " " + kind : "");
}

function pad(n, len) { return String(n).padStart(len || 2, "0"); }

function fmtTime(sec, msSep) {
  const ms = Math.round((sec - Math.floor(sec)) * 1000);
  const s = Math.floor(sec) % 60;
  const m = Math.floor(sec / 60) % 60;
  const h = Math.floor(sec / 3600);
  return pad(h) + ":" + pad(m) + ":" + pad(s) + msSep + pad(ms, 3);
}

function toTxt(segs, withTs) {
  return segs.map(function (s) {
    return withTs ? "[" + fmtTime(s.start, ".").slice(0, 8) + "] " + s.text : s.text;
  }).join("\n");
}
function toSrt(segs) {
  return segs.map(function (s, i) {
    return (i + 1) + "\n" +
      fmtTime(s.start, ",") + " --> " + fmtTime(s.start + s.dur, ",") + "\n" +
      s.text + "\n";
  }).join("\n");
}
function toVtt(segs) {
  return "WEBVTT\n\n" + segs.map(function (s) {
    return fmtTime(s.start, ".") + " --> " + fmtTime(s.start + s.dur, ".") + "\n" + s.text + "\n";
  }).join("\n");
}
function toJson(segs) {
  return JSON.stringify(segs.map(function (s) {
    return { start: s.start, duration: s.dur, text: s.text };
  }), null, 2);
}

function render(segs, fmt, withTs) {
  if (fmt === "srt") return toSrt(segs);
  if (fmt === "vtt") return toVtt(segs);
  if (fmt === "json") return toJson(segs);
  return toTxt(segs, withTs);
}

function safeName(s) {
  return (s || "transcript").replace(/[\\/:*?"<>|]+/g, "_").replace(/\s+/g, " ").trim().slice(0, 80);
}

function download(text, filename, mime) {
  const blob = new Blob([text], { type: mime + ";charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
}

function sendToTab(payload) {
  return new Promise(function (resolve, reject) {
    chrome.tabs.sendMessage(state.tabId, payload, function (resp) {
      if (chrome.runtime.lastError) { reject(new Error(chrome.runtime.lastError.message)); return; }
      resolve(resp);
    });
  });
}

async function init() {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  const tab = tabs[0];
  if (!tab || !/^https:\/\/www\.youtube\.com\//.test(tab.url || "")) {
    titleEl.textContent = "Open a YouTube video page, then click the icon.";
    setStatus("Not a YouTube page.", "err");
    return;
  }
  state.tabId = tab.id;

  let resp;
  try {
    resp = await sendToTab({ type: "GET_TRACKS" });
  } catch (e) {
    setStatus("Couldn't reach the page — reload the YouTube tab and try again.", "err");
    return;
  }

  if (!resp || !resp.ok) {
    setStatus("No player found. Open a video (a /watch page), not the homepage.", "err");
    return;
  }
  if (!resp.tracks || resp.tracks.length === 0) {
    titleEl.textContent = resp.title || "";
    setStatus("This video has no captions/transcript available.", "err");
    return;
  }

  state.videoId = resp.videoId;
  state.title = resp.title;
  state.tracks = resp.tracks;
  titleEl.textContent = resp.title || resp.videoId || "";

  langSel.innerHTML = "";
  resp.tracks.forEach(function (t, i) {
    const opt = document.createElement("option");
    opt.value = String(i);
    opt.textContent = t.name + (t.kind === "asr" ? " (auto)" : "");
    langSel.appendChild(opt);
  });
  langSel.disabled = false;
  dlBtn.disabled = false;
  setStatus(resp.tracks.length + " track(s) available.", "ok");
}

dlBtn.addEventListener("click", async function () {
  const track = state.tracks[Number(langSel.value)];
  if (!track) return;
  const fmt = fmtSel.value;
  dlBtn.disabled = true;
  setStatus("Fetching transcript…");
  try {
    const resp = await sendToTab({ type: "GET_TRANSCRIPT", baseUrl: track.baseUrl });
    if (!resp || !resp.ok) throw new Error(resp && resp.error ? resp.error : "Fetch failed");
    if (!resp.segments.length) throw new Error("Transcript came back empty.");

    const text = render(resp.segments, fmt, tsBox.checked);
    const mimes = { txt: "text/plain", srt: "text/plain", vtt: "text/vtt", json: "application/json" };
    const base = safeName(state.title || state.videoId);
    download(text, base + "." + fmt, mimes[fmt] || "text/plain");
    setStatus("Downloaded " + base + "." + fmt, "ok");
  } catch (e) {
    setStatus(e.message || "Something went wrong.", "err");
  } finally {
    dlBtn.disabled = false;
  }
});

init();
