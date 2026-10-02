# Month 21: recover the workload, then prove hidden health

**G4-E03: G4-O05 and G4-O06.** Recover a compound failure, verify the less visible postconditions, and leave a reusable environment. The local scenario is L0 rehearsal. The multi-node recovery outcome requires an actual authorized L2 run; a narrative or JSON result cannot replace that evidence.

## Why process recovery is not workload recovery

A restarted process may have lost optimizer state, resumed from an incomplete checkpoint, duplicated externally visible work, or joined the wrong allocation. Recovery is complete only when the workload's required state and service invariants hold again.

**Worked example 1.** A job last committed all checkpoint shards at step 200. A partial step-250 directory exists when a worker fails at step 280. Restarting from 250 because its filename is newer risks missing state. Restarting from the validated step-200 checkpoint repeats 80 steps. If each step takes 0.2 seconds and initialization takes 12 seconds, regaining previous progress takes `80*.2 + 12 = 28 seconds`, excluding scheduling delay. That is the cost to compare against a valid alternative.

**Worked example 2.** At recovery minute 5, all workers report running, but a current telemetry sample is absent on one node. At minute 6, a stale success record from before repair arrives. The process-state check passes; the observability and qualification checks do not. Promotion should remain blocked until current evidence is tied to the recovered generation.

**Counterexample.** A stateless task whose result is idempotently keyed may safely repeat work. A task that charges, publishes, or appends without deduplication may not. You must know the workload's external side effects rather than assume every retry is harmless.

## Local student scenario

The affected node has completed repair and is waiting for qualification. Begin with [the lifecycle fault](../labs/fleet/fixtures/lifecycle-fault.json) and [the stale signal excerpt](../labs/fleet/fixtures/signal-fault.json).

```sh
python3 labs/fleet/fleet_lab.py lifecycle labs/fleet/fixtures/lifecycle-fault.json
python3 labs/fleet/fleet_lab.py signal labs/fleet/fixtures/signal-fault.json
```

Before running, predict whether the node should accept work. During a 75-minute episode, the instructor releases facts at minutes 15, 30, and 50. Choose a recovery mode, keep the failed evidence, and build a new event sequence. Do not turn all check booleans true just to reach the target state. Each must correspond to a scenario observation or an actual test.

Your local sequence must reject a duplicate intent, reject a stale generation, retain the original failed qualification, and recover through new checks. Reference healthy/recovered fixtures are available only for the post-attempt comparison. The [key](instructor/21-key.md) supplies hidden defects and a control.

## L2 execution path

Complete the [two-host CPU batch recovery runbook](l2-recovery-runbook.md). The supplied G2 Kubernetes environment has one worker and the supplied Slurm reference has one compute host; neither alone meets this L2 requirement. The advanced runbook reuses the G2 checkpoint application and the Slurm Run/compare skills taught to both primary-platform routes. It requires an owner-provisioned two-host Slurm environment, not Build depth in a second platform. Keep the G2 version and semantics evidence, then record the actual advanced environment separately.

1. Before booking, record the named environment owner, recovery owner, exact topology, exclusive scope, allowed workload-only fault, maintenance window, aborts, and return-to-service checks. Ensure checkpoint state and the test environment can be restored.
2. Capture a healthy baseline on at least two actual participating nodes. Verify the workload correctness oracle and observe collection/delivery health.
3. Under the approved runbook, let one exercise-owned process exit with its built-in fault after a committed checkpoint. Do not power-cycle nodes, modify firmware, disrupt a shared control plane, or manipulate physical links.
4. Detect the failure from user-visible work and the platform's native state. Recover with the selected mode and record actual scheduling, initialization, replay, and total recovery time separately.
5. Check workload correctness, committed state, unique output or documented duplicate handling, node identity, allocation membership, current telemetry, and future admission. Then remove only exercise-owned artifacts and restore the baseline policy.

The executable L2 workload is two replicated independent CPU tasks, with one result per logical task. It is not distributed training, a collective, or RDMA. The compound synthetic defects above and this observed process-recovery exercise are separate evidence in the same assessed bundle. If any required ownership or environment condition is absent, perform L0 only and mark the L2 outcome pending. The native procedure is NOT_RUN in this course build; its existence is not runtime evidence.

## Evidence and acceptance

Submit pre-fault correctness and versions, fault boundary, timestamped detection, recovery decision, failed and passing current checks, workload result comparison, residual state, and cleanup proof. A local PASS shows the modeled state path; the L2 claim needs native runtime evidence from two participating nodes.

Abort on uncontrolled spread, missing state needed for recovery, loss of observability, unauthorized identities, or impact on unrelated work. The safe fallback is stop exercise submissions and hand back control to the environment owner with the exact state recorded. Never improvise a physical recovery.

Objective checks: no promotion with failed current qualification; replay starts from a complete checkpoint; duplicate externally visible work is addressed; hidden health is checked rather than inferred; reset is demonstrated. Apply the common rubric.

## Questions for defense

1. Why is a checkpoint directory's existence insufficient?
2. Which time intervals make up workload recovery, and why keep them separate?
3. What distinguishes a new successful qualification from an old delayed success?
4. What lower claim is justified when only the local model ran?

## Four-week application plan

Weeks 1-2: 9h/week for recovery invariants, local scenario, approved L2 preparation, and baseline. Weeks 3-4: 9h/week for the bounded run if available, hidden-health verification, reset, and evidence review. Continue to [Month 22](22-rack-readiness.md).
