"""WSGI entry point for production servers (gunicorn on Render, etc.).

Run with:  gunicorn wsgi:app --bind 0.0.0.0:$PORT

The static web/ directory is resolved relative to this file (the repo root),
so it works regardless of how the package was installed.

Because YouTube blocks datacenter IPs, set a proxy via env vars to make live
fetch work from a cloud host:
  - WEBSHARE_PROXY_USERNAME / WEBSHARE_PROXY_PASSWORD  (Webshare residential — recommended)
  - or TUBESCRIBE_PROXY                                (a generic http(s):// proxy URL)
"""

import os
from pathlib import Path

from tubescribe.server import create_app

_ws_user = os.environ.get("WEBSHARE_PROXY_USERNAME")
_ws_pass = os.environ.get("WEBSHARE_PROXY_PASSWORD")
_webshare = (_ws_user, _ws_pass) if _ws_user and _ws_pass else None

app = create_app(
    web_dir=Path(__file__).resolve().parent / "web",
    proxy=os.environ.get("TUBESCRIBE_PROXY") or None,
    webshare=_webshare,
)
