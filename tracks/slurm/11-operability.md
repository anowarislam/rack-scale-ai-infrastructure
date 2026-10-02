# Month 11: Trust, accounting, persistent state, and safe upgrades

The problem is to operate a scheduler without confusing authenticated submission, enforced resource isolation, durable accounting, and recoverable controller state. This prepares **G2-E05 / G2-O09 and G2-O10**. Prerequisites: Linux identity, allocations/steps, queue policy, and recovery contracts.

## What each mechanism can establish

MUNGE supplies authenticated credentials in the reference environment. Consistent UID/GID mapping is still required across participating nodes. Filesystem permissions determine which data an executing user can read or modify. Associations/QOS constrain scheduled use only when the relevant accounting/enforcement configuration is active. Cgroups constrain executing tasks according to configured controls; they are not implied by the existence of a partition.

Slurm's cgroup v2 plugin has Linux/systemd and build/runtime prerequisites. The [cgroup v2 guide](https://slurm.schedmd.com/cgroup_v2.html) explains its integration; a configuration copied from another host is not proof that this host delegated the required controllers. The minimal course VM deliberately leaves TaskPlugin unset and uses `proctrack/linuxproc`, so it is only a trusted-user sandbox. An optional hardened profile must be validated before making isolation claims.

Observability separates current state (`squeue`, `scontrol`), daemon logs, completion records, step/resource accounting, and application output. The base profile writes a job-completion file but leaves AccountingStorageType unset. Therefore it does not provide the SlurmDBD-backed job/association history taught in the optional profile. [Accounting documentation](https://slurm.schedmd.com/accounting.html) describes the database service and its bounded outage cache, not unlimited history without one.

## Worked example 1: A resource limit that exists only on paper

A job requests 128 MiB, and the scheduler reserves 128 MiB. The program allocates 512 MiB. If no runtime enforcement prevents it, the request itself is not a guarantee that neighboring jobs remain protected. The scheduler's reservation and the kernel's enforcement are separate layers.

Now consider two Unix users, alice and bob. Alice's checkpoint directory is mode 0700 and owned by alice. Bob's read attempt should fail even if both users submit to the same partition. This tests a filesystem boundary. It says nothing by itself about whether bob can access an unassigned GPU device, because device access is a different boundary.

The correct test matrix names the requested limit, enforcing mechanism, violating operation, expected denial, and observed evidence. Do not present one denied file read as proof that every memory, CPU, network, and device control is effective.

## Worked example 2: Controller failover is not database restore

Suppose two controller hosts share the required persistent controller state and have a configured primary/backup relationship. The primary stops, and the backup takes responsibility after the relevant failure-detection process. Running jobs may continue on their nodes while new scheduling and administrative operations are affected. The actual interruption must be measured; adding a second hostname to configuration is not failover evidence.

Now remove the shared state storage instead of the primary host. Both controllers may lose what they need. A second controller in the same storage failure domain does not solve the different failure. Similarly, SlurmDBD and its database hold accounting data; the controller's StateSaveLocation and the accounting database are not interchangeable backups. The versioned [slurm.conf manual](https://raw.githubusercontent.com/SchedMD/slurm/slurm-25-05-3-1/doc/man/man5/slurm.conf.5) describes SlurmctldHost and persistent state.

For a constructed timing example, detection takes 30 seconds, takeover 10, and client retry 5. The earliest observed resumed control action is around 45 seconds, assuming no other dependency blocks it. If an application's collective times out after 20 seconds because the actual fault also disrupts the data network, controller redundancy does not repair that application failure. Trace the blast radius before assigning the incident to the scheduler.

## Upgrade compatibility is a path, not a number

Slurm releases can change RPC compatibility, state formats, database schemas, and plugins. Read the release-specific upgrade guide and NEWS for both endpoints and every intermediate version. Inventory controller, node, client, database-daemon, and custom-plugin versions. Where SlurmDBD is used, upgrade order and its compatibility window matter. Do not transfer Kubernetes's version-skew rules to Slurm.

After newer daemons transform persistent state, restoring an old binary alone is not a sound rollback plan. The official [upgrade guide](https://slurm.schedmd.com/upgrades.html) warns about reverting after daemon startup. Define either forward repair or restoration of mutually consistent pre-change controller/database state, with explicit acceptance of history lost after that point. Snapshotting only the executable does not preserve scheduling or accounting meaning.

Counterexample: an upgrade appears healthy because `scontrol ping` succeeds. New submissions may still fail an association lookup, a job step may not launch on older nodes, or GPU plugins may load incorrectly. Positive health must include a representative new submission, execution, result, accounting path if configured, and recovery checks.

## Lab and higher-scope runbook

In the dedicated VM, record active authentication, priority, task/proctrack, accounting, and completion plugins with `scontrol show config`. Run the two-user file-permission denial test from the runbook. Explain why it is bounded filesystem isolation. For the base profile, record `sacct` as unavailable/not applicable for SlurmDBD history rather than inventing output.

The runbook also describes a bounded controller restart while a test step runs. That can establish single-controller restart behavior and StateSaveLocation persistence. It cannot establish backup takeover. To execute HA, obtain a separate environment with two controller hosts, correctly shared persistent state, consistent authentication/identity, dedicated test nodes, and isolated accounting as appropriate. Baseline, fail only the assigned primary, observe takeover and job continuity, restore, and test a new job. Abort on state-store failure, unexpected dual ownership, or impact outside the allocation.

Primary Build work: defend that runbook and a version-specific upgrade path. Secondary Run work: inventory actual controls and explain what the observed records do and do not establish. The gate accepts an honestly analyzed HA plan at its stated scope; do not label it executed HA.

## Four-week combined plan

| Week | Primary 5 h | Secondary 2 h | Evidence/review 1-3 h |
|---|---|---|---|
| 1 | Trace trust and enforcement layers | Compare Kubernetes access boundaries | Run bounded denial test |
| 2 | Inventory current/history/application signals | Review counterpart telemetry gaps | Distinguish unavailable from zero |
| 3 | Work controller/state/database scenarios | Compare upgrade compatibility models | Write tested or analyzed recovery path |
| 4 | Defend failed-upgrade scenario | Challenge isolation and HA overclaims | G2-E05 and remediation |

## Questions

1. Why is `--mem=128M` not alone evidence of runtime isolation?
2. What does the base profile's completion file fail to replace?
3. Why can two controllers still share one fatal dependency?
4. Why is copying back an older Slurm binary an incomplete rollback?
5. Is `scontrol ping` enough to declare an upgrade successful?

<details>
<summary>Reasoned answers</summary>

1. It expresses a scheduling request/limit intent, but the runtime needs an active enforcement path. Verify the configured plugin/controllers and a bounded violating workload.
2. It does not create SlurmDBD's association history, full step/resource records, or the prerequisites for historical fair-share behavior. Use it only for the fields it actually records.
3. Both may depend on the same state storage, network, authentication, or power domain. Redundancy covers only the failures its dependencies can survive.
4. New daemons may have transformed state and database schemas. A consistent restore or supported forward repair must address those changes and any lost post-backup history.
5. No. It establishes a controller response. Test new submission, node execution, correct output, active accounting, and the relevant recovery path before accepting the change.

</details>
