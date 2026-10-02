# GitHub: a successful election can produce an unusable service

**Decision question:** A failed link is back, but database writes now go to another region. Should you immediately promote the old primary again to recover latency?

Two assumptions need testing: that restoring connectivity restores the previous data state, and that any elected primary is suitable for the application. Neither follows from an election result. This case separates authority, data history, and useful performance.

## Mechanism: three different contracts

For this teaching model, a safe database transition must satisfy three contracts:

1. **Authority:** which node may accept writes, and how are former writers prevented from continuing?
2. **History:** which acknowledged writes exist on each candidate, and how will differences be reconciled?
3. **Service:** can callers meet their latency and correctness requirements against the resulting topology?

An election protocol can establish a leader under its rules without copying every application record or checking every caller's timeout. Treat those as separate proofs. **Fencing** means preventing an obsolete owner from carrying out operations; announcing a new owner alone does not demonstrate that the old owner is unable to act.

Suppose two copies share history `C`, then one contains `C + A` while the other contains `C + B`. Choosing the copy with the newest timestamp does not preserve both branches. Concatenating changes is also unsafe when operations conflict: two independent updates to an exclusive ownership record cannot both remain authoritative. The application needs a reconciliation rule, not merely a reachable database.

These are general course models. They do not assert which fencing mechanism GitHub used internally.

## Published account

**Reported by the operator:** GitHub traced its October 21, 2018 incident to maintenance that interrupted connectivity between an East Coast network hub and data center. Connectivity returned after 43 seconds; service degradation lasted 24 hours and 11 minutes. This is GitHub's account of its own system. [GitHub's post-incident analysis](https://github.blog/news-insights/company-news/oct21-post-incident-analysis/)

During the partition, Orchestrator promoted West Coast database primaries. Both regions then contained writes absent from the other. The application could not tolerate the resulting cross-country database latency, while immediate failback risked data integrity. Engineers chose recovery that preserved accepted writes. [GitHub's topology and recovery explanation](https://github.blog/news-insights/company-news/oct21-post-incident-analysis/)

Recovery involved restoring databases, synchronizing replicas, returning to a viable topology, and processing queued work. GitHub planned to prohibit automatic promotion across regions. The report describes expired webhook payloads during backlog processing. It says user data was not lost, while reconciliation of some database writes remained in progress when published. This does not establish independently verified, lossless delivery of every event. [GitHub's recovery and reconciliation account](https://github.blog/news-insights/company-news/oct21-post-incident-analysis/)

## Worked example: reachable but too slow

**Synthetic assumptions:** An application holds one of 200 worker slots for each request. Each request performs 12 sequential database round trips and 40 ms of other work. Local round trips take 1 ms; a proposed remote topology takes 70 ms. Ignore database compute, queueing, retries, and variation. These invented values illustrate a bound, not GitHub's timings.

```text
Local service time = 12 * 1 ms + 40 ms = 52 ms
Remote service time = 12 * 70 ms + 40 ms = 880 ms
Local concurrency ceiling = 200 / 0.052 = about 3,846 requests/s
Remote concurrency ceiling = 200 / 0.880 = about 227 requests/s
```

At an arrival rate of 600 requests/s, the remote topology accumulates at least `600 - 227.27 = 372.73 requests/s` while all slots remain occupied under these assumptions. After a minute, that is about `372.73 * 60 = 22,364` waiting requests, unless admission rejects work or a queue limit intervenes.

A 500 ms request deadline is already impossible for the modeled remote path before queueing. Increasing worker count might increase concurrency, but it cannot reduce the 880 ms sequential dependency chain. It may instead send more simultaneous work to a database that is already busy recovering.

The decisive measurement is an end-to-end transaction in the proposed topology. A successful connection and leader-election status do not test this contract. Parallelizing queries could alter the bound, but only if their data dependencies permit it.

## What would you do?

The old primary responds quickly again. The promoted primary has accepted new writes. An operator suggests pointing all clients back immediately because the network incident lasted less than a minute. What decides whether that is safe?

<details>
<summary>Reasoned answer</summary>

First establish writer authority and preserve both histories. Compare acknowledged writes and replication positions, identify conflicts, and use a tested reconciliation or recovery procedure before changing ownership. If safe writes cannot be guaranteed, constrain admission instead of creating another branch. Assess read freshness separately. In parallel, measure the current topology's useful transaction capacity and choose a load limit it can sustain. Restoring the old route is evidence about connectivity, not proof that the old database contains all accepted work.

</details>

## Tradeoffs and counterfactual

**Course judgment:** Automatic failover should be restricted to topologies whose data and application contracts have been tested. A narrower failover policy can lengthen unavailability during a real regional failure. A broader policy can preserve access only if callers, replication, and ownership rules support it. Neither policy is universally safer.

A counterfactual with no promotion would avoid creating a new writing branch, but could leave the service unavailable for an unknown partition duration. That is a choice between specific risks, not proof that automation itself was the mistake.

## Transfer to AI infrastructure

**Course inference:** Apply the same three contracts to scheduler leadership, job ownership, checkpoint publication, and model-registry promotion. A restarted scheduler must not authorize duplicate exclusive work. A reachable checkpoint store may still be too distant for the recovery objective. Validate the whole transaction and preserve the history needed to distinguish completed work from retries.

Continue with [committed checkpoint state](../curriculum/04-fabric-storage.md), [Kubernetes quorum reasoning](../tracks/kubernetes/11-operability.md), and [recovery-mode selection](../curriculum/15-incidents-and-change.md).

**Evidence limits:** The operator article is the historical authority here. Internal database logs, individual customer outcomes, and later reconciliation completion were not examined.
