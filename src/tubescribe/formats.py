"""Output formatters for transcripts."""

from __future__ import annotations

import json

from .core import Transcript


def _fmt_timestamp(seconds: float, *, comma: bool = False) -> str:
    millis = int(round(seconds * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    sep = "," if comma else "."
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{sep}{millis:03d}"


def to_txt(transcript: Transcript, *, with_timestamps: bool = False) -> str:
    """Plain text, one line per cue. Optionally prefixed with [HH:MM:SS]."""
    lines = []
    for seg in transcript.segments:
        text = seg.text.replace("\n", " ").strip()
        if with_timestamps:
            stamp = _fmt_timestamp(seg.start).split(".")[0]
            lines.append(f"[{stamp}] {text}")
        else:
            lines.append(text)
    return "\n".join(lines) + "\n"


def to_srt(transcript: Transcript) -> str:
    """SubRip (.srt) subtitle format."""
    blocks = []
    for i, seg in enumerate(transcript.segments, start=1):
        start = _fmt_timestamp(seg.start, comma=True)
        end = _fmt_timestamp(seg.end, comma=True)
        blocks.append(f"{i}\n{start} --> {end}\n{seg.text.strip()}\n")
    return "\n".join(blocks)


def to_vtt(transcript: Transcript) -> str:
    """WebVTT (.vtt) subtitle format."""
    blocks = ["WEBVTT\n"]
    for seg in transcript.segments:
        start = _fmt_timestamp(seg.start)
        end = _fmt_timestamp(seg.end)
        blocks.append(f"{start} --> {end}\n{seg.text.strip()}\n")
    return "\n".join(blocks)


def to_json(transcript: Transcript) -> str:
    """Structured JSON with metadata and segments."""
    payload = {
        "video_id": transcript.video_id,
        "language": transcript.language,
        "language_code": transcript.language_code,
        "is_generated": transcript.is_generated,
        "segments": [
            {"text": s.text, "start": s.start, "duration": s.duration}
            for s in transcript.segments
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


FORMATTERS = {
    "txt": to_txt,
    "srt": to_srt,
    "vtt": to_vtt,
    "json": to_json,
}


def render(transcript: Transcript, fmt: str, *, with_timestamps: bool = False) -> str:
    if fmt not in FORMATTERS:
        raise ValueError(f"Unknown format {fmt!r}. Choose from: {', '.join(FORMATTERS)}")
    if fmt == "txt":
        return to_txt(transcript, with_timestamps=with_timestamps)
    return FORMATTERS[fmt](transcript)
