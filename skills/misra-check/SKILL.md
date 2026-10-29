---
name: misra-check
description: Run MISRA C:2012 checks with cppcheck, fix safe violations and document justified deviations. Use when asked about MISRA, coding-standard compliance or static analysis of embedded C.
argument-hint: "<source dir>"
---

# MISRA check

1. Run `cppcheck --addon=misra --quiet --template='{file}:{line}:{id}' <src>` and group findings by rule.
2. Fix violations that are mechanical and behavior-preserving (braces, explicit casts, boolean
   conditions, unused parameters) and re-run the project's tests after each batch.
3. For rules that would require an API or architecture change, add a row to
   `docs/misra-deviations.md`: `| misra-c2012-X.Y | justification | risk | mitigation |`.
4. Re-run `python3 tools/safety_gate.py` and report: violations before, fixed, deviated, remaining.
