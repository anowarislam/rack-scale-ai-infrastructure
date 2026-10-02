# Month 12: Defend a complete platform result

Your decision is whether the reference meets its workload contract and which conclusions transfer to a different deployment. This chapter prepares **G2-E06 / G2-O11 and G2-O12** and integrates the prior five bundles. Do not convert the existence of all files into a passing learner assessment: the evidence must contain your observations and reasoning.

## Build an explanation across boundaries

An operational result connects intent, policy, placement, runtime, data, output, and recovery. Each connection needs an identifier and observation time. A Job name without UID can confuse retries; a GPU allocation without device identity can confuse capacity; a completion counter without an application invariant can count invalid work.

For Kubernetes, retain the manifest and image digest, namespace permissions and quota, Job/Pod UIDs, scheduling events, node placement, each attempt's exit information, checkpoint identity, final result, and cleanup verification. The [Job semantics](https://v1-34.docs.kubernetes.io/docs/concepts/workloads/controllers/job/) explain why a single final status is insufficient to reconstruct execution. Where you lack audit retention or metrics, say so rather than reconstructing a precise history from a screenshot.

The integration exercise is deliberately smaller than a production platform. You built and explained a real CPU reference, diagnosed placement, verified workload recovery, tested access boundaries, and defended change/recovery design. GPU exposure, physical topology, cross-node storage recovery, and executed HA require their own named environments and evidence.

## Worked example 1: Allocation is not goodput

Suppose a report shows 8 GPUs allocated for one hour. That is `8 * 1 = 8 GPU-hours` of allocated capacity. During 15 minutes the workers wait for a missing peer, and during 5 minutes they checkpoint. If the remaining 40 minutes perform valid training, the time fraction producing training progress is `40 / 60 = 66.7%`, not 100% merely because all GPUs remained allocated.

Assume 2,400 valid steps completed during those 40 minutes. Measured end-to-end goodput is `2,400 / 3,600 = 0.667 steps/s`. Compute-active step rate is `2,400 / 2,400 = 1 step/s`. Both are legitimate with different denominators. A scheduler placement change that eliminates 15 minutes of peer wait could improve end-to-end goodput without changing the active step kernel at all.

This constructed example does not establish utilization from device telemetry; allocation, GPU busy time, and useful application progress are different observations. Kubernetes resource requests and Pod durations can support an allocation estimate, but they are not automatically a durable, complete billing ledger. Specify the source, retained history, missing attempts, and cost model before turning them into charges.

## Worked example 2: Choose a platform for a concrete contract

Team A runs interactive inference services and periodic data preparation. It needs request routing, rolling replacement, readiness behavior, and integration with existing API-driven service operations. Team B runs bounded multi-node batch allocations with project associations, queue policy, and historical accounting. A defensible first position is to prototype Team A in Kubernetes and Team B in Slurm, then measure the actual constraints. This is a design inference from stated requirements, not a universal industry distribution claim.

Now change Team B's request: the training service must also maintain a persistent online endpoint with availability objectives. The original batch fit no longer answers the entire requirement. Similarly, Team A may require a coordinated multi-worker training job whose partial admission strands accelerators. Kubernetes's service strengths do not prove the selected training admission mechanism is sufficient.

Quantify a choice. If Team A's existing deployment path takes 20 minutes of operator work per release and integration reduces it to 5 across 12 releases/month, the observed labor difference would be `(20 - 5) * 12 = 180 minutes/month`. That hypothetical saving must be measured and weighed against new operational failure modes, rather than calling any migration an automatic efficiency gain.

## Native differences to defend

| Question | Kubernetes reference answer | Slurm comparison question |
|---|---|---|
| What is scheduled? | Individual Pods; controller owns desired workload | How does a job allocation relate to its steps? |
| What restores computation? | Application plus durable compatible state | What happens when the batch script is requeued? |
| What limits a tenant? | RBAC, admission/quota, runtime/network/data controls | What do Linux identity, associations/QOS, and cgroups enforce? |
| What counts use? | An explicitly designed telemetry/accounting pipeline | Is SlurmDBD configured, or only completion/current-state records? |
| What does gang mean? | Name the selected coordinated-admission integration | Why is Slurm GANG time-slicing a different mechanism? |
| What survives control loss? | Separate running-node behavior from new reconciliation | Separate running steps, controller state, and accounting database |

Use the other track's observed evidence. [Slurm accounting](https://slurm.schedmd.com/accounting.html), [requeue](https://slurm.schedmd.com/scontrol.html), and [gang scheduling](https://slurm.schedmd.com/gang_scheduling.html) supply native semantics; they do not substitute for your secondary run.

Counterexample: declaring Kubernetes superior because it has a dashboard, or Slurm superior because a queue starts a job quickly, ignores the contract, workload mix, and operational cost. A comparison needs a decision criterion, observations, and a known scope.

## G2 integration exercise

Assemble one packet containing the six existing bundles. Link observations instead of repeating them. For G2-E06, write a two-page operational handoff: the exact reference, healthy state, failed state, recovery evidence, isolation evidence, upgrade/restore stops, telemetry gaps, cleanup, and next-fidelity requirement. Add a comparison memo covering topology, fairness, identity, change, recovery, and accounting/evidence on both platforms.

Defend two fresh variations without consulting the key: the workload requests an absent device class; then a checkpoint passes JSON parsing but has the wrong target. For each, predict the rejecting layer and the evidence that would falsify your explanation. Re-run only the bounded local variant needed to resolve uncertainty. There are still six assessed bundles, not new exams for each question.

Use `bash labs/platforms/kubernetes/run.sh evidence` before cleanup. Then run `bash labs/platforms/kubernetes/run.sh cleanup`. Save redacted evidence outside ephemeral cluster storage. The guard permits deleting only the uniquely named course cluster recorded by the script; never replace this with broad Docker cleanup.

## Four weeks, 8-10 combined hours each

| Week | Primary 5 h | Secondary 2 h | Evidence/review 1-3 h |
|---|---|---|---|
| 1 | Trace end-to-end evidence | Close missing native counterpart run | Identify unsupported conclusions |
| 2 | Work allocation/goodput example | Review native accounting availability | Calculate denominators honestly |
| 3 | Integrate and rehearse operational handoff | Write comparison with observed differences | Peer challenge and corrections |
| 4 | Remediate and defend reference | Explain secondary recovery limits | G2 decision and cleanup |

## Questions

1. Why are GPU-hours and valid steps/s different decision inputs?
2. Can the Python placement model satisfy the secondary native-workload outcome?
3. What is missing if the comparison cites Slurm accounting but the lab has no SlurmDBD?
4. Why should rejected changes remain in the evidence packet?
5. What would justify extending a local Pod-retry claim to storage disaster recovery?

<details>
<summary>Reasoned answers</summary>

1. One measures allocated capacity over time; the other measures useful output over a stated time denominator. They can diverge during peer wait, recomputation, or invalid execution.
2. No. It exercises a chosen model. The gate separately requires an actual workload on each native platform with recorded versions and observed behavior.
3. The memo must state which records exist and which do not. Completion files/current-state output can support a bounded evidence review; they cannot masquerade as durable database accounting or demonstrate historical fair share.
4. They reveal the tested invariants and why an intervention was refused. Removing them leaves a success-only narrative that cannot demonstrate diagnosis or safe stopping.
5. An explicitly authorized test that loses the relevant storage, restores a compatible committed state from an independent copy, and verifies application correctness and ownership. The process-retry test alone cannot supply that evidence.

</details>
