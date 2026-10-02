# The 24-month study calendar

Follow the sequence at your own pace. Each row contains four scheduled course weeks; month labels organize dependencies rather than demand a particular start date. Reserve eight additional break weeks wherever your real calendar needs them. Bridge work is additional and diagnostic-dependent.

## The core: months 1-18

For every month in this table, week 1 explains and models the mechanism; week 2 applies it; week 3 introduces failure, recovery, or a harder decision; week 4 validates evidence and remediates gaps. A mandatory teaching unit therefore occupies at most three active weeks. The lesson supplies the detailed weekly tasks.

| Month / weeks | Study and practice | Evidence bundle |
|---|---|---|
| 1 / 1-4 | [System map and safe experiments](curriculum/01-system-map.md) | G1-E01 |
| 2 / 5-8 | [Server topology, identity, and control](curriculum/02-server-control.md) | G1-E02 |
| 3 / 9-12 | [GPU and runtime boundaries](curriculum/03-gpu-runtime.md) | G1-E03 |
| 4 / 13-16 | [Fabric, collectives, storage, and checkpointing](curriculum/04-fabric-storage.md) | G1-E04 |
| 5 / 17-20 | [Power, telemetry, time, and security](curriculum/05-power-telemetry-security.md) | G1-E05 |
| 6 / 21-24 | [Integrated workloads](curriculum/06-workloads.md) and G1 defense | G1-E06 |
| 7 / 25-28 | [Shared workload contract](curriculum/07-workload-contract.md) | G2-E01 |
| 8 / 29-32 | Primary platform construction and secondary first workload | G2-E02 |
| 9 / 33-36 | Scheduling, placement, topology, and fairness | G2-E03 |
| 10 / 37-40 | Workload lifecycle, checkpoint, and recovery | G2-E04 |
| 11 / 41-44 | Isolation, observability, upgrade, and control-plane recovery | G2-E05 |
| 12 / 45-48 | Platform integration, secondary comparison, and G2 defense | G2-E06 |
| 13 / 49-52 | [Fleet truth and time](curriculum/13-fleet-truth.md) | G3-E01 |
| 14 / 53-56 | [Reliability and uncertainty](curriculum/14-reliability.md) | G3-E02 |
| 15 / 57-60 | [Incident response and change](curriculum/15-incidents-and-change.md) | G3-E03 |
| 16 / 61-64 | [Lifecycle automation](curriculum/16-lifecycle-automation.md) | G3-E04 |
| 17 / 65-68 | [Capacity and readiness](curriculum/17-capacity-and-readiness.md) | G3-E05 |
| 18 / 69-72 | [Specialty integration](curriculum/18-specialty-integration.md) and G3 defense | G3-E06 |

For months 8-12, use the [Kubernetes track](tracks/kubernetes/README.md) or [Slurm track](tracks/slurm/README.md) as primary and the other as secondary. Their combined work must fit the weekly budget. Read the secondary package, not a second full Build route.

## The spiral: months 19-24

The first four months apply previously learned mechanisms. Each month has two bounded units of two weeks: reconstruct/diagnose, then intervene/verify. The fourth week is an applied replay or defense of that month's experiment. It is counted as application, not as an additional reserved remediation week. If remediation is needed, repeat or substitute that work; do not increase the compulsory budget.

| Month / weeks | First two weeks | Second two weeks | Evidence bundle |
|---|---|---|---|
| 19 / 73-76 | [Inherit and baseline](practicum/19-inherit.md): reconstruct an unfamiliar system | Distinguish evidence from guesses; defend the experiment plan | G4-E01 |
| 20 / 77-80 | [Cross-layer performance](practicum/20-performance.md): diagnose the regression | Measure a controlled intervention and replay against a decoy | G4-E02 |
| 21 / 81-84 | [Compound recovery](practicum/21-recovery.md): isolate and recover | Prove hidden health, reset, and repeat in the available environment | G4-E03 |
| 22 / 85-88 | [Rack readiness](practicum/22-rack-readiness.md): authorized role and evidence review | Supervised work or explicit reduced-fidelity alternative; close findings | G4-E04 |
| 23 / 89-92 | [Portfolio decision](practicum/23-portfolio.md): defend the selected role capstone | Respond to changed evidence and show follow-through | G4-E05 |
| 24 / 93-96 | [Final defense](practicum/24-defense.md): reproduce and answer challenges | Close remediation and prepare workplace transfer | G4-E06 |

## Budget check

- Months 1-18: 54 build/apply weeks and 18 validation/remediation weeks.
- Months 19-22: 16 application weeks, with no new survey domains.
- Months 23-24: 8 capstone defense/transfer weeks.
- Total: 70 build/apply + 18 validation/remediation + 8 defense/transfer = 96 scheduled weeks.
- At 8-10 hours per scheduled week: 768-960 core hours, plus bridge work and eight unscheduled break weeks.

Hardware waiting time is not evidence of learning. Plan access early, use lower-fidelity work to keep studying, and retain pending higher-fidelity outcomes in the [progress record](assessments/progress-template.md). The [machine-readable map](course-map.json) and [gates](assessments/gates.md) are the corresponding checklist.
