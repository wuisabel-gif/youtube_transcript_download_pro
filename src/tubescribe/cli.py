"""Command-line interface for TubeScribe."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .core import TubeScribeError, extract_video_id, fetch_transcript
from .formats import FORMATTERS, render


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tubescribe",
        description="Download and archive YouTube transcripts.",
    )
    parser.add_argument("--version", action="version", version=f"tubescribe {__version__}")
    parser.add_argument(
        "urls",
        nargs="+",
        metavar="URL_OR_ID",
        help="One or more YouTube video URLs or 11-character video ids.",
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
    return parser


def _process_one(url: str, args: argparse.Namespace) -> int:
    video_id = extract_video_id(url)
    languages = [c.strip() for c in args.languages.split(",") if c.strip()]
    transcript = fetch_transcript(video_id, languages=languages)
    rendered = render(transcript, args.format, with_timestamps=args.timestamps)

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        out_path = args.output_dir / f"{video_id}.{args.format}"
        out_path.write_text(rendered, encoding="utf-8")
        print(f"✓ {video_id} → {out_path}", file=sys.stderr)
    else:
        sys.stdout.write(rendered)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    failures = 0
    for url in args.urls:
        try:
            _process_one(url, args)
        except TubeScribeError as exc:
            print(f"✗ {url}: {exc}", file=sys.stderr)
            failures += 1
        except Exception as exc:  # noqa: BLE001 - surface unexpected errors per-video
            print(f"✗ {url}: unexpected error: {exc}", file=sys.stderr)
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
