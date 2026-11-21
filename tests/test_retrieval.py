import pytest
from langchain_core.documents import Document

from app.database import build_database
from app.retrieval import HybridRetriever, reciprocal_rank_fusion, structured_search, tokenize


def chunk(chunk_id, text="text"):
    return Document(id=chunk_id, page_content=text, metadata={"source": chunk_id})


class FakeVectorStore:
    """Stands in for Chroma, so these tests need no embedding model."""

    def __init__(self, chunks, vector_results=()):
        self.chunks = chunks
        self.vector_results = list(vector_results)

    def get(self, include):
        return {
            "ids": [c.id for c in self.chunks],
            "documents": [c.page_content for c in self.chunks],
            "metadatas": [c.metadata for c in self.chunks],
        }

    def similarity_search(self, query, k):
        return self.vector_results[:k]


# BM25 gives a term no weight when it appears in half of the chunks, so these
# fixtures need several unrelated chunks, like a real collection has.
CHUNKS = [
    chunk("vpn", "VG-619 tunnel could not be established"),
    chunk("other-vpn", "VG-809 NAT or firewall interference"),
    chunk("battery", "Battery Care mode limits charging to 80%"),
    chunk("wifi", "Install Wi-Fi driver 23.60 from Control Center"),
    chunk("sync", "Update VeloSync to version 4.1.3"),
]


def test_tokenize_keeps_codes_and_versions_whole():
    assert tokenize("Error VG-619, update to 4.1.3.") == ["error", "vg-619", "update", "to", "4.1.3"]


def test_fusion_ranks_a_chunk_found_by_both_searches_first():
    a, b, c = chunk("a"), chunk("b"), chunk("c")
    assert reciprocal_rank_fusion([[a, b], [c, b]])[0].id == "b"


def test_fusion_returns_each_chunk_once():
    a = chunk("a")
    assert len(reciprocal_rank_fusion([[a], [a]])) == 1


def test_keyword_search_matches_the_exact_code():
    retriever = HybridRetriever(FakeVectorStore(CHUNKS))
    assert [c.id for c in retriever.keyword_search("VG-619", k=5)] == ["vpn"]


def test_keyword_search_returns_nothing_without_a_matching_term():
    retriever = HybridRetriever(FakeVectorStore(CHUNKS))
    assert retriever.keyword_search("printer", k=5) == []


def test_search_finds_a_code_that_vector_search_missed():
    missed_by_vector = [CHUNKS[1], CHUNKS[2]]
    retriever = HybridRetriever(FakeVectorStore(CHUNKS, missed_by_vector))
    assert "vpn" in [c.id for c in retriever.search("VG-619", k=2)]


def test_search_still_uses_vector_results_when_no_keyword_matches():
    retriever = HybridRetriever(FakeVectorStore(CHUNKS, [CHUNKS[3]]))
    assert [c.id for c in retriever.search("wireless keeps dropping", k=5)] == ["wifi"]


def test_search_respects_k():
    retriever = HybridRetriever(FakeVectorStore(CHUNKS, CHUNKS))
    assert len(retriever.search("VG-619", k=2)) == 2


def test_empty_vector_store_gives_a_clear_error():
    with pytest.raises(RuntimeError, match="app.ingest"):
        HybridRetriever(FakeVectorStore([]))


@pytest.fixture(scope="module")
def database():
    build_database()


def sources(documents):
    return [document.metadata["source"] for document in documents]


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("I get VG-619 at the hotel", ["VG-619"]),
        ("what does vb-e07 mean", ["VB-E07"]),
        ("Tell me about KI-140", ["KI-140"]),
        ("VG-619 and ID-423", ["VG-619", "ID-423"]),
    ],
)
def test_exact_ids_are_found(database, query, expected):
    assert sources(structured_search(query)) == expected


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("Online-only files are slow on macOS 26. Is that known?", "KI-140"),
        ("Wi-Fi keeps dropping on 6 GHz", "KI-127"),
        ("High CPU with a large library", "KI-118"),
        ("My VPN tunnel could not be established", "VG-619"),
        ("Storage is full and my quota was exceeded", "VS-1107"),
        ("The fan is overheating", "VB-E09"),
    ],
)
def test_plain_language_questions_find_the_record(database, query, expected):
    assert sources(structured_search(query))[0] == expected


@pytest.mark.parametrize(
    "query",
    [
        "How do I fix my Canon printer paper jam?",
        "What is the VeloSync Linux client download link?",
        "How long can I restore deleted files on the Team plan?",
        "battery",
    ],
)
def test_unrelated_questions_find_nothing(database, query):
    assert structured_search(query) == []


def test_unknown_code_falls_back_to_the_question_words(database):
    assert sources(structured_search("VG-999 my tunnel could not be established"))[0] == "VG-619"


def test_error_code_carries_the_escalate_flag(database):
    assert structured_search("ID-429")[0].metadata["escalate"] is True
    assert structured_search("VS-1042")[0].metadata["escalate"] is False


def test_results_record_how_they_were_matched(database):
    assert structured_search("VG-619")[0].metadata["match_type"] == "exact"
    assert structured_search("The fan is overheating")[0].metadata["match_type"] == "keyword"


def test_how_many_does_not_match_the_word_many(database):
    results = sources(structured_search("How many failed attempts before an account is locked?"))
    assert results == ["ID-423"]


def test_unfixed_known_issue_says_so(database):
    document = structured_search("KI-140")[0]
    assert "not fixed yet" in document.page_content
    assert document.metadata["product"] == "VeloSync"
