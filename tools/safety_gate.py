#!/usr/bin/env python3
"""Safety gate: requirement traceability + MISRA C check. Fails (exit 1) when evidence is missing."""
import argparse
import html
import os
import re
import subprocess
import sys
from pathlib import Path

REQ_TAG = re.compile(r"@req\s+(REQ-\d+)")
VER_TAG = re.compile(r"@verifies\s+(REQ-\d+)")
DEV_RULE = re.compile(r"misra-c2012-\d+\.\d+")


def load_requirements(path):
    reqs, cur = [], None
    for raw in Path(path).read_text().splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^-\s+(\w+):\s*(.*)$", line)
        if m:
            cur = {m.group(1): m.group(2).strip().strip('"')}
            reqs.append(cur)
            continue
        m = re.match(r"^\s+(\w+):\s*(.*)$", line)
        if m and cur is not None:
            cur[m.group(1)] = m.group(2).strip().strip('"')
    return reqs


def scan(root, pattern, exts=(".c", ".h")):
    hits = {}
    for f in sorted(Path(root).rglob("*")):
        if f.suffix not in exts:
            continue
        for n, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            for rid in pattern.findall(line):
                hits.setdefault(rid, []).append(f"{f}:{n}")
    return hits


def misra(src):
    try:
        out = subprocess.run(
            ["cppcheck", "--addon=misra", "--quiet", "--template={file}:{line}:{id}", str(src)],
            capture_output=True, text=True, check=False).stderr
    except FileNotFoundError:
        sys.exit("cppcheck not found")
    return sorted({l for l in out.splitlines() if ":misra-c2012-" in l})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--src", default="src")
    ap.add_argument("--tests", default="tests")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    proj = Path(a.project)
    reqs = load_requirements(proj / "requirements.yaml")
    code = scan(proj / a.src, REQ_TAG)
    tests = scan(proj / a.tests, VER_TAG)
    dev_file = proj / "docs" / "misra-deviations.md"
    deviated = set(DEV_RULE.findall(dev_file.read_text())) if dev_file.exists() else set()
    violations = misra(proj / a.src)
    undeviated = [v for v in violations if v.rsplit(":", 1)[1] not in deviated]
    rules = {}
    for v in violations:
        rules.setdefault(v.rsplit(":", 1)[1], 0)
        rules[v.rsplit(":", 1)[1]] += 1

    n = len(reqs)
    with_code = sum(1 for r in reqs if r["id"] in code)
    with_test = sum(1 for r in reqs if r["id"] in tests)
    ok = with_code == n and with_test == n and not undeviated

    md = ["# Safety Gate Report", "",
          f"**Result: {'PASS' if ok else 'FAIL'}**", "",
          f"- Requirements with code: **{with_code}/{n}**",
          f"- Requirements with tests: **{with_test}/{n}**",
          f"- MISRA C:2012 violations: **{len(violations)}** "
          f"({len(violations) - len(undeviated)} with documented deviation, **{len(undeviated)} undocumented**)",
          "", "## Traceability matrix", "",
          "| Requirement | ASIL | Title | Code | Tests | Status |", "|---|---|---|---|---|---|"]
    for r in reqs:
        c, t = code.get(r["id"], []), tests.get(r["id"], [])
        st = "OK" if c and t else ("NO CODE" if not c else "NO TEST")
        md.append(f"| {r['id']} | {r.get('asil','')} | {r.get('title','')} | "
                  f"{'<br>'.join(Path(x).name for x in c) or '-'} | "
                  f"{'<br>'.join(Path(x).name for x in t) or '-'} | {st} |")
    md += ["", "## MISRA C:2012 by rule", "", "| Rule | Count | Deviation documented |", "|---|---|---|"]
    for rule, cnt in sorted(rules.items(), key=lambda x: -x[1]):
        md.append(f"| {rule} | {cnt} | {'yes' if rule in deviated else 'NO'} |")
    md += ["", "_Evidence for a human safety assessor. Not a certification._"]
    report = "\n".join(md) + "\n"
    print(report)

    if a.out:
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "report.md").write_text(report)
        rows = "".join(f"<pre>{html.escape(l)}</pre>" if False else "" for l in [])
        (out / "report.html").write_text(
            "<!doctype html><meta charset=utf-8><title>Safety Gate</title>"
            "<style>body{font-family:sans-serif;max-width:960px;margin:2em auto}"
            "table{border-collapse:collapse}td,th{border:1px solid #ccc;padding:4px 8px}</style>"
            f"<pre style='white-space:pre-wrap'>{html.escape(report)}</pre>{rows}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as fh:
            fh.write(report)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
