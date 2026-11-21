"""API tests. The answering function is faked, so no model loading and no API calls."""
import anthropic
import httpx
import pytest
from fastapi.testclient import TestClient

from app import main
from app.schema import Source, SupportResponse

ANSWER = SupportResponse(
    outcome="answered",
    answer="Select Sign in again in VeloSync.",
    escalate=False,
    escalation_reason="",
    sources=[Source(id="VS-1042", title="Sign-in expired", type="error_code")],
)


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(main, "warm_up", lambda: None)
    asked = []

    def fake_answer(question):
        asked.append(question)
        return ANSWER

    main.app.dependency_overrides[main.get_answerer] = lambda: fake_answer
    with TestClient(main.app) as test_client:
        test_client.asked = asked
        yield test_client
    main.app.dependency_overrides.clear()


def failing(error):
    def answer(question):
        raise error
    return lambda: answer


def api_error(cls, status):
    request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    return cls("boom", response=httpx.Response(status, request=request), body=None)


def test_ask_returns_the_answer(client):
    response = client.post("/ask", json={"question": "  VeloSync says VS-1042  "})
    assert response.status_code == 200
    assert response.json() == ANSWER.model_dump()
    assert client.asked == ["VeloSync says VS-1042"]  # whitespace stripped


@pytest.mark.parametrize("body", [{}, {"question": ""}, {"question": "   "}, {"question": "x" * 2001}, {"question": 5}])
def test_ask_rejects_bad_questions(client, body):
    assert client.post("/ask", json=body).status_code == 422
    assert client.asked == []


@pytest.mark.parametrize(
    ("error", "status"),
    [
        (api_error(anthropic.RateLimitError, 429), 503),
        (api_error(anthropic.InternalServerError, 500), 503),
        (api_error(anthropic.AuthenticationError, 401), 502),
        (RuntimeError("Claude returned no answer"), 502),
    ],
)
def test_ask_maps_upstream_errors(client, error, status):
    main.app.dependency_overrides[main.get_answerer] = failing(error)
    response = client.post("/ask", json={"question": "Hello"})
    assert response.status_code == status
    assert "boom" not in response.json()["detail"]  # internal details stay in the log


def test_health_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_startup_failure_is_reported(monkeypatch):
    def broken():
        raise FileNotFoundError("chroma_db missing")

    monkeypatch.setattr(main, "warm_up", broken)
    with TestClient(main.app) as client:
        health = client.get("/health")
        assert health.status_code == 503
        assert "chroma_db missing" in health.json()["error"]
        assert client.post("/ask", json={"question": "Hello"}).status_code == 503


def test_frontend_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<html" in response.text


@pytest.mark.parametrize(("path", "content_type"), [("/", "text/html"), ("/style.css", "text/css"),
                                                     ("/app.js", "javascript")])
def test_frontend_files_are_revalidated(client, path, content_type):
    # Without this header a browser can keep using a stale (once empty) style.css or app.js.
    response = client.get(path)
    assert response.status_code == 200
    assert content_type in response.headers["content-type"]
    assert response.headers["cache-control"] == "no-cache"
