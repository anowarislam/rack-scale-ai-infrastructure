# Amazon S3, February 2017: surviving a restart is a separate design problem

**Decision question:** What should a maintenance tool prove before removing capacity, and what should a recovery drill prove after the serving process loses its state?

The assumption to challenge is that tolerating individual failures demonstrates recovery from a much larger interruption. A running service can spread incremental work across many machines. Restarting it may require ordered reconstruction, validation, and dependency startup. The relevant capacity and critical path can be different.

## Published account

**Verified source; operator account.** AWS reports that at 09:37 PST on February 28, 2017, an incorrect command input removed more S3 subsystem capacity than intended in US-EAST-1. An authorized operator was following a maintenance playbook. The affected index and placement subsystems required full restarts. The index supported object operations; placement depended on it and was additionally needed for writes.

AWS attributes prolonged restoration to growth since those subsystems' previous full restarts and the time required for metadata safety checks. GET, LIST, and DELETE were fully functioning at 13:18 PST; placement completed recovery at 13:54, restoring normal S3 operation. Dependent services still needed to clear accumulated work. AWS describes subsequent safeguards on capacity removal and further partitioning work. These are statements about that regional incident, not present-day S3 architecture or measured recovery guarantees. [AWS's service-event summary](https://aws.amazon.com/message/41926/)

## Mechanism: two different budgets

**Course analysis.** A maintenance budget limits how much functioning capacity can disappear. A recovery budget limits how long the system can remain unable to reconstruct useful service. Neither follows automatically from the other.

For a hypothetical subsystem, define:

```text
additional removable capacity
  = currently healthy capacity
  - minimum required capacity
  - capacity already reserved for other removals
```

Evaluate this inequality for every subsystem an operation touches. A tool scoped to a named maintenance task might still affect shared processes or hosts. A check against only the task's nominal subsystem would miss that dependency.

The check and reservation must also work together. If two operators each observe the same spare capacity and then remove it independently, both decisions can appear safe while their combined result is unsafe. A central reservation or another enforceable coordination mechanism addresses that race; adding another confirmation prompt does not.

Recovery has its own graph. If step B requires validated output from step A, adding workers to B cannot make A finish sooner. Estimate a lower bound from the longest required chain, including data movement, consistency checks, and readiness validation. A service returning its first successful request is a useful milestone, but it does not establish all operations or all dependencies have recovered.

## Worked example: quantify the cold path

**Synthetic scenario.** A metadata service must read `1.2 TB` before validation. Use decimal units: `1 TB = 1,000,000 MB`. Effective aggregate read throughput is `200 MB/s`. Validation takes 20 minutes, placement startup requires validated metadata and takes 15 minutes, and final service checks take 5 minutes. Assume those phases cannot overlap.

```text
Read time = 1,200,000 MB / 200 MB/s = 6,000 s = 100 min
Earliest validated service = 100 + 20 + 15 + 5 = 140 min
```

Doubling the number of readers does nothing if they still share a `200 MB/s` bottleneck. Doubling effective aggregate throughput to `400 MB/s` reduces total time to `50 + 20 + 15 + 5 = 90` minutes. It halves only the read phase.

Now consider six balanced, independent cells. A single failed cell contains `200,000 MB`. If it retains the same `200 MB/s` throughput and the same later phase durations, its recovery bound becomes `1,000 s + 40 min = 56 min 40 s`. The unaffected cells can continue under the model's independence assumption.

That last condition matters. If all cells must restart and share one recovery device, assigning each the full device throughput overstates the benefit. Partitioning reduces a failure's scope only when placement, control, and recovery dependencies preserve the intended boundary. These numbers describe a proposed system, not S3 measurements.

## What would you do?

A synthetic region has six cells. A drill recovers one idle cell in 57 minutes, so a proposal promises regional recovery within an hour. Accept the promise?

<details>
<summary>Reasoned answer</summary>

No. The drill supports one cell under the tested competing load. Inventory shared recovery storage, network links, credentials, orchestration, and operator steps. Exercise concurrent recovery or produce a conservative capacity model for it. Also state whether the objective means initial reads, restored writes, ordinary latency, or cleared dependent backlogs. The one-cell result remains valuable evidence, but its scope must accompany the number.

</details>

## Mitigations, tradeoffs, and counterfactual

Enforce removal limits where the action is admitted, with reservations for concurrent work and a verified mapping from targets to affected services. Stronger restrictions can slow emergency maintenance, so design a separately controlled emergency path whose consequences are explicit.

Keep recovery datasets, startup dependencies, and validation durations in capacity planning. Test with realistic data volume and storage contention. Smaller cells can bound reconstruction work and reduce the population affected by one failure, at the cost of more placement decisions, fragmented spare capacity, and additional boundaries to operate.

**Counterfactual:** a perfect input validator could block the initiating maintenance mistake while leaving the cold recovery problem untouched. Hardware loss or another fault could still require that path. Conversely, faster recovery reduces duration but does not justify removing too much capacity.

## Transfer to AI infrastructure and limits

**Course inference.** Object access can sit beneath model loading, dataset reads, container startup, and checkpoint restoration. A useful AI recovery plan distinguishes already-running work from new work and recovery work. Trace these paths in [fabric and storage](../curriculum/04-fabric-storage.md) and apply the recovery modes in [Month 15](../curriculum/15-incidents-and-change.md).

The public report supports the historical ordering and times. The model supplies reasoning about a hypothetical design. No production restart was performed here, no internal AWS topology was inspected, and the one-cell example is not a present-day S3 service-level claim.
