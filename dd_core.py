"""Diligence Desk shared core: agent runs, output parsing, prompt building.

SDK shapes verified against docs.seekr.com on Oct 25, 2026 ("Run an agent"):
client.agents.threads.create(), threads.create_message(thread_id, role, content),
client.agents.runs.run(agent_id, thread_id, stream=False) -> .run_id,
client.agents.runs.retrieve(run_id, thread_id=...) -> .status,
client.agents.threads.list_messages(thread_id)[0] -> newest message.
"""
import json, re, time

STATUSES = {"yes": "Yes", "partial": "Partial", "no": "No", "not covered": "Not covered"}
REPLY_MARKERS = {
    "offscope": "I can only draft questionnaire responses",
    "unknown_company": "couldn't find trust documents",
    "disambiguate": "Did you mean",
    "which_company": "Which company should I answer for",
}

def message_text(content):
    """Flatten a thread message's content (string, list of parts, or object) to text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for part in content:
            if isinstance(part, str):
                out.append(part)
            elif isinstance(part, dict):
                out.append(str(part.get("text") or part.get("content") or json.dumps(part)))
            else:
                out.append(str(getattr(part, "text", None) or part))
        return "\n".join(out)
    return str(getattr(content, "text", content))

def ask_agent(client, agent_id, prompt, timeout_s=240, poll_s=1.5):
    """One thread per call so runs never share context. Returns text plus run metadata."""
    t0 = time.time()
    thread = client.agents.threads.create()
    client.agents.threads.create_message(thread_id=thread.id, role="user", content=prompt)
    run = client.agents.runs.run(agent_id=agent_id, thread_id=thread.id, stream=False)
    run_id = run.run_id
    while True:
        status = str(getattr(client.agents.runs.retrieve(run_id, thread_id=thread.id), "status", "")).lower()
        if status.endswith("completed"):
            break
        if any(s in status for s in ("fail", "cancel", "expire", "error")):
            raise RuntimeError(f"run {run_id} ended with status {status}")
        if time.time() - t0 > timeout_s:
            raise TimeoutError(f"run {run_id} exceeded {timeout_s}s")
        time.sleep(poll_s)
    messages = client.agents.threads.list_messages(thread.id)
    return {"text": message_text(messages[0].content), "run_id": run_id, "thread_id": thread.id,
            "latency_s": round(time.time() - t0, 2)}

def build_prompt(company, items):
    """items: list of (qnum, question). Same input format as the bronze agent."""
    return f"For {company}, answer:\n" + "\n".join(f"{q}. {text}" for q, text in items)

def normalize_status(s):
    s = re.sub(r"[*_`]", "", str(s)).strip().lower()
    return STATUSES.get(s, s.title() if s else "")

_ROW = re.compile(r"^\s*\|(.+)\|\s*$")
def parse_table(text):
    """Parse the agent's six-column markdown table into row dicts."""
    rows = []
    for line in text.splitlines():
        m = _ROW.match(line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if len(cells) < 6 or set("".join(cells)) <= set("-: ") or cells[0] == "#":
            continue
        num = re.sub(r"\D", "", cells[0])
        if not num:
            continue
        rows.append({"qnum": int(num), "question": cells[1], "answer": cells[2],
                     "status": normalize_status(cells[3]),
                     "evidence": cells[4].strip("\"\u201c\u201d "), "source": cells[5]})
    return rows

def needs_human(text):
    m = re.search(r"NEEDS HUMAN:\s*([^\n]+)", text)
    return m.group(1).strip() if m else None

def chunk_ids(text):
    """Source-tracing chunk IDs appended to assistant messages when File Search runs."""
    return sorted(set(re.findall(r"chunk_id['\"]?\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{6,})", text)))

def classify_reply(text):
    if parse_table(text):
        return "table"
    for kind, marker in REPLY_MARKERS.items():
        if marker.lower() in text.lower():
            return kind
    return "other"
