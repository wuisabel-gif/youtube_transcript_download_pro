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


def webshare_proxy_url(username: str, password: str) -> str:
    """Build the rotating-endpoint URL for Webshare residential proxies.

    Mirrors how youtube-transcript-api's ``WebshareProxyConfig`` rotates across
    the pool (``-rotate`` username suffix); used to pass the same proxy to
    yt-dlp for playlist/channel enumeration.
    """
    return f"http://{username}-rotate:{password}@p.webshare.io:80"


def _explain(exc: Exception) -> str:
    """Turn a youtube-transcript-api error into a short, honest message.

    The library's default messages blame "IP blocking" for almost everything;
    here we distinguish the real causes so the user knows what to actually do.
    Callers already prefix the video id, so it isn't repeated here.
    """
    from youtube_transcript_api._errors import (
        AgeRestricted,
        IpBlocked,
        RequestBlocked,
        TranscriptsDisabled,
        VideoUnavailable,
        VideoUnplayable,
    )

    if isinstance(exc, (IpBlocked, RequestBlocked)):
        return (
            "YouTube blocked this request — the IP is likely a cloud/datacenter "
            "address. Use a residential proxy (--proxy URL, or Webshare credentials)."
        )
    if isinstance(exc, TranscriptsDisabled):
        return "the uploader has disabled captions/transcripts for this video."
    if isinstance(exc, AgeRestricted):
        return "this video is age-restricted, so its transcript can't be fetched."
    if isinstance(exc, (VideoUnavailable, VideoUnplayable)):
        return "this video is unavailable or can't be played."
    return "could not retrieve the transcript (unknown reason)."


def fetch_transcript(
    video_id: str,
    languages: Iterable[str] = ("en",),
    proxy: str | None = None,
    webshare: tuple[str, str] | None = None,
) -> Transcript:
    """Fetch the best available transcript for a video.

    Prefers a manually created transcript in one of ``languages``, falling back
    to an auto-generated one. If none match, raises a :class:`TubeScribeError`
    that lists the languages the video *does* have, so the caller can retry with
    the right ``-l`` code.

    Proxy options (for cloud IPs that YouTube blocks):
      - ``webshare`` — a ``(username, password)`` pair for Webshare residential
        proxies (recommended; uses the rotating residential pool).
      - ``proxy`` — a generic ``http(s)://`` proxy URL.
    ``webshare`` takes precedence if both are given.
    """
    # Imported lazily so ``--help`` and unit tests don't require the network dep.
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        CouldNotRetrieveTranscript,
        NoTranscriptFound,
    )

    langs = list(languages) or ["en"]
    if webshare:
        from youtube_transcript_api.proxies import WebshareProxyConfig

        api = YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=webshare[0], proxy_password=webshare[1]
            )
        )
    elif proxy:
        from youtube_transcript_api.proxies import GenericProxyConfig

        api = YouTubeTranscriptApi(
            proxy_config=GenericProxyConfig(http_url=proxy, https_url=proxy)
        )
    else:
        api = YouTubeTranscriptApi()

    try:
        listing = api.list(video_id)
    except CouldNotRetrieveTranscript as exc:
        raise TubeScribeError(_explain(exc)) from exc

    available_codes = [t.language_code for t in listing]

    try:
        picked = listing.find_transcript(langs)
    except NoTranscriptFound:
        try:
            picked = listing.find_generated_transcript(langs)
        except NoTranscriptFound:
            # The requested language(s) aren't available — tell the user what is.
            avail = ", ".join(available_codes) if available_codes else "none"
            hint = f" Try -l {available_codes[0]}." if available_codes else ""
            raise TubeScribeError(
                f"no transcript in {', '.join(langs)}. Available: {avail}.{hint}"
            ) from None

    try:
        fetched = picked.fetch()
    except CouldNotRetrieveTranscript as exc:
        raise TubeScribeError(_explain(exc)) from exc
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
