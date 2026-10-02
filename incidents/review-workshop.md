# From a failure story to an incident review

Produce a review that another engineer can challenge and use. A good submission explains the mechanism, preserves uncertainty, and ties each proposed action to a test. It does not need to recreate a company's internal incident document.

Use this after [the reading method](reading-method.md) and at least two [cases](README.md). The exercise is optional course practice and fits the reasoning work in [month 15](../curriculum/15-incidents-and-change.md). It does not replace an assessment gate or prove experience leading a production incident.

## Compare mechanisms, not company names

Choose a pair and answer the question before reopening the two reports.

| Pair | Comparison to defend |
|---|---|
| [Meta network](01-meta-network.md) and [GitHub partition](02-github-partition.md) | Why might network connectivity be necessary but insufficient for recovery? Separate reachability from state correctness. |
| [Cloudflare regex](03-cloudflare-regex.md) and [Fastly bug](04-fastly-latent-bug.md) | How would your test plan distinguish bounded runtime cost from coverage of rare valid states? |
| [OpenAI control plane](05-openai-control-plane.md) and [EBS recovery storm](11-ebs-remirroring.md) | Which locally useful operation can become harmful when every client or repair worker performs it together? |
| [GitLab restore](07-gitlab-backups.md) and [Cloudflare power](08-cloudflare-power.md) | Which recovery assumptions depend on state, and which depend on physical independence? |
| [Llama training](09-llama-training.md) and [silent corruption](10-silent-corruption.md) | What different evidence is required to measure useful progress and correct progress? |
| [S3 recovery](06-s3-recovery.md) and [Google network](12-google-network.md) | Where should an automation scope limit be enforced so that a mistaken input cannot bypass it? |
| [OpenAI isolation](13-openai-data-isolation.md) and [silent corruption](10-silent-corruption.md) | Why can successful requests and green process-health metrics miss a service-contract violation? |

These are our questions for comparison. The reports do not establish that two operators used the same architecture or remediation.

## A complete synthetic incident packet

All events, measurements, capacities, and roles in this exercise are invented. Treat them as the available record, not as hidden facts from a real outage. There is no need to run a cluster.

Six inference workers serve a total of 300 requests/s. Each can sustain 80 requests/s for this fixed request mix. A metadata service handles at most 400 equal-cost operations/s in the simplified model. Normal clients generate 120 metadata operations/s. Existing inference workers can keep serving from cached metadata; creating or replacing a worker requires this metadata service.

A new inventory collector is deployed to six agents. In this version, each agent generates 150 metadata operations/s. In the model the queue is unbounded, FIFO, begins empty, and loses no requests. There are no retries, timeouts, or changes in service rate unless an event says otherwise. These simplifying assumptions make the arithmetic possible; a real queue needs its own measurements.

| Time | Available observation |
|---|---|
| Before 00:00 | Normal metadata arrivals are 120 operations/s. Inference succeeds at 300 requests/s. |
| 00:00 | All six collectors begin sending 150 operations/s each. |
| 01:30 | Queue depth is 55,800 operations. A proposal arrives to restart every inference worker. |
| 01:30 | The response team can pause the collectors through a separate, tested management path. The existing queue cannot be safely discarded under the exercise rules. |
| 02:00 | In a separate branch of the exercise, a rack fault could remove two inference workers. Assume load is balanced across surviving workers without extra metadata operations. |

Stop here. Decide whether to restart, pause, shed load, or wait. Calculate the queue-drain time after your action. State which observation would falsify your explanation.

<details>
<summary>Worked incident review</summary>

**Impact and scope.** At the reported observation point, the metadata queue threatens replacement and management operations. The packet does not report failed inference requests. Report degraded control operations and a risk to replacement; do not invent a full serving outage.

**Mechanism.** The collectors add `6 * 150 = 900` operations/s. Total offered work is `900 + 120 = 1,020` operations/s, exceeding the modeled capacity by `620` operations/s. Over 90 seconds, the expected backlog is `620 * 90 = 55,800` operations, matching the packet. The match supports the load explanation within the model. In a real investigation it would not independently prove constant service cost or eliminate a coincident service-rate reduction.

