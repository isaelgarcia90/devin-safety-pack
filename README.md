# Devin Safety Pack

**Safety evidence for software, with potential applications beyond automotive.**

Devin Safety Pack is a plugin that helps Devin work on software that needs safety evidence. The idea comes from my experience in automotive software development. Automotive teams already use coding-standard checks, and some projects cannot reach production until safety-related issues are resolved. However, some legacy projects may have gaps in these checks or lack clear records of previous reviews.

The plugin connects code to requirements and checks that each requirement has a test. It also helps review C code using **MISRA** (Motor Industry Software Reliability Association) guidelines. Issues must be fixed or documented with a reason for accepting the exception. An automatic check fails when required evidence is missing.

During the hackathon, I used the plugin with an open-source vehicle diagnostics library from the OpenXC project. In a Devin session, all 10 demo requirements were linked to code and tests. Four tests were added. Of the 72 coding-rule findings, 36 were fixed, while the remaining findings were documented as exceptions.

Safety Pack may also serve as a code-audit service. It would provide an extra review, even when a client has already run their own coding-standard checks. The goal is to find possible gaps and give human reviewers evidence they can check again.

**This approach could also be adapted to biomedical software, including medical devices, as well as aerospace and other regulated industries.** Each version would need rules based on the relevant standards and validation by specialists. Safety Pack does not certify software or guarantee that it is safe. It supports human review rather than replacing it.

The current prototype focuses on embedded C. Its automotive demo is inspired by **ISO 26262**, the international standard for automotive functional safety. Applications in other industries have not yet been validated.

## Hackathon presentation

