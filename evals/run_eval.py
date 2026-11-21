"""Run the held-out questions through the real RAG chain and grade every answer.

Usage (from the repo root):
    python -m evals.run_eval --approve-harness          # you run this once, after reviewing the harness
    python -m evals.run_eval --ids H01,S01 --reps 1     # pilot
    python -m evals.run_eval                            # full run: every case, 2 reps
    python -m evals.run_eval --check                    # grader sanity checks (oracle, null, judge negatives)

Output goes to .claude/hillclimb/heldout/<variant>/: results.jsonl (one row per case and rep, written as each
finishes), traces/<id>_rep<k>.json, and errors.jsonl for attempts that never produced a gradable answer.
"""
import argparse
import hashlib
import json
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import anthropic

from app import rag_chain
from app.config import settings
from app.schema import Source, SupportResponse
from evals.judge import JUDGE_MODEL, judge

ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = ROOT / "data/eval/heldout_questions.jsonl"
FLOW_DIR = ROOT / ".claude/hillclimb/heldout"
STATE_PATH = FLOW_DIR / "_state.json"
HARNESS_FILES = ["evals/run_eval.py", "evals/judge.py", "data/eval/heldout_questions.jsonl"]
MAX_ATTEMPTS = 5


class CaseError(Exception):
    """An attempt that produced nothing gradable. Goes to errors.jsonl, never to results.jsonl."""

    def __init__(self, failure_class: str, message: str, retries: int = 0, model=None, usage=None):
        super().__init__(message)
        self.failure_class, self.retries, self.model, self.usage = failure_class, retries, model, usage


# ---------------------------------------------------------------- harness gate

def load_state() -> dict:
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def harness_sha(state: dict) -> str:
    digest = hashlib.sha256()
    for rel in sorted(set(HARNESS_FILES + state.get("harness_paths", []))):
        digest.update(rel.encode())
        digest.update((ROOT / rel).read_bytes().replace(b"\r\n", b"\n"))
    return digest.hexdigest()


def check_harness(approve: bool) -> None:
    state = load_state()
    current = harness_sha(state)
    if approve:
        state["harness_sha"] = current
        STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        print(f"Harness approved: {current[:12]}")
        sys.exit(0)
    if state.get("harness_sha") != current:
        print("The eval harness changed since it was last approved (or was never approved).\n"
              "Review evals/run_eval.py, evals/judge.py and the questions, then run:\n"
              "    python -m evals.run_eval --approve-harness", file=sys.stderr)
        sys.exit(2)


# ---------------------------------------------------------------- API calls

def usage_dict(usage) -> dict:
    return {
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "cache_read_input_tokens": usage.cache_read_input_tokens or 0,
        "cache_creation_input_tokens": usage.cache_creation_input_tokens or 0,
    }


def call_with_backoff(fn, retries: list, **request):
    """Retry rate limits, overloads, 5xx and connection errors with jittered exponential backoff."""
    for attempt in range(MAX_ATTEMPTS):
        try:
            return fn(**request)
        except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError) as error:
            if attempt == MAX_ATTEMPTS - 1:
                raise CaseError("harness", f"API error after {attempt + 1} attempts: {error!r}", retries[0]) from error
            retries[0] += 1
            time.sleep(min(30.0, 2 ** attempt) * random.uniform(0.5, 1.5))
        except anthropic.APIStatusError as error:  # 400s etc.: retrying will not help
            raise CaseError("harness", f"API error: {error!r}", retries[0]) from error


def check_model(response, requested: str) -> None:
    served = response.model
    if served != requested and not served.startswith(requested + "-"):
        raise CaseError("serving", f"Asked for {requested}, served {served}", model=served,
                        usage=usage_dict(response.usage))


class RecordingClient:
    """Wraps the real client so the runner sees exactly what the app sent and got back."""

    def __init__(self, real, requested_model: str):
        self.real, self.requested_model = real, requested_model
        self.request = self.response = None
        self.retries = [0]
        self.messages = SimpleNamespace(parse=self.parse)

    def parse(self, **request):
        self.request = request
        self.response = call_with_backoff(self.real.messages.parse, self.retries, **request)
        check_model(self.response, self.requested_model)
        return self.response


# Retrieval runs once per case; record what the model was shown. A lock keeps the shared index single-threaded.
_retrieval_lock = threading.Lock()
_seen = threading.local()
_real_retrieve = rag_chain.retrieve


def recording_retrieve(query, *args, **kwargs):
    with _retrieval_lock:
        documents = _real_retrieve(query, *args, **kwargs)
    _seen.documents = documents
    return documents


rag_chain.retrieve = recording_retrieve


# ---------------------------------------------------------------- grading

def reply_text(response: SupportResponse) -> str:
    lines = [f"Outcome: {response.outcome}"]
    if response.escalate:
        lines.append(f"Escalation reason: {response.escalation_reason}")
    lines += ["", response.answer, "", "Cited sources: " + (", ".join(s.id for s in response.sources) or "none")]
    return "\n".join(lines)


