# Month 9: Queue policy, allocation shape, and useful backfill

The problem is to explain why a job waits even when a cluster looks idle, and when allowing later work to run helps rather than harms service. This prepares **G2-E03 / G2-O05 and G2-O06**. Prerequisites: job allocations, steps, partitions, and the month 7 contract.

## Policy and feasibility have different jobs

The controller evaluates resource requests against eligible nodes, partition rules, reservations, and configured limits. The selected plugins determine placement and priority behavior. **GRES** names generic resources such as GPUs on nodes; **TRES** provides trackable resource dimensions used in allocation/accounting policies. A resource being counted does not prove its runtime isolation or application use. See [GRES scheduling](https://slurm.schedmd.com/gres.html).

**QOS** can express service classes and limits. **Associations** relate a cluster, account, user, and optionally partition to policy/accounting state. **Multifactor priority** combines configured factors; fair-share can reflect past resource consumption against entitlement when its database prerequisites exist. A high priority does not override every feasibility or association limit. The [priority guide](https://slurm.schedmd.com/priority_multifactor.html) explicitly requires the accounting database for the fair-share factor.

**Backfill** considers whether a lower-priority job can run without delaying expected starts of higher-priority jobs. Requested time limits affect that prediction. This is why honest runtime estimates matter operationally. It is not a promise that every short job always jumps the queue. See [scheduling configuration](https://slurm.schedmd.com/sched_config.html).

## Worked example 1: Why a short job fits the gap

Imagine four nodes. Higher-priority job A needs all four for one hour. Two nodes are occupied for another 20 minutes, so A cannot start until then. Job B needs one of the currently idle nodes for 10 minutes. Under these simplified conditions, B can finish before A's expected start, so backfilling B does not delay A.

Now let B request 45 minutes. Starting it could retain a node beyond A's expected start at minute 20. Backfill may leave B waiting even if its author believes it "usually finishes in ten." The scheduler sees the declared time and current policy, not that unverified belief.

Finally, suppose B requests 10 minutes but actually requires 30. Under a finite time limit, B risks termination before producing a result. Making requests artificially short can raise apparent starts while lowering useful completions. Improve runtime estimates using observed distributions and checkpoint capability; do not game one metric.

## Worked example 2: Fair share is not an equal-start rule

Two projects, A and B, have equal nominal entitlement. Over the relevant history A used 800 CPU-hours and B used 200. A configured fair-share factor may increase the relative priority of B's waiting work, but exact priority depends on the algorithm, decay, hierarchy, weights, age, QOS, and other factors. You cannot derive an exact ordering from those two numbers alone.

Even if B has higher priority, a 64-node B job cannot fit while only eight eligible nodes are free. A lower-priority two-node A job may fit a permitted backfill gap. Seeing A start first does not by itself prove that fair share is broken. Inspect the job's constraints, limits, priority components, expected start, and available shape.

The supplied VM has `PriorityType=priority/basic` and no database. Therefore its queue experiment does not demonstrate historical fair share. The intended lesson is to state what is active and refuse to infer an absent mechanism. An optional database exercise in the runbook supplies the additional prerequisites.

## The gang-scheduling false friend

Slurm's documented **GANG** mode time-slices jobs using suspend/resume behavior. It is not the name for merely allocating several nodes to a batch job. Multiple resident jobs must also fit memory, and suspension does not erase application state. See [Slurm gang scheduling](https://slurm.schedmd.com/gang_scheduling.html).

In Kubernetes discussions, gang scheduling often describes admitting related Pods together so a partial group does not strand resources. The month 7 all-or-nothing model illustrates that admission concern. Do not claim Slurm GANG is a drop-in solution to it. A Slurm multi-node allocation and the application launch inside it should be analyzed directly.

Topology is another separate constraint. Slurm topology plugins can describe network relationships and influence allocation. The [topology guide](https://slurm.schedmd.com/topology.html) distinguishes supported models. A one-node VM cannot validate switch-aware placement. Nor does a configured graph prove real link speed, congestion, or collective performance.

## Native queue experiment

In the guarded VM runbook, submit `hold.sbatch`, wait until it owns the node, then submit `job.sbatch`. The first job requests exclusive node allocation. The second should wait while no eligible allocation is free; inspect its actual reason with `squeue` and `scontrol show job`. Cancel only the recorded hold Job ID. Observe the second job progress to execution and verify its result.

Do not assert a universal exact reason string: scheduler timing can expose `Priority` or `Resources` at different points. The explanation must use the complete resource/configuration evidence. The experiment demonstrates contention and release, not a statistically measured fair-share policy or backfill optimization.

Primary Build work: derive the two worked examples and propose one bounded policy change with its tradeoff. Secondary Run work: reproduce pending-to-running evidence and compare it with Kubernetes quota rejection and Pod filtering.

Counterexample: changing a node's configured GPU count from four to eight can make accounting look larger, but it cannot create four physical GPUs. GRES detection and inventory reconciliation prevent a bookkeeping change from masquerading as capacity.

## Four-week combined plan

| Week | Primary 5 h | Secondary 2 h | Evidence/review 1-3 h |
|---|---|---|---|
| 1 | Solve backfill and feasibility examples | Analyze Pod-level feasibility | Separate shape from total capacity |
| 2 | Run hold/pending/release experiment | Run counterpart pending experiment | Preserve actual reason transitions |
| 3 | Explain associations/QOS/fair-share prerequisites | Compare quota and priority | State which mechanisms are absent |
| 4 | Defend topology and gang distinctions | Review other platform's tradeoffs | G2-E03 and remediation |

## Questions

1. Why can a 10-minute job backfill when a 45-minute one cannot?
2. Does a higher fair-share factor guarantee the next start?
3. Does the reference VM demonstrate fair-share accounting?
4. What does Slurm's GANG mode mean?
5. Does configuring GRES prove device isolation?

<details>
<summary>Reasoned answers</summary>

1. In the example, a 10-minute run ends before the higher-priority reservation begins, whereas 45 minutes overlaps it. The decision depends on requested limits and the actual resource plan.
2. No. Other priority factors, limits, and feasibility still matter; backfill may start smaller work without harming the higher-priority job's expected start.
3. No. Basic priority and absent SlurmDBD are explicit limitations. Current-state and completion records are useful but are not historical entitlement accounting.
4. Time-slicing jobs through suspension/resumption. It is distinct from coordinated admission of several Kubernetes Pods and from simply requesting a multi-node allocation.
5. No. GRES describes resources and allocation. Runtime access enforcement needs the configured isolation mechanisms and an actual unauthorized-device-access test on the hardware.

</details>
