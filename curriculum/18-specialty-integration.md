# Month 18: Prove one intervention and hand it over

Your specialty is successful when another operator can understand what changed, reproduce the relevant evidence, and recover safely. It is not successful merely because you explored many technologies. **G3-E06** assesses **G3-O11**, one bounded specialty intervention, and **G3-O12**, operationalizing it and proposing a role-family capstone. All other G3 outcomes must already have evidence or recorded remediation.

## Choose a narrow causal question

Select one of the [four specialty packets](../specialties/README.md). Each offers one defined intervention:

| Lane | Intervention | Primary measured outcome |
|---|---|---|
| Rack lifecycle | Gate promotion on current, complete qualification evidence | Unsafe promotions under supplied fault cases |
| Performance | Stagger one workload's checkpoint starts | Useful work per elapsed time and checkpoint tail |
| Workload platform | Add one per-tenant aggregate GPU admission cap | Wait time for the declared job class plus harm to others |
| Fleet automation | Bind retry intent and qualification to state generation | Duplicate/stale actions that mutate state |

These are deliberately narrow. Exploring other hypotheses can support your choice; implementing a second intervention would make attribution and the time budget worse. Your chosen packet specifies the minimum fidelity. L0 emulation can demonstrate policy logic but cannot establish physical speed, RDMA behavior, real firmware compatibility, or rack service competence.

The operating sequence is characterize, intervene, validate, recover, operationalize. Characterization establishes what you know before changing anything. Intervention changes one mechanism. Validation checks useful outcomes and side effects. Recovery demonstrates a way back or a justified safe terminal state. Operationalization assigns maintenance and evidence responsibilities.

## Explain the causal chain before measuring the result

A causal chain has a controllable input, a predicted intermediate effect, and a user-relevant outcome. For checkpoint staggering: change start times -> fewer concurrent writes -> less storage contention -> shorter stalls -> more correct training progress per hour. If stalls improve without a change in concurrent writes, the proposed mechanism is not yet demonstrated. If stalls improve but correctness fails, the intervention fails.

Choose guardrails before seeing results. A guardrail is an outcome whose deterioration can veto the primary metric. Examples include checkpoint recoverability, small-job latency, telemetry coverage, or maximum unavailable assets. Do not pick the primary measure after inspecting which number improved.

## Worked example 1: an apparent 20% gain disappears

**Synthetic calculation.** Before an intervention, a test pool completes 100 useful units in 100 seconds: 1 unit/s. Afterward it completes 120 in 100 seconds: 1.2 units/s, apparently a 20% gain. But a contemporaneous unchanged control also moves from 100 to 120 because the input dataset becomes easier. A simple ratio-of-ratios is `(120/100)/(120/100) = 1`: no differential gain is visible.

Now hold workload and time windows comparable. The intervention pool moves from 100 to 126; control moves from 100 to 105. The ratio-of-ratios is `1.26/1.05 = 1.2`, a 20% differential change. That still does not prove causality if pools share a bottleneck or differ in hardware. It makes the question sharper: what mechanism could explain the remaining difference, and what additional paired or reversed trial would distinguish it?