def code_grade(case: dict, response: SupportResponse) -> dict:
    cited = {s.id for s in response.sources}
    expected = case["expected_sources"]
    return {
        "outcome_ok": float(response.outcome == case["expected_behavior"]),
        # Only defined when the case names sources; None is left out of the mean.
        "source_ok": float(bool(cited & set(expected))) if expected else None,
    }


def full_grade(case: dict, response: SupportResponse, sources_text: str, judge_client):
    """Code checks plus the judge. Returns (grade, explanation, judge_response)."""
    grade = code_grade(case, response)
    verdict, judge_response = judge(judge_client, rag_chain.SYSTEM_PROMPT, case["question"], sources_text,
                                    reply_text(response), case["key_points"])
    met = [kp.met for kp in verdict.key_points]
    grade["grounded"] = float(verdict.grounded)
    grade["key_points"] = sum(met) / len(met)
    grade["pass"] = float(grade["outcome_ok"] == 1.0 and grade["source_ok"] != 0.0
                          and verdict.grounded and all(met))
    grade = {k: grade[k] for k in ("pass", "outcome_ok", "source_ok", "grounded", "key_points")}
    explanation = {
        "grounded": "Unsupported: " + "; ".join(verdict.unsupported_claims) if verdict.unsupported_claims
        else "Every specific claim is supported by the sources.",
        "key_points": "\n".join(f"[{'met' if kp.met else 'MISSED'}] {kp.point}: {kp.reasoning}"
                                for kp in verdict.key_points),
    }
    return grade, explanation, judge_response


# ---------------------------------------------------------------- one case

def run_case(case: dict, rep: int, variant_dir: Path, real_client, model: str) -> dict:
    client = RecordingClient(real_client, model)
    start = time.perf_counter()
    try:
        response = rag_chain.answer_question(case["question"], client=client)
    except CaseError as error:
        error.retries = client.retries[0]
        raise
    except Exception as error:
        raw = client.response
        if raw is not None and raw.stop_reason == "max_tokens":
            response = None  # truncated: written as a row, left out of the means
        else:
            raise CaseError("harness", repr(error), client.retries[0],
                            raw.model if raw else None, usage_dict(raw.usage) if raw else None) from error
    latency = time.perf_counter() - start
    raw = client.response
    documents = getattr(_seen, "documents", [])
    sources_text = rag_chain.format_sources(documents)

    row = {
        "prompt_id": case["id"], "rep": rep, "prompt": case["question"], "tags": case["tags"],
        "status": "ok" if response else "truncated", "stop_reason": raw.stop_reason,
        "model": raw.model, "usage": usage_dict(raw.usage), "latency_s": round(latency, 2),
        "meta": {
            "expected": case["expected_behavior"], "expected_sources": case["expected_sources"],
            "retrieved": [d.metadata.get("source") for d in documents], "retries": client.retries[0],
            "failure_class": "refusal" if raw.stop_reason == "refusal" else None,
        },
    }
    trace = [
        {"role": "system", "content": rag_chain.SYSTEM_PROMPT},
        {"role": "user", "content": client.request["messages"][0]["content"]},
    ]
    if response is None:
        row["grade"] = {k: None for k in ("pass", "outcome_ok", "source_ok", "grounded", "key_points")}
        trace.append({"role": "assistant", "content": "(truncated at max_tokens)"})
    else:
        judge_retries = [0]
        judge_client = SimpleNamespace(messages=SimpleNamespace(
            parse=lambda **r: call_with_backoff(real_client.messages.parse, judge_retries, **r)))
        try:
            grade, explanation, judge_response = full_grade(case, response, sources_text, judge_client)
        except CaseError as error:
            error.failure_class, error.model, error.usage = "grader", raw.model, usage_dict(raw.usage)
            raise
        except Exception as error:
            raise CaseError("grader", repr(error), client.retries[0], raw.model, usage_dict(raw.usage)) from error
        check_model(judge_response, JUDGE_MODEL)
        row.update(grade=grade, explanation=explanation, judge_model=judge_response.model,
                   judge_usage=usage_dict(judge_response.usage))
        row["meta"].update(outcome=response.outcome, escalated=response.escalate,
                           cited=[s.id for s in response.sources], judge_retries=judge_retries[0])
        trace.append({"role": "assistant", "content": reply_text(response)})

    traces = variant_dir / "traces"
    traces.mkdir(parents=True, exist_ok=True)
    (traces / f"{case['id']}_rep{rep}.json").write_text(json.dumps(trace, indent=2), encoding="utf-8")
    return row


def run_with_ceiling(timeout_s: float, fn, *args):
    """Hard wall-clock ceiling per case. The abandoned call may keep running, but its slot is freed."""
    box = {}

    def target():
        try:
            box["row"] = fn(*args)
        except BaseException as error:  # handed back to the caller
            box["error"] = error

    worker = threading.Thread(target=target, daemon=True)
    worker.start()
    worker.join(timeout_s)
    if worker.is_alive():
        raise CaseError("timeout", f"Case took longer than {timeout_s:.0f}s")
    if "error" in box:
        raise box["error"]
    return box["row"]


# ---------------------------------------------------------------- grader checks

