"""RAG chain tests. They use a fake Claude client, so they cost nothing and need no key."""

from types import SimpleNamespace

import pytest
from langchain_core.documents import Document

import app.rag_chain as rag_chain
from app.config import settings
from app.rag_chain import SYSTEM_PROMPT, answer_question
from app.schema import ModelAnswer


def document(source, source_type="kb_article", **metadata):
    return Document(
        page_content=f"Text of {source}",
        metadata={"source": source, "source_type": source_type, "title": f"Title {source}", **metadata},
    )


class FakeClient:
    """Records each request and returns a prepared response."""

    def __init__(self, parsed_output=None, stop_reason="end_turn"):
        self.requests = []
        response = SimpleNamespace(stop_reason=stop_reason, parsed_output=parsed_output)

        def parse(**request):
            self.requests.append(request)
            return response

        self.messages = SimpleNamespace(parse=parse)


def model_answer(outcome="answered", cited=("KB-1002",), reason=""):
    return ModelAnswer(
        outcome=outcome, answer="Do this.", cited_sources=list(cited), escalation_reason=reason
    )


@pytest.fixture
def retrieved(monkeypatch):
    """Replace retrieval with a fixed list of documents."""
    documents = [document("KB-1002")]
    monkeypatch.setattr(rag_chain, "retrieve", lambda question: documents)
    return documents


def test_request_sends_sources_question_and_settings(retrieved):
    client = FakeClient(model_answer())
    answer_question("VeloSync is stuck", client=client)

    request = client.requests[0]
    assert request["model"] == settings.llm_model
    assert request["output_format"] is ModelAnswer
    assert "fallbacks" not in request  # Haiku 5.5 has no server-side fallback.
    assert request["system"][0]["text"] == SYSTEM_PROMPT
    assert request["system"][0]["cache_control"] == {"type": "ephemeral"}
    content = request["messages"][0]["content"]
    assert '<source id="KB-1002" type="kb_article"' in content
    assert "<question>\nVeloSync is stuck\n</question>" in content


def test_sources_come_from_the_citations(retrieved):
    retrieved.append(document("T-48410", "ticket"))
    response = answer_question("q", client=FakeClient(model_answer(cited=["T-48410", "KB-1002"])))
    assert [(s.id, s.type) for s in response.sources] == [("T-48410", "ticket"), ("KB-1002", "kb_article")]


def test_citations_of_sources_not_given_are_dropped(retrieved):
    response = answer_question("q", client=FakeClient(model_answer(cited=["KB-1002", "KB-9999", "KB-1002"])))
    assert [s.id for s in response.sources] == ["KB-1002"]


def test_exact_error_code_marked_escalate_forces_escalation(retrieved):
    retrieved.append(document("ID-429", "error_code", escalate=True, match_type="exact"))
    response = answer_question("ID-429", client=FakeClient(model_answer()))
    assert response.outcome == "escalate"
    assert response.escalate is True
    assert "ID-429" in response.escalation_reason


def test_keyword_match_marked_escalate_does_not_force_escalation(retrieved):
    retrieved.append(document("ID-429", "error_code", escalate=True, match_type="keyword"))
    response = answer_question("too many attempts", client=FakeClient(model_answer()))
    assert response.outcome == "answered"
    assert response.escalate is False


def test_escalation_reason_is_cleared_when_not_escalating(retrieved):
    response = answer_question("q", client=FakeClient(model_answer(reason="stray text")))
    assert response.escalation_reason == ""


def test_escalation_from_claude_is_kept(retrieved):
    response = answer_question("q", client=FakeClient(model_answer("escalate", reason="Ransomware")))
    assert response.escalate is True
    assert response.escalation_reason == "Ransomware"


def test_refusal_is_escalated_to_a_human(retrieved):
    response = answer_question("q", client=FakeClient(stop_reason="refusal"))
    assert response.outcome == "escalate"
    assert response.sources == []


def test_missing_answer_raises(retrieved):
    with pytest.raises(RuntimeError, match="max_tokens"):
        answer_question("q", client=FakeClient(stop_reason="max_tokens"))
