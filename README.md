# TubeScribe

Download and archive YouTube transcripts from the command line — in plain text,
SubRip (`.srt`), WebVTT (`.vtt`), or structured JSON.

```bash
tubescribe https://youtu.be/dQw4w9WgXcQ
```

## Features

- Accepts full URLs (`watch`, `youtu.be`, `embed`, `shorts`, `live`) or bare 11-char video ids.
- Output as `txt`, `srt`, `vtt`, or `json`.
- Language preference with automatic fallback: manual → auto-generated → translated.
- Batch multiple videos in one call; write one file per video with `--output-dir`.
- Optional `[HH:MM:SS]` timestamps for plain text.

## Install

```bash
pip install -e .
```

This installs the `tubescribe` console command (and the `youtube-transcript-api` dependency).

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
```

| Option | Description |
| --- | --- |
| `-f, --format` | `txt` (default), `srt`, `vtt`, `json` |
| `-l, --languages` | Comma-separated preferred language codes (default `en`) |
| `-o, --output-dir` | Write one file per video into this directory |
| `-t, --timestamps` | Prefix `txt` lines with `[HH:MM:SS]` |

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

- Playlist and channel ingestion (bulk download).
- Chunking + embedding pipeline with a pluggable vector store.
- Retrieval-augmented Q&A over a downloaded corpus.

## License

MIT