def run_checks(cases: list[dict], real_client) -> None:
    """Oracle and null through the code checks; three bad replies through the judge. All must behave."""
    def fake(outcome, answer, cited):
        return SupportResponse(outcome=outcome, answer=answer, escalate=outcome == "escalate",
                               escalation_reason="test" if outcome == "escalate" else "",
                               sources=[Source(id=s, title=s, type="kb") for s in cited])

    oracle = [code_grade(c, fake(c["expected_behavior"], "x", c["expected_sources"][:1])) for c in cases]
    null = [code_grade(c, fake("answered", "", [])) for c in cases]
    for name, grades in (("oracle", oracle), ("null (always 'answered', no sources)", null)):
        outcome = sum(g["outcome_ok"] for g in grades) / len(grades)
        scored = [g["source_ok"] for g in grades if g["source_ok"] is not None]
        print(f"{name:38} outcome_ok {outcome:.0%}   source_ok {sum(scored) / len(scored):.0%}")

    judge_client = SimpleNamespace(messages=SimpleNamespace(
        parse=lambda **r: call_with_backoff(real_client.messages.parse, [0], **r)))
    by_id = {c["id"]: c for c in cases}
    wrong = ("To reset your Veloria ID password, open id.veloria.com, choose Forgot password, and follow the "
             "link we email you within 5 minutes.")
    print("\nJudge negatives (every one must fail):")
    for case_id in ("S01", "S21", "H01"):
        case = by_id[case_id]
        for label, answer in (("empty", ""), ("I don't know", "I don't know."), ("wrong question", wrong)):
            response = fake(case["expected_behavior"], answer, case["expected_sources"][:1])
            documents = rag_chain.retrieve(case["question"])
            grade, _, _ = full_grade(case, response, rag_chain.format_sources(documents), judge_client)
            verdict = "FAIL (good)" if grade["pass"] == 0 else "PASS (judge is too lenient)"
            print(f"  {case_id} {label:15} key_points {grade['key_points']:.2f} "
                  f"grounded {grade['grounded']:.0f} -> {verdict}")


# ---------------------------------------------------------------- main

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--variant", default="baseline", help="baseline or v1, v2, ...")
    parser.add_argument("--model", default=settings.llm_model, help="model the app calls")
    parser.add_argument("--reps", type=int, default=2)
    parser.add_argument("--timeout-s", type=float, default=180)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--ids", help="comma-separated case IDs (for a pilot)")
    parser.add_argument("--check", action="store_true", help="run grader sanity checks instead of the eval")
    parser.add_argument("--approve-harness", action="store_true", help="record the reviewed harness (user only)")
    args = parser.parse_args()

    check_harness(args.approve_harness)
    if args.variant != "baseline" and not (args.variant[:1] == "v" and args.variant[1:].isdigit()):
        parser.error("--variant must be 'baseline' or v<N>")

    cases = [json.loads(line) for line in CASES_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    if args.ids:
        wanted = args.ids.split(",")
        cases = [c for c in cases if c["id"] in wanted]
    settings.llm_model = args.model
    real_client = rag_chain.get_client().with_options(max_retries=0)  # the runner does its own visible retries

    from app.retrieval import get_retriever
    get_retriever()  # load the embedding model before any timing starts

    if args.check:
        run_checks(cases, real_client)
        return

    variant_dir = FLOW_DIR / args.variant
    variant_dir.mkdir(parents=True, exist_ok=True)
    results_path, errors_path = variant_dir / "results.jsonl", variant_dir / "errors.jsonl"
    done = set()
    if results_path.exists():
        for line in results_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                done.add((row["prompt_id"], row["rep"]))
    todo = [(c, rep) for c in cases for rep in range(args.reps) if (c["id"], rep) not in done]
    print(f"{len(todo)} to run ({len(done)} already done) on {args.model}, judge {JUDGE_MODEL}")

    write_lock = threading.Lock()
    counts = {"ok": 0, "error": 0}
    started = time.perf_counter()

    def work(item):
        case, rep = item
        try:
            row = run_with_ceiling(args.timeout_s, run_case, case, rep, variant_dir, real_client, args.model)
        except CaseError as error:
            record = {"prompt_id": case["id"], "rep": rep, "failure_class": error.failure_class,
                      "error": str(error), "retries": error.retries, "model": error.model, "usage": error.usage}
            with write_lock:
                with errors_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(record) + "\n")
                counts["error"] += 1
                print(f"  ERROR {case['id']} rep{rep}: {error.failure_class}: {error}")
            return
        with write_lock:
            with results_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")
            counts["ok"] += 1
            g = row["grade"]
            print(f"  {case['id']} rep{rep} {row['meta']['expected']:8} -> {row['meta'].get('outcome', '-'):8} "
                  f"pass={g['pass']} key_points={g['key_points']} {row['latency_s']}s")

    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        list(pool.map(work, todo))
    print(f"\n{counts['ok']} graded, {counts['error']} errors, {time.perf_counter() - started:.0f}s wall clock")
    print("Summary: python -m evals.report")


if __name__ == "__main__":
    main()
