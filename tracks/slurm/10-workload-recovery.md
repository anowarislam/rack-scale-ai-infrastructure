# Month 10: Requeue is a new execution of the batch script

The problem is to preserve useful application progress when an allocation is interrupted. Slurm can return a batch job to the queue; it does not infer the application's checkpoint format or restore a process's memory. This prepares **G2-E04 / G2-O07 and G2-O08**. Prerequisites: allocations, steps, job state, and single-writer checkpointing.

## Separate the layers of failure

A batch job owns an allocation and runs a script. The script can launch one or more steps. A step's failed task, a failed batch shell, a missing node, a time limit, cancellation, and controller unavailability are different events. Their consequences depend on options and site policy. Inspect the job, relevant steps, exit codes, and logs before deciding what to retry.

`scontrol requeue` returns an eligible batch job to pending state. On re-execution the batch script starts from its beginning, and `SLURM_RESTART_COUNT` can expose that restart history. Eligibility and automatic behavior depend on configuration and submission options. A nonzero application exit is not a promise of automatic requeue. These details come from [scontrol](https://slurm.schedmd.com/scontrol.html) and [the versioned sbatch manual](https://raw.githubusercontent.com/SchedMD/slurm/slurm-25-05-3-1/doc/man/man1/sbatch.1).

The supplied script uses `--requeue` and append-mode output. It resumes application state from a directory keyed by Job ID. That teaches a single-writer recovery path. Production checkpoint identity should also include immutable run inputs and schema; Job IDs alone can be reused over a system's lifetime and are not globally unique data identities.

## Worked example 1: Same Job ID, different attempt

Job 42 computes 100 steps. Its first attempt writes the checkpoint for step 20. The sum is `20 * 21 * 41 / 6 = 2,870`. The operator explicitly requeues job 42. The running execution ends and the job waits for resources again. The new script starts at its first line; its application reads step 20 and continues at 21.

Expected final total is `100 * 101 * 201 / 6 = 338,350`. Evidence should contain the same Job ID, different attempt count, a positive `resumed_from`, the preserved checkpoint, and the correct final total. Queue delay after requeue belongs in recovery time even when the application restore itself is fast.

What would a misleading success look like? The new attempt could ignore the checkpoint, recompute all 100 steps, and still return 338,350. Or it could retain a checkpoint from a different target and generate a plausible total. Therefore the exercise verifies both state reuse and identity, not only an exit code.

## Worked example 2: Checkpoint placement changes the failure you can survive

Assume an application saves 8 GiB every ten minutes. At a sustained effective write rate of 1 GiB/s, the idealized transfer time is 8 seconds, before metadata, coordination, serialization, and contention. Four jobs checkpointing together could contend for the same path; multiplying nominal device bandwidth by job count does not establish effective throughput.

If those files live only on a failed compute node's local disk, requeueing onto another node may find no checkpoint. Shared storage or an independently durable copy extends the covered failure boundary, but introduces its own availability and consistency dependencies. The scheduler cannot restore data it cannot access.

For a distributed run, rank 0 might publish metadata saying generation 5 is complete before rank 3's file is durable. Restoring every rank from whichever file is newest can combine generations. A valid protocol needs a commit rule for the group, integrity checks, and fencing of previous writers. This is application/distributed-storage design, not an automatic consequence of `--requeue`.

Counterexample: a batch script registers an external experiment or bills an account at its first line. Requeue executes that line again. Make the registration idempotent using an immutable run key, or check the external transaction result before repeating it. Append-mode logs preserve attempt history but do not make side effects idempotent.

## Native recovery experiment

In the [VM runbook](../../labs/platforms/slurm/runbook.md), submit `job.sbatch`, wait until its checkpoint exists and the job is still RUNNING, then run `scontrol requeue` for that exact Job ID. The lab includes the waiting and validation commands so a finished job is not accidentally used as evidence of a mid-run interruption.

Expected: the job transitions through waiting/execution again, output contains a new attempt count, and the application resumes from a completed step greater than zero but below 100. A final total of 338,350 establishes arithmetic correctness. Exact resumed step varies because interruption races with checkpoint writes; that variation is evidence of the observed interruption point, not an error.

Primary Build work: identify the mechanism that keeps only one intended writer and explain what additional fencing is needed if the old node might continue writing during a network partition. Secondary Run work: execute the requeue and compare its same-Job-ID/new-script-attempt semantics with Kubernetes new-Pod attempts.

Troubleshooting: a rejected requeue requires checking ownership, state, `Requeue`, and local policy. A zero resume count requires checking path persistence and run target. Missing final history with successful application output may reflect absent accounting rather than execution failure. Preserve all three observations rather than forcing them into one status.

## Training and inference require different lifecycle plans

A batch allocation fits bounded training or offline inference with a completion rule. Running an online inference server inside an allocation also requires endpoint discovery, service readiness, client retry policy, allocation expiry handling, and desired availability. Slurm allocating the process does not automatically provide a Kubernetes Deployment's reconciliation or a request router. Conversely, a Deployment maintaining replicas does not itself provide Slurm's configured batch accounting policies. Design from the contract instead of reusing a convenient launcher for every lifecycle.

## Four-week combined plan

| Week | Primary 5 h | Secondary 2 h | Evidence/review 1-3 h |
|---|---|---|---|
| 1 | Trace batch/step/node failures | Trace replacement Pod behavior | Specify resume and output invariants |
| 2 | Run checkpoint and explicit requeue | Run secondary native recovery | Capture all attempt and state evidence |
| 3 | Work local/shared/distributed checkpoint cases | Compare endpoint versus batch lifecycle | Calculate loss and recovery time |
| 4 | Defend duplicate-writer and corrupt-state cases | Explain remaining fidelity gaps | G2-E04 and remediation |

## Questions

1. Where does a requeued batch script begin executing?
2. Why does `--requeue` not prove that any failed application will automatically retry?
3. Why can the final arithmetic answer be correct while recovery was inefficient?
4. Can a node-local checkpoint establish recovery from loss of that node's storage?
5. What is the additional danger when a "failed" node is only network-isolated?

<details>
<summary>Reasoned answers</summary>

1. At the beginning of the script. The application or script must explicitly discover and restore valid state; shell local variables and process memory are not restored by requeue.
2. Requeue eligibility and configured triggers are separate from every possible nonzero exit. The exercise uses an explicit operation and records policy instead of assuming a universal trigger.
3. Recomputing from zero can produce the same answer. Resume evidence, lost-work measurement, and elapsed recovery time establish whether committed progress was reused.
4. No. It covers failures that leave that storage accessible. Node/disk-loss recovery requires a surviving independent copy and a validated restore path.
5. The old process may still write while its replacement runs elsewhere. Fencing and generation ownership are needed to prevent concurrent attempts from corrupting the result.

</details>