Verified public fact: before/after canary comparisons can be confounded by time, while shared dependencies can affect treatment and control together. A control helps only when its scope and independence are understood. [Canarying Releases](https://sre.google/workbook/canarying-releases/)

**Counterexample.** A tuning change makes the workload skip validation and return wrong results faster. Raw throughput rises but useful work is zero under a correctness requirement. Keep the unit of success explicit.

## Worked example 2: a zero-failure gate can still overclaim

**Synthetic calculation.** A promotion guard is tested with 12 designed cases: four stale checks, three duplicate intents, two incomplete inventories, and three valid promotions. It rejects all nine unsafe cases and accepts all three valid ones. This establishes correct outcomes on those 12 cases. It does not establish a real-world false-negative rate of zero: the cases were selected, not sampled from a known operational distribution.

During a second trial, the guard rejects one valid promotion because an unrelated counter updates the resource generation. Safety behavior is conservative, but the availability cost is real. The better next step may be to bind qualification to the relevant immutable configuration identity rather than every volatile field. That redesign would need new tests; do not silently broaden this month's intervention.

An honest result is: "The guard prevented all nine designed unsafe promotions and allowed three valid cases; one additional benign-version-change case was conservatively blocked. Measured effect on production admission delay remains unknown." You can defend that statement because each clause points to evidence.

**Counterexample.** Removing the version check makes the benign case pass but also permits stale qualification. Improving the acceptance count by weakening the invariant is not an acceptable recovery.

## Build the handoff while the experiment is small

Your operating note should answer: who owns it, what inputs it trusts, where outputs are observed, which exact configuration was tested, what makes evidence stale, what stops expansion, and how to recover. Include a negative test. Someone taking over should be able to show that the detector still notices a lost source or a stale request, not merely rerun a successful path.

A runbook handles a known situation with concrete preconditions and postconditions. An investigation guide handles uncertainty with competing hypotheses and discriminating observations. Keep the difference visible. A runbook saying "if unhealthy, investigate and fix" transfers no operational knowledge.

## Your G3-E06 submission

1. Read the selected specialty packet and write its single intervention in one sentence. State the fidelity and exact claim it could establish.
2. Complete a baseline and the packet's fault-free control. Predict intermediate and final outcomes before the intervention.
3. Run the bounded change, retain raw evidence, and analyze correctness and guardrails alongside the primary measure.
4. Recover or reset; demonstrate the final postconditions and reintroduce one relevant fault to test detection.
5. Hand the package to a peer. Ask them to execute the local validation without oral help. Record where the handoff failed and repair it.
6. Propose one [role-family capstone](../practicum/capstones/README.md) that reuses this technical anchor during months 19-24. Include a decision, stakeholders, success evidence, exclusions, and a fallback when hardware access is unavailable.

Use [the evidence template](../assessments/evidence-template.md). This single assessment integrates the specialty; it does not add another gate. A failed experiment can support a strong learning result when diagnosis, safe recovery, and the bounded conclusion are correct. It cannot support an improvement claim that did not occur.

## How to state the result

| Evidence you actually have | Permitted statement | Statement to withhold |
|---|---|---|
| L0 synthetic event replay | This implementation enforced the tested logical guards | This rack is safe to update |
| L1 single-device trial | This workload behaved this way on this device/software tuple | Multi-node scaling improved |
| L2 recorded multi-node trial | This topology/workload recovered under this controlled failure | Every fleet topology is resilient |
| L3 supervised approved procedure | Named role performed or observed this procedure on the recorded BOM | Independent physical service competence without assessment |

Executed, observed, simulated, and analyzed are different verbs. For leadership, course-observed incident decisions can be assessed here. Sustained coaching, succession, and organizational design remain workplace-evidenced or transfer objectives.

## Questions

1. Why must a specialty intervention be narrower than its technology lane?
2. What does a treatment/control ratio-of-ratios near one suggest, and what does it not prove?
3. Why do 12 designed test cases not establish a population failure probability?
4. How can a safety guard succeed and still require operational improvement?
5. What distinguishes operationalization from writing a runbook?

## Reasoned answers

1. A narrow change makes mechanism, measurement, recovery, and attribution feasible within the course budget. The lane defines context; it is not permission to redesign the entire system.
2. The observed changes are similar after normalization. It does not prove no possible effect: contamination, noise, or inadequate comparison can conceal one.
3. They were selected to cover mechanisms, not drawn independently from a defined distribution. Coverage and statistical prevalence are different claims.
4. It can correctly prevent unsafe admission while blocking benign cases or increasing toil. Measure those costs without removing the safety invariant to improve a score.
5. A maintained owner, working signals, tested recovery, freshness triggers, and an independently usable handoff. A document can exist while every one of those is absent.

## Four-week study plan

| Week | Nine-hour allocation | Result |
|---|---|---|
| 1 | Specialty characterization 5h; causal design 2h; prediction 2h | Baseline and intervention contract |
| 2 | Bounded trial 5h; guardrails 2h; recovery 2h | Measured intervention |
| 3 | Independent handoff 4h; capstone proposal 3h; defense 2h | G3-E06 draft |
| 4 | Remediation 4h; G3 integration 3h; archive 2h | G3 decision and practicum entry |

The complete [practicum sequence](../practicum/README.md) begins with inheriting an unfamiliar system, not with adding a second specialty.
