# MISRA C:2012 deviation records

| Rule | Justification | Risk | Mitigation |
|---|---|---|---|
| misra-c2012-8.4 | Public API functions are declared in uds.h; cppcheck analyses .c files in isolation and does not see the prototype. | Low | Headers are included by every translation unit; verified by `-Wall -Werror` build. |
| misra-c2012-2.7 | Unused parameters in `extras.c` belong to the published API for features not implemented yet (MIL, VIN, DTC). | Low | Functions return an incomplete handle; tracked as open finding for the assessor. |
| misra-c2012-12.1 | Operator precedence is standard arithmetic/bit operations in OBD-II decoding. | Low | Covered by REQ-009 tests with known physical values. |
| misra-c2012-10.4 | Mixed essential types in OBD-II formulas (uint8 * int / float) mandated by SAE J1979 formulas. | Medium | Results checked against reference values in tests (REQ-009). |
| misra-c2012-15.5 | Early returns in switch-based decoders improve readability; refactor deferred to avoid behavior changes in legacy code. | Low | Full unit-test suite (21 tests) guards behavior. |
| misra-c2012-17.7 | Return values of logging/ISO-TP calls not used where failure is handled by the handle state. | Medium | Handle `completed/success` flags checked in REQ-002/REQ-008 tests. |
| misra-c2012-14.4 | Pointer/integer used as condition (legacy style). | Low | Mechanical fix planned; no behavior impact. |
| misra-c2012-13.4 | Assignment result used in expression (legacy style). | Low | Mechanical fix planned. |
| misra-c2012-18.4 | Pointer arithmetic on payload buffers with explicit size checks. | Medium | Bounds covered by multi-frame test (REQ-008). |
| misra-c2012-17.8 | Function parameters modified locally in legacy helpers. | Low | Mechanical fix planned. |
| misra-c2012-2.2 | Dead code reported in stubbed functions of `extras.c`. | Low | Open finding: stubs must be implemented or removed before production. |
| misra-c2012-15.7 | Missing final `else` in an if/else-if chain. | Low | Mechanical fix planned. |
| misra-c2012-15.6 | Single-statement body without braces. | Low | Mechanical fix planned. |
| misra-c2012-15.4 | More than one `break` in a loop. | Low | Loop covered by REQ-005 test. |
| misra-c2012-10.3 | Implicit narrowing assignment between essential types. | Medium | Values bounded by CAN frame size (<= 8 bytes). |
