"""Expand playlist and channel URLs into individual video ids.

Uses ``yt-dlp`` (an optional dependency) to enumerate videos. Single-video URLs
are handled without it via :func:`tubescribe.core.extract_video_id`.
"""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from .core import _VIDEO_ID_RE, TubeScribeError, extract_video_id

_CHANNEL_PREFIXES = ("/@", "/channel/", "/c/", "/user/")
_CHANNEL_TABS = ("/videos", "/streams", "/shorts", "/playlists", "/featured", "/community")


def is_collection_url(url: str) -> bool:
    """True if the URL refers to a playlist or a channel (not a single video)."""
    parsed = urlparse(url.strip())
    host = (parsed.hostname or "").lower().removeprefix("www.")
    if host not in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
        return False
    if "list" in parse_qs(parsed.query):
        return True
    if parsed.path == "/playlist":
        return True
    return any(parsed.path.startswith(p) for p in _CHANNEL_PREFIXES)


def _normalize_channel_url(url: str) -> str:
    """Point a bare channel URL at its Videos tab for clean enumeration.

    ``youtube.com/@handle`` -> ``youtube.com/@handle/videos``. URLs that already
    target a specific tab, or that are playlists, are returned unchanged.
    """
    parsed = urlparse(url.strip())
    path = parsed.path
    is_channel = any(path.startswith(p) for p in _CHANNEL_PREFIXES)
    if not is_channel:
        return url
    if any(tab in path for tab in _CHANNEL_TABS):
        return url
    new_path = path.rstrip("/") + "/videos"
    return parsed._replace(path=new_path).geturl()


def _collect_ids(info: object, out: list[str]) -> None:
    """Recursively gather 11-char video ids from a yt-dlp info dict."""
    if not isinstance(info, dict):
        return
    entries = info.get("entries")
    if entries:
        for entry in entries:
            _collect_ids(entry, out)
        return
    vid = info.get("id")
    if isinstance(vid, str) and _VIDEO_ID_RE.match(vid):
        if vid not in out:
            out.append(vid)


def expand_collection(
    url: str, limit: int | None = None, proxy: str | None = None
) -> list[str]:
    """Return the video ids contained in a playlist or channel URL."""
    try:
        import yt_dlp  # noqa: F401
    except ImportError as exc:  # pragma: no cover - exercised only without the extra
        raise TubeScribeError(
            "Playlist/channel expansion requires yt-dlp. "
            "Install it with: pip install 'tubescribe[playlists]'"
        ) from exc

    from yt_dlp import YoutubeDL
    from yt_dlp.utils import DownloadError

    target = _normalize_channel_url(url)
    opts: dict = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": True,
    }
    if limit:
        opts["playlistend"] = limit
    if proxy:
        opts["proxy"] = proxy

    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(target, download=False)
    except DownloadError as exc:
        raise TubeScribeError(f"Could not enumerate {url}: {exc}") from exc

    ids: list[str] = []
    _collect_ids(info, ids)
    if limit:
        ids = ids[:limit]
    if not ids:
        raise TubeScribeError(f"No videos found at {url}.")
    return ids


def resolve_video_ids(
    url: str, limit: int | None = None, proxy: str | None = None
) -> list[str]:
    """Resolve any supported URL/id into a list of video ids.

    Single videos return a one-element list; playlists and channels are expanded.
    """
    if is_collection_url(url):
        return expand_collection(url, limit=limit, proxy=proxy)
    return [extract_video_id(url)]
