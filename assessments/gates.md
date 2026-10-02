# Four gates: what you must demonstrate

Use these gates to decide whether to move on. Reading every page or running the test suite does not pass a learner gate. The software tests check the course's exercises; you must supply your own observations and explanations.

Choose one primary platform, one secondary platform, one specialty, and one role-family capstone. Each gate has six assessed bundles and twelve atomic outcomes. Practice questions and repeated attempts are preparation within those bundles, not additional mandatory assessments.

## Scoring and progression

For each outcome, score diagnosis, action/recovery, verification, and explanation from 0 to 3: 0 means absent or unsupported; 1 means partial and dependent on the key; 2 means independently correct with usable evidence; 3 means correct under changed conditions, including decoys and explicit limitations. A passing outcome scores at least 2 in every applicable dimension. Do not average away a failing outcome.

Separately check claim honesty, safety, authorization, licensing, and evidence handling. A zero in any of these blocks progression for that exercise. A local simulation has no license to trigger a physical experiment. Human judgment is required for causal explanations and leadership decisions; machine checks are required for deterministic state and invariants. Build and Lead claims need both where applicable.

For independent study, self-score first, then use the key. Record key-assisted work as practice. Reattempt with a changed input or a different scenario before claiming independent completion. Use a technically qualified peer for a gate defense. Consequential leadership exercises use two reviewers or a recorded adjudication; self-review alone supports practice, not independently assessed Lead depth.

No course-wide certificate or job-equivalence claim is awarded. Record fidelity per outcome. You may continue studying while a hardware requirement is pending, but do not mark that outcome passed at a higher fidelity.

## G1: Systems, months 1-6

| Bundle | Two outcomes | Evidence and required boundary |
|---|---|---|
| G1-E01 | G1-O01 Map request-to-rack dependencies; G1-O02 bound a fault and its safe experiment | System map, hypotheses, and abort/recovery plan; L0 is sufficient for this reasoning task |
| G1-E02 | G1-O03 reconcile host/management/inventory identity; G1-O04 explain topology and a safe lifecycle change | Reconciliation and NUMA/PCIe placement explanation; synthetic records are labeled |
| G1-E03 | G1-O05 distinguish driver/runtime/device failures; G1-O06 validate a single-GPU workload | Diagnostic packet and actual L1 workload evidence for O06; L0 rehearsal alone leaves O06 pending |
| G1-E04 | G1-O07 distinguish scale-up, scale-out, and storage bottlenecks; G1-O08 verify a committed recoverable checkpoint | Units and bottleneck calculation plus checkpoint invariant; physical RDMA claims require physical RDMA evidence |
| G1-E05 | G1-O09 detect misleading telemetry and timing; G1-O10 apply power, thermal, and access boundaries | Signal-health check and bounded security/safety decision; no physical manipulation |
| G1-E06 | G1-O11 compare throughput, goodput, latency, and correctness; G1-O12 recover and verify an integrated workload | Failure/recovery evidence including real L1 work for the gate's workload claim |

## G2: Platforms, months 7-12

| Bundle | Two outcomes | Evidence and required boundary |
|---|---|---|
| G2-E01 | G2-O01 specify workload resource/recovery needs; G2-O02 translate them into native platform semantics | Platform-neutral contract and explicit Kubernetes/Slurm differences |
| G2-E02 | G2-O03 construct a primary reference environment; G2-O04 run a secondary representative workload | Exact versions, construction record, workload outputs on both native platforms; a queue simulation is preparation |
| G2-E03 | G2-O05 diagnose primary placement/fairness; G2-O06 analyze secondary scheduling/admission | Pending-work experiment and native decision evidence |
| G2-E04 | G2-O07 recover primary workload state correctly; G2-O08 recover a secondary failure | Interrupted and recovered results, checkpoint integrity, duplicate-work analysis |
| G2-E05 | G2-O09 verify isolation/observability; G2-O10 defend upgrade and control-plane recovery | Access-denial test, signal check, compatibility and recovery procedure; distinguish rehearsed from executed HA |
| G2-E06 | G2-O11 integrate primary operation and evidence; G2-O12 compare both platforms using observed behavior | Primary defense plus secondary accounting/evidence review and comparison memo |

