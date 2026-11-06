"""Diligence Desk verification standard v1: metrics and gates G1 to G3.

A row passes only when status, evidence, source, and isolation are all right.
Thresholds are the proposed standard; record any change and its reason.
"""
import re
import pandas as pd

DEFAULT_SIGNATURES = ["14 days", "72 hours", "180 days", "8 hours", "azure", "february 2026",
                      "hipaa", "baa", "carepost"]   # Lumera Health values that must never appear for Lumera Pay
DOC_NAMES = {"D1": ["security policy", "information security"], "D2": ["data handling", "privacy"],
             "D3": ["subprocessor", "vendor"], "D4": ["continuity", "incident response"]}

GATES = {
    "G2": {"status_acc": 0.94, "overclaim_rate": 0.0, "fabrication_rate": 0.0, "quote_in_source": 1.0,
           "source_acc": 0.94, "contaminated_rows": 0, "consistency": 1.0, "completion": 1.0},
    "G3": {"status_acc": 0.94, "overclaim_rate": 0.0, "fabrication_rate": 0.0, "quote_in_source": 1.0,
           "source_acc": 0.94, "contaminated_rows": 0, "consistency": 1.0, "completion": 1.0,
           "audit_complete": 1.0},
}
LOWER_IS_BETTER = {"overclaim_rate", "fabrication_rate", "contaminated_rows"}

def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", str(s))).strip().lower()

def load_corpus(paths):
    return {p.name[:2]: norm(p.read_text()) for p in paths}

def has_signature(text, signatures):
    t = str(text).lower()
    return any(re.search(r"(?<![\w.])" + re.escape(s.lower()) + r"\b", t) for s in signatures)

def score(rows, key, corpus, signatures=DEFAULT_SIGNATURES):
    """rows: DataFrame with qnum, status, evidence, source, answer. key: answer_key.csv columns."""
    m = key.merge(rows, on="qnum", how="left", suffixes=("", "_got")).fillna("")
    m["missing"] = m.status == ""
    m["status_ok"] = m.status.str.lower() == m.expected_status.str.lower()
    m["overclaim"] = ((m.status == "Yes") & (m.expected_status != "Yes")) | \
                     (m.status.isin(["Yes", "Partial"]) & m.expected_status.isin(["No", "Not covered"]))
    m["fabrication"] = (m.expected_status == "Not covered") & (m.status != "Not covered") & ~m.missing
    m["evidence_has_key"] = m.apply(lambda r: r.evidence_substring == "" or
                                    norm(r.evidence_substring) in norm(r.evidence), axis=1)
    m["quote_in_source"] = m.apply(lambda r: r.expected_status == "Not covered" or
                                   (len(norm(r.evidence)) > 3 and any(norm(r.evidence) in t for t in corpus.values())), axis=1)
    m["source_ok"] = m.apply(lambda r: r.source_doc == "" or
                             any(n in str(r.source).lower() for n in DOC_NAMES.get(r.source_doc, [])), axis=1)
    m["contaminated"] = m.apply(lambda r: has_signature(f"{r.answer} {r.evidence}", signatures), axis=1)
    m["pass"] = m.status_ok & m.evidence_has_key & m.quote_in_source & m.source_ok & ~m.contaminated
    return m

def metrics(scored):
    answered = scored[scored.expected_status != "Not covered"]
    nc_pred = scored[scored.status == "Not covered"]
    return {
        "rows": len(scored),
        "completion": round(1 - scored.missing.mean(), 3),
        "status_acc": round(scored.status_ok.mean(), 3),
        "overclaim_rate": round(scored.overclaim.mean(), 3),
        "fabrication_rate": round(scored.fabrication.mean(), 3),
        "abstain_recall": round(scored[scored.expected_status == "Not covered"].status.eq("Not covered").mean(), 3)
                          if (scored.expected_status == "Not covered").any() else None,
        "abstain_precision": round(nc_pred.expected_status.eq("Not covered").mean(), 3) if len(nc_pred) else None,
        "quote_in_source": round(answered.quote_in_source.mean(), 3) if len(answered) else 1.0,
        "source_acc": round(scored.source_ok.mean(), 3),
        "contaminated_rows": int(scored.contaminated.sum()),
        "row_pass_rate": round(scored["pass"].mean(), 3),
    }

def consistency(scored_runs):
    if len(scored_runs) < 2:
        return 1.0
    statuses = pd.concat([s.set_index("qnum").status for s in scored_runs], axis=1)
    return round((statuses.nunique(axis=1) == 1).mean(), 3)

def evaluate_gate(gate, m):
    results = []
    for k, threshold in GATES[gate].items():
        v = m.get(k)
        ok = v is not None and (v <= threshold if k in LOWER_IS_BETTER else v >= threshold)
        results.append({"check": k, "value": v, "threshold": ("<= " if k in LOWER_IS_BETTER else ">= ") + str(threshold),
                        "pass": bool(ok)})
    return pd.DataFrame(results)

def gate_markdown(gate, table, context):
    lines = [f"# Gate {gate}: {'PASS' if table['pass'].all() else 'FAIL'}", ""]
    lines += [f"- {k}: {v}" for k, v in context.items()] + ["", "| Check | Value | Threshold | Pass |", "| --- | --- | --- | --- |"]
    lines += [f"| {r.check} | {r.value} | {r.threshold} | {'yes' if r['pass'] else 'NO'} |" for _, r in table.iterrows()]
    return "\n".join(lines) + "\n"