[**Open the hackathon presentation**](https://raw.githack.com/isaelgarcia90/devin-safety-pack/main/docs/HACKATHON_PRESENTATION_2026-10-29.html)

The presentation keeps the original hackathon slides. Use its controls to switch between Spanish and English or between light and dark themes.

Source file: [`docs/HACKATHON_PRESENTATION_2026-10-29.html`](docs/HACKATHON_PRESENTATION_2026-10-29.html)

## Quickstart: run the demo in Devin Desktop

This is the happy path: install the plugin, then send one message to run the demo. **You do not need to start a session on the web or send a separate message for each skill.**

You need Devin Desktop signed in and Git installed. To publish the result, Devin also needs GitHub access with permission to open a pull request (PR), a proposed code change.

### 1. Clone and open the repository

Run this in a terminal, using a new folder:

```bash
git clone --branch main --single-branch https://github.com/isaelgarcia90/devin-safety-pack.git devin-safety-pack-demo
cd devin-safety-pack-demo
```

Open the `devin-safety-pack-demo` folder in Devin Desktop. Starting from `main` keeps this demo separate from earlier completed reviews.

### 2. Install Safety Pack

In Devin Desktop, use **Open customizations** from the session menu and go to **Plugins**. Install the plugin from this GitHub repository:

```text
isaelgarcia90/devin-safety-pack
```

The plugin is at the repository root, so leave the subdirectory empty if requested. Review the security notice and confirm the installation if you trust the source.

Check that Safety Pack appears in the installed plugins list. Then start a new session for the folder you opened. If it is already installed, just start the new session.

Cloning the repository does not install the plugin. Also, this repository includes skill files that Devin can discover separately. Seeing the skills alone is therefore not proof of installation. See the official [Desktop plugin guide](https://docs.devin.ai/desktop/devin-local/customizations#plugins) and [skill discovery guide](https://docs.devin.ai/product-guides/skills#skill-discovery).

### 3. Send one message

Paste the following into the new Desktop session. Devin will use the skills in order and generate the before-and-after evidence.

```text
Run the Safety Pack demo on demo/uds-c in this repository.
Use the installed Safety Pack rules and skills.

Create a new branch from a clean main checkout. Do not overwrite
uncommitted work. Keep README.md unchanged throughout the demo.

Prepare the C build tools, Python 3, cppcheck with its MISRA addon,
and the Check test library. The reference GitHub workflow uses
Ubuntu 22.04. Record the actual tool versions and use the same analyzer
version before and after the changes.

Read AGENTS.md. Show the demo source and requirements before editing.

Run from the repository root:
make -C demo/uds-c test
python3 tools/safety_gate.py --project demo/uds-c --out safety-report/before

The baseline gate is expected to fail because evidence is missing.
Preserve this report before making changes.

Use trace-matrix to link requirements to code and meaningful tests.
Report partial or unmet requirements honestly.
Then use misra-check to fix suitable coding-rule findings and document
exceptions with their reasons and risks.
Do not weaken the gate or rewrite requirements to hide problems.

Run the final checks:
make -C demo/uds-c test
python3 tools/safety_gate.py --project demo/uds-c --out safety-report/after

Use safety-pr to open a new pull request with a Safety Impact Analysis.
Include the actual before-and-after results. Distinguish fixed findings
from documented exceptions and keep open issues visible.
Do not commit generated reports or build files.

Wait for the GitHub checks and address failures without weakening them.
Do not merge the pull request.
```

You do not need to type `trace-matrix`, `misra-check`, or `safety-pr` as separate commands. The single message asks Devin to use all of them.

### 4. Review the result

Compare these reports in the demo workspace:

- `safety-report/before/report.md`
- `safety-report/after/report.md`

Each folder also contains `report.html`, which you can open in a browser. Running the Python gate only checks the evidence; the changes are made by Devin following the skills.

Open the PR link Devin provides. Review **Files changed** and the **Safety Impact Analysis**, the report about the change's effect on safety. In **Checks**, confirm that `safety-gate` has finished and inspect its result.

For a recording, show the original code and baseline report, then the final report and PR. Record in segments so you can remove the waiting time. Use the actual results from your session.

## Demo source code

The demo uses [`openxc/uds-c`](https://github.com/openxc/uds-c), an open-source vehicle diagnostics library from the OpenXC project. **UDS** means Unified Diagnostic Services, a vehicle diagnostics protocol.

Its dependencies are included: [`openxc/isotp-c`](https://github.com/openxc/isotp-c) and [`openxc/bitfield-c`](https://github.com/openxc/bitfield-c). The original license notices are kept with the source files.

| File | What to inspect |
|---|---|
| [`demo/uds-c/src/uds/uds.c`](demo/uds-c/src/uds/uds.c) | The C implementation being reviewed. |
| [`demo/uds-c/tests/test_core.c`](demo/uds-c/tests/test_core.c) | The existing unit tests. |
| [`demo/uds-c/requirements.yaml`](demo/uds-c/requirements.yaml) | The demonstration requirements. |
| [`AGENTS.md`](AGENTS.md) | The rules Devin should follow. |

**The requirements and their assigned safety levels were written for this demonstration. They are not official Ford requirements or the result of a formal safety assessment.**

## Example result from the hackathon

In [PR #2](https://github.com/isaelgarcia90/devin-safety-pack/pull/2), a Devin session produced the following results with cppcheck 2.7:

| Measure | Before | After |
|---|---:|---:|
| Requirements with code links | 0/10 | 10/10 |
| Requirements with test links | 0/10 | 10/10 |
| Unit tests | 19 | 23 |
| MISRA findings fixed during the run | — | 36 |
| MISRA findings covered by documented exceptions | 0 | 36 |
| MISRA findings without a documented exception | 72 | 0 |
| Safety gate | FAIL | PASS |

The baseline already had passing tests. What was initially missing was their connection to the demo requirements.

These numbers belong to that run. A new session may produce different results, especially with a different analyzer version.

The example also reports a partially met requirement, REQ-008. **A passing gate does not mean every requirement is fully satisfied.** A documented exception is not a fix.

You can inspect the [original failed run](https://github.com/isaelgarcia90/devin-safety-pack/actions/runs/40933201498) and the [successful run for the example PR](https://github.com/isaelgarcia90/devin-safety-pack/actions/runs/40937201809).

This compares the original code with the reviewed branch. It is not a controlled comparison of Devin without the plugin against Devin with it: the repository also contains the rules and skills.

## What is included

| File or folder | Purpose |
|---|---|
| [`.devin-plugin/plugin.json`](.devin-plugin/plugin.json) | Defines the plugin name and version. |
| [`AGENTS.md`](AGENTS.md) | Gives Devin standing rules for safety-relevant changes. |
| [`skills/trace-matrix`](skills/trace-matrix) | Links requirements to code and tests. Reports missing evidence. |
| [`skills/misra-check`](skills/misra-check) | Uses cppcheck, a static analyzer that examines code without executing it. Guides fixes and documented exceptions. |
| [`skills/safety-pr`](skills/safety-pr) | Prepares a PR with the Safety Impact Analysis. |
| [`tools/safety_gate.py`](tools/safety_gate.py) | Checks requirement links and reported findings against documented exceptions. |
| [`.github/workflows/safety-gate.yml`](.github/workflows/safety-gate.yml) | Runs tests and the gate in continuous integration (CI), the automated checks for submitted changes. |

## Limits and use in other projects

The gate checks whether each requirement has a code tag and a test tag. It does not prove that a linked test fully verifies the required behavior or that every function has a requirement tag.

MISRA exceptions currently apply to a whole rule rather than a specific finding location. Analyzer settings also affect the results; the current gate does not pass the project's include paths to cppcheck or fully validate analyzer execution. This is not a complete MISRA compliance assessment.

The GitHub workflow runs unit tests before the evidence gate. To prevent merging when checks fail, the repository must configure them as required checks in its branch protection rules.

For another project, installing the plugin alone does not create its automated checks. It needs approved requirements and suitable tests. The gate and workflow must also be added and adapted to its build system.

The current demo is automotive. Biomedical or aerospace use would require domain-specific rules and validation by specialists. Safety Pack supports human review; it does not replace a safety process or provide certification.