The secondary minimum is all five of: representative workload, native scheduling/admission analysis, failure/recovery, accounting or evidence review, and comparison memo. Kubernetes and Slurm are not substitutes for each other's evidence. Build depth requires an actual primary platform, not just L0 simulation. A one-node CPU environment establishes only the topology and workload class actually exercised.

## G3: Fleet and specialty, months 13-18

| Bundle | Two outcomes | Evidence and required boundary |
|---|---|---|
| G3-E01 | G3-O01 reconcile authoritative fleet state; G3-O02 verify telemetry freshness and time | Conflicting-source decision, freshness test, and residual uncertainty |
| G3-E02 | G3-O03 calculate exposure-normalized reliability; G3-O04 interpret uncertainty and alert quality | Reproducible calculations with denominators, assumptions, censoring, and base rates |
| G3-E03 | G3-O05 lead a bounded incident role; G3-O06 select and verify a change/recovery mode | Timeline, owner decisions, communications, and postconditions; simulated leadership labeled |
| G3-E04 | G3-O07 implement safe lifecycle transitions; G3-O08 reject stale or duplicate unsafe actions | State-machine evidence and failure tests, including concurrency/identity limits |
| G3-E05 | G3-O09 size capacity under loss and headroom; G3-O10 close readiness/NPI findings | Capacity model, bottleneck assumptions, owner/stop conditions, and closure evidence |
| G3-E06 | G3-O11 validate one bounded specialty intervention; G3-O12 operationalize it and propose a capstone | Before/after comparison, recovery, handoff, and causal limitations; actual environment required for a physical intervention claim |

## G4: Practicum, months 19-24

| Bundle | Two outcomes | Evidence and required boundary |
|---|---|---|
| G4-E01 | G4-O01 reconstruct an unfamiliar system; G4-O02 state evidence gaps and discriminate hypotheses | Inherited-system map and prioritized experiment plan |
| G4-E02 | G4-O03 diagnose a cross-layer regression; G4-O04 validate a measurable improvement | Controlled comparison with correctness and uncertainty |
| G4-E03 | G4-O05 recover a compound failure; G4-O06 prove hidden health and reset | Actual L2 exercise for multi-node recovery claim; tabletop result remains L0 |
| G4-E04 | G4-O07 execute an authorized readiness/serviceability role; G4-O08 reconcile outcome and residual risk | Supervised L3 evidence, or an explicitly reduced L2 alternative; never imply physical service from a tabletop |
| G4-E05 | G4-O09 defend a role-family decision; G4-O10 demonstrate follow-through under changed evidence | Capstone artifact, inject responses, owners, and closure; no claim of longitudinal management competence |
| G4-E06 | G4-O11 reproduce and defend the portfolio; G4-O12 close remediation and define transfer | Reproduction record, reviewer challenges, limitations, and specific workplace experiments |

The [two-host CPU recovery route](../practicum/l2-recovery-runbook.md) supplies a concrete G4-E03 exercise using the Slurm Run/compare skills taught to both primary-platform routes. It requires an owner-provisioned two-host environment. Multiple container nodes on one laptop remain a local rehearsal. The exercise demonstrates recovery of independent replicated tasks, not collective training, physical RDMA, or host-loss recovery.

## Reassessment

Keep the failed attempt. Name the missing invariant or reasoning step, return to the linked lesson, rerun a small discriminating experiment, and defend a new attempt. A different-looking document with the same untested assertion is not remediation. Use the reserved weeks before adding scope.

Use [the evidence template](evidence-template.md) for each bundle and [the progress template](progress-template.md) to track the four gates. The complete study sequence is in [the course map](../course-map.json).
