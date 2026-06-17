"""Core transcript fetching and formatting logic."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import parse_qs, urlparse

_VIDEO_ID_RE = re.compile(r"^[0-9A-Za-z_-]{11}$")


class TubeScribeError(Exception):
    """Base error for TubeScribe."""


def extract_video_id(url_or_id: str) -> str:
    """Pull an 11-character YouTube video id out of a URL or bare id.

    Supports the common forms:
      - https://www.youtube.com/watch?v=VIDEOID
      - https://youtu.be/VIDEOID
      - https://www.youtube.com/embed/VIDEOID
      - https://www.youtube.com/shorts/VIDEOID
      - VIDEOID (already an id)
    """
    candidate = url_or_id.strip()

    if _VIDEO_ID_RE.match(candidate):
        return candidate

    parsed = urlparse(candidate)
    host = (parsed.hostname or "").lower().removeprefix("www.")

    if host == "youtu.be":
        vid = parsed.path.lstrip("/").split("/")[0]
        if _VIDEO_ID_RE.match(vid):
            return vid

    if host in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
        if parsed.path == "/watch":
            vid = parse_qs(parsed.query).get("v", [""])[0]
            if _VIDEO_ID_RE.match(vid):
                return vid
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) >= 2 and parts[0] in {"embed", "shorts", "v", "live"}:
            if _VIDEO_ID_RE.match(parts[1]):
                return parts[1]

    raise TubeScribeError(f"Could not extract a video id from: {url_or_id!r}")


@dataclass
class Segment:
    """A single timed caption cue."""

    text: str
    start: float
    duration: float

    @property
    def end(self) -> float:
        return self.start + self.duration


@dataclass
class Transcript:
    """A fetched transcript for a single video."""

    video_id: str
    language: str
    language_code: str
    is_generated: bool
    segments: list[Segment]


def fetch_transcript(
    video_id: str,
    languages: Iterable[str] = ("en",),
) -> Transcript:
    """Fetch the best available transcript for a video.

    Prefers a manually created transcript in one of ``languages``, falling back
    to an auto-generated one, then to any available transcript that can be
    translated into the first requested language.
    """
    # Imported lazily so ``--help`` and unit tests don't require the network dep.
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        CouldNotRetrieveTranscript,
        NoTranscriptFound,
        TranscriptsDisabled,
    )

    langs = list(languages) or ["en"]
    api = YouTubeTranscriptApi()

    try:
        listing = api.list(video_id)
    except TranscriptsDisabled as exc:
        raise TubeScribeError(f"Transcripts are disabled for {video_id}.") from exc
    except CouldNotRetrieveTranscript as exc:
        raise TubeScribeError(f"Could not retrieve transcript for {video_id}: {exc}") from exc

    try:
        picked = listing.find_transcript(langs)
    except NoTranscriptFound:
        try:
            picked = listing.find_generated_transcript(langs)
        except NoTranscriptFound:
            # Last resort: take any transcript and translate it.
            available = list(listing)
            if not available:
                raise TubeScribeError(f"No transcripts available for {video_id}.")
            base = available[0]
            picked = base.translate(langs[0]) if base.is_translatable else base

    fetched = picked.fetch()
    segments = [
        Segment(text=row["text"], start=float(row["start"]), duration=float(row["duration"]))
        for row in fetched.to_raw_data()
    ]
    return Transcript(
        video_id=video_id,
        language=picked.language,
        language_code=picked.language_code,
        is_generated=picked.is_generated,
        segments=segments,
    )
