"""Gate G0: data readiness. Run before any upload.
python check_corpus.py --company "Lumera Pay, Inc." --other "Lumera Health" corpus/D1_*.md corpus/D2_*.md ...
Exit code 1 if any check fails."""
import argparse, pathlib, re, sys

def check(path, company, others):
    text, issues = path.read_text(), []
    lines = text.splitlines()
    if not re.search(r"(Version|[Ee]ffective|[Ll]ast updated|Updated)\s", text):
        issues.append("no version or effective date line")
    starts = [i for i, l in enumerate(lines) if l.startswith("## ")]
    if not starts:
        issues.append("no '## ' sections found")
    for i in starts:
        nxt = [l for l in lines[i + 1:i + 6] if l.strip()][:3]
        found = [re.match(r"^Company:\s*(.+?)\s*\|", l) for l in nxt]
        names = [f.group(1) for f in found if f]
        if not names:
            issues.append(f"line {i+1}: section without a company line: {lines[i][:60]}")
        elif names[0] != company:
            issues.append(f"line {i+1}: company line names '{names[0]}', expected '{company}'")
    for o in others:
        for n, l in enumerate(lines, 1):
            if o.lower() in l.lower():
                issues.append(f"line {n}: names another company '{o}' (cross-naming plants it in the store)")
    widths, prev = [], None
    for n, l in enumerate(lines, 1):
        if l.strip().startswith("|"):
            w = l.count("|")
            if prev is not None and w != prev:
                issues.append(f"line {n}: table row has {w-1} cells, previous row {prev-1}")
            prev = w
        else:
            prev = None
    return issues

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--company", required=True); ap.add_argument("--other", action="append", default=[])
    ap.add_argument("files", nargs="+")
    a = ap.parse_args(); failed = False
    for f in a.files:
        issues = check(pathlib.Path(f), a.company, a.other)
        print(("PASS " if not issues else "FAIL ") + f)
        for i in issues: print("   -", i)
        failed |= bool(issues)
    print("G0:", "FAIL" if failed else "PASS"); sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
