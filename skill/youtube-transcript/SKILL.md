---
name: youtube-transcript
description: Download and save YouTube transcripts/captions from a video, playlist, or channel in txt, srt, vtt, or json. Use when the user wants to fetch, download, save, extract, or read the transcript, captions, or subtitles of one or more YouTube videos.
---

# YouTube Transcript

Fetch transcripts from YouTube videos, playlists, and channels using the
`tubescribe` CLI (from the youtube_transcript_download_pro project).

## Instructions

### Step 1: Make sure `tubescribe` is installed

Check first:

```bash
tubescribe --version
```

If that fails, install it from the project (run from the repo root, or point
pip at the repo path):

```bash
pip install ".[playlists]"      # from inside the repo
# or, from anywhere:
pip install "/path/to/youtube_transcript_download_pro[playlists]"
```

The `[playlists]` extra adds `yt-dlp`, needed for playlist/channel URLs. Plain
single-video fetching works without it.

### Step 2: Fetch the transcript

Single video → print to screen:

```bash
tubescribe "https://www.youtube.com/watch?v=VIDEO_ID"
```

The first positional argument also accepts a bare video id (`dQw4w9WgXcQ`) and
you can pass several at once. Common options:

| Goal | Command |
|------|---------|
| Pick a format | `tubescribe URL -f srt` (choices: `txt`, `srt`, `vtt`, `json`) |
| Choose language(s) | `tubescribe URL -l ko,en` (priority order; default `en`) |
| Save to files | `tubescribe URL -o out/` (writes `<video_id>.<format>` per video) |
| Add timestamps (txt) | `tubescribe URL -t` |
| Playlist/channel | `tubescribe "https://youtube.com/playlist?list=..."` |
| Cap a playlist | `tubescribe PLAYLIST_URL -n 25` |
| Skip already-downloaded | `tubescribe PLAYLIST_URL -o out/ --skip-existing` |

### Step 3: Read or return the result

- Without `-o`, the transcript is written to stdout — capture and show it.
- With `-o DIR`, one file per video is written; report the paths (printed to
  stderr as `✓ <id> → <path>`).

### Step 4: Handle failures honestly

`tubescribe` prints a specific reason per video, e.g.:

- *Transcripts are disabled for this video* — nothing can be fetched.
- *No transcript in the requested language(s)* — it lists what IS available;
  retry with one of those codes via `-l`.
- *YouTube is blocking requests from this IP* — only happens from datacenter
  IPs (cloud servers). From a normal machine this is rare. If it occurs, route
  through a **residential** proxy: `tubescribe URL --proxy "http://user:pass@host:port"`.

Relay the real reason rather than guessing. Datacenter proxies do not bypass
YouTube's block — only residential ones do.

## Notes

- Exit code is `0` on full success, `1` if any video failed.
- `--skip-existing` requires `-o/--output-dir`.
- For a web UI / API instead of the CLI, run `tubescribe-serve` (needs the
  `[server]` extra).
