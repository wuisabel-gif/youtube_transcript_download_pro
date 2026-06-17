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
pip install -e .                 # core: single videos
pip install -e ".[playlists]"    # + playlist/channel bulk download (adds yt-dlp)
```

This installs the `tubescribe` console command. The `playlists` extra adds
[`yt-dlp`](https://github.com/yt-dlp/yt-dlp), which TubeScribe uses to enumerate
the videos in a playlist or channel.

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

### Playlists and channels

Pass a playlist or channel URL and TubeScribe expands it into the individual
videos before fetching transcripts:

- Playlist: `https://www.youtube.com/playlist?list=...`
- Channel: `https://www.youtube.com/@handle`, `/channel/UC...`, `/c/...`, `/user/...`
  (a bare channel URL resolves to its **Videos** tab)

Requires the `playlists` extra (`pip install -e ".[playlists]"`).

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
