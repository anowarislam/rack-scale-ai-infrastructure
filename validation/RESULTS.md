# Validation results

Date: 2026-10-02 UTC. **Final local validation passed; independent content reviews accepted the course after corrections.** The coordinator used Python 3.11.11 in the local macOS workspace.

These results establish the named artifact and model properties. They do not pass a learner gate or establish native/hardware behavior.

## Final unit tests

The coordinator independently ran all five suites after the relevant corrections.

| Suite | Observed result | Full output |
|---|---|---|
| Systems and checkpoint workload | 19 passed | [Systems log](logs/final-systems-tests.txt) |
| Platform placement and checkpoint recovery | 7 passed | [Platform log](logs/final-platforms-tests.txt) |
| Slurm documented recovery preconditions | 4 passed | [Guard log](logs/final-slurm-guards-tests.txt) |
| Fleet signal, statistics, lifecycle, and capacity | 22 passed | [Fleet log](logs/final-fleet-tests.txt) |
| Two-task recorder and checkpoint integration | 5 passed | [Practicum log](logs/final-practicum-tests.txt) |
| **Total** | **57 passed, zero failures** | All five final suites exited 0 |

Coverage includes broken and healthy controls, partial repairs, checkpoint corruption and resumption, fragmented placement, time/identity validation, exposure denominators, reference uncertainty calculations, stale and duplicate lifecycle intent, malformed top-level input, correlated capacity loss, unsafe requeue preconditions, duplicate-writer protection, and per-task result aggregation.

The Slurm guard tests execute the actual Markdown function with mocked commands. The practicum tests execute the actual checkpoint application with mocked host identities. Neither contacts a native Slurm service or establishes two-host execution.

## CLI and shell evidence

Authors and independent reviewers also ran ordinary command-line workflows, separate from the unit tests:

- All six systems scenarios: initial check failed with exit 1, configured recovery and healthy controls passed with exit 0, and reset restored the original failure. The small training application resumed from published step 20 after interruption at 23 and matched the uninterrupted step-40 result. Corrupt checkpoint input was rejected with exit 2. See [systems verification](../labs/systems/verification.md).
- Platform checkpoint application: an injected exit 75 at step 5 was followed by a separate process resuming from 5 and returning exit 0 with the correct result 650. A changed target rejected the old checkpoint. See [platform validation](../labs/platforms/VALIDATION.md).
- Fleet CLI: stale/missing observations, failed qualification, and deficient capacity were detected; corrected inputs produced the intended valid states. See [fleet transcript](../labs/fleet/validation-transcript.txt).
- Two-host runbook control flow: the author exercised fourteen mocked cases across Bash and zsh, and the independent reviewer exercised six selected cases. Failed setup, existing evidence, invalid/duplicate phases, changed configuration, and expected exit-75 handling were checked. See [shell-check record](../practicum/l2-shell-validation.txt) and [the independent fleet review](fleet-teaching-review.md). These are overlapping checks, not a count of distinct native scenarios.

## Course structure and static checks

`python3 tools/validate_course.py` passed. It checks 24 ordered months, 96 unique scheduled weeks, the 70/18/8 week allocation, 48 unique outcomes, six bundles per gate, both platform paths, four specialties, capstone/key presence, required source-record fields, unique source identifiers, and local Markdown file-link targets. It does not prove prose quality or validate remote URLs or link fragments.

The final source ledgers contain 94 records. Their access dates, version scopes, supported claims, and limitations are explicit. Authors verified cited sources; independent reviewers revisited selected claims. This is not an independent full audit of every sentence of every source.

The coordinator also checked:

- Twelve Python files using AST parsing.
- Nineteen JSON files using JSON parsing.
- Ten YAML documents using the available PyYAML parser.
- Three shell/batch files using `bash -n`.
- Source-text trailing whitespace and final newlines, plus `git diff --check`.
- Active course areas for unresolved TODO, TBD, FIXME, and coming-soon markers: no matches.

YAML parsing and static object checks are not API-server acceptance. Shell parsing is not runtime validation. Historical planning documents are explicitly superseded; their old unchecked planning tasks are not unfinished course-delivery requirements.

## Independent instructional acceptance

All 30 lesson chapters were read by an agent other than their author. The reviewers evaluated explanation quality, prerequisite flow, worked calculations, contrasting cases, answer keys, scenario solvability, and fidelity limits. Review reports record full scope and the targeted primary sources rechecked.

| Review | Final disposition | Evidence |
|---|---|---|
| Seven systems lessons and root learner route | Accepted after source-version correction | [Systems/route review](systems-and-route-review.md) |
| Eleven platform lessons and reference procedures | No open blocking findings after corrections | [Platform review](platform-teaching-review.md) |
| Twelve fleet/practicum lessons, four specialties, six keys, three capstones | Accepted after five findings were corrected and rechecked | [Fleet/practicum review](fleet-teaching-review.md) |

Real defects were retained in the review history. These included a Slurm sequence that could continue after a failed prerequisite, unsupported plugin terminology, missing prerequisite definitions, mixed NCCL page versions, an incomplete two-node procedure, absent initial scenario evidence, and prematurely revealed scenario answers. The fleet CLI's malformed-input traceback was also reproduced and corrected with a regression test. Passing tests were not used as a substitute for instructional review.

## Unrun native and physical environments

| Environment | Status and reason |
|---|---|
| Native Kubernetes | **NOT_RUN.** Matching pinned tools could not be downloaded within the bounded attempt. No course cluster was created, and no existing kubeconfig context or workload was changed. |
| Native Slurm | **NOT_RUN.** Required binaries and an appropriate Linux environment were unavailable; no daemon or accounting database was configured. |
| CUDA/GPU | **NOT_RUN.** The optional path reported that an already installed, approved PyTorch environment is required. No physical GPU evidence was produced. |
| Native two-host CPU recovery | **NOT_RUN.** The complete procedure requires two owner-provisioned compute hosts. Local mocks validate the recorder/control flow only. |
| Physical RDMA and supervised rack work | **NOT_RUN.** No appropriate authorized hardware session was performed. |

The Kubernetes setup failures were recorded as:

```text
kind: curl (28), timeout after 60002 ms, 540663 of 10624850 bytes received
kubectl: curl (28), timeout after 60006 ms, 753339 of 59775314 bytes received
```

The original download process was stopped, and partial downloads were left nonexecutable with `.part` suffixes. The [platform report](../labs/platforms/VALIDATION.md) records the exact environment, pins, and boundaries. An unavailable native environment is an unrun validation, not a passing result and not a missing authored lesson.

## Remaining evidence boundaries

No learner pilot, longitudinal management assessment, production-readiness review, vendor-support approval, or public-release approval was performed. Estimated pacing remains provisional. Learners must produce and defend their own evidence using [the assessment gates](../assessments/gates.md), including actual native and hardware observations for the outcomes that require them.
