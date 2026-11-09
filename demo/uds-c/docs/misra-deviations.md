# MISRA C:2012 deviation records

Analysis configuration: `cppcheck --addon=misra src` as run by `tools/safety_gate.py` (cppcheck 2.7,
no `-I` include paths). Each row covers every occurrence of the rule in `src/` under that configuration.

| Rule | Justification | Risk | Mitigation |
|---|---|---|---|
| misra-c2012-8.4 | All 13 findings are external functions that do have a compatible declaration in `uds/uds.h` / `uds/extras.h`, which each `.c` file includes. The gate runs cppcheck without `-I`, so the headers are not resolved; with `-Isrc -Ideps/isotp-c/src -Ideps/isotp-c/deps/bitfield-c/src` the count is 0. Analysis-configuration artefact. | Low: prototype mismatch would also be caught by gcc `-Wall -Werror` when the tests compile against the headers. | Re-run the check with include paths before release; the compiler build is part of CI (`make test`). |
| misra-c2012-14.4 | Findings are on `bool` operands (`has_pid`, `completed`, `success`) declared in `uds_types.h` through `<stdbool.h>`. Without include paths cppcheck cannot see the essential Boolean type; with include paths the rule reports 0. Analysis-configuration artefact. | Low: the controlling expressions are essentially Boolean. | Same as 8.4. |
| misra-c2012-2.2 | Two findings on `PID_BYTE_INDEX * CHAR_BIT` (`PID_BYTE_INDEX` is 1). The multiplication documents the byte-to-bit offset computation and is intentional; removing it would hide the intent and would break if the index changes. | None: the operation is a compile-time constant. | Code review; covered by REQ-004 tests that check PID bytes on the wire. |
| misra-c2012-2.7 | Unused parameters in the `src/uds/extras.c` stubs (`diagnostic_request_vin`, `_dtc`, `_malfunction_indicator_status`, `diagnostic_clear_dtc`, `diagnostic_enumerate_pids`). The stubs are not covered by any requirement in `requirements.yaml`, so per AGENTS.md they are not modified; the parameters are part of the public API in `extras.h`. | Medium: callers receive an empty handle; the functions do not implement any behaviour. | Reported as a finding. Do not use `extras.c` in a product until requirements and an implementation exist. |
| misra-c2012-10.4 | All remaining findings are in `diagnostic_response_to_string` / `diagnostic_request_to_string` (mixed `int`/`size_t` arithmetic on `bytes_used`). These logging helpers have no requirement, so they are not modified under AGENTS.md. | Medium: if `snprintf` truncates, `destination_length - bytes_used` can wrap and the next `snprintf` may write out of bounds. Only reachable when a log shim is configured. | Reported as a finding; helpers are only called with 128-byte buffers, which fit the longest string they produce. Requires a requirement before fixing. |
| misra-c2012-10.3 | `int remaining_space = destination_length - bytes_used;` in `diagnostic_request_to_string` (no requirement, not modified). | Same as 10.4. | Same as 10.4. |
| misra-c2012-18.4 | `destination + bytes_used` pointer arithmetic in the two `*_to_string` helpers (no requirement, not modified). | Same as 10.4. | Same as 10.4. |
| misra-c2012-17.7 | Unused `snprintf` return value in the two `*_to_string` helpers (no requirement, not modified). All `memcpy` calls in traced code now cast the result to `(void)`. | Low: output is diagnostic logging only. | Same as 10.4. |

Note for the assessor: with include paths, cppcheck reports additional rules (mostly 10.4 essential type,
8.7, 2.5, 21.x) that the gate configuration does not see. They are outside the scope of this record.
