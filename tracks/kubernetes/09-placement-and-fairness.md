# Month 9: Explain why work is waiting

The problem is to separate policy rejection, insufficient feasible resources, and runtime failure. Your target is a defensible intervention, not merely a Pending count of zero. This chapter prepares **G2-E03 / G2-O05 and G2-O06**. It assumes the month 8 reference and month 7 contract.

## Scheduling is a feasibility problem before it is a ranking problem

In the reference scheduler, filtering identifies feasible nodes and scoring ranks candidates. A **label** is a key/value metadata pair used for selection, such as `course.rack=course-local`. **Affinity** expresses placement relationships: node affinity can select that rack, while Pod affinity can request proximity to related Pods. A **taint** can keep Pods away unless they have an appropriate **toleration**; tolerating a dedicated-GPU node does not require choosing it. A Pod can combine these with topology-spread rules. Required conditions eliminate candidates; preferred conditions influence ranking without guaranteeing placement. These mechanisms are documented in [node assignment](https://v1-34.docs.kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) and [the scheduling framework](https://v1-34.docs.kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/).

Three topology scopes must stay separate. Node labels can represent rack or zone identity. CPU/device placement within a node can depend on kubelet resource managers. The physical fabric determines the actual communication path. The kubelet's [Topology Manager](https://v1-34.docs.kubernetes.io/docs/tasks/administer-cluster/topology-manager/) combines resource-placement hints within its supported scopes; it is not a measurement of inter-rack network quality.

**Fragmentation** means free resources have an unusable shape or location for the requested work. **Priority** influences ordering and may participate in preemption. **Fairness** is a policy question about who should receive service over time. **ResourceQuota** bounds aggregate namespace consumption; it does not on its own establish usage-decayed project entitlement or guarantee wait times. [Quota documentation](https://v1-34.docs.kubernetes.io/docs/concepts/policy/resource-quotas/) specifies admission behavior; the longer-term fairness design needs an explicitly selected integration.

## Worked example 1: Aggregate GPU capacity lies

Four nodes each expose 8 whole GPUs. Existing allocations leave free counts `[3, 3, 3, 3]`. A new job needs two workers with 4 GPUs each. The aggregate free count is 12, larger than the 8 requested, but no worker fits on any node. Spreading two workers across nodes cannot divide a single four-GPU worker between nodes. The relevant unit is each Pod's resource request.

Suppose one three-GPU job completes on node A, producing `[6, 3, 3, 3]`. One new worker can fit, but the other still cannot. Under independent Pod scheduling, admitting the first worker may reserve GPUs while it waits for its peer. That can lower useful utilization even as allocated GPU count increases.

Possible responses include waiting for both workers to fit, changing the application parallelism shape, reserving suitable capacity, or using a verified coordinated-admission mechanism. They have different latency/fairness costs. The default v1.34 Job plus Pod scheduler should not be described as an atomic whole-job allocator. A plugin or queue controller must be named, pinned, configured, and tested before claiming stronger behavior.

## Worked example 2: Admission rejection is not scheduler Pending

A namespace quota allows 2 requested CPUs. Existing active Pods account for 1.5 CPUs. A new Pod requests 1 CPU. The sum would be 2.5, so quota admission can reject creation. There may be 20 idle CPUs elsewhere. No scheduling score can repair an object that was never admitted.

Now lower that Pod's request to 0.5 CPU with an application justification. The sum is 2, so the quota constraint is satisfied. Add `nodeSelector: {course.rack: course-invalid}` when no node has that label. The object can now exist but remain unschedulable. The two failures require different evidence: API/controller rejection versus Pod scheduling condition and events.

The quota error does not prove that the quota is wrong. The node-selector failure does not prove labels should be changed. First determine whether the contract, namespace allocation, or actual infrastructure inventory is incorrect.

## Native experiment and evidence

```sh
bash labs/platforms/kubernetes/run.sh pending
bash labs/platforms/kubernetes/run.sh repair
```

The first command submits a Pod constrained to a nonexistent course rack. Expected evidence includes `PodScheduled=False`, reason `Unschedulable`, and an event describing unmatched constraints. Other nodes may also be rejected for a control-plane taint; record all reasons instead of insisting on one exact event sentence. The repair recreates the Pod with the worker's actual course label; expected result is Succeeded and output `650`. Recreation changes UID: preserve both identities.

Primary Build work: explain why the workload field, rather than an invented infrastructure label, is repaired in this intentionally seeded case. Use month 7's model to compare same-domain versus cross-domain placement and name the application's missing performance evidence. Secondary Run work: reproduce one native Pending state and its recovery, then compare it with a Slurm pending reason from your actual environment.

**GPU extension, separately bounded:** use only an assigned Linux GPU node with a frozen driver/runtime/device-plugin bill of materials. Record detected devices, allocatable `nvidia.com/gpu`, and actual container device visibility. A one-GPU request commonly uses an integer extended-resource limit, with matching request rules described in [Schedule GPUs](https://v1-34.docs.kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/). This CPU kind lab does not install a plugin or simulate a GPU. MIG, sharing, and topology policy change semantics; [NVIDIA's MIG guidance](https://docs.nvidia.com/datacenter/cloud-native/kubernetes/latest/index.html) is an extension source, not evidence that this sandbox supports them.

Counterexample: labeling every node `fast-fabric=true` may make a Pod schedulable while violating its physical needs. A successful bind is evidence of policy satisfaction against recorded labels, not proof of label truth or bandwidth. Reconcile labels with inventory and an observed workload result.

## Four weeks, 8-10 combined hours each

| Week | Primary 5 h | Secondary 2 h | Evidence/review 1-3 h |
|---|---|---|---|
| 1 | Derive filter/score and fragmentation examples | Learn native queue/allocation reasons | Draw required/preferred distinction |
| 2 | Run Pending and repair experiment | Run counterpart scheduling analysis | Preserve events and object identities |
| 3 | Analyze fairness and topology contract | Compare quota versus fair-share policy | Explain an intervention's cost |
| 4 | Defend changed-shape scenario | Challenge a false-equivalence claim | G2-E03 and remediation |

## Questions

1. Why do twelve free GPUs fail to satisfy an eight-GPU job in the example?
2. Does a toleration place a Pod on its matching node?
3. What distinguishes quota rejection from unschedulable Pending?
4. Why is increasing priority insufficient for a nonexistent required label?
5. Is a topology-spread rule proof of a low-latency network path?

<details>
<summary>Reasoned answers</summary>

1. Each four-GPU worker needs four resources on one node, and every node has only three free. The aggregate ignores indivisible worker shape.
2. No. It removes one barrier to consideration; other filters and scoring still apply. Affinity/selection expresses placement intent separately.
3. A quota denial may prevent the Pod object from being created; scheduling Pending concerns an existing unbound Pod. Follow owner events and API results as well as Pod status.
4. Priority cannot make a candidate satisfy a required condition. Preemption can release resources in some cases, but it does not create missing hardware labels or capabilities.
5. No. It places replicas across declared domains. Labels can be stale, and spreading can increase communication distance. The workload's path and timing must be measured.

</details>
