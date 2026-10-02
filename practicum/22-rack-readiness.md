# Month 22: make a rack readiness decision at the right fidelity

**G4-E04: G4-O07 and G4-O08.** Execute an authorized readiness role and reconcile the result with residual risk. Choose supervised L3 when the required environment and qualified people exist. Otherwise use the explicit L2 alternative. An L0 tabletop is preparation, not L2 or L3 execution.

## A rack is a shared failure boundary

A change that seems local can affect a shared fabric, management plane, power domain, or admission pool. Ask not only whether a component passed, but what depended on it and whether the service returned to its promised state. Component tests and integrated workload tests answer different questions.

**Worked example 1.** A teaching pool has five 24-GPU domains. Removing one leaves 96 GPUs. Reserving 25% of the remainder leaves 72, or nine 8-GPU jobs. A promise of ten such jobs is unsupportable during that activity. Demand reduction or additional qualified capacity must precede the change. A planned removal should not be discounted by a guessed low failure probability.

**Worked example 2.** A packet says all ten checks passed. Nine refer to the current configuration; the recovery drill uses the previous software tuple. The correct conclusion is not simply 90% ready, because the stale check may be essential. If stored-state compatibility changed, the recovery path remains unknown. Many green rows cannot offset a missing critical condition.

**Counterexample.** A manager who observes a qualified person's work and correctly evaluates residual risk has evidence of an observed readiness role. That is valuable but is not evidence that the manager performed the service or can do so unsupervised.

## Student scenario

Meridian is onboarding a revised rack configuration. A stakeholder wants it counted toward the next capacity commitment. The following is the complete initial synthetic packet. Configuration labels and evidence IDs are invented; they are not vendor compatibility claims. Your task is to identify what evidence would justify promotion and what limitations may remain.

| Packet field | Initial record |
|---|---|
| Candidate configuration | CFG-B: firmware F1, runtime R2, workload W1 |
| Previous configuration | CFG-A: firmware F1, runtime R1, workload W1 |
| Capacity before maintenance | Four qualified domains of 32 GPUs each; one homogeneous pool |
| Maintenance window | Remove one 32-GPU domain for 90 minutes; no new domain becomes qualified during the window |
| Admission contract | Whole 8-GPU jobs; keep 20% of surviving capacity uncommitted; requested concurrent commitment is 80 GPUs |
| Named roles | Synthetic service lead S, recovery owner R, workload reviewer W; booking confirmation is awaiting the final roster |
| Proposed outcome | Count candidate capacity and approve the bounded maintenance window |

| Checklist entry | Submitted status | Evidence ID and scope |
|---|---|---|
| Inventory and topology reconciliation | Green | EV-101, CFG-B, candidate asset list, observed today |
| Workload output and throughput | Green | EV-102, CFG-B, fixed W1 input and result, observed today |
| Telemetry delivery and identity | Green | EV-103, CFG-B, current-generation collection test, observed today |
| Recovery from committed state | Green | EV-090, CFG-A, restore plus output comparison, observed last month |
| Service and rollback plan | Green | PLAN-7, candidate scope, named roles and stop conditions; roster confirmation pending |

For each row, reviewers are W for EV-102, R for EV-090 and PLAN-7, and S for EV-101 and EV-103. These are submitted attestations to evaluate, not instructions to perform physical work. The verbal assurance is: "The last recovery drill should still apply." No additional compatibility result is initially supplied.

Use Meridian's prior capacity ledger and [Month 17's ORR structure](../curriculum/17-capacity-and-readiness.md). Replace checkmarks with evidence IDs, exact configuration scope, reviewer, and freshness. During a 60-minute review, updates arrive at minutes 15, 30, and 45. Record the decision after each: ready, ready with an explicit bounded condition, or blocked. The [instructor key](instructor/22-key.md) contains the hidden facts and control.

## L3 path: supervised role on an approved rack

Before execution, the environment owner supplies the supported exact BOM, private asset map, qualified service lead, safety/facility ownership, booking and exclusive scope, permitted observations/actions, recovery mode, stop conditions, and return-to-service tests. This packet cannot replace a vendor procedure or supply those approvals.

The learner may reconcile physical labels/topology with approved inventory under supervision; observe a qualified person's approved service or firmware workflow; record prerequisites, task state, and discrepancies; participate in workload qualification; and prepare the handoff. A manager may take the observation and risk-review role. Every entry records who acted and who observed.

Do not reproduce or improvise physical service instructions. The qualified person follows the site's controlled vendor procedure. Stop if configuration identity is uncertain, supervision is absent, evidence collection is lost, or a specified stop condition is reached. The named recovery owner controls any physical recovery.

## L2 fallback: reduced claim, actual multi-node work

Use the previously qualified dedicated multi-node environment. Perform a software-only readiness review for a bounded workload/configuration change: current identity/version reconciliation, admission hold for exercise work, correctness baseline, approved change, workload validation, telemetry-delivery test, and rollback or forward-recovery rehearsal. Reuse the primary platform runbook and [Month 21](21-recovery.md).

No physical service, firmware writes, BMC resets, cabling, power, or thermal manipulation is included. The claim is "executed a software readiness and recovery review on the recorded multi-node environment." It does not establish physical rack topology or vendor-service competence. If only a laptop is available, record L0 preparation and leave the L2 requirement pending.

## NPI closure and evidence

For each discrepancy, create a new-product-introduction record: configuration, expected/observed result, effect on readiness, reproducible evidence, owner, next test, and reopen trigger. Demonstrate one closure by satisfying its original condition. A vendor response without a reproduced result remains a response, not closure.

Submit decision history, configuration/evidence matrix, capacity calculation, actor/fidelity log, a closed finding, residual risks, and reset/return-to-service proof. A conditional decision states what is allowed, for how long, by whose authority, and what triggers withdrawal.

Objective checks: critical evidence matches the current scope; capacity is assessed under planned unavailability; actor labels are accurate; risk is evaluated by consequence rather than checkmark count; the approved final state is independently verified. The common rubric applies.

## Questions

1. Why can an old recovery test be insufficient for a new configuration?
2. Why model planned maintenance deterministically?
3. What does the L2 fallback leave untested?
4. What changes an NPI finding from acknowledged to closed?

## Four-week application plan

Weeks 1-2: 9h/week on readiness theory, capacity, evidence freshness, actor/safety boundaries, and the timed review. Weeks 3-4: 9h/week on the approved L3 role or L2 fallback, closure, handoff, and assessment. Continue to [Month 23](23-portfolio.md).
