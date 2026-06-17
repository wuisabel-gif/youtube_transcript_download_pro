"""Command-line interface for TubeScribe."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .core import TubeScribeError, fetch_transcript
from .formats import FORMATTERS, render
from .sources import is_collection_url, resolve_video_ids


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tubescribe",
        description="Download and archive YouTube transcripts from videos, playlists, and channels.",
    )
    parser.add_argument("--version", action="version", version=f"tubescribe {__version__}")
    parser.add_argument(
        "urls",
        nargs="+",
        metavar="URL_OR_ID",
        help="Video URLs/ids, or playlist/channel URLs (requires the 'playlists' extra).",
    )
    parser.add_argument(
        "-f", "--format",
        choices=sorted(FORMATTERS),
        default="txt",
        help="Output format (default: txt).",
    )
    parser.add_argument(
        "-l", "--languages",
        default="en",
        help="Comma-separated preferred language codes (default: en).",
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        help="Write a file per video into this directory instead of stdout.",
    )
    parser.add_argument(
        "-t", "--timestamps",
        action="store_true",
        help="Include [HH:MM:SS] timestamps (txt format only).",
    )
    parser.add_argument(
        "-n", "--limit",
        type=int,
        default=None,
        help="Cap the number of videos pulled from each playlist/channel.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip videos whose output file already exists (requires --output-dir).",
    )
    return parser


def _fetch_and_write(video_id: str, args: argparse.Namespace) -> str:
    """Fetch one transcript and write/print it. Returns a short status word."""
    languages = [c.strip() for c in args.languages.split(",") if c.strip()]

    if args.output_dir:
        out_path = args.output_dir / f"{video_id}.{args.format}"
        if args.skip_existing and out_path.exists():
            print(f"– {video_id} → exists, skipped", file=sys.stderr)
            return "skipped"

    transcript = fetch_transcript(video_id, languages=languages)
    rendered = render(transcript, args.format, with_timestamps=args.timestamps)

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        out_path = args.output_dir / f"{video_id}.{args.format}"
        out_path.write_text(rendered, encoding="utf-8")
        print(f"✓ {video_id} → {out_path}", file=sys.stderr)
    else:
        sys.stdout.write(rendered)
    return "ok"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.skip_existing and not args.output_dir:
        print("✗ --skip-existing requires --output-dir.", file=sys.stderr)
        return 2

    # First expand any playlist/channel URLs into concrete video ids.
    targets: list[str] = []
    seen: set[str] = set()
    failures = 0
    for url in args.urls:
        try:
            collection = is_collection_url(url)
            ids = resolve_video_ids(url, limit=args.limit)
            if collection:
                print(f"• {url} → {len(ids)} video(s)", file=sys.stderr)
            for vid in ids:
                if vid not in seen:
                    seen.add(vid)
                    targets.append(vid)
        except TubeScribeError as exc:
            print(f"✗ {url}: {exc}", file=sys.stderr)
            failures += 1

    # Then fetch each video's transcript.
    for video_id in targets:
        try:
            _fetch_and_write(video_id, args)
        except TubeScribeError as exc:
            print(f"✗ {video_id}: {exc}", file=sys.stderr)
            failures += 1
        except Exception as exc:  # noqa: BLE001 - surface unexpected errors per-video
            print(f"✗ {video_id}: unexpected error: {exc}", file=sys.stderr)
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
