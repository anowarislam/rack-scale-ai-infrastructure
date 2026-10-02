# Specialty: bound one tenant's GPU admission

**One intervention:** apply one per-tenant aggregate GPU cap on your primary platform and measure its effect on a second tenant's access. Use the platform's native policy. This is a fairness and admission experiment, not a custom scheduler project.

## Characterize

Resource ownership, admission, and placement are separate. Admission can refuse or delay work that exceeds a tenant's allowance. Placement selects a node for admitted work. A cap does not reserve a contiguous GPU topology, guarantee a start time, or make priorities identical across platforms.

**Synthetic worked example:** a 16-GPU pool has tenant A offering three 4-GPU jobs and tenant B offering one 8-GPU job. Without a cap, A can occupy 12 GPUs and leave B unable to fit despite four idle GPUs. Capping A at 8 leaves aggregate room for B's eight. This prediction assumes an appropriate eight-GPU placement exists and that admission/queue behavior supports the policy. It does not prove B will start immediately.

**Counterexample:** two nodes each have four free GPUs, while B requires eight on one node. A's cap creates eight aggregate free GPUs but cannot satisfy B's topology. The observed pending reason matters more than the arithmetic alone.

## Intervene in the primary platform

For Kubernetes, use a dedicated tenant namespace and a `ResourceQuota` on `requests.nvidia.com/gpu` for the existing device-resource path. Quota rejection occurs at admission; do not describe an uncreated Pod as scheduler-pending. Verify actual resource naming and device exposure in the G2 environment. Official documentation supports extended-resource quotas, but the current documentation is not your cluster's version record. [Kubernetes Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)

For Slurm, use an instructor-controlled test association or QOS aggregate GPU TRES limit appropriate to the existing accounting configuration. Record which association/QOS applies and the native pending reason. Limits can interact hierarchically; inspect existing ones before changing a single selected cap. [Slurm Resource Limits](https://slurm.schedmd.com/resource_limits.html)

Reuse the actual platform procedures and version contract from G2. Record the exact old policy and rollback path before altering the dedicated environment. This packet does not authorize editing shared policy or creating production associations.

## Validate and recover

Replay the same submission sequence before and after the cap, with a no-change run as control. Capture submission, admission or rejection, scheduling, start, completion, allocated GPU count, output correctness, and native reason records. Report B's wait and A's lost/delayed throughput together. Repeat a no-contention control: the cap should not affect A while it stays within its allowance.

Restore the original policy and remove only exercise-owned workloads. Verify active workload count, policy state, and accounting completeness. Abort if a non-exercise tenant is affected, policy identity is ambiguous, or the workload lacks a valid cleanup path.

Deliver the native configuration diff, event timeline, comparison, fairness tradeoff, rollback proof, and operational note for limit changes. A pass requires understanding the platform-specific reason for delay/rejection; matching a numerical target through a different accidental bottleneck does not pass.

An actual CPU-only cluster can demonstrate CPU admission semantics with a renamed resource, but it cannot establish GPU or topology behavior. L0 queue simulation is preparation. A GPU policy claim needs real resource exposure; a multi-node placement claim needs L2. One native platform is sufficient for the specialty; the secondary comparison remains the G2 requirement.
