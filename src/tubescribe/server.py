"""A tiny Flask backend that serves the TubeScribe web UI and a fetch API.

It is intentionally thin: every endpoint just calls the same library functions
the CLI uses (:mod:`tubescribe.sources`, :mod:`tubescribe.core`,
:mod:`tubescribe.formats`), so the web app and the command line stay in sync.

Run it with::

    pip install -e ".[server,playlists]"
    tubescribe-serve            # → http://127.0.0.1:8000
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .core import TubeScribeError, fetch_transcript
from .formats import FORMATTERS, render
from .sources import resolve_video_ids

# Repo layout: src/tubescribe/server.py → <repo>/web/index.html
WEB_DIR = Path(__file__).resolve().parent.parent.parent / "web"

MAX_VIDEOS = 100  # safety cap so one request can't fan out unbounded


def _parse_languages(value) -> list[str]:
    if isinstance(value, str):
        return [c.strip() for c in value.split(",") if c.strip()] or ["en"]
    if isinstance(value, list) and value:
        return [str(c).strip() for c in value if str(c).strip()]
    return ["en"]


def create_app(web_dir: Path = WEB_DIR, proxy: str | None = None):
    from flask import Flask, jsonify, request, send_from_directory

    app = Flask(__name__, static_folder=None)

    @app.after_request
    def _cors(resp):
        # Permissive CORS so the page also works if opened from file:// during dev.
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return resp

    @app.get("/")
    def index():
        if not (web_dir / "index.html").exists():
            return ("web/index.html not found — run from a source checkout.", 404)
        return send_from_directory(web_dir, "index.html")

    @app.get("/api/health")
    def health():
        return jsonify({"ok": True, "service": "tubescribe"})

    @app.route("/api/transcript", methods=["POST", "OPTIONS"])
    def transcript():
        if request.method == "OPTIONS":
            return ("", 204)

        data = request.get_json(silent=True) or {}

        urls = data.get("urls") or []
        if isinstance(urls, str):
            urls = [urls]
        urls = [u.strip() for u in urls if isinstance(u, str) and u.strip()]
        if not urls:
            return jsonify({"error": "No URLs or video ids provided."}), 400

        fmt = str(data.get("format", "txt"))
        if fmt not in FORMATTERS:
            return jsonify({"error": f"Unknown format {fmt!r}."}), 400

        languages = _parse_languages(data.get("languages"))
        timestamps = bool(data.get("timestamps"))
        raw_limit = data.get("limit")
        try:
            limit = int(raw_limit) if raw_limit not in (None, "", 0, "0") else None
        except (TypeError, ValueError):
            limit = None

        # 1) Expand any playlist/channel URLs into concrete video ids.
        video_ids: list[str] = []
        seen: set[str] = set()
        errors: list[dict] = []
        for url in urls:
            try:
                for vid in resolve_video_ids(url, limit=limit, proxy=proxy):
                    if vid not in seen:
                        seen.add(vid)
                        video_ids.append(vid)
            except TubeScribeError as exc:
                errors.append({"input": url, "error": str(exc)})

        truncated = len(video_ids) > MAX_VIDEOS
        video_ids = video_ids[:MAX_VIDEOS]

        # 2) Fetch + render each transcript.
        results: list[dict] = []
        for vid in video_ids:
            try:
                t = fetch_transcript(vid, languages=languages, proxy=proxy)
                content = render(t, fmt, with_timestamps=timestamps)
                duration = t.segments[-1].end if t.segments else 0.0
                results.append(
                    {
                        "video_id": vid,
                        "format": fmt,
                        "filename": f"{vid}.{fmt}",
                        "language": t.language,
                        "language_code": t.language_code,
                        "is_generated": t.is_generated,
                        "segments": len(t.segments),
                        "duration": duration,
                        "content": content,
                    }
                )
            except TubeScribeError as exc:
                errors.append({"input": vid, "error": str(exc)})
            except Exception as exc:  # noqa: BLE001 - never 500 on one bad video
                errors.append({"input": vid, "error": f"unexpected error: {exc}"})

        return jsonify({"results": results, "errors": errors, "truncated": truncated})

    return app


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tubescribe-serve",
        description="Serve the TubeScribe web UI and transcript API.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default 127.0.0.1).")
    parser.add_argument("--port", type=int, default=8000, help="Bind port (default 8000).")
    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode.")
    parser.add_argument(
        "--proxy",
        default=None,
        metavar="URL",
        help="Route YouTube requests through an http(s):// proxy (helps from blocked IPs).",
    )
    args = parser.parse_args(argv)

    try:
        app = create_app(proxy=args.proxy)
    except ImportError:
        print(
            "Flask is required to run the server. Install it with:\n"
            '    pip install "tubescribe[server]"',
        )
        return 1

    print(f"TubeScribe → http://{args.host}:{args.port}  (Ctrl+C to stop)")
    app.run(host=args.host, port=args.port, debug=args.debug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
