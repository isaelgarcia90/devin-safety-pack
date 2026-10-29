---
name: trace-matrix
description: Build the requirement -> code -> test traceability matrix for a C project, report gaps and close them. Use when asked about traceability, requirement coverage, ISO 26262 / ASPICE evidence.
argument-hint: "<project dir containing requirements.yaml>"
---

# Traceability matrix

1. Run `python3 tools/safety_gate.py --project <dir> --out <dir>/safety-report` and read
   `safety-report/report.md`.
2. For every requirement **without code**: find the function(s) that implement it and add
   `/* @req REQ-xxx */` right above each definition. Do not tag code you did not verify implements it.
3. For every requirement **without a test**: tag existing tests that really verify it with
   `/* @verifies REQ-xxx */`; if none exists, write a new focused test, register it in the suite,
   and run the project's tests.
4. If you find a requirement whose implementation is a stub or behaves differently than the text,
   do not hide it: report it as a finding.
5. Re-run the gate until traceability is 100% and summarize before/after coverage.
