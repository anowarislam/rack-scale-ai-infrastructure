# Month 11: Make the platform explainable and changeable

The problem is to retain isolation and recoverability while a shared platform changes. More running replicas do not automatically give stronger security or a recoverable control plane. This prepares **G2-E05 / G2-O09 and G2-O10**. Prerequisites are namespaces, RBAC, Pods/Jobs, and the distinction between application and controller state.

## Four independent boundaries

**Authentication** identifies the caller; **authorization** determines allowed API actions; **admission** validates or changes an accepted request before persistence; **runtime isolation** limits executing code. Kubernetes RBAC grants actions against resources, API groups, and scopes. A namespaced RoleBinding does not create a kernel boundary. [RBAC documentation](https://v1-34.docs.kubernetes.io/docs/reference/access-authn-authz/rbac/) is the source for permission semantics.

The reference uses a restricted Pod security profile, non-root UID, no privilege escalation, dropped capabilities, and no automatically mounted ServiceAccount token. These controls serve distinct purposes. The restricted profile's exact checks are versioned; see [Pod Security Standards](https://v1-34.docs.kubernetes.io/docs/concepts/security/pod-security-standards/). Network isolation requires a network implementation that enforces NetworkPolicy; creating an object alone is not proof of packet filtering. The default lab does not claim that enforcement. See [NetworkPolicy](https://v1-34.docs.kubernetes.io/docs/concepts/services-networking/network-policies/).

Observability also has layers. API audit records answer who changed intent. Events and controller metrics expose reconciliation. Node/runtime signals expose execution prerequisites. Application counters establish completed useful work. Missing telemetry is not a zero failure rate: capture signal freshness, collection errors, and scope alongside the value.

## Worked example 1: A permission test that teaches scope

Identity `system:serviceaccount:course-platform:reader` has `get/list/watch` on Pods, Pod logs, and events, plus Jobs. Predict four authorization queries:

| Request | Expected | Reason |
|---|---|---|
| List Pods in `course-platform` | yes | Granted by RoleBinding in that namespace |
| Delete a Pod there | no | Delete verb absent |
| Get a Secret there | no | Secrets resource absent |
| List Pods in `default` | no | RoleBinding is not in that namespace |

Run `bash labs/platforms/kubernetes/run.sh rbac` to compare predictions with the authorization engine. The administrator uses impersonation for this test. This establishes the RBAC answers for that identity and configuration; it does not prove that a compromised node cannot read a workload's data.

Now consider an adjacent mistake: binding `cluster-admin` to make a log collector work. The collector needs a read path, but the proposed action grants unrelated mutation powers. Diagnose the denied resource/verb and grant the narrow needed access. If logs contain secrets, even correctly scoped log access still has a data-exposure cost.

## Worked example 2: Three control-plane members and a failed upgrade

An etcd cluster with three voting members needs a majority of two for quorum. Losing one leaves two, so it can continue if the remaining members can communicate. Losing two leaves one and loses quorum. Three machines in one failure domain do not protect against that domain disappearing.

Suppose an upgrade removes one member and a second member is already unhealthy. Treating "three configured members" as "three healthy members" would turn planned maintenance into an outage. A precheck must establish current health and the intended failure budget. Backups are a separate protection: a replicated accidental deletion is still a deletion. Restore testing must happen in an isolated target with known snapshot age and application reconciliation checks.

Kubeadm supports stacked and external etcd topology choices, each with different coupled failure domains; see [HA topology](https://v1-34.docs.kubernetes.io/docs/setup/production-environment/tools/kubeadm/ha-topology/). Our two-node kind layout has one control-plane member. It is not an HA implementation, even though a separate worker runs applications.

## Upgrade reasoning before commands

Record all component versions and integrations, read the version-specific upgrade procedure, verify skew at every intermediate state, rehearse, change one permitted unit, and check positive health before continuing. A release number alone does not establish compatibility of CNI, CSI, GPU drivers/plugins, admission webhooks, or CRDs. The v1.34 [version-skew policy](https://v1-34.docs.kubernetes.io/releases/version-skew-policy/) supports kubectl within one minor version of the API server; this lab uses matching binaries to remove that variable.

Draining a node marks it unavailable for new placement and requests eviction of eligible workloads. A PodDisruptionBudget constrains voluntary disruptions; it is not a guarantee against arbitrary node failure or insufficient replacement capacity. Local storage and DaemonSets need explicit treatment. See [safe drain](https://v1-34.docs.kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/). Do not add `--force` or deletion flags to bypass a blocked drain without understanding the blocked workload's owner and data.

Counterexample: every readiness probe returns success, but the checkpoint store rejects writes. The service may appear available until a worker fails and cannot restore. A useful health check covers the dependency or a representative transaction, plus telemetry freshness, rather than treating one probe as universal health.

## Lab and higher-fidelity runbook

Run `rbac`, `inspect`, and `evidence` actions in the isolated sandbox. Inventory namespace controls, the application result, failed/recovered attempts, and collection time. Use the exact configuration to explain the four permission answers above. Write an upgrade/recovery plan whose preconditions include known-good backup, compatible versions, capacity headroom, stop conditions, and named rollback/restore ownership.

To extend to actual multi-node control-plane recovery, use a separately assigned environment with at least three control-plane/etcd members, a dedicated API endpoint, independent failure domains as available, and disposable application data. First record the endpoint, member health, application baseline, and snapshot/restore rehearsal. Remove only the authorized single member, measure API writes and application progress, restore it, and verify membership and data. Abort if a second member is unhealthy. The outcome must explicitly distinguish executed member failure, analyzed topology, and untested storage disaster recovery. No such fault is executed by the supplied kind scripts.

## Four weeks, 8-10 combined hours each

| Week | Primary 5 h | Secondary 2 h | Evidence/review 1-3 h |
|---|---|---|---|
| 1 | Trace identity/admission/runtime boundaries | Compare native user/account controls | Predict then run denial tests |
| 2 | Map signals and blind spots | Review other platform's records | Preserve freshness and missing data |
| 3 | Work upgrade and quorum scenarios | Compare control-plane persistence | Draft prechecks, stops, recovery |
| 4 | Defend one failed-change scenario | Challenge isolation/HA overclaims | G2-E05 and remediation |

## Questions

1. What does a denied Secret read prove, and what does it not prove?
2. Why can a NetworkPolicy manifest exist without effective isolation?
3. How many failures can a healthy three-member etcd cluster tolerate while retaining majority?
4. Does a disruption budget guarantee service through node failure?
5. Why is a tested snapshot restore different from an HA deployment?

<details>
<summary>Reasoned answers</summary>

1. It proves the tested API identity lacks that authorized action in the tested scope. It does not evaluate every alternative credential, node privilege, log leak, or storage path.
2. Enforcement is performed by the network implementation. API acceptance of a policy is not a data-plane test; verify allowed and denied traffic with the selected provider.
3. One member failure, assuming the other two communicate and remain healthy. Correlated failure domains and existing degraded members reduce the practical margin.
4. No. It constrains certain voluntary evictions. Hardware failures, network isolation, and unavailable replacement capacity can still violate application availability.
5. HA keeps service available through covered member failures; restore recovers from lost or corrupted persistent state. Replication can reproduce corruption, so both mechanisms need distinct evidence.

</details>
