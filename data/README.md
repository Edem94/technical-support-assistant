# Sample support data: Veloria Systems

**Veloria Systems is a fictional company.** All products, tickets, error codes and web addresses here are made up for this portfolio project. Replace this folder when you choose a real data source.

Veloria sells four products to individuals and business customers:

| Product | Type | Current version |
|---------|------|-----------------|
| VeloSync | File sync and backup client | 4.1.3 |
| VeloGuard VPN | Remote access VPN | 6.2.1 |
| VeloBook 14 | Business laptop | BIOS 1.18 |
| Veloria ID | Single sign-on and MFA | n/a |

## Contents

| Path | Format | Contents | Use it for |
|------|--------|----------|------------|
| `knowledge_base/` | Markdown with front matter | 15 support articles | Vector search (RAG) |
| `manuals/` | PDF | VeloBook 14 User Guide | Vector search; tests PDF parsing |
| `structured/products.csv` | CSV | Product catalog | SQL lookup |
| `structured/error_codes.csv` | CSV | 18 error codes | Exact lookup (embeddings handle codes poorly) |
| `structured/known_issues.csv` | CSV | 5 known issues, including one open | SQL lookup |
| `structured/tickets.jsonl` | JSON Lines | 15 past tickets | Vector search on resolved tickets |
| `eval/golden_questions.jsonl` | JSON Lines | 16 test questions | Measuring retrieval and answer quality |

## Load the data

```bash
python -m app.ingest
```

This rebuilds `data/support.db` (SQLite) and `chroma_db/` (vector store) from these files. Both are generated, so neither is committed.

Articles, the PDF and resolved tickets go into Chroma. Error codes and known issues stay in SQLite for exact lookups. KB-2003 (deprecated) and open tickets are not added to Chroma.

## Traps built in on purpose

- **KB-2003 is deprecated.** It describes L2TP, which VeloGuard 6 no longer supports. Filter it out of retrieval, or the assistant will give outdated advice.
- **Some topics must escalate.** Ransomware, swollen batteries and suspected account compromise need a human (see KB-5001).
- **T-48933 is unresolved.** Do not treat an open ticket as a solution.
- **KI-140 has no KB article.** The answer is only in `known_issues.csv`.
- **The LED codes exist only in the PDF.** Question Q05 fails if PDF ingestion breaks.
- **Some questions should be declined.** Q14 to Q16 are out of scope, unanswerable or a prompt injection attempt.
