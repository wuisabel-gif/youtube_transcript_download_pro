# TubeScribe

Download and archive YouTube transcripts from the command line — in plain text,
SubRip (`.srt`), WebVTT (`.vtt`), or structured JSON.

```bash
tubescribe https://youtu.be/dQw4w9WgXcQ
```

## Features

- Accepts full URLs (`watch`, `youtu.be`, `embed`, `shorts`, `live`) or bare 11-char video ids.
- **Bulk download** entire playlists and channels — they're expanded into their videos automatically.
- Output as `txt`, `srt`, `vtt`, or `json`.
- Language preference with automatic fallback: manual → auto-generated → translated.
- Batch multiple inputs in one call; write one file per video with `--output-dir`.
- Resume long runs with `--skip-existing`; cap volume with `--limit`.
- Optional `[HH:MM:SS]` timestamps for plain text.

## Install

```bash
pip install -e .                          # core: single videos
pip install -e ".[playlists]"             # + playlist/channel bulk download (adds yt-dlp)
pip install -e ".[server,playlists]"      # + the web UI / API server (adds Flask)
```

This installs the `tubescribe` console command. The `playlists` extra adds
[`yt-dlp`](https://github.com/yt-dlp/yt-dlp), which TubeScribe uses to enumerate
the videos in a playlist or channel. The `server` extra adds the
`tubescribe-serve` command (see [Web UI](#web-ui)).

## Usage

```bash
# Print a transcript to stdout
tubescribe https://www.youtube.com/watch?v=VIDEO_ID

# Save several videos as .srt files into ./out
tubescribe VIDEO_ID1 VIDEO_ID2 -f srt -o out/

# Prefer Spanish, fall back automatically
tubescribe VIDEO_ID -l es,en

# Plain text with timestamps
tubescribe VIDEO_ID -t

# Download a whole playlist as .srt files
tubescribe "https://www.youtube.com/playlist?list=PLAYLIST_ID" -f srt -o out/

# Download a channel's latest 25 videos, resumable
tubescribe "https://www.youtube.com/@SomeChannel" -n 25 -o out/ --skip-existing
```

> Quote playlist/channel URLs in zsh — the `?`, `&`, and `=` characters are
> otherwise interpreted by the shell.

| Option | Description |
| --- | --- |
| `-f, --format` | `txt` (default), `srt`, `vtt`, `json` |
| `-l, --languages` | Comma-separated preferred language codes (default `en`) |
| `-o, --output-dir` | Write one file per video into this directory |
| `-t, --timestamps` | Prefix `txt` lines with `[HH:MM:SS]` |
| `-n, --limit` | Cap videos pulled from each playlist/channel |
| `--skip-existing` | Skip videos already downloaded (needs `--output-dir`) |
| `--proxy` | Route requests through an `http(s)://` proxy |

> **Blocked from a server/cloud IP?** YouTube rate-limits datacenter addresses.
> Pass `--proxy http://user:pass@host:port` (CLI) or `tubescribe-serve --proxy …`
> to route through a residential/proxy endpoint.

### Playlists and channels

Pass a playlist or channel URL and TubeScribe expands it into the individual
videos before fetching transcripts:

- Playlist: `https://www.youtube.com/playlist?list=...`
- Channel: `https://www.youtube.com/@handle`, `/channel/UC...`, `/c/...`, `/user/...`
  (a bare channel URL resolves to its **Videos** tab)

Requires the `playlists` extra (`pip install -e ".[playlists]"`).

## Web UI

TubeScribe ships with a small single-page web app (`web/index.html`) and a thin
Flask backend that reuses the same library functions as the CLI.

```bash
pip install -e ".[server,playlists]"
tubescribe-serve            # → http://127.0.0.1:8000
```

Open the URL and you get two tabs:

- **Get transcript** — paste video/playlist/channel URLs; the page validates each
  one live, then either **fetches transcripts** through the backend (download per
  video) or shows the exact `tubescribe` command to run yourself.
- **Convert transcript** — paste `tubescribe … -f json` output and convert it to
  `txt`/`srt`/`vtt` entirely in the browser, no backend needed.

The page degrades gracefully: opened directly as a file (no backend), the live
**Fetch** button is disabled and you still get the command builder and converter.

### Deploying the page

`web/index.html` is fully static, so it can be hosted on GitHub Pages. The
included workflow (`.github/workflows/pages.yml`) publishes `web/` on every push
to `main`; enable Pages → "GitHub Actions" in the repo settings. On Pages the
converter and command builder work; live fetch needs a running `tubescribe-serve`
backend (point the page at it, or run locally).

### API

The backend exposes one endpoint:

```
POST /api/transcript
{
  "urls": ["VIDEO_ID", "https://www.youtube.com/playlist?list=..."],
  "format": "srt",          // txt | srt | vtt | json
  "languages": "en,es",     // string or list
  "timestamps": false,      // txt only
  "limit": 25               // cap per playlist/channel
}
→ { "results": [ { "video_id", "filename", "language", "segments", "duration", "content" } ],
    "errors":  [ { "input", "error" } ],
    "truncated": false }
```

Playlist/channel URLs are expanded server-side; one bad input never fails the
whole request — it lands in `errors` instead.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## Roadmap

TubeScribe starts as a transcript downloader, but it's designed to grow into a
searchable knowledge layer over video content:

```text
YouTube Channel
      ↓
Transcripts          ← you are here
      ↓
Knowledge Graph      (entities & relationships across videos)
      ↓
Vector Database      (chunk + embed transcripts)
      ↓
Semantic Search      (find moments by meaning, not keywords)
      ↓
LLM Chat             (ask questions across an entire channel)
```

Planned next steps:

- ✅ Playlist and channel ingestion (bulk download).
- Chunking + embedding pipeline with a pluggable vector store.
- Retrieval-augmented Q&A over a downloaded corpus.

## License

MIT
