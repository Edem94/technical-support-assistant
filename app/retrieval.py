"""Hybrid search: combine vector search with BM25 keyword search.

Vector search finds text with a similar meaning, even in different words.
Keyword search finds exact terms such as VG-619, which embeddings handle poorly.
Reciprocal rank fusion merges the two ranked lists into one.
"""

import re
from collections import defaultdict
from functools import lru_cache

from langchain_chroma import Chroma
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from app.config import settings
from app.ingest import get_vector_store

# Keeps error codes and versions whole: "VG-619" and "4.1.3" are single tokens.
TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:[-.][a-z0-9]+)*")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def reciprocal_rank_fusion(rankings: list[list[Document]]) -> list[Document]:
    """Merge ranked lists, favouring chunks that rank highly in several lists.

    Fusion uses positions rather than scores, because vector distances and
    BM25 scores are on different scales and cannot be compared directly.
    """
    scores = defaultdict(float)
    chunks = {}
    for ranking in rankings:
        for rank, chunk in enumerate(ranking, start=1):
            scores[chunk.id] += 1 / (settings.rrf_k + rank)
            chunks[chunk.id] = chunk
    return [chunks[chunk_id] for chunk_id in sorted(scores, key=scores.get, reverse=True)]


class HybridRetriever:
    def __init__(self, vector_store: Chroma):
        stored = vector_store.get(include=["documents", "metadatas"])
        if not stored["ids"]:
            raise RuntimeError("The vector store is empty. Run: python -m app.ingest")

        self.vector_store = vector_store
        self.chunks = [
            Document(id=chunk_id, page_content=text, metadata=metadata)
            for chunk_id, text, metadata in zip(
                stored["ids"], stored["documents"], stored["metadatas"]
            )
        ]
        self.keyword_index = BM25Okapi([tokenize(chunk.page_content) for chunk in self.chunks])

    def vector_search(self, query: str, k: int) -> list[Document]:
        return self.vector_store.similarity_search(query, k=k)

    def keyword_search(self, query: str, k: int) -> list[Document]:
        scores = self.keyword_index.get_scores(tokenize(query))
        ranked = sorted(zip(scores, self.chunks), key=lambda pair: pair[0], reverse=True)
        # A score of 0 means the chunk shares no terms with the query.
        return [chunk for score, chunk in ranked[:k] if score > 0]

    def search(self, query: str, k: int = settings.retrieval_top_k) -> list[Document]:
        candidates = settings.retrieval_candidates
        fused = reciprocal_rank_fusion(
            [self.vector_search(query, candidates), self.keyword_search(query, candidates)]
        )
        return fused[:k]


@lru_cache
def get_retriever() -> HybridRetriever:
    """Return a shared retriever, so the model and index are only loaded once."""
    return HybridRetriever(get_vector_store())
