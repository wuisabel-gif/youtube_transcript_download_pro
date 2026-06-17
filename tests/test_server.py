import pytest

pytest.importorskip("flask")

from tubescribe import server
from tubescribe.core import Segment, Transcript


@pytest.fixture
def client(monkeypatch):
    # Stub network-touching functions so the endpoint is tested in isolation.
    def fake_resolve(url, limit=None, proxy=None):
        if "playlist" in url:
            return ["aaaaaaaaaaa", "bbbbbbbbbbb"][: (limit or 2)]
        if "bad" in url:
            from tubescribe.core import TubeScribeError

            raise TubeScribeError("cannot resolve")
        return [url]

    def fake_fetch(video_id, languages=("en",), proxy=None):
        return Transcript(
            video_id=video_id,
            language="English",
            language_code="en",
            is_generated=False,
            segments=[Segment(text="hi", start=0.0, duration=1.0)],
        )

    monkeypatch.setattr(server, "resolve_video_ids", fake_resolve)
    monkeypatch.setattr(server, "fetch_transcript", fake_fetch)

    app = server.create_app()
    app.testing = True
    return app.test_client()


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json()["ok"] is True


def test_single_video(client):
    res = client.post("/api/transcript", json={"urls": ["12345678901"], "format": "srt"})
    data = res.get_json()
    assert res.status_code == 200
    assert len(data["results"]) == 1
    r = data["results"][0]
    assert r["video_id"] == "12345678901"
    assert r["filename"] == "12345678901.srt"
    assert "00:00:00,000 --> 00:00:01,000" in r["content"]
    assert data["errors"] == []


def test_playlist_expansion_and_dedup(client):
    res = client.post(
        "/api/transcript",
        json={"urls": ["https://youtube.com/playlist?list=x", "aaaaaaaaaaa"]},
    )
    data = res.get_json()
    # playlist -> aaaa, bbbb; plus aaaa again should dedupe to 2 total
    ids = [r["video_id"] for r in data["results"]]
    assert ids == ["aaaaaaaaaaa", "bbbbbbbbbbb"]


def test_per_input_error_does_not_fail_request(client):
    res = client.post("/api/transcript", json={"urls": ["https://youtube.com/bad"]})
    data = res.get_json()
    assert res.status_code == 200
    assert data["results"] == []
    assert data["errors"][0]["error"] == "cannot resolve"


def test_empty_and_bad_format(client):
    assert client.post("/api/transcript", json={"urls": []}).status_code == 400
    assert (
        client.post("/api/transcript", json={"urls": ["x"], "format": "pdf"}).status_code
        == 400
    )
