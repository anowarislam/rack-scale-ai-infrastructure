# Month 21 instructor key - sealed by convention

Synthetic ground truth: the initial lifecycle sequence fails telemetry qualification at generation 4. The signal excerpt has an old boot and missing node. The first offered checkpoint is incomplete. Clearing the failure field would conceal the problem.

| Time | Inject | Expected handling |
|---|---|---|
| 15 min | A step-450 directory exists, but one shard lacks a committed manifest; step 400 is complete | Use validated step 400 unless a supported completion path is proved |
| 30 min | All processes run after restart, but the workload result differs from the baseline because optimizer state was not restored | Reopen recovery; running is not correctness |
| 50 min | A complete checkpoint restores correct output; current telemetry now matches both asset incarnations | Create new qualification evidence and promote only after all invariants hold |

Reference local recovery is lifecycle-recovered.json: quarantine at generation 5, authorized repair at 6, requalification at 7, checks accepted at 8, promotion at 9. The original failed check remains. Learners can choose a different legal path if they defend its policy and provide tests; changing expected_final merely to make the wrong result PASS is not valid.

Fault-free control: lifecycle-healthy.json reaches available generation 6 and signal-healthy.json passes. The listed healthy sequence includes its planned repair cycle; it does not need an extra repair or quarantine beyond that sequence. Decoys are the newest directory and the running-process dashboard. Do not demand a failure diagnosis from a fault-free control.

Answers: checkpoint completeness includes all required state and a commit criterion; recovery time can include detection, scheduling, initialization, state restore, and replay; current evidence matches identity/configuration generation and observation window; L0 supports modeled recovery semantics, not observed multi-node recovery.

Grade hidden-health and reset independently from speed. L2 evidence must identify at least two actual participating nodes, workload correctness, native fault/recovery records, and the approved scope. Without it, keep that outcome pending at L2 while accepting the L0 practice result. Remediation changes the hidden failure to duplicated output after a retry; require a new postcondition rather than repeating the optimizer-state answer.
