"""Run a questionnaire file through the agent: reviewer spreadsheet, audit log, and pass-or-fail report.

python run_questionnaire.py --questions testsets/standard_questionnaire.csv --company "Lumera Pay, Inc." \
    --agent-ids agent_ids.json --answer-key testsets/answer_key.csv --documents corpus/lumera-pay \
    --runs 3 --concurrency 4 --check gold --out out/gold/standard
Re-running the same command resumes: finished work in out/<name>/audit.jsonl is skipped.
Exit code 1 if the check fails.
"""
import argparse, glob, hashlib, json, pathlib, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from seekrai import SeekrFlow
import dd_core, verify

def read_questions(p):
    df = pd.read_excel(p) if str(p).endswith((".xlsx", ".xls")) else pd.read_csv(p)
    df.columns = [c.strip().lower() for c in df.columns]
    return df[["qnum", "question"]].dropna()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", required=True); ap.add_argument("--company", required=True)
    ap.add_argument("--agent-ids", default="agent_ids.json"); ap.add_argument("--agent-id")
    ap.add_argument("--answer-key"); ap.add_argument("--documents", default="corpus/lumera-pay", help="folder holding the company's documents")
    ap.add_argument("--runs", type=int, default=1); ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--concurrency", type=int, default=4); ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=240); ap.add_argument("--check", choices=["silver", "gold"], default="gold")
    ap.add_argument("--out", default="out/run")
    ap.add_argument("--signatures", help="semicolon-separated values that belong only to OTHER companies in the Org, or none. Default: the Lumera Health demo values. Always set this for a real company.")
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    agent_id = a.agent_id or json.loads(pathlib.Path(a.agent_ids).read_text())["agent_id"]
    qs = read_questions(a.questions)
    items = list(zip(qs.qnum.astype(int), qs.question))
    batches = [items[i:i + a.batch_size] for i in range(0, len(items), a.batch_size)]
    audit_path, lock = out / "audit.jsonl", threading.Lock()
    done = set()
    if audit_path.exists():
        for line in audit_path.read_text().splitlines():
            r = json.loads(line)
            if r.get("ok"): done.add((r["run"], r["batch"]))
    client = SeekrFlow()

    def work(run, b):
        prompt = dd_core.build_prompt(a.company, batches[b])
        for attempt in range(a.retries + 1):
            try:
                res = dd_core.ask_agent(client, agent_id, prompt, timeout_s=a.timeout)
                return {"run": run, "batch": b, "ok": True, "attempt": attempt, "prompt": prompt,
                        "qnums": [q for q, _ in batches[b]], "sha256": hashlib.sha256(res["text"].encode()).hexdigest(),
                        "chunk_ids": dd_core.chunk_ids(res["text"]), "needs_human": dd_core.needs_human(res["text"]),
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **res}
            except Exception as e:
                err = repr(e); time.sleep(2 ** attempt)
        return {"run": run, "batch": b, "ok": False, "error": err, "qnums": [q for q, _ in batches[b]]}

    todo = [(r, b) for r in range(a.runs) for b in range(len(batches)) if (r, b) not in done]
    print(f"{len(todo)} agent runs to do, {len(done)} already in the audit log")
    with ThreadPoolExecutor(max_workers=a.concurrency) as pool:
        for fut in as_completed([pool.submit(work, r, b) for r, b in todo]):
            rec = fut.result()
            with lock, audit_path.open("a") as f:
                f.write(json.dumps(rec) + "\n")
            print(("ok  " if rec["ok"] else "ERR ") + f"run {rec['run']} batch {rec['batch']}")

    recs = [json.loads(l) for l in audit_path.read_text().splitlines()]
    latest = {}
    for r in recs:
        if r["ok"] or (r["run"], r["batch"]) not in latest: latest[(r["run"], r["batch"])] = r
    runs = []
    for run in range(a.runs):
        rows = []
        for b in range(len(batches)):
            r = latest.get((run, b))
            if r and r["ok"]:
                for row in dd_core.parse_table(r["text"]):
                    row.update(run_id=r["run_id"], latency_s=r["latency_s"], chunk_ids=",".join(r["chunk_ids"]))
                    rows.append(row)
        runs.append(pd.DataFrame(rows, columns=["qnum", "question", "answer", "status", "evidence", "source",
                                                "run_id", "latency_s", "chunk_ids"]))
    last = runs[-1].merge(qs.rename(columns={"question": "question_asked"}), on="qnum", how="right")
    lat = pd.Series([r["latency_s"] for r in recs if r.get("ok")])
    context = {"company": a.company, "agent_id": agent_id, "questions": len(qs), "runs": a.runs,
               "agent_calls_ok": int(sum(1 for r in latest.values() if r["ok"])),
               "latency_p50_s": round(lat.quantile(.5), 1) if len(lat) else None,
               "latency_p95_s": round(lat.quantile(.95), 1) if len(lat) else None}
    check_ok = True
    with pd.ExcelWriter(out / "responses.xlsx") as xw:
        last[["qnum", "question_asked", "answer", "status", "evidence", "source"]].to_excel(xw, sheet_name="Draft responses", index=False)
        last[last.status.isin(["Not covered", "", None]) | last.status.isna()][["qnum", "question_asked"]].to_excel(xw, sheet_name="Gaps", index=False)
        if a.answer_key:
            key = pd.read_csv(a.answer_key).fillna("")
            documents = verify.load_documents(sorted(pathlib.Path(a.documents).glob("*.md")))
            sigs = ([] if a.signatures.strip().lower() == "none" else [x.strip() for x in a.signatures.split(";") if x.strip()]) if a.signatures else verify.DEFAULT_SIGNATURES
            scored = [verify.score(df, key, documents, sigs) for df in runs]
            m = verify.metrics(scored[-1]); m["consistency"] = verify.consistency(scored)
            answered = scored[-1][scored[-1].expected_status != "Not covered"]
            m["audit_complete"] = round((answered.run_id != "").mean(), 3) if len(answered) else 1.0
            table = verify.evaluate_check(a.check, m); check_ok = bool(table["pass"].all())
            pd.DataFrame([{**context, **m}]).to_excel(xw, sheet_name="Measures", index=False)
            table.to_excel(xw, sheet_name="Pass bar", index=False)
            scored[-1].to_excel(xw, sheet_name="Scored rows", index=False)
            (out / "check_report.md").write_text(verify.check_markdown(a.check, table, {**context, **m}))
            print(verify.check_markdown(a.check, table, {**context, **m}))
    print("wrote", out / "responses.xlsx")
    print("Draft responses for human review. Not a compliance determination.")
    sys.exit(0 if check_ok else 1)

if __name__ == "__main__":
    main()
