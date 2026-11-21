import pytest

from app.config import settings
from app.database import SessionLocal, build_database
from app.ingest import (
    chunk_documents,
    extract_pages_from_pdf,
    load_articles,
    load_manuals,
    load_tickets,
)

MANUALS_DIR = settings.data_dir / "manuals"


@pytest.fixture(scope="module")
def session():
    build_database()
    with SessionLocal() as session:
        yield session


def sources(documents):
    return {document.metadata["source"] for document in documents}


def test_deprecated_articles_are_left_out(session):
    articles = sources(load_articles(session))
    assert len(articles) == 14
    assert "KB-2003" not in articles


def test_articles_are_split_by_section(session):
    sections = [
        document.metadata.get("section")
        for document in load_articles(session)
        if document.metadata["source"] == "KB-1002"
    ]
    assert "VS-1042: Path too long" in sections


def test_open_tickets_are_left_out(session):
    tickets = sources(load_tickets(session))
    assert len(tickets) == 14
    assert "T-48933" not in tickets


def test_ticket_keeps_its_product_name_and_articles(session):
    ticket = next(d for d in load_tickets(session) if d.metadata["source"] == "T-48501")
    assert ticket.metadata["product"] == "VeloSync"
    assert ticket.metadata["kb_refs"] == "KB-1003,KB-5001"


def test_pdf_table_rows_stay_on_one_line():
    pages = extract_pages_from_pdf(MANUALS_DIR / "velobook-14-user-guide.pdf")
    row = next(line for line in pages[0].splitlines() if "VB-E07" in line)
    assert "SSD not detected" in row


def test_manual_pages_have_page_numbers():
    manual = load_manuals(MANUALS_DIR)[0]
    assert manual.metadata["source"] == "velobook-14-user-guide.pdf"
    assert manual.metadata["page"] == 1


def test_chunks_have_unique_ids_titles_and_a_size_limit(session):
    documents = load_articles(session) + load_tickets(session) + load_manuals(MANUALS_DIR)
    chunks = chunk_documents(documents)

    assert len({chunk.id for chunk in chunks}) == len(chunks)
    for chunk in chunks:
        title = chunk.metadata["title"]
        assert chunk.page_content.startswith(title)
        assert len(chunk.page_content) <= settings.chunk_size + len(title) + 2
