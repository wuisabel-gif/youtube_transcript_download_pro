# TubeScribe — Chrome Web Store submission

Everything you need to paste into the Chrome Web Store Developer Dashboard when
publishing the extension. Upload `tubescribe-extension-v1.0.0.zip` as the package.

---

## Store listing

**Name** (max 45 chars)
```
TubeScribe — YouTube Transcript Downloader
```

**Summary** (max 132 chars)
```
Download any YouTube video's transcript as txt, srt, vtt, or json — straight from your browser. No account, no API key.
```

**Category:** Productivity
**Language:** English (United States)

**Detailed description**
```
TubeScribe downloads the transcript (captions) of any YouTube video as a clean
file — plain text, SubRip (.srt), WebVTT (.vtt), or structured JSON.

Open a YouTube video, click the TubeScribe icon, pick a language and a format,
and hit Download. That's it.

WHY IT'S DIFFERENT
• Runs entirely in your browser. It reads the captions YouTube already loaded
  and fetches them on your own connection — so there's no datacenter-IP blocking
  that breaks server-based transcript sites.
• No account, no sign-up, no API key, no payment.
• Doesn't send your data anywhere. There is no server and no tracking.

FEATURES
• Four formats: txt, srt, vtt, json.
• Every language the video offers — pick from the list, auto-generated tracks
  are marked.
• Optional timestamps for plain text.
• Files are named after the video and saved to your Downloads folder.

HOW TO USE
1. Open a YouTube video (a /watch page).
2. Click the TubeScribe toolbar icon.
3. Choose a language and a format.
4. Click Download.

If a video has captions disabled, TubeScribe tells you clearly instead of
failing silently.

TubeScribe is free and open source.
```

---

## Privacy & practices (required tab)

**Single purpose**
```
TubeScribe downloads the transcript/captions of the YouTube video the user is
currently viewing, saving it as a text-based file (txt, srt, vtt, or json).
```

**Permission justifications**

- **Host permission `https://www.youtube.com/*`**
```
Required to (1) read the list of available caption tracks from the YouTube watch
page the user is viewing, and (2) fetch the selected caption file from YouTube's
own timedtext endpoint. The extension only ever accesses youtube.com — no other
websites.
```

- **Content script on youtube.com**
```
A content script runs only on youtube.com to read the page's caption track data
and pass it to the popup for download. It does not modify the page or run on any
other site.
```

- **Remote code:** None. All code is bundled in the package; the extension loads
  no remote scripts.

**Data usage disclosures** (check these in the dashboard)
```
This extension does NOT collect or transmit any user data.
- No personally identifiable information.
- No health, financial, authentication, personal communications, location, or
  web-history data.
- No analytics, no remote servers, no third-party calls.
All processing happens locally in the browser. The only network request is to
YouTube to retrieve the caption file the user explicitly asked for; the result
is saved directly to the user's Downloads folder.
```

Tick: "I do not sell or transfer user data to third parties."
Tick: "I do not use or transfer user data for purposes unrelated to the item's
single purpose."

---

## Assets to upload

| Asset | File | Notes |
|-------|------|-------|
| Store icon (128×128) | `icons/icon128.png` | already in the package |
| Screenshot 1 (1280×800) | `store/screenshot-1.png` | "Download any transcript" |
| Screenshot 2 (1280×800) | `store/screenshot-2.png` | "Pick language and format" |
| Small promo tile (440×280) | `store/promo-440x280.png` | optional but recommended |

---

## One-time setup checklist

1. Register a Chrome Web Store developer account (one-time $5 USD fee).
2. Create a new item, upload `tubescribe-extension-v1.0.0.zip`.
3. Paste the name, summary, description above.
4. Upload the icon, screenshots, and promo tile.
5. Fill the Privacy tab with the single-purpose, permission, and data-usage text above.
6. Add a privacy policy URL if prompted — the repo README or a short page stating
   "TubeScribe collects no data" is sufficient.
7. Submit for review (typically a few days).
