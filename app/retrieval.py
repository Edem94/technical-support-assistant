"""Hybrid search: combine vector search with BM25 keyword search.

Vector search finds text with a similar meaning, even in different words.
Keyword search finds exact terms such as VG-619, which embeddings handle poorly.
Reciprocal rank fusion merges the two ranked lists into one.

Error codes and known issues live in SQLite, not Chroma. retrieve() looks them up
by exact code, falls back to matching the words of a plain-language question, and
returns any matches ahead of the hybrid search results.
"""

import re
from collections import defaultdict
from functools import lru_cache

from langchain_chroma import Chroma
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
from sqlalchemy.orm import Session

from app.config import settings
from app.database import (
    ErrorCode,
    KnownIssue,
    SessionLocal,
    get_structured_record,
    search_structured_records,
)
from app.ingest import get_vector_store

# Keeps error codes and versions whole: "VG-619" and "4.1.3" are single tokens.
TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:[-.][a-z0-9]+)*")

# Matches VG-619, VB-E07 and KI-140.
RECORD_ID_PATTERN = re.compile(r"\b[a-z]{2}-[a-z]?\d{2,4}\b", re.IGNORECASE)

# "Long" means something in "path too long", but not in "how long can I".
QUESTION_PHRASE_PATTERN = re.compile(r"\bhow (?:long|many|much)\b", re.IGNORECASE)

# Common question words, which say nothing about which record is relevant.
STOP_WORDS = frozenset(
    """
    a about after all am an and any are as at be been but by can cannot could did do does
    error errors few fix for from get gets getting got had has have help how i if in into
    is issue issues it its just keep keeps known me more my no not of on or our please
    problem problems should so some than that the their them then there these they this
    to too up very was we were what when where which who why will with would you your
    """.split()
)


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


def find_by_id(session: Session, query: str) -> list[ErrorCode | KnownIssue]:
    record_ids = dict.fromkeys(code.upper() for code in RECORD_ID_PATTERN.findall(query))
    records = [get_structured_record(session, record_id) for record_id in record_ids]
    return [record for record in records if record is not None]


def find_by_words(session: Session, query: str) -> list[ErrorCode | KnownIssue]:
    question = QUESTION_PHRASE_PATTERN.sub(" ", query)
    terms = [term for term in tokenize(question) if term not in STOP_WORDS]
    return search_structured_records(session, terms)


def to_document(record: ErrorCode | KnownIssue, match_type: str) -> Document:
    """Convert a record. match_type is "exact" (ID in the query) or "keyword" (shared words).

    Only trust the escalate flag on exact matches: a keyword match can be a coincidence.
    """
    if isinstance(record, ErrorCode):
        text = (
            f"Error code {record.code}: {record.title}\n"
            f"Cause: {record.cause}\n"
            f"Fix: {record.fix_summary}"
        )
        metadata = {
            "source": record.code,
            "source_type": "error_code",
            "escalate": record.escalate,
        }
    else:
        text = (
            f"Known issue {record.issue_id}: {record.title}\n"
            f"Affected versions: {record.affected_versions}\n"
            f"Status: {record.status}\n"
            f"Fixed in: {record.fixed_in or 'not fixed yet'}\n"
            f"Workaround: {record.workaround}"
        )
        metadata = {
            "source": record.issue_id,
            "source_type": "known_issue",
            "escalate": False,
        }

    metadata |= {
        "title": record.title,
        "product": record.product.name,
        "kb_id": record.kb_id or "",
        "match_type": match_type,
    }
    return Document(id=metadata["source"], page_content=text, metadata=metadata)


def structured_search(query: str) -> list[Document]:
    """Look up records by exact ID, or by the words of the question if no ID matches."""
    with SessionLocal() as session:
        if records := find_by_id(session, query):
            return [to_document(record, "exact") for record in records]
        return [to_document(record, "keyword") for record in find_by_words(session, query)]


def retrieve(query: str, k: int = settings.retrieval_top_k) -> list[Document]:
    """Return SQLite matches first, followed by the top k hybrid search results."""
    return structured_search(query) + get_retriever().search(query, k)
