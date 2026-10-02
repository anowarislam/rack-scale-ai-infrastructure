# Months 19-24: investigate, recover, and defend an unfamiliar fleet

The practicum reuses the mechanisms you have already learned. It adds ambiguity, competing responsibilities, and evidence that changes while you work. It does not add a new survey of technologies. Complete [G3](../assessments/gates.md) first or explicitly record unresolved outcomes.

| Month | Packet | Assessed bundle | Main output |
|---|---|---|---|
| 19 | [Inherit](19-inherit.md) | G4-E01, outcomes O01-O02 | System map, trustworthy baseline, hypothesis tests |
| 20 | [Performance](20-performance.md) | G4-E02, outcomes O03-O04 | Cross-layer diagnosis and validated intervention |
| 21 | [Recovery](21-recovery.md) | G4-E03, outcomes O05-O06 | Recovery, hidden-health checks, reset evidence |
| 22 | [Rack readiness](22-rack-readiness.md) | G4-E04, outcomes O07-O08 | Authorized role evidence and residual risk |
| 23 | [Portfolio](23-portfolio.md) | G4-E05, outcomes O09-O10 | One role-family capstone and follow-through |
| 24 | [Defense](24-defense.md) | G4-E06, outcomes O11-O12 | Reproduction, remediation, bounded transfer plan |

Select one [role-family capstone](capstones/README.md). Its work is accumulated across these six packets, not added as a seventh assessment. Use the [evidence template](../assessments/evidence-template.md) and [common rubric](../assessments/gates.md).

## How a scenario runs

Before beginning, the learner writes an expected result and a minimal evidence request. During the scenario, the instructor releases timed injects. The learner maintains facts, hypotheses, actions, and uncertainty separately. After the scenario, the learner reproduces the result, writes the operating handoff, and faces a changed-input defense.

The instructor materials are **sealed by convention**: they are ordinary readable Markdown, not an access-control boundary. The instructor should keep the key closed during a first attempt. A self-study learner can reveal it afterward, label that attempt key-assisted, and ask a peer to vary the next run. Knowing the hidden answer does not demonstrate independent diagnosis.

All supplied organizations, assets, events, timings, capacities, and business values are synthetic. They are not production incidents or vendor performance data. The evolving fleet is called Meridian. It has an illustrative 128-GPU capacity ledger in four domains; the two-node signal fixture is an explicitly partial record excerpt, not proof of full 128-GPU telemetry coverage.

## Evidence and fidelity

Every artifact records environment, accelerator count/topology, RDMA status, operation risk, actor, support posture, and whether the work was executed, observed, simulated, or analyzed. L0 solves reasoning and logical-transition tasks. L1 supports actual single-node behavior. L2 supports observed multi-node behavior on the recorded topology. L3 supports a supervised authorized rack role on the exact BOM. These are course categories, not certifications.

For months 21 and 22, laptop work is a rehearsal. A missing L2/L3 environment does not prevent study, but it does prevent the corresponding physical claim. Month 22 includes an explicit L2 alternative; it is not equivalent to L3. No scenario authorizes firmware writes, live electrical work, physical faults, production changes, or external messages.

The laptop evaluator is [labs/fleet](../labs/fleet/README.md). Its tests verify supplied software behavior; they do not pass a learner gate. Instructor approval is based on the learner's explanation, actions, and raw evidence, with machine checks for deterministic invariants.

## Time and review

The central 96-week calendar controls course accounting. Months 19-22 each use two two-week application units, at 8-10 hours per week. Months 23-24 use the eight defense and transfer weeks. Timed classroom episodes fit inside these hours; they are not extra months of work.

An observer records decisions and handoffs rather than helping solve the fault. Use two reviewers for consequential leadership scoring or record an adjudication. The reviewer can accept a different technical choice when the evidence, safety boundary, and postconditions are at least as strong as the key. Never average a safety or claim-honesty failure into a passing score.
