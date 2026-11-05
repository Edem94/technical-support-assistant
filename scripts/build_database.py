"""Build data/support.db (SQLite) from the files in data/.

Run from the repository root:

    python scripts/build_database.py

The database is a generated file, so it is safe to delete and rebuild.
"""

import csv
import json
import re
import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "support.db"

SCHEMA = """
CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    current_version TEXT,
    supported_platforms TEXT,
    description TEXT
);

CREATE TABLE kb_articles (
    kb_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    product TEXT NOT NULL,
    category TEXT NOT NULL,
    applies_to TEXT,
    updated TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('published', 'deprecated')),
    superseded_by TEXT,
    file_name TEXT NOT NULL,
    body TEXT NOT NULL
);

CREATE TABLE error_codes (
    code TEXT PRIMARY KEY,
    product_id TEXT NOT NULL REFERENCES products (product_id),
    title TEXT NOT NULL,
    severity TEXT NOT NULL,
    cause TEXT,
    fix_summary TEXT,
    kb_id TEXT REFERENCES kb_articles (kb_id),
    escalate INTEGER NOT NULL
);

CREATE TABLE known_issues (
    issue_id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL REFERENCES products (product_id),
    title TEXT NOT NULL,
    affected_versions TEXT,
    fixed_in TEXT,
    status TEXT NOT NULL,
    workaround TEXT,
    kb_id TEXT REFERENCES kb_articles (kb_id),
    reported_on TEXT
);

CREATE TABLE tickets (
    ticket_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    product_id TEXT NOT NULL REFERENCES products (product_id),
    version TEXT,
    os TEXT,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    resolution TEXT,
    csat INTEGER
);

CREATE TABLE ticket_kb_refs (
    ticket_id TEXT NOT NULL REFERENCES tickets (ticket_id),
    kb_id TEXT NOT NULL REFERENCES kb_articles (kb_id),
    PRIMARY KEY (ticket_id, kb_id)
);
"""


def read_csv(name):
    with open(DATA_DIR / "structured" / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def empty_to_none(row):
    return {key: (value if value != "" else None) for key, value in row.items()}


def parse_article(path):
    """Split a Markdown article into its front-matter fields and body."""
    match = re.match(r"---\n(.*?)\n---\n(.*)", path.read_text(encoding="utf-8"), re.DOTALL)
    if match is None:
        raise ValueError(f"{path.name} has no front matter")
    fields = dict(line.split(": ", 1) for line in match.group(1).splitlines())
    return {
        "kb_id": fields["id"],
        "title": fields["title"],
        "product": fields["product"],
        "category": fields["category"],
        "applies_to": fields.get("applies_to"),
        "updated": fields["updated"],
        "status": fields["status"],
        "superseded_by": fields.get("superseded_by"),
        "file_name": path.name,
        "body": match.group(2).strip(),
    }


def insert(connection, table, rows):
    columns = list(rows[0])
    names = ", ".join(columns)
    placeholders = ", ".join(f":{column}" for column in columns)
    connection.executemany(f"INSERT INTO {table} ({names}) VALUES ({placeholders})", rows)


def main():
    DB_PATH.unlink(missing_ok=True)
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA)

        articles = [parse_article(p) for p in sorted((DATA_DIR / "knowledge_base").glob("*.md"))]
        error_codes = [
            {**row, "escalate": int(row["escalate"] == "true")}
            for row in read_csv("error_codes.csv")
        ]
        known_issues = [empty_to_none(row) for row in read_csv("known_issues.csv")]

        tickets, ticket_refs = [], []
        with open(DATA_DIR / "structured" / "tickets.jsonl", encoding="utf-8") as f:
            for line in f:
                ticket = json.loads(line)
                refs = ticket.pop("kb_refs")
                tickets.append(ticket)
                ticket_refs += [{"ticket_id": ticket["ticket_id"], "kb_id": ref} for ref in refs]

        # Insert parents first so the foreign key checks pass.
        insert(connection, "products", read_csv("products.csv"))
        insert(connection, "kb_articles", articles)
        insert(connection, "error_codes", error_codes)
        insert(connection, "known_issues", known_issues)
        insert(connection, "tickets", tickets)
        insert(connection, "ticket_kb_refs", ticket_refs)
        connection.commit()

        for table in ("products", "kb_articles", "error_codes", "known_issues", "tickets"):
            count = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table}: {count}")
    finally:
        connection.close()
    print(f"Created {DB_PATH}")


if __name__ == "__main__":
    main()
