import pytest

from tubescribe.core import (
    Segment,
    Transcript,
    TubeScribeError,
    extract_video_id,
    webshare_proxy_url,
)
from tubescribe import formats


def test_webshare_proxy_url():
    assert (
        webshare_proxy_url("user", "pass")
        == "http://user-rotate:pass@p.webshare.io:80"
    )


def test_explain_maps_known_errors():
    from tubescribe.core import _explain
    from youtube_transcript_api._errors import (
        IpBlocked,
        TranscriptsDisabled,
        VideoUnavailable,
    )

    # These exceptions take the video_id as their constructor arg.
    assert "residential proxy" in _explain(IpBlocked("vid"))
    assert "disabled" in _explain(TranscriptsDisabled("vid"))
    assert "unavailable" in _explain(VideoUnavailable("vid"))
    # Anything unrecognised gets the safe fallback, not a raised error.
    assert "could not retrieve" in _explain(ValueError("boom")).lower()


@pytest.mark.parametrize(
    "url,expected",
    [
        ("dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s", "dQw4w9WgXcQ"),
    ],
)
def test_extract_video_id(url, expected):
    assert extract_video_id(url) == expected


def test_extract_video_id_invalid():
    with pytest.raises(TubeScribeError):
        extract_video_id("https://example.com/not-youtube")


@pytest.fixture
def sample():
    return Transcript(
        video_id="abc12345678",
        language="English",
        language_code="en",
        is_generated=False,
        segments=[
            Segment(text="Hello world", start=0.0, duration=1.5),
            Segment(text="second line", start=1.5, duration=2.0),
        ],
    )


def test_txt(sample):
    out = formats.render(sample, "txt")
    assert out == "Hello world\nsecond line\n"


def test_txt_timestamps(sample):
    out = formats.render(sample, "txt", with_timestamps=True)
    assert out.startswith("[00:00:00] Hello world")


def test_srt(sample):
    out = formats.render(sample, "srt")
    assert "1\n00:00:00,000 --> 00:00:01,500\nHello world" in out


def test_vtt(sample):
    out = formats.render(sample, "vtt")
    assert out.startswith("WEBVTT")
    assert "00:00:01.500 --> 00:00:03.500" in out


def test_json(sample):
    import json

    out = json.loads(formats.render(sample, "json"))
    assert out["video_id"] == "abc12345678"
    assert len(out["segments"]) == 2
