# GitLab, January 2017: a backup must become a working service

**Decision question:** If production data disappears now, which retained artifact can restore a correct service, how much committed work will be missing, and how long will the whole recovery take?

The assumption to challenge is that having several backup mechanisms means having several usable recovery paths. Each path is a chain: produce an artifact, retain it, find it, read it, restore it, and validate its application meaning. A broken link can make an otherwise convincing checklist irrelevant.

## Published account

**Verified source; operator account.** GitLab's February 10 postmortem describes accidental deletion from the GitLab.com primary database on January 31, 2017, during work to repair secondary replication. Neither database host then supplied a usable recovery copy. Scheduled logical backups had failed because an older `pg_dump` was selected; failure emails had been rejected. Database disk snapshots were not enabled.

Recovery used an LVM snapshot made about six hours before the outage. Slow source storage made copying lengthy. GitLab reports restoring database state from January 31 at 17:20 UTC, with final restoration procedures finished around 18:00 UTC on February 1. Some database changes were permanently lost; Git repositories and wikis were unavailable but did not suffer that data loss. Self-managed installations were outside the incident's scope. At publication, hourly LVM snapshots were operating; automated restore testing remained an improvement item. [GitLab's postmortem](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/)

## Mechanism: recoverability is a conjunction

**Course model.** A recovery artifact is useful only if several statements hold together:

```text
usable recovery = artifact exists
                  AND artifact is readable
                  AND required state is included
                  AND a compatible restorer is available
                  AND application invariants can be restored
```

These are not independent probabilities. A common credential, retention policy, or administrative mistake can break multiple paths simultaneously. Counting copies does not measure independence.

The recovery point describes the latest reconstructable committed state; recovery time describes the time needed to deliver service again. RPO and RTO name objectives for those dimensions. Record both the target and the rehearsal's observed outcome.

Application invariants extend beyond whether a database opens. For a hypothetical job platform, a restored task must retain its owner, checkpoint reference, completion state, and relationship to external outputs. If a task appears incomplete but its output was already published, blindly running it again may create a duplicate. If a staging copy has transformed tenant identities or removed integrations, being readable does not make it a faithful production recovery source.

A live replica may faithfully follow an unwanted change. An earlier retained state preserves a recovery point only if its storage and authority boundaries survive the initiating fault.

## Worked example: the network is not the bottleneck

**Synthetic inputs.** A verified snapshot is four hours old and contains `900 GB`. Use decimal units. The recovery source reads at `90 MB/s`, the network carries `180 MB/s`, and the target writes at `300 MB/s`. Provisioning takes 15 minutes and validation takes 25 minutes. Assume copying streams through all three resources and these other phases occur sequentially.

```text
Effective copy rate = min(90, 180, 300) = 90 MB/s
Copy time = 900,000 MB / 90 MB/s = 10,000 s = 166 min 40 s
Total time = 15 min + 166 min 40 s + 25 min
           = 206 min 40 s = 3 h 26 min 40 s
```

Doubling network capacity leaves the source limit unchanged. A two-hour recovery objective is missed by `1 h 26 min 40 s`, even though the copy succeeds. Without another usable artifact or change log, the reconstructed state is also four hours behind the failure.

Suppose a verified, contiguous change log reaches ten minutes before the failure and replay takes another 30 minutes. The new path takes `3 h 56 min 40 s` but improves the recovery point to ten minutes before failure. That is a tradeoff between time and lost work. It is valid only if replay succeeds and preserves application invariants; the mere presence of log files does not establish either condition.

## What would you do?

You find a newer untested archive and an older snapshot with a successful restore rehearsal. The newer archive has an unfamiliar format. Which becomes the incident's recovery plan?

<details>
<summary>Reasoned answer</summary>

Preserve both. Start the known recovery path in isolation while a separate bounded investigation tests the newer archive's compatibility and completeness. Choose the production recovery point from demonstrated results and the explicit cost of losing newer state. Do not overwrite the validated copy or expose the candidate service to writes while its integrity is uncertain. Before reopening service, reconcile external side effects and record the exact reconstructed state and known gaps.

</details>

## Mitigations, tradeoffs, and counterfactual

Give restore testing an owner and a measurable result: recover a known artifact in an isolated environment, verify representative relationships, and record elapsed time. Monitor artifact freshness and successful restoration separately from whether a scheduled command exited successfully. Test the notification path too; an alarm that nobody receives supplies no operational evidence.

Retaining more versions increases recovery options and storage cost. Faster source storage reduces copying time but may be expensive for rarely used archives. Independent credentials can protect copies from one administrative failure while adding access-management work during an emergency. Include that access path in the rehearsal.

**Counterfactual:** preventing the particular mistaken deletion would protect against that trigger. It would not prove recovery from storage failure, corruption, or another destructive operation. A backup program needs both prevention and demonstrated restoration.

## Transfer to AI infrastructure and limits

**Course inference.** Treat training checkpoints as stateful recovery artifacts, with model, optimizer, step, dataset, and workload identity checked together. A newer directory with missing shards can be less useful than an older complete checkpoint. Connect this reasoning to [Kubernetes workload recovery](../tracks/kubernetes/10-workload-recovery.md) and the [recovery practicum](../practicum/21-recovery.md).

Confidence is high in the historical account and conditional arithmetic. This page does not test GitLab backups, inspect current operations, or establish current database-version compatibility.