**Immediate action.** Pause the collectors through the stated surviving management path. Keep healthy inference workers running. Restarting all of them introduces a dependency on a service already unable to keep up and gives up the cached-state advantage. This decision relies on the packet's claim that existing workers can serve correctly with cached metadata; without that claim, freshness and authorization would require investigation.

**Drain estimate.** With collectors paused, normal arrivals remain 120 operations/s, leaving `400 - 120 = 280` operations/s for the backlog. Drain time is `55,800 / 280 = 199.2857` seconds, approximately 3 minutes 19 seconds after the pause. This is a deterministic estimate under the queue assumptions, not a real-world restoration promise. An observed drain slope far below 280 operations/s would challenge the service-rate or arrival-rate assumptions.

**Capacity branch.** Losing two inference workers leaves `4 * 80 = 320` requests/s, just 20 above demand. Utilization relative to that simplified capacity becomes `300 / 320 = 93.75%`. This arithmetic proves only aggregate capacity under the fixed request mix and ideal balancing. It does not prove a latency objective at that utilization. A third worker loss leaves 240 requests/s, so at least 60 requests/s need deferral, shedding, or qualified additional capacity under this model.

**Recovery evidence.** Check that all collectors actually stopped, the metadata queue drains, an isolated replacement operation completes, and inference correctness and service objectives remain satisfied. A low queue after clients stop sending would not prove that replacements work. Finish by recording which collector version remains disabled and who owns a qualified return to service.

</details>

## Write the corrective actions

The following proposals address different parts of the synthetic causal chain. An owner is a role in this exercise, not a statement about a real organization.

| Owner role | Proposed change | Closure evidence | Residual limitation |
|---|---|---|---|
| Collector owner | Give collection work an enforced aggregate request budget below spare metadata capacity | A six-agent test plus a larger-client test shows admitted collection work stays within budget | The budget must be revisited when normal load or operation cost changes |
| Metadata owner | Separate lower-priority inventory work from operations needed for service recovery | Under injected collection overload, a replacement probe completes within its defined objective | Priority alone does not create capacity; starvation and fairness still need review |
| Release owner | Test collector behavior against a representative dependency and bound expansion by dependency impact | A deliberately excessive collector release is stopped before the next scope expansion | A finite canary may still miss a rare state or a larger scale boundary |
| Incident lead | Preserve and exercise the independent pause path | A bounded rehearsal disables collectors while their ordinary metadata dependency is unavailable | The pause path has its own credentials, network, and availability assumptions |

There is no magic number for the safe request budget in the packet. Normal work consumes 120 of the modeled 400 operations/s, but allocating all remaining 280 to inventory leaves no margin for bursts, uncertainty, or recovery. Choose a proposed margin, justify what it protects, and label it as a design decision requiring measurement.

## Your reusable review sheet

Copy these prompts into a local note under `learner-work/`. Link the public sources you actually read and date your review.

1. **Contract and impact:** who could not do what, over which observed interval? What remains unknown?
2. **Causal chain:** trigger, local effect, propagation, containment boundary, and recovery obstruction. Mark the evidence for each arrow.
3. **Alternative explanation:** what else fits the observations, and what would distinguish it?
4. **Decision point:** what information was available then? Which action preserved the most useful options?
5. **Recovery proof:** which availability, state, correctness, and isolation properties must be checked separately?
6. **Actions:** choose two specific changes, owner roles, verification experiments, and residual risks.
7. **Transfer:** name one dependency your own system shares with the case and one important difference that could invalidate the analogy.

Review on four dimensions: fidelity to the source, clarity of the mechanism, defensibility of the recovery decision, and strength of the action tests. For each dimension, mark **unsupported**, **partly supported**, or **supported by named evidence**. A reviewer should be able to identify the exact missing premise. This is a practice rubric, not an additional course certification.

Return to [the casebook](README.md) or continue with [the compound recovery practicum](../practicum/21-recovery.md).
