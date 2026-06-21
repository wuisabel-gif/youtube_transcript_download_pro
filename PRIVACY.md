# TubeScribe Privacy Policy

_Last updated: 2026-06-20_

TubeScribe (the web app, the command-line tool, and the browser extension) is
built to do one thing: download YouTube transcripts. It is designed to collect
nothing.

## What we collect

**Nothing.** TubeScribe has no account system, no analytics, no tracking, and no
backend database. We do not collect, store, sell, or transmit any personal
information.

## The browser extension

- Runs entirely in your browser.
- The only network request it makes is to **YouTube**, to fetch the caption file
  for the video you explicitly chose. This uses your own connection.
- The resulting transcript is saved directly to your **Downloads** folder.
- No data is sent to the developer or any third party. There is no server.

## The web app and CLI

- The web app converts and (where possible) fetches transcripts; it does not log
  or store the URLs you enter beyond the lifetime of your request.
- The CLI runs locally on your machine and writes files you ask for. Nothing is
  reported anywhere.

## Permissions

The extension requests access to `youtube.com` only. This is required to read the
caption track list from the page you are viewing and to fetch the caption file.
It is never used for any other purpose, and it touches no other website.

## Changes

If this policy ever changes, the updated version will be published in this file
in the project repository.

## Contact

Questions: open an issue at
https://github.com/wuisabel-gif/youtube_transcript_download_pro
