---
name: safety-pr
description: Open a pull request with a Safety Impact Analysis (affected requirements, ASIL, MISRA delta, traceability coverage, test evidence). Use when finishing a change on safety-relevant code.
---

# Safety PR

1. Run the project's tests and `python3 tools/safety_gate.py --project <dir>`; both must pass.
2. Open the PR with this description:

```
## Safety Impact Analysis
- Affected requirements: REQ-... (ASIL ...)
- Traceability: X/Y requirements with code, X/Y with tests (before -> after)
- MISRA C:2012: N violations, M fixed, K documented deviations, 0 undocumented
- New/changed tests: ...
- Findings for the safety assessor: ...
- Note: this is evidence for a human assessor, not a certification.
```
