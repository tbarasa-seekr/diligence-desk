# %% [markdown]
# # Diligence Desk silver, v1.3: the SDK agent, scored against the verification standard
# Run `setup_sdk_agent.py` first; it writes `ids.json`. This notebook runs the golden questionnaire through the SDK
# agent three times, scores every row, and checks gate G2. Shapes verified against docs.seekr.com on Oct 25, 2026.

# %%
import json, pathlib
import pandas as pd
from seekrai import SeekrFlow
import dd_core, verify

client = SeekrFlow()                      # reads SEEKR_API_KEY from the environment
COMPANY = "Lumera Pay, Inc."
IDS = json.loads(pathlib.Path("ids.json").read_text())   # use ids_facts.json for the custom-tool variant
RUNS = 3
questions = pd.read_csv("testsets/questionnaire_golden.csv")
key = pd.read_csv("testsets/answer_key.csv").fillna("")
corpus = verify.load_corpus(sorted(pathlib.Path("corpus").glob("D[1-4]_*.md")))
print(IDS)

# %%
# One question per run, so each row maps to one run ID and its source-trace chunks.
def run_once():
    rows = []
    for q, text in zip(questions.qnum, questions.question):
        res = dd_core.ask_agent(client, IDS["agent_id"], dd_core.build_prompt(COMPANY, [(int(q), text)]))
        for r in dd_core.parse_table(res["text"]):
            r.update(run_id=res["run_id"], latency_s=res["latency_s"], chunk_ids=",".join(dd_core.chunk_ids(res["text"])))
            rows.append(r)
    return pd.DataFrame(rows)

runs = [run_once() for _ in range(RUNS)]
scored = [verify.score(df, key, corpus) for df in runs]

# %%
m = verify.metrics(scored[-1]); m["consistency"] = verify.consistency(scored)
gate = verify.evaluate_gate("G2", m)
print(json.dumps(m, indent=2)); print(gate.to_string(index=False))
print("G2:", "PASS" if gate["pass"].all() else "FAIL")

# %%
with pd.ExcelWriter("silver_v1_3_results.xlsx") as xw:
    scored[-1][["qnum", "question", "answer", "status", "evidence", "source", "run_id"]].to_excel(xw, sheet_name="Draft responses", index=False)
    scored[-1][scored[-1].status == "Not covered"][["qnum", "question"]].to_excel(xw, sheet_name="Gaps", index=False)
    pd.DataFrame([m]).to_excel(xw, sheet_name="Metrics", index=False)
    gate.to_excel(xw, sheet_name="Gate G2", index=False)
    scored[-1].to_excel(xw, sheet_name="Eval rows", index=False)
print("Wrote silver_v1_3_results.xlsx. Draft responses for human review \u2014 not a compliance determination.")
