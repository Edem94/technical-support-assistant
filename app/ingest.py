"""Load support documents into the Chroma vector store.

Run from the repository root:

    python -m app.ingest

Each run rebuilds the SQLite database and the Chroma collection from data/.
CSV data (error codes, known issues) stays in SQLite for exact lookups.
"""

import re
from collections import Counter
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from pypdf import PdfReader
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Article, SessionLocal, Ticket, build_database

MANUAL_PRODUCTS = {"velobook-14-user-guide.pdf": "VeloBook 14"}

section_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("##", "section")], strip_headers=False
)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap
)


def extract_pages_from_pdf(pdf_path: Path) -> list[str]:
    """Return the text of each page, keeping table rows on one line."""
    reader = PdfReader(pdf_path)
    return [page.extract_text(extraction_mode="layout") for page in reader.pages]


def load_articles(session: Session) -> list[Document]:
    """Return one document per article section. Deprecated articles are left out."""
    articles = session.scalars(select(Article).where(Article.status == "published"))
    documents = []
    for article in articles:
        # The title is added to every chunk later, so drop the "# Title" line here.
        body = re.sub(r"^# .*\n+", "", article.body)
        for section in section_splitter.split_text(body):
            section.metadata |= {
                "source": article.kb_id,
                "source_type": "kb_article",
                "title": article.title,
                "product": article.product,
                "category": article.category,
                "updated": article.updated,
            }
            documents.append(section)
    return documents


def load_manuals(manuals_dir: Path) -> list[Document]:
    """Return one document per PDF page."""
    documents = []
    for path in sorted(manuals_dir.glob("*.pdf")):
        title = PdfReader(path).metadata.title or path.stem
        for page_number, text in enumerate(extract_pages_from_pdf(path), start=1):
            metadata = {
                "source": path.name,
                "source_type": "manual",
                "title": title,
                "product": MANUAL_PRODUCTS[path.name],
                "page": page_number,
            }
            documents.append(Document(page_content=text, metadata=metadata))
    return documents


def load_tickets(session: Session) -> list[Document]:
    """Return one document per ticket. Open tickets have no solution, so they are left out."""
    tickets = session.scalars(select(Ticket).where(Ticket.status == "resolved"))
    return [
        Document(
            page_content=f"Problem: {ticket.description}\nResolution: {ticket.resolution}",
            metadata={
                "source": ticket.ticket_id,
                "source_type": "ticket",
                "title": ticket.subject,
                "product": ticket.product.name,
                "updated": ticket.created_at[:10],
                "kb_refs": ",".join(article.kb_id for article in ticket.articles),
            },
        )
        for ticket in tickets
    ]


def chunk_documents(documents: list[Document]) -> list[Document]:
    """Split documents into chunks that start with their title and have a stable ID."""
    chunks = text_splitter.split_documents(documents)
    counts = Counter()
    for chunk in chunks:
        source = chunk.metadata["source"]
        chunk.id = f"{source}#{counts[source]}"
        counts[source] += 1
        chunk.page_content = f"{chunk.metadata['title']}\n\n{chunk.page_content}"
    return chunks


def get_vector_store() -> Chroma:
    return Chroma(
        collection_name=settings.chroma_collection,
        embedding_function=HuggingFaceEmbeddings(model_name=settings.embedding_model),
        persist_directory=settings.chroma_db_path,
    )


def ingest() -> None:
    build_database()
    with SessionLocal() as session:
        documents = (
            load_articles(session)
            + load_tickets(session)
            + load_manuals(settings.data_dir / "manuals")
        )
    chunks = chunk_documents(documents)

    vector_store = get_vector_store()
    vector_store.reset_collection()
    vector_store.add_documents(chunks, ids=[chunk.id for chunk in chunks])

    counts = Counter(chunk.metadata["source_type"] for chunk in chunks)
    print(f"Stored {len(chunks)} chunks in {settings.chroma_db_path}: {dict(counts)}")


if __name__ == "__main__":
    ingest()
