# Safety Pack (always-on rule)

You are working on safety-relevant embedded C code. Follow these rules in every change:

1. **Traceability to requirements.** Every function you add or change under `src/` must carry a
   `/* @req REQ-xxx */` comment that references an existing id in the project's `requirements.yaml`.
   If no requirement covers the change, stop and ask for one instead of inventing behavior.
2. **Every requirement is verified.** Each requirement in `requirements.yaml` needs at least one test
   tagged with `/* @verifies REQ-xxx */`. When a requirement has no test, write one.
3. **MISRA C:2012.** Do not introduce new MISRA violations (`cppcheck --addon=misra`). If a violation
   cannot be fixed safely, record a deviation in `docs/misra-deviations.md` (rule, justification, risk).
4. **Evidence in every PR.** Run `python3 tools/safety_gate.py --project <dir>` before finishing and
   use the `safety-pr` skill so the PR includes a "Safety Impact Analysis".
5. Never claim the code is "certified". The plugin produces evidence for a human safety assessor.
