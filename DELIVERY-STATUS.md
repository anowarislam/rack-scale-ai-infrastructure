# Course delivery status

Date: 2026-10-02 UTC. **Course authoring and independent content review are complete. The course is ready for self-study.**

The main deliverable is theory with worked examples and reasoned answers. Local and native lab procedures support that learning. Native-platform and physical-hardware execution remain separately recorded below.

## What is delivered

| Area | Delivered state |
|---|---|
| Fundamentals and systems | Bridge plus six systems lessons, worked calculations, questions/answers, six local scenarios, checkpoint workload, and hardware workbook |
| Platforms | Shared workload-contract lesson plus five Kubernetes and five Slurm lessons, primary/secondary routes, examples, local model, and native reference procedures |
| Fleet and reliability | Six lessons covering evidence, time, statistics, incidents, lifecycle, capacity, readiness, and specialty integration |
| Specialty choices | Four bounded interventions; select one |
| Practicum | Six integrated scenario packets, six separate instructor keys, and a concrete two-host CPU recovery procedure |
| Capstones | Three distinct routes: engineer/principal, aspiring leader, manager/director |
| Learner integration | Entry guide, 24-month calendar, four gates, evidence/progress templates, and machine-readable map |
| Source records | 94 scoped primary-source records across three ledgers; citations within lessons |

There are **30 lesson chapters including the bridge and both platform tracks**. One learner follows 24 monthly lessons plus the bridge, with the secondary platform's bounded comparison work. Four gates contain 24 assessed bundles and 48 atomic outcomes. The 96-week calendar contains 70 build/apply weeks, 18 remediation weeks, and eight defense/transfer weeks, plus eight unscheduled break weeks.

## Completed acceptance checks

- [x] Audit the starting repository and resolve its planning-only restriction.
- [x] Complete theory, worked examples, practice questions, and reasoned answers across the course.
- [x] Complete both platform tracks, all specialties, practicum packets, and capstones.
- [x] Integrate the first-session guide, calendar, gates, evidence, and progress records.
- [x] Independently review all 30 lessons, the specialty/capstone paths, and learner integration.
- [x] Correct material findings and have the reviewers recheck them.
- [x] Run final local software, syntax, source-record, mapping, and navigation checks.
- [x] Record unrun environments and distinguish them from authoring completion.

Three GPT Astra agents at maximum reasoning effort authored separate areas and reviewed another author's work. The main agent coordinated scope, integration, acceptance, and independent final checks.

## Verification status

**Observed by the coordinator:** 57 unit tests passed across five suites; all ten YAML documents, twelve Python files, three shell/batch files, and nineteen JSON files passed the recorded syntax checks. The course validator passed calendar accounting, gate mappings, source-record structure, and local file-link targets. Whitespace checks passed. Full evidence and review links are in [validation results](validation/RESULTS.md).

**Independently reviewed:** all lesson chapters, four specialties, three capstone routes, and learner navigation. Corrections included Slurm recovery preconditions and plugin terminology, undefined Kubernetes terms, a source-version mismatch, an incomplete two-host application path, missing scenario data, prematurely revealed scenario facts, and a malformed-input error. The review reports contain the precise findings and their resolutions.

**NOT_RUN:** native Kubernetes and Slurm deployments, actual CUDA/GPU execution, native two-host recovery, physical RDMA, and supervised rack work. The pinned Kubernetes tool downloads timed out; no cluster was created. Slurm and a configured CUDA/PyTorch environment were unavailable. Source/static checks and local mocks do not establish these native results.

**Not yet measured:** actual learner completion times or learning effectiveness in a pilot. Eight to ten hours per scheduled week is a design estimate. Learner progress starts unattempted; authoring and test results are not learner assessment evidence.

## Where the loop came from

Verified starting state in this checkout: a design charter, a plan for a planning package, and `.gitignore`; two commits; no lessons, course entrypoint, or labs. The plan explicitly prohibited chapters and executable labs. The [delivery decision](decisions/0005-deliver-the-course.md) superseded that restriction under the user's current instruction and preserved the useful learning architecture and safety boundaries.

The repository evidence supports that scope mismatch. It does not establish the history of other conversations or other copies of the course. The old documents remain clearly marked as history and are not prerequisite work to repeat.

## Start studying

Open [the learning guide](LEARNING-GUIDE.md), attempt [the bridge diagnostic](curriculum/00-bridge.md), then read [Month 1](curriculum/01-system-map.md). Begin with the theory and examples; run the practical exercise after you can predict its result. Use the [calendar](CALENDAR.md) to continue and [the gates](assessments/gates.md) to decide when to advance.

All changes are saved locally. No Git commit or remote publication was made. Public-release approval, vendor endorsement, certification, and job equivalence are not claimed.
