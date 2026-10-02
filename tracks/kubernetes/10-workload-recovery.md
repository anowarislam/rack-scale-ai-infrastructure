# Month 10: Recover useful state, not merely a green Pod

The problem is that Kubernetes can replace failed execution without reconstructing the application's meaning. A successful replacement that repeats an external charge, consumes different data, or joins the wrong training generation is not a successful recovery. This chapter prepares **G2-E04 / G2-O07 and G2-O08**. Prerequisites are the Job lifecycle, workload contract, and basic persistent storage.

## The recovery responsibilities

A Pod is not moved intact between nodes. Replacement creates another execution with its own identity. A Job controller can retry failed work subject to its policy, but an application must tolerate its execution semantics. Kubernetes explicitly warns that even a one-completion Job can sometimes start the program more than once. Use idempotent output publication or deduplication where effects matter. See [Jobs](https://v1-34.docs.kubernetes.io/docs/concepts/workloads/controllers/job/).

Three states must agree: controller intent, application progress, and committed output. A **checkpoint generation** identifies a consistent state boundary. **Fencing** prevents an old attempt from writing after its successor takes ownership. **Idempotency** makes repeating an operation safe for the intended effect. **Rendezvous** is how cooperating workers find their peers and agree on their generation. A Pod restart policy cannot supply all four.

Storage lifetime matters. A container's writable layer, an `emptyDir`, a PVC-backed volume, and an external object store have different failure boundaries. `emptyDir` survives container restarts within its Pod but is removed with the Pod. A PVC refers to persistent storage with its own access mode, provisioning, topology, and reclaim behavior. Persistent does not mean replicated or cross-node accessible. See [volumes](https://v1-34.docs.kubernetes.io/docs/concepts/storage/volumes/) and [persistent volumes](https://v1-34.docs.kubernetes.io/docs/concepts/storage/persistent-volumes/).

## Worked example 1: A retry that can be proved correct

The lab computes the sum of squares through step 40. Its reference answer is `40 * 41 * 81 / 6 = 22,140`. At step 8, the committed checkpoint contains completed step 8 and total `8 * 9 * 17 / 6 = 204`. The process then exits 75 deliberately.

The Job controller observes a failed Pod and creates a replacement within `backoffLimit: 2`. The replacement mounts the same claim, reads the checkpoint, validates target 40 and total 204, and begins at step 9. It must report `resumed_from=8` and final total 22,140. The first failed Pod is expected evidence, not a reason to hide the experiment.

Why not just check final total? A replacement could start again at zero, waste eight steps, and still return 22,140. Correct final state and demonstrated reuse of a committed checkpoint are different observations. Why validate the target? Reusing a checkpoint from another workload could produce an apparently plausible result with the wrong identity.

The file operation writes a temporary checkpoint, flushes it, and replaces the previous name. This reduces partial-file exposure for this single-writer, process-failure experiment. It does not claim distributed atomicity, cross-file consistency, concurrent-writer safety, or survival of storage/power loss. The application explicitly has one writer.

## Worked example 2: Training restart versus inference retry

Consider four training ranks that perform synchronized steps. Rank 2 disappears after step 500, while peers wait in a collective. A safe recovery design must choose whether the framework supports elastic membership or whether all ranks restart from a common generation. If ranks 0, 1, and 3 restore step 500 but rank 2 restores step 490, the group has inconsistent model/optimizer state even if every Pod is Running.

Now consider a request-serving replica. Request R was accepted, the replica wrote an external result, and the response was lost during a restart. A client retries R. Starting a replacement is useful, but without an idempotency key the external effect may be repeated. A readiness probe can keep an uninitialized process out of service; it cannot infer that R has already committed.

Suppose inference capacity is 100 requests/s per healthy replica, arrival rate is 180 requests/s, and there are two replicas. Losing one produces demand 80 requests/s above the assumed capacity. A queue can grow even while the remaining replica is Ready. Scaling/recovery should therefore observe arrival, completion, queue depth, and latency, not only replica count. These are constructed examples; no benchmark value is implied.

Counterexample: an aggressive liveness probe restarts workers during a legitimate long checkpoint. Repeated restarts can prevent any checkpoint from completing. Separate startup, readiness, and liveness intent; verify timeouts against real application phases. Their different actions are described in [probe documentation](https://v1-34.docs.kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/).

## Run the bounded recovery experiment

After month 8 setup:

```sh
bash labs/platforms/kubernetes/run.sh recover
bash labs/platforms/kubernetes/run.sh evidence
```

Expected: one failed attempt with exit 75, a replacement that starts from 8, and a Complete Job with final total 22,140. Exact Pod names and controller timing vary. Preserve both attempts and the PVC identity. The kind storage backing is local to the lab; deleting the cluster deletes that learning environment. This test does not prove worker-disk-loss recovery.

Primary Build work: explain each ownership boundary and add a negative local test using a copied checkpoint whose total is corrupt. The supplied Python test demonstrates rejection; preserve the error rather than resetting the directory to make it disappear. Secondary Run work: reproduce the native failure and recovery and identify the equivalent Slurm batch-requeue boundary.

Troubleshooting: if the replacement starts at zero, examine whether it used the same claim, subdirectory, target, and permissions. If the PVC is Pending, inspect provisioning and topology. If the Job exhausts retries, inspect each attempt's exit code. A `CrashLoopBackOff` container and a series of failed Job Pods have different restart boundaries; do not collapse them into one counter.

## Four weeks, one combined 8-10 hour budget

| Week | Primary 5 h | Secondary 2 h | Evidence/review 1-3 h |
|---|---|---|---|
| 1 | Trace storage and retry lifetimes | Trace other platform's retry boundary | State a correctness invariant |
| 2 | Run failure and restore | Run native secondary recovery | Capture all attempt identities |
| 3 | Work training and inference examples | Compare duplicate-side-effect risk | Calculate lost work and recovery time |
| 4 | Defend corrupted-state refusal | Explain remaining recovery limits | G2-E04 and remediation |

## Questions

1. Why does a Complete Job not prove exactly-once effects?
2. Can `emptyDir` recover a deleted Pod's checkpoint?
3. Why is `resumed_from=8` useful in addition to the final total?
4. All four training Pods are Running. What additional state must agree?
5. Would this local PVC experiment justify a claim of node-loss recovery?

<details>
<summary>Reasoned answers</summary>

1. Controller completion is not a transaction across the application's external systems. More than one execution can occur, so output publication needs its own deduplication or transaction semantics.
2. No. Its lifetime is tied to the Pod. A replacement Pod needs a storage path that survives the relevant failure and contains compatible committed state.
3. The correct answer could also be obtained by recomputing from zero. The resume marker demonstrates reused progress; the final total demonstrates application correctness.
4. The workers need compatible data/code identity, checkpoint generation, rank/world-size expectations, and rendezvous state. Running is a process/lifecycle observation, not proof of a coherent computation.
5. No. The experiment covers process/Pod retry with the backing storage available. Loss of a node and its local data is a different failure and requires a separately designed storage/recovery test.

</details>
