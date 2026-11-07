"""SQLite database of support data: tables, connection and rebuild from data/.

Rebuild it on its own with `python -m app.database`.
`python -m app.ingest` also rebuilds it before loading Chroma.
"""

import csv
import json
import re
from collections import Counter
from pathlib import Path

from sqlalchemy import Column, ForeignKey, Table, create_engine, event, text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)

from app.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(engine)


@event.listens_for(engine, "connect")
def enable_foreign_keys(connection, _):
    # SQLite ignores foreign keys unless this is set on every connection.
    connection.execute("PRAGMA foreign_keys = ON")


class Base(DeclarativeBase):
    pass


ticket_kb_refs = Table(
    "ticket_kb_refs",
    Base.metadata,
    Column("ticket_id", ForeignKey("tickets.ticket_id"), primary_key=True),
    Column("kb_id", ForeignKey("kb_articles.kb_id"), primary_key=True),
)


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]
    current_version: Mapped[str | None]
    supported_platforms: Mapped[str | None]
    description: Mapped[str | None]


class Article(Base):
    __tablename__ = "kb_articles"

    kb_id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    product: Mapped[str]
    category: Mapped[str]
    applies_to: Mapped[str | None]
    updated: Mapped[str]
    status: Mapped[str]
    superseded_by: Mapped[str | None]
    file_name: Mapped[str]
    body: Mapped[str]


class ErrorCode(Base):
    __tablename__ = "error_codes"

    code: Mapped[str] = mapped_column(primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.product_id"))
    title: Mapped[str]
    severity: Mapped[str]
    cause: Mapped[str | None]
    fix_summary: Mapped[str | None]
    kb_id: Mapped[str | None] = mapped_column(ForeignKey("kb_articles.kb_id"))
    escalate: Mapped[bool]

    product: Mapped[Product] = relationship()


class KnownIssue(Base):
    __tablename__ = "known_issues"

    issue_id: Mapped[str] = mapped_column(primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.product_id"))
    title: Mapped[str]
    affected_versions: Mapped[str | None]
    fixed_in: Mapped[str | None]
    status: Mapped[str]
    workaround: Mapped[str | None]
    kb_id: Mapped[str | None] = mapped_column(ForeignKey("kb_articles.kb_id"))
    reported_on: Mapped[str | None]

    product: Mapped[Product] = relationship()


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[str]
    product_id: Mapped[str] = mapped_column(ForeignKey("products.product_id"))
    version: Mapped[str | None]
    os: Mapped[str | None]
    priority: Mapped[str]
    status: Mapped[str]
    subject: Mapped[str]
    description: Mapped[str]
    resolution: Mapped[str | None]
    csat: Mapped[int | None]

    product: Mapped[Product] = relationship()
    articles: Mapped[list[Article]] = relationship(secondary=ticket_kb_refs)


def read_csv(name: str) -> list[dict]:
    path = settings.data_dir / "structured" / name
    with open(path, encoding="utf-8", newline="") as f:
        # An empty CSV cell means "no value", not an empty string.
        return [{k: v or None for k, v in row.items()} for row in csv.DictReader(f)]


def parse_article(path: Path) -> Article:
    """Read a Markdown article, splitting its front matter from its body."""
    match = re.match(r"---\n(.*?)\n---\n(.*)", path.read_text(encoding="utf-8"), re.DOTALL)
    if match is None:
        raise ValueError(f"{path.name} has no front matter")
    fields = dict(line.split(": ", 1) for line in match.group(1).splitlines())
    return Article(
        kb_id=fields["id"],
        title=fields["title"],
        product=fields["product"],
        category=fields["category"],
        applies_to=fields.get("applies_to"),
        updated=fields["updated"],
        status=fields["status"],
        superseded_by=fields.get("superseded_by"),
        file_name=path.name,
        body=match.group(2).strip(),
    )


def read_tickets(articles: dict[str, Article]) -> list[Ticket]:
    with open(settings.data_dir / "structured" / "tickets.jsonl", encoding="utf-8") as f:
        rows = [json.loads(line) for line in f]
    return [
        Ticket(**row, articles=[articles[kb_id] for kb_id in refs])
        for row in rows
        for refs in [row.pop("kb_refs")]
    ]


def build_database() -> None:
    """Recreate every table from the files in data/."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    knowledge_base = sorted((settings.data_dir / "knowledge_base").glob("*.md"))
    articles = {article.kb_id: article for article in map(parse_article, knowledge_base)}
    error_codes = [
        ErrorCode(**{**row, "escalate": row["escalate"] == "true"})
        for row in read_csv("error_codes.csv")
    ]

    with SessionLocal.begin() as session:
        session.add_all(Product(**row) for row in read_csv("products.csv"))
        session.add_all(articles.values())
        session.flush()  # The tables below reference these rows, so write them first.
        session.add_all(error_codes)
        session.add_all(KnownIssue(**row) for row in read_csv("known_issues.csv"))
        session.add_all(read_tickets(articles))

    build_search_index()


def build_search_index() -> None:
    """Index error codes and known issues for plain-language search (SQLite FTS5).

    The porter tokenizer reduces words to their stem, so "dropping" matches "drops".
    """
    statements = [
        "DROP TABLE IF EXISTS structured_search",
        """CREATE VIRTUAL TABLE structured_search
           USING fts5(record_id UNINDEXED, content, tokenize='porter')""",
        """INSERT INTO structured_search
           SELECT code, title || ' ' || COALESCE(cause, '') FROM error_codes""",
        "INSERT INTO structured_search SELECT issue_id, title FROM known_issues",
    ]
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def get_structured_record(session: Session, record_id: str) -> ErrorCode | KnownIssue | None:
    return session.get(ErrorCode, record_id) or session.get(KnownIssue, record_id)


def search_structured_records(session: Session, terms: list[str]) -> list[ErrorCode | KnownIssue]:
    """Return the records sharing the most terms, ignoring those below the minimum."""
    matches = Counter()
    for term in set(terms):
        record_ids = session.scalars(
            text("SELECT record_id FROM structured_search WHERE content MATCH :term"),
            {"term": f'"{term}"'},  # Quoted, so FTS5 reads it as text, not as a query operator.
        )
        matches.update(record_ids)

    return [
        get_structured_record(session, record_id)
        for record_id, count in matches.most_common(settings.structured_search_limit)
        if count >= settings.structured_min_matches
    ]


if __name__ == "__main__":
    build_database()
    print(f"Built {settings.database_url}")
