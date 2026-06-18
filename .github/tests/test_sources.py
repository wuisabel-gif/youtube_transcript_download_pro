import pytest

from tubescribe import sources


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://www.youtube.com/playlist?list=PLabc", True),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLabc", True),
        ("https://www.youtube.com/@TED", True),
        ("https://www.youtube.com/@TED/videos", True),
        ("https://www.youtube.com/channel/UCabc", True),
        ("https://www.youtube.com/c/SomeName", True),
        ("https://www.youtube.com/user/SomeUser", True),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", False),
        ("https://youtu.be/dQw4w9WgXcQ", False),
        ("dQw4w9WgXcQ", False),
    ],
)
def test_is_collection_url(url, expected):
    assert sources.is_collection_url(url) is expected


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://www.youtube.com/@TED", "https://www.youtube.com/@TED/videos"),
        ("https://www.youtube.com/channel/UCabc", "https://www.youtube.com/channel/UCabc/videos"),
        # Already-tabbed URLs are left alone.
        ("https://www.youtube.com/@TED/videos", "https://www.youtube.com/@TED/videos"),
        ("https://www.youtube.com/@TED/streams", "https://www.youtube.com/@TED/streams"),
        # Non-channel URLs untouched.
        ("https://www.youtube.com/playlist?list=PLabc", "https://www.youtube.com/playlist?list=PLabc"),
    ],
)
def test_normalize_channel_url(url, expected):
    assert sources._normalize_channel_url(url) == expected


def test_collect_ids_flat():
    info = {"entries": [{"id": "dQw4w9WgXcQ"}, {"id": "8jPQjjsBbIc"}]}
    out: list[str] = []
    sources._collect_ids(info, out)
    assert out == ["dQw4w9WgXcQ", "8jPQjjsBbIc"]


def test_collect_ids_nested_and_deduped():
    info = {
        "entries": [
            {"entries": [{"id": "dQw4w9WgXcQ"}]},
            {"id": "dQw4w9WgXcQ"},  # duplicate, dropped
            {"id": "PLnotavideoid01234"},  # not 11 chars, dropped
            {"id": "8jPQjjsBbIc"},
        ]
    }
    out: list[str] = []
    sources._collect_ids(info, out)
    assert out == ["dQw4w9WgXcQ", "8jPQjjsBbIc"]
