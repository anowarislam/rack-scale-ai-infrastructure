# Month 12: Defend the allocation-to-result evidence chain

Your decision is whether the built reference satisfies its contract, which operating mechanisms are active, and where evidence stops. This chapter prepares **G2-E06 / G2-O11 and G2-O12**. It consolidates the prior six-month work into one operational handoff and comparison, without adding more assessed bundles.

## A platform result is a chain of identified observations

For each submitted job, retain immutable application/input identity, submission options, Job ID, attempt count, allocation and steps, node list, relevant timestamps, exit information, checkpoint generation, application correctness, and available accounting/completion fields. Missing a link limits the question you can answer.

For example, `squeue` is useful for current work but a completed job may no longer appear. A local application log can prove a result but not all scheduler decisions. SlurmDBD-backed `sacct` can expose retained job/step records when configured, but its fields and collection depend on the environment. See [sacct](https://slurm.schedmd.com/sacct.html) and [accounting](https://slurm.schedmd.com/accounting.html). Record field availability instead of filling gaps with inferred precision.

An operational handoff includes what to do when the chain breaks: how to find the owning job and attempt, distinguish infrastructure from application failures, stop a harmful retry, preserve state, choose recovery, and prove the final result. The audience should be able to act without your conversation history.

## Worked example 1: Allocated CPU time, elapsed time, and CPU consumption

A job is allocated 8 CPUs for 30 minutes. Allocated CPU time is `8 * 30 = 240 CPU-minutes`, or 4 CPU-hours. If its processes collectively consume 60 CPU-minutes of actual CPU time, the ratio to allocation is `60 / 240 = 25%`. That does not immediately prove wasted allocation: the job might be intentionally I/O-bound, waiting on a GPU, or blocked by a fault.

Now suppose the application completes 120 valid batches in those 30 minutes. End-to-end goodput is `120 / 1,800 = 0.0667 batches/s`. Cutting CPU allocation in half might save allocated CPU-hours if goodput stays constant; it might also lengthen preprocessing and reduce GPU progress. The intervention requires a controlled comparison with identical inputs and correctness checks.

In a full accounting profile, compare allocation fields, elapsed time, and collected CPU consumption while distinguishing job and step rows. In the base profile, do not invent TotalCPU from elapsed time: allocated CPUs multiplied by elapsed time is a reservation measure, not observed consumption. Label the absent measurement.

## Worked example 2: Recovery can improve while queue experience worsens

Assume a job originally ran for 60 minutes and lost 20 minutes of work on failure. A checkpoint change reduces lost work to 2 minutes but adds 4 minutes of checkpoint overhead per run. Under the same failure event, computation saved is `20 - 2 = 18 minutes`; subtracting the 4-minute overhead gives a 14-minute improvement before considering changed queue or storage effects.

Now suppose the policy requeues interrupted jobs at a service class that waits an additional 25 minutes. End-to-end completion can still be 11 minutes worse than the original comparison: `25 - 14 = 11`. This is a constructed example, not an endorsement of that policy. It shows why recovery time includes queueing, and why application checkpoint tuning and scheduling policy must be evaluated together.

Do not hide the tradeoff by reporting only restore duration. Include lost work, checkpoint overhead, queue delay, elapsed completion, correctness, and the fairness effect on other users. A policy that makes one learner's job faster by starving every other job is not automatically a platform improvement.

## Comparison that respects native semantics

| Decision dimension | Slurm reference evidence | Kubernetes comparison |
|---|---|---|
| Execution shape | Allocation plus batch/application steps | Pod placement plus workload-controller intent |
| Coordination | Multi-node allocation does not prove framework rendezvous | Multiple created Pods do not prove atomic group admission |
| Fairness | Active priority plugin; database prerequisites for fair share | Namespace caps/priority plus chosen queue integration |
| Identity | Linux identity, MUNGE, filesystem and account association | API identity/RBAC, admission, runtime/data identity |
| Recovery | Requeued batch begins again; application restores | Replacement Pod runs again; application restores |
| History | Current queue, completion log, or configured SlurmDBD | Explicit event/metric/audit/accounting retention design |
| Change | Version-specific RPC/state/database compatibility | Component skew plus integration compatibility |

This table is a set of questions to answer with your actual configurations. It is not proof of every feature in a product family. See the [Kubernetes reference track](../kubernetes/README.md) and source links at each relevant mechanism.

Counterexample: "Slurm has accounting, therefore our VM has historical fair-share evidence." The product supports a mechanism; your profile does not enable it. The equally flawed Kubernetes claim would be "NetworkPolicy exists, therefore these packets were denied." Active configuration and observed behavior close that gap.

## Integrate, defend, and clean up

Assemble the six G2 bundles with an index mapping each outcome to the relevant evidence. Your primary handoff must state the exact source commit and build environment, configuration, native successful job, pending/release trace, requeue/restore trace, bounded isolation test, observability limits, upgrade/recovery plan, and cleanup state. The secondary minimum must include its actual workload, scheduling analysis, failure recovery, evidence/accounting review, and comparison memo.

Defend two variations: a job asks for more nodes than exist in the partition, and a checkpoint is valid JSON but belongs to another target. Predict whether submission, placement, launch, or application validation rejects the request. Consult native documentation where policy changes the answer; an honest conditional answer is stronger than a guessed universal behavior.

Use the runbook's exact-Job-ID cleanup and stop only the course daemons in the dedicated VM. Preserve evidence outside the VM before disposing of it. Never use `scancel -u` against a shared system merely to clean a learning exercise.

## Four-week combined plan

| Week | Primary 5 h | Secondary 2 h | Evidence/review 1-3 h |
|---|---|---|---|
| 1 | Reconstruct identified allocation-to-result history | Close secondary native evidence gaps | Mark absent fields and scope |
| 2 | Work allocation/goodput/recovery calculations | Compare accounting semantics | Verify denominators and tradeoffs |
| 3 | Rehearse operational handoff | Defend platform comparison | Peer challenges and corrections |
| 4 | Remediate and defend integration | Explain unsupported cross-platform claims | G2 decision and cleanup |

## Questions

1. Why does allocated CPU time differ from consumed CPU time?
2. Why can better checkpoints worsen end-to-end completion in the example?
3. Can a product feature list replace evidence of your active profile?
4. What remains incomplete if Kubernetes primary is demonstrated but Slurm secondary was only simulated?
5. What is the correct claim for a written HA plan without a failover run?

<details>
<summary>Reasoned answers</summary>

1. Allocation reserves capacity for a duration; consumption measures actual execution. Waiting or underused resources can create a gap, whose cause must be diagnosed rather than assumed.
2. The saved computation is outweighed by added queue delay. End-to-end measurement includes overhead and policy effects, not just restore speed.
3. No. A feature may be disabled, misconfigured, incompatible, or dependent on absent infrastructure. Inventory and positive/negative tests establish the bounded active behavior.
4. The secondary native workload, scheduling, and recovery requirements remain pending. The model is useful preparation but not native platform evidence.
5. Analyzed or rehearsed recovery design at its stated fidelity, not executed HA. Actual takeover, state consistency, and workload continuity need observed tests in an appropriate environment.

</details>
