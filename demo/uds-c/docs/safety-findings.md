# Findings for the safety assessor

These are behaviours that do not match `requirements.yaml`. They stay visible on purpose.
Traceability tags show where each requirement is implemented and tested. A tag does not mean the requirement is met.

| Id | Requirement | Finding | Evidence | Status |
|---|---|---|---|---|
| F-01 | REQ-008 (ASIL B) | Multi-frame (ISO-TP) responses are not reassembled into one response. With `STITCH_MULTIFRAME=1`, the completed `DiagnosticResponse` holds only the payload of the last consecutive frame (8 bytes instead of 18). Each earlier call returns only its partial frame. | `tests/test_core.c` `test_response_multi_frame` asserts `payload_length == 8`. Its `@verifies REQ-008` tag is partial and labelled as such. | Open |
| F-02 | REQ-007 (ASIL B) | On a negative response (0x7F), `DiagnosticResponse.success` is `false` and the NRC (negative response code) is reported. However, `diagnostic_receive_can_frame` sets `handle->success = true`, so a caller that reads the handle sees success. | `src/uds/uds.c` `diagnostic_receive_can_frame`. `test_negative_response` checks the response but not `handle.success`. | Open |
| F-03 | REQ-004 (ASIL B) | `autoset_pid_length` sends a 1-byte PID in enhanced mode 0x22 when the PID is <= 0xFF. The requirement asks for 2 bytes in enhanced modes. | `test_autoset_pid_length` asserts a 3-byte frame for mode 0x22 / PID 0x12. That test is therefore not tagged `@verifies REQ-004`. | Open |
| F-04 | none | `src/uds/extras.c` (MIL, VIN, DTC, PID enumeration) is a stub with no requirement. It returns empty handles. | `src/uds/extras.c`, MISRA 2.7 / 8.4 deviations. | Out of scope |
| F-05 | gate | `tools/safety_gate.py` runs cppcheck without include paths and accepts deviations per rule, not per location. This causes the 8.4 / 14.4 artifacts. A rule-level deviation would also hide any new finding of the same rule. | `tools/safety_gate.py` `misra()`. | Gate unchanged. Reviewer should rerun with `-I` |

_Evidence for a human safety assessor. Not a certification._
