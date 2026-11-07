# MISRA C:2012 deviation records

Checked with cppcheck 2.7 (`--addon=misra`) as invoked by `tools/safety_gate.py` (no include paths).
Each record covers the whole rule for `src/`, as the gate matches deviations per rule.

| Rule | Justification | Risk | Mitigation |
|---|---|---|---|
| misra-c2012-8.4 | False positive: every external function in `uds.c`/`extras.c` has a compatible prototype in `uds.h`/`extras.h`. The gate runs cppcheck without `-I`, so the headers are not resolved. With `-Isrc -Ideps/isotp-c/src -Ideps/isotp-c/deps/bitfield-c/src` the rule reports 0 findings. | Low: a prototype mismatch would also be caught by the compiler (`-Wall -Werror`). | Re-check with include paths on each change; prototypes live only in the public headers. |
| misra-c2012-14.4 | False positive: the flagged controlling expressions (`has_pid`, `completed`, `success`) are `bool` from `<stdbool.h>`, which cppcheck cannot resolve without include paths. With include paths the rule reports 0 findings. | Low: the operands are essentially Boolean. | Same as 8.4. |
| misra-c2012-2.7 | Unused parameters in the `extras.c` stubs (MIL, VIN, DTC, PID enumeration). These functions have no requirement in `requirements.yaml`; AGENTS.md forbids changing code without a requirement. | Low: the stubs return an empty handle / `false` and are not called by the library or tests. | Remove or implement the stubs only once a requirement exists for them. |
| misra-c2012-2.2 | `PID_BYTE_INDEX * CHAR_BIT` and `sizeof(uint16_t) * CHAR_BIT` multiply by a named constant equal to 1; the operation is kept so the bit offset stays self-describing (REQ-004 PID encoding). | None: the value is a compile-time constant. | Covered by `test_autoset_pid_length` and `test_request_pid_enhanced`. |
| misra-c2012-15.4 | `diagnostic_receive_can_frame` loop has two `break`s (completed message / partial frame). Restructuring changes the REQ-006/REQ-008 receive control flow, which needs its own requirement-driven change. | Medium: two exits make the loop harder to review. | Behavior covered by `test_receive_wrong_arb_id`, `test_send_functional_request`, `test_response_multi_frame` and `test_multi_frame_partials_cover_full_message`. |
| misra-c2012-10.4 | Reported by the gate only in `diagnostic_request_to_string` / `diagnostic_response_to_string` (`int` vs `size_t` arithmetic). These debug-log helpers have no requirement, so they are not modified. With include paths cppcheck also reports 10.4 in requirement-covered functions (integer constants vs `uint8_t`); see note below. | Medium: mixed signedness in the length arithmetic of the log helpers. | Raise a requirement for the log helpers, then fix; full essential-type review pending with include paths. |
| misra-c2012-10.3 | `int remaining_space = destination_length - bytes_used;` in `diagnostic_request_to_string` (no requirement, not modified). | Medium: narrowing `size_t` to `int`. | Same as 10.4. |
| misra-c2012-18.4 | `destination + bytes_used` pointer arithmetic in the `*_to_string` helpers (no requirement, not modified). | Medium: if `snprintf` truncates, `bytes_used` can exceed `destination_length` and the next write overflows. Callers use a 128-byte buffer, larger than the longest string produced. | Same as 10.4; reported as a finding in the PR. |
| misra-c2012-17.7 | `snprintf` return values ignored in the `*_to_string` helpers (no requirement, not modified). With include paths it is also reported for `isotp_continue_send` in `diagnostic_receive_can_frame`. | Low: log output only / send status is tracked in the ISO-TP handle. | Same as 10.4. |

Note for the assessor: running cppcheck with include paths (not done by the gate) reports additional
rules (10.4 in covered code, 8.7, 9.2, 2.3/2.4/2.5, 21.1) that the gate does not see.
