# TubeScribe — Chrome extension

Download the transcript/captions of any YouTube video as **txt**, **srt**, **vtt**, or **json**, right from the browser toolbar.

Unlike the server version, this runs entirely in your browser: it reads the
caption tracks YouTube already loaded and fetches them with *your* IP and
cookies — so there's **no datacenter-IP blocking and no proxy needed**.

## Install (unpacked / developer mode)

1. Open `chrome://extensions` in Chrome (or any Chromium browser — Edge, Brave, Arc).
2. Toggle **Developer mode** on (top-right).
3. Click **Load unpacked** and select this `extension/` folder.
4. Pin the TubeScribe icon to your toolbar.

## Use

1. Open a YouTube video (`/watch` page).
2. Click the TubeScribe toolbar icon.
3. Pick a **language** (auto-generated tracks are marked `(auto)`) and a **format**.
4. Optionally tick **Include timestamps** (txt only).
5. Click **Download** — the file saves to your Downloads folder, named after the video.

## Notes & limitations

- Works on regular `/watch` pages. The homepage, Shorts feed, or a video with
  captions disabled will show a clear message instead.
- If you just installed/updated the extension, **reload any open YouTube tab**
  once so the content script is present.
- Languages listed are whatever that specific video provides. There's no fixed
  language set — French, Korean, Japanese, etc. all work if the video has them.

## How it works

| File | Role |
|------|------|
| `manifest.json` | MV3 manifest; content script on `youtube.com`, popup action |
| `inject.js` | Runs in the page's main world to read `ytInitialPlayerResponse` and list caption tracks |
| `content.js` | Bridges popup ↔ page; fetches the chosen caption track (json3) same-origin |
| `popup.html` / `popup.js` | UI: language + format pickers, formats the segments, triggers the download |

No external servers, no API keys, no tracking.
