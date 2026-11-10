"""Verification checks for Diligence Desk: scoring, metrics, and the silver and gold pass bars.

A row passes only when its status, evidence, source, and company isolation are all correct.
"""
import re
import unicodedata
import pandas as pd

# Lumera Health values that must never appear in a Lumera Pay answer.
DEFAULT_SIGNATURES = ["14 days", "72 hours", "180 days", "8 hours", "azure", "february 2026",
                      "hipaa", "baa", "carepost"]
# Keywords that identify each demo document in the agent's Source column.
# For any other document, the words in its file name (hyphens read as spaces) are used.
DOC_NAMES = {"security-policy": ["security policy", "information security"],
             "data-handling": ["data handling", "privacy"],
             "subprocessors": ["subprocessor", "vendor"],
             "continuity": ["continuity", "incident response"]}

CHECKS = {
    "silver": {"status_acc": 0.94, "overclaim_rate": 0.0, "fabrication_rate": 0.0, "quote_in_source": 1.0,
               "source_acc": 0.94, "contaminated_rows": 0, "consistency": 1.0, "completion": 1.0},
    "gold": {"status_acc": 0.94, "overclaim_rate": 0.0, "fabrication_rate": 0.0, "quote_in_source": 1.0,
             "source_acc": 0.94, "contaminated_rows": 0, "consistency": 1.0, "completion": 1.0,
             "audit_complete": 1.0},
}
LOWER_IS_BETTER = {"overclaim_rate", "fabrication_rate", "contaminated_rows"}

_FOLD = {ord(c): "-" for c in "\u2010\u2011\u2012\u2013\u2014\u2015\u2212"}
_FOLD.update({ord(c): "'" for c in "\u2018\u2019\u201b"})
_FOLD.update({ord(c): '"' for c in "\u201c\u201d"})

def norm(s):
    """Lowercase, drop bold marks, and treat typographic hyphens, quotes, and spaces as plain ones."""
    s = unicodedata.normalize("NFKC", str(s)).translate(_FOLD)
    return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", s)).strip().lower()

def load_documents(paths):
    """Map each document's file name (without extension) to its normalized text."""
    return {p.stem: norm(p.read_text()) for p in paths}

def has_signature(text, signatures):
    t = str(text).lower()
    return any(re.search(r"(?<![\w.])" + re.escape(s.lower()) + r"\b", t) for s in signatures)

def score(rows, key, documents, signatures=DEFAULT_SIGNATURES):
    """rows: DataFrame of agent answers. key: answer_key.csv. Returns one scored row per question."""
    m = key.merge(rows, on="qnum", how="left", suffixes=("", "_got")).fillna("")
    m["missing"] = m.status == ""
    m["status_ok"] = m.status.str.lower() == m.expected_status.str.lower()
    m["overclaim"] = ((m.status == "Yes") & (m.expected_status != "Yes")) | \
                     (m.status.isin(["Yes", "Partial"]) & m.expected_status.isin(["No", "Not covered"]))
    m["fabrication"] = (m.expected_status == "Not covered") & (m.status != "Not covered") & ~m.missing
    m["evidence_has_key"] = m.apply(lambda r: r.evidence_substring == "" or
                                    norm(r.evidence_substring) in norm(f"{r.evidence} {r.answer}"), axis=1)
    m["quote_in_source"] = m.apply(lambda r: r.expected_status == "Not covered" or
                                   (len(norm(r.evidence)) > 3 and any(norm(r.evidence) in t for t in documents.values())), axis=1)
    def _source_ok(r):
        expected = [d for d in str(r.source_doc).split("|") if d]
        if not expected:
            return True
        # The quote must come from an expected document, or the Source column must name one.
        for d in expected:
            if d in documents and len(norm(r.evidence)) > 3 and norm(r.evidence) in documents[d]:
                return True
            if any(n in str(r.source).lower() for n in DOC_NAMES.get(d, [d.replace("-", " ")])):
                return True
        return False
    m["source_ok"] = m.apply(_source_ok, axis=1)
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
    """Share of questions with the same status in every repeated run."""
    if len(scored_runs) < 2:
        return 1.0
    statuses = pd.concat([s.set_index("qnum").status for s in scored_runs], axis=1)
    return round((statuses.nunique(axis=1) == 1).mean(), 3)

def evaluate_check(check, m):
    results = []
    for k, threshold in CHECKS[check].items():
        v = m.get(k)
        ok = v is not None and (v <= threshold if k in LOWER_IS_BETTER else v >= threshold)
        results.append({"check": k, "value": v, "threshold": ("<= " if k in LOWER_IS_BETTER else ">= ") + str(threshold),
                        "pass": bool(ok)})
    return pd.DataFrame(results)

def check_markdown(check, table, context):
    lines = [f"# {check.capitalize()} check: {'PASS' if table['pass'].all() else 'FAIL'}", ""]
    lines += [f"- {k}: {v}" for k, v in context.items()] + ["", "| Measure | Value | Required | Pass |", "| --- | --- | --- | --- |"]
    lines += [f"| {r.check} | {r.value} | {r.threshold} | {'yes' if r['pass'] else 'NO'} |" for _, r in table.iterrows()]
    return "\n".join(lines) + "\n"
