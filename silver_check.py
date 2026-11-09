"""Silver check: run the standard questionnaire through the SDK agent three times and score every row.

python silver_check.py                          # documents only agent (agent_ids.json)
python silver_check.py agent_ids_facts.json     # agent with the compliance record tool
Writes out/silver/<name>.xlsx and prints "Silver check: PASS" or "Silver check: FAIL".
"""
import json, pathlib, sys
import pandas as pd
from seekrai import SeekrFlow
import dd_core, verify

COMPANY = "Lumera Pay, Inc."
RUNS = 3

def main(agent_ids_file="agent_ids.json"):
    client = SeekrFlow()                                  # reads SEEKR_API_KEY from the environment
    ids = json.loads(pathlib.Path(agent_ids_file).read_text())
    questions = pd.read_csv("testsets/standard_questionnaire.csv")
    key = pd.read_csv("testsets/answer_key.csv").fillna("")
    documents = verify.load_documents(sorted(pathlib.Path("corpus/lumera-pay").glob("*.md")))

    def run_once():
        # One question per run, so each row has its own run ID and source-trace chunks.
        rows = []
        for q, text in zip(questions.qnum, questions.question):
            res = dd_core.ask_agent(client, ids["agent_id"], dd_core.build_prompt(COMPANY, [(int(q), text)]))
            for r in dd_core.parse_table(res["text"]):
                r.update(run_id=res["run_id"], latency_s=res["latency_s"], chunk_ids=",".join(dd_core.chunk_ids(res["text"])))
                rows.append(r)
        return pd.DataFrame(rows, columns=["qnum", "question", "answer", "status", "evidence", "source",
                                           "run_id", "latency_s", "chunk_ids"])

    scored = [verify.score(run_once(), key, documents) for _ in range(RUNS)]
    m = verify.metrics(scored[-1]); m["consistency"] = verify.consistency(scored)
    table = verify.evaluate_check("silver", m)
    print(json.dumps(m, indent=2)); print(table.to_string(index=False))
    print("Silver check:", "PASS" if table["pass"].all() else "FAIL")

    out = pathlib.Path("out/silver"); out.mkdir(parents=True, exist_ok=True)
    name = pathlib.Path(agent_ids_file).stem.replace("agent_ids", "results").strip("_") or "results"
    with pd.ExcelWriter(out / f"{name}.xlsx") as xw:
        scored[-1][["qnum", "question", "answer", "status", "evidence", "source", "run_id"]].to_excel(xw, sheet_name="Draft responses", index=False)
        scored[-1][scored[-1].status == "Not covered"][["qnum", "question"]].to_excel(xw, sheet_name="Gaps", index=False)
        pd.DataFrame([m]).to_excel(xw, sheet_name="Measures", index=False)
        table.to_excel(xw, sheet_name="Pass bar", index=False)
        scored[-1].to_excel(xw, sheet_name="Scored rows", index=False)
    print(f"Wrote {out / (name + '.xlsx')}. Draft responses for human review. Not a compliance determination.")
    return bool(table["pass"].all())

if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else "agent_ids.json") else 1)
