# Cloudflare, November 2023: three sites can still contain one critical dependency

**Decision question:** If a whole facility disappears, which user functions remain available, which become delayed, and how long can the delayed functions wait before information is lost?

Distributing a service across sites does not necessarily distribute its dependencies. Redundancy belongs to the complete path delivering a function. A required service, credential, artifact, or queue can recreate a single failure point underneath healthy replicas.

## Published account

**Verified source; operator account.** Cloudflare reports a control-plane and analytics outage beginning November 2, 2023, after a power failure at its PDX-04 facility. Some services depended on components present only at that site despite participating in a wider high-availability design. Cloudflare had tested partial failure boundaries, but not complete loss of that facility.

Most control-plane service was restored through disaster recovery by 17:57 UTC on November 2. Full restoration was reported at 04:25 UTC on November 4; some logging data could not be recovered. Cloudflare states that traffic through its network continued while customers experienced control and analytics limitations. It announced stricter recovery-plan requirements and full-facility failure testing. Its account labels parts of the electrical sequence as informed speculation because provider confirmation was incomplete. The site's detailed electrical cause is not independently established here. [Cloudflare's November 4 postmortem](https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/)

## Mechanism: draw functions, not just replicas

**Course model.** Consider an invented management service with replicas A, B, and C and one mandatory audit writer K. The service can accept a change only when at least one replica and K are available:

```text
change available = (A OR B OR C) AND K
```

Moving A, B, and C into separate facilities does not remove K from the expression. The relevant question is whether K is genuinely mandatory. Some operations might safely queue an audit record; others may require a durable record before acknowledging a security-sensitive change. That decision belongs in the service contract. Calling every dependency optional to improve uptime can trade an outage for lost integrity.

Next distinguish the normal path from the recovery path. A service may continue with its current configuration but need unavailable identity, artifact storage, or naming services to restart. A replica count describes neither path fully. Draw both and mark each dependency's facility, authority, and capacity limits.

Buffering changes an immediate failure into a deadline. To claim that delayed processing is acceptable, specify the arrival rate, free durable capacity, maximum delay, restart time, and catch-up throughput. A queue that survives a short test can still fill during a longer incident. Its recovery must handle new arrivals as well as old work.

## Worked example: backlog must drain while work keeps arriving

**Synthetic inputs.** A logging queue has `2 TB` of free durable capacity. Records arrive at `80 MB/s`, and the processor is unavailable for four hours. Use decimal units, fixed-size accounting, and constant rates; ignore compression and storage overhead.

```text
Time until full = 2,000,000 MB / 80 MB/s
                = 25,000 s = 6 h 56 min 40 s
Four-hour backlog = 80 MB/s * 14,400 s
                  = 1,152,000 MB = 1.152 TB
```

After restoration, assume processing capacity is `140 MB/s` while arrivals remain `80 MB/s`. Only `60 MB/s` is available for catching up. Drain time is therefore:

```text
1,152,000 MB / (140 - 80) MB/s = 19,200 s = 5 h 20 min
```

It is incorrect to divide by `140` and treat the processor as serving only the backlog. At the instant processing resumes, the queue is still holding four hours of delayed records. A green process health check does not mean analytics are current.

The model also distinguishes loss from lateness. A ten-hour processor outage would exceed the queue's capacity deadline. What happens then depends on the designed policy: reject new work, discard records, or interrupt the function that generates them. None is automatically acceptable for all record types.

## What would you do?

In this synthetic system, the processor's repair estimate becomes ten hours. The manager says that user traffic is still serving, so no further action is needed. How do you respond?

<details>
<summary>Reasoned answer</summary>

Explain the remaining buffer deadline and identify which functions require these records. Confirm actual free capacity and arrival rate, then evaluate an alternate processor or durable sink before capacity is exhausted. If reducing record volume is an authorized option, preserve mandatory audit data and disclose the lost observability. Keep traffic availability, ability to change configuration, data durability, and analytics freshness as separate incident status lines. An uncertain repair estimate cannot justify assuming the queue will survive.

</details>

## Mitigations, tradeoffs, and counterfactual

Assign each user function a failure contract and test it at the intended boundary: process, host, rack, or whole site. A lower-level test provides evidence only for that lower-level event. Inventory recovery dependencies as carefully as serving dependencies, including how operators obtain the artifacts and authority needed after a site disappears.

More buffering buys time at a storage and retention cost. Extra processing capacity shortens catch-up but can sit unused normally. Synchronous replication can improve durability while adding latency and failure coupling. Select among these mechanisms from the function's requirements rather than maximizing a single availability number.

**Counterfactual:** additional application replicas would not make the invented expression true if K remained unavailable. Making K independent could preserve change availability, but would still leave queue capacity and recovery sequencing to validate.

## Transfer to AI infrastructure and limits

**Course inference.** A GPU fleet can continue an admitted job while losing telemetry, checkpoint catalog access, or the ability to admit replacements. Report those functions separately. Use [power and telemetry](../curriculum/05-power-telemetry-security.md) to distinguish measured condition from stale evidence, and [rack readiness](../practicum/22-rack-readiness.md) to define the proof needed before readmission.

The historical account is primary evidence of Cloudflare's observations and conclusions. The Boolean model and queue arithmetic are original teaching examples. This page does not audit the facility provider, validate electrical equipment, reproduce the event, or establish the current service topology.
