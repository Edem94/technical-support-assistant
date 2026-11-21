"""Turn results.jsonl into a Markdown report: python -m evals.report [variant ...]"""
import json
import math
import sys
from collections import Counter, defaultdict
from statistics import median

from evals.run_eval import FLOW_DIR, load_state

# Dollars per million tokens. Cache writes cost 1.25x input, cache reads 0.1x input.
PRICES = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.00, 10.00)}


def cost(model: str | None, usage: dict | None) -> float:
    if not model or not usage:
        return 0.0
    price_in, price_out = next(p for name, p in PRICES.items() if model.startswith(name))
    return (usage["input_tokens"] * price_in + usage["cache_creation_input_tokens"] * price_in * 1.25
            + usage["cache_read_input_tokens"] * price_in * 0.1 + usage["output_tokens"] * price_out) / 1e6


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] \
        if path.exists() else []


def mean_ci(values):
    n = len(values)
    if not n:
        return "-"
    mean = sum(values) / n
    half = 1.96 * math.sqrt(max(mean * (1 - mean), 0.0) / n) if all(v in (0, 1) for v in values) \
        else 1.96 * (sum((v - mean) ** 2 for v in values) / max(n - 1, 1)) ** 0.5 / math.sqrt(n)
    return f"{mean:.0%} ± {half:.0%} (n={n})"


def ratio(hits, total):
    return f"{hits / total:.0%} ({hits}/{total})" if total else "-"


def report(variant: str) -> str:
    state = load_state()
    rows = read_jsonl(FLOW_DIR / variant / "results.jsonl")
    errors = read_jsonl(FLOW_DIR / variant / "errors.jsonl")
    ok = [r for r in rows if r["status"] == "ok"]
    cases = {r["prompt_id"] for r in rows}
    reps = max((r["rep"] for r in rows), default=-1) + 1
    out = [f"# Held-out eval: {variant}", "",
           f"{len(cases)} cases, {len(rows)} graded rows ({reps} reps), "
           f"{len(rows) - len(ok)} truncated, {len(errors)} failed attempts in errors.jsonl. "
           f"Model: {', '.join(sorted({r['model'] for r in rows}))}; judge: "
           f"{', '.join(sorted({r.get('judge_model') or '-' for r in rows}))}.", "",
           "## Quality", "", "| Metric | Score (95% interval) |", "|---|---|"]
    for metric in state["metrics"]:
        values = [r["grade"][metric["id"]] for r in ok if r["grade"].get(metric["id"]) is not None]
        out.append(f"| {metric['label']} | {mean_ci(values)} |")

    # Escalation as a classifier: positives are the cases a human should handle.
    expected_esc = [r for r in ok if r["meta"]["expected"] == "escalate"]
    did_esc = [r for r in ok if r["meta"].get("outcome") == "escalate"]
    both = [r for r in did_esc if r["meta"]["expected"] == "escalate"]
    others = [r for r in ok if r["meta"]["expected"] != "escalate"]
    out += ["", "## Escalation", "", "| Measure | Value |", "|---|---|",
            f"| Recall (should escalate, did) | {ratio(len(both), len(expected_esc))} |",
            f"| Precision (escalated, should have) | {ratio(len(both), len(did_esc))} |",
            f"| False escalation rate (should not, did) | {ratio(len(did_esc) - len(both), len(others))} |"]

    labels = ["answered", "escalate", "decline"]
    matrix = Counter((r["meta"]["expected"], r["meta"].get("outcome")) for r in ok)
    out += ["", "## Outcomes (rows: expected, columns: actual)", "",
            "| Expected | " + " | ".join(labels) + " |", "|---|" + "---|" * len(labels)]
    out += [f"| {e} | " + " | ".join(str(matrix[(e, a)]) for a in labels) + " |" for e in labels]

    latencies = sorted(r["latency_s"] for r in rows)
    app_cost = [cost(r["model"], r["usage"]) for r in rows]
    judge_cost = [cost(r.get("judge_model"), r.get("judge_usage")) for r in rows]
    error_cost = sum(cost(e.get("model"), e.get("usage")) for e in errors)
    if rows:
        out += ["", "## Speed and cost", "", "| Measure | Value |", "|---|---|",
                f"| Latency, median / 90th percentile / max | {median(latencies):.1f}s / "
                f"{latencies[int(0.9 * (len(latencies) - 1))]:.1f}s / {latencies[-1]:.1f}s |",
                f"| Output tokens per answer, median | {median(r['usage']['output_tokens'] for r in rows):.0f} |",
                f"| Assistant cost per answer, mean | ${sum(app_cost) / len(rows):.5f} |",
                f"| Assistant cost, whole run | ${sum(app_cost):.4f} |",
                f"| Judge cost, whole run | ${sum(judge_cost):.4f} |",
                f"| Cost of failed attempts | ${error_cost:.4f} |",
                f"| Total | ${sum(app_cost) + sum(judge_cost) + error_cost:.4f} |"]

    by_case = defaultdict(list)
    for r in rows:
        by_case[r["prompt_id"]].append(r)
    out += ["", "## Per case", "", "| Case | Expected | Pass | Outcomes | Key points | Grounded | Traces |",
            "|---|---|---|---|---|---|---|"]
    for case_id in sorted(by_case):
        reps_rows = sorted(by_case[case_id], key=lambda r: r["rep"])
        scored = [r for r in reps_rows if r["status"] == "ok"]
        pass_rate = sum(r["grade"]["pass"] for r in scored) / len(scored) if scored else 0
        out.append(
            f"| {case_id} | {reps_rows[0]['meta']['expected']} | {pass_rate:.0%} | "
            + ", ".join(r["meta"].get("outcome") or r["status"] for r in reps_rows) + " | "
            + ", ".join(f"{r['grade']['key_points']:.2f}" for r in scored) + " | "
            + ", ".join(f"{r['grade']['grounded']:.0f}" for r in scored) + " | "
            + ", ".join(f"[rep{r['rep']}]({variant}/traces/{case_id}_rep{r['rep']}.json)" for r in reps_rows) + " |")

    failed = [r for r in ok if r["grade"]["pass"] == 0]
    if failed:
        out += ["", "## Why cases failed", ""]
        for r in sorted(failed, key=lambda r: (r["prompt_id"], r["rep"])):
            g = r["grade"]
            out += [f"### {r['prompt_id']} rep{r['rep']}: expected {r['meta']['expected']}, "
                    f"got {r['meta'].get('outcome')}", "",
                    f"Outcome ok: {g['outcome_ok']:.0f}. Source ok: {g['source_ok']}. "
                    f"Cited: {', '.join(r['meta'].get('cited') or []) or 'none'}.", "",
                    f"Grounded: {r['explanation']['grounded']}", "", "```text", r["explanation"]["key_points"], "```", ""]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    variants = sys.argv[1:] or ["baseline"]
    for name in variants:
        text = report(name)
        path = FLOW_DIR / ("report.md" if name == "baseline" else f"report_{name}.md")
        path.write_text(text, encoding="utf-8")
        print(f"wrote {path.relative_to(FLOW_DIR.parent.parent.parent)}")
