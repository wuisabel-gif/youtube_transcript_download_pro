"""WSGI entry point for production servers (gunicorn on Render, etc.).

Run with:  gunicorn wsgi:app --bind 0.0.0.0:$PORT

The static web/ directory is resolved relative to this file (the repo root),
so it works regardless of how the package was installed. Set the optional
TUBESCRIBE_PROXY env var to route YouTube requests through a proxy — useful
because YouTube rate-limits/blocks datacenter IPs.
"""

import os
from pathlib import Path

from tubescribe.server import create_app

app = create_app(
    web_dir=Path(__file__).resolve().parent / "web",
    proxy=os.environ.get("TUBESCRIBE_PROXY") or None,
)
