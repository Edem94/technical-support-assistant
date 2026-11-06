import pytest
from langchain_core.documents import Document

from app.retrieval import HybridRetriever, reciprocal_rank_fusion, tokenize


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
