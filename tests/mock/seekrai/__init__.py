"""Offline stand-in for the seekrai SDK. Answers from the answer key so the pipeline can be proven end to end."""
import csv, itertools, os, re, types
_KEY = {int(r["qnum"]): r for r in csv.DictReader(open(os.environ.get("MOCK_KEY", "testsets/answer_key.csv")))}
_SRC = {"D1": "Information Security Policy §2", "D2": "Data Handling Standard §2", "D3": "Subprocessor List §1",
        "D4": "Business Continuity §2", "": "\u2014"}
_ids = itertools.count(1); _threads = {}
def _reply(prompt):
    if "Fernwell" in prompt or ("Lumera Health" in prompt and prompt.startswith("For Lumera Health")):
        return "I couldn't find trust documents for 'X' in the library. Please check the name and try again."
    if prompt.startswith(("Write", "Compare")):
        return "I can only draft questionnaire responses from the trust documents in my library."
    if prompt.startswith("For Lumera,"):
        return "Did you mean Lumera Pay, Inc. or Lumera Health, Inc.?"
    if not prompt.startswith("For "):
        return "Which company should I answer for? For example: 'For [Company Name], answer: ...'"
    rows, nh = [], []
    for q in [int(n) for n in re.findall(r"(?:^|answer:\s*)(\d+)\.\s", prompt, re.M)]:
        k = _KEY[q]; ev = k["evidence_substring"]
        if os.environ.get("MOCK_FAULT") == "overclaim" and q == 2:
            k = dict(k, expected_status="Yes")
        if k["expected_status"] == "Not covered":
            nh.append(str(q)); rows.append(f"| {q} | q | Not covered in the trust documents \u2014 route to the security owner. | Not covered | \u2014 | \u2014 |")
        else:
            rows.append(f"| {q} | q | Draft citing {ev}. | {k['expected_status']} | \"{ev}\" | {_SRC[k['source_doc']]} |")
    return ("Lumera Pay, Inc. \u2014 Draft Questionnaire Responses\n| # | Question | Answer | Status | Evidence | Source |\n|---|---|---|---|---|---|\n"
            + "\n".join(rows) + f"\nNEEDS HUMAN: {', '.join(nh) or 'none'}\nDraft responses for human review \u2014 not a compliance determination.\n"
            + "chunk_id: mockchunk001 section: Section 2")
class _Threads:
    def create(self): t = types.SimpleNamespace(id=f"th{next(_ids)}"); _threads[t.id] = []; return t
    def create_message(self, thread_id, role, content): _threads[thread_id].append(content)
    def list_messages(self, thread_id): return [types.SimpleNamespace(content=_reply(_threads[thread_id][-1]))]
class _Runs:
    def run(self, agent_id, thread_id, stream=False): return types.SimpleNamespace(run_id=f"run{next(_ids)}")
    def retrieve(self, run_id, thread_id=None): return types.SimpleNamespace(status="RunStatus.COMPLETED")
class _Agents:
    threads = _Threads(); runs = _Runs()
class SeekrFlow:
    def __init__(self, *a, **k): self.agents = _Agents()
