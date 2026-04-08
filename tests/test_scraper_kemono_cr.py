from scrapers import kemono_cr


class _MockResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def test_build_api_url_preserves_tag_query():
    assert (
        kemono_cr._build_api_url(
            "https://kemono.cr/patreon/user/50049787?tag=AYEH"
        )
        == "https://kemono.cr/api/v1/patreon/user/50049787/posts?tag=AYEH"
    )


def test_build_api_url_preserves_search_query():
    assert (
        kemono_cr._build_api_url(
            "https://kemono.cr/patreon/user/841381?q=chapter"
        )
        == "https://kemono.cr/api/v1/patreon/user/841381/posts?q=chapter"
    )


def test_scrape_uses_query_api_url(monkeypatch):
    called = {}
    payload = [
        {
            "id": "153192843",
            "user": "50049787",
            "service": "patreon",
            "title": "70. Duty",
            "published": "2026-03-16T17:24:32",
        }
    ]

    def fake_get(url, headers=None, timeout=None):
        called["url"] = url
        called["headers"] = headers
        called["timeout"] = timeout
        return _MockResponse(payload)

    monkeypatch.setattr(kemono_cr.requests, "get", fake_get)

    chapter, timestamp, success, error, post_url = kemono_cr.scrape(
        "https://kemono.cr/patreon/user/50049787?tag=AYEH"
    )

    assert called["url"] == "https://kemono.cr/api/v1/patreon/user/50049787/posts?tag=AYEH"
    assert called["headers"]["Accept"] == "text/css"
    assert called["timeout"] == 15
    assert chapter == "70. Duty"
    assert timestamp == "2026/03/16"
    assert success is True
    assert error is None
    assert post_url == "https://kemono.cr/patreon/user/50049787/post/153192843"
