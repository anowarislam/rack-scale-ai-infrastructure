# Month 13: Establish fleet truth before acting

A green fleet dashboard is a claim. Your job this month is to decide whether the underlying observations justify that claim. Begin after G2 with a primary platform you can inspect and a record of its topology. This lesson uses L0 synthetic records first; importing real read-only evidence is optional and requires redaction.

**G3-E01** assesses two outcomes: **G3-O01**, reconcile authoritative fleet state, and **G3-O02**, verify telemetry freshness and time. The exercises below form one evidence bundle, not extra gate assessments. The course's [gate rubric](../assessments/gates.md) applies.

## What is authoritative, and for which question?

An inventory database may own the intended rack position. A BMC may report a chassis serial. A host may know its current boot ID. A scheduler knows which work it believes is allocated. None of these alone proves the physical location, current identity, ownership, and availability of a machine. Authority is a field-specific responsibility, not a property of a database's name.

Use this contract before merging records:

| Question | Proposed authority | Independent check | Disagreement action |
|---|---|---|---|
| Which asset is this? | Registered immutable asset ID and serial | Read-only management inventory | Quarantine identity for write actions |
| Who owns the asset and the service? | Owner register | On-call and escalation record | Escalate; do not infer from hostname |
| What should run here? | Approved desired configuration | Signed change record | Preserve desired/observed distinction |
| What is running now? | Current boot-scoped host observation | Platform and management observations | Mark mismatch; investigate freshness |
| Can it accept work? | Admission state plus workload qualification | End-to-end probe and dependencies | Require all necessary postconditions |

This table is a course design, not a vendor standard. Its value is that it makes a disagreement actionable. A replacement motherboard, reused IP, or renamed host must not silently inherit permission to receive an old action. Bind observations and work to an asset identity plus an incarnation such as a boot ID or generation.

Desired state says what should be true. Observed state says what a named observer saw at a named time. Unknown is a valid observed state. Never convert a missing row to zero errors, a removed machine to repaired, or a successful request submission to completed work.

## A timestamp needs an error model

Verified public fact: OpenTelemetry distinguishes the time recorded by an event's source from the time the collection system observed it. It does not make those two clocks equal. Preserve both fields when constructing an incident timeline. [OpenTelemetry Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/)

Let `source_time` be the timestamp on the originating clock and `offset` be source clock minus reference clock. Then `corrected_time = source_time - offset`. Record offset uncertainty too. An event at reference time `990 +/- 2` could have occurred between 988 and 992. Two overlapping event intervals cannot establish a strict order by timestamps alone. Sequence numbers and request IDs can add ordering evidence within their own scopes.

Verified public fact: NTP's four-timestamp exchange estimates offset and round-trip delay. That is a timing mechanism, not a promise that every event can be globally ordered without uncertainty. [RFC 5905, section 8](https://datatracker.ietf.org/doc/html/rfc5905#section-8)

## Worked example: fresh dashboard, old machine

**Synthetic calculation.** Reference time is 1,000 seconds. A temperature event says source time 970, observed time 998, clock offset +40, and uncertainty 1. Its corrected event time is 930. Its conservative age is `1000 - 930 + 1 = 71 s`. The dashboard's ingest age is only `1000 - 998 = 2 s`. Under a declared 30-second freshness requirement, the event fails even though the collector is active.

The event also carries boot ID `boot-a1`, while inventory expects `boot-a2`. Replaying the previous boot's last good value could explain both observations. That is a hypothesis, not a confirmed cause. A fresh boot-scoped read is the discriminating check. If node B has no row, coverage is one of two expected assets, not 100% of reporting assets. The denominator changes the conclusion.

If a second source event is stamped 1,030 with measured offset +40, its corrected time is 990; do not reject it merely because the uncorrected timestamp is in the future. Time correction must use independently supplied clock evidence, not an offset chosen to make a check pass.

## Worked example 2: a precise timestamp cannot identify the asset

**Synthetic reasoning.** At 10:00, a registry maps hostname `worker-7` to serial `SYNTH-OLD`, boot 4. At 10:02, a replacement maps the same hostname to `SYNTH-NEW`, boot 1. An action queued at 10:01 reaches the host at 10:03. Its timestamp is fresh and its hostname resolves correctly, but its target identity is no longer the same. A hostname-only guard permits the wrong action. Comparing the expected serial and incarnation rejects it and forces a new decision.

Now consider two events from the replacement. A management event has corrected time `100 +/- 3`; a host event has `102 +/- 2`. Their possible intervals are [97, 103] and [100, 104]. The intervals overlap, so clock evidence alone does not establish which came first. If the host event includes the management request's operation ID and records its completion, that causal linkage provides stronger ordering evidence than choosing timestamp midpoints.

**Counterexample.** Two records can have different ingestion timestamps merely because one collector buffered its input. Sorting by arrival time produces a clean-looking timeline and the wrong sequence of system events. Preserve the distinction among source time, observation time, uncertainty, and causal identity.

## Run the investigation

From the repository root:

```sh
python3 labs/fleet/fleet_lab.py signal labs/fleet/fixtures/signal-fault.json
python3 labs/fleet/fleet_lab.py signal labs/fleet/fixtures/signal-healthy.json
```

The first command intentionally exits 1. Save its output. Before reading the healthy fixture, write three competing explanations: old boot replay, source clock error, and missing collection. State the next observation that would distinguish each.

1. Copy the fault fixture into your own evidence directory. Preserve its `synthetic: true` label.
2. Create a reconciliation table for every expected asset, including absent assets. Identify which fields are known, conflicting, and unknown.
3. Calculate both event and collection ages by hand, with the declared uncertainty. Run the validator and compare.
4. Produce a corrected fixture representing a new observation, with an explicit synthetic change record. Do not edit the original observation and call it repaired history.
5. Inject a unit error using [the unit fixture](../labs/fleet/fixtures/signal-unit-fault.json). Explain why converting 55,000 mC to 55 C needs a source unit contract, not an assumption that a large value is impossible.
6. Re-run your new snapshot, show a passing result, then duplicate a sequence number and show that the detector fails again. Retain both results.

No temperature in this exercise is a vendor operating limit. The validator checks data integrity, not thermal safety.

## Evidence to submit

- Field-authority table, source provenance, exact fixture hashes, and command transcript.
- Asset coverage denominator and reasons for every exclusion.
- Timestamp calculation, offset source, uncertainty, boot/sequence scope, and competing hypotheses.
- Failed original, newly observed corrected state, and deliberately reintroduced fault.
- One admission rule that fails closed on ambiguous identity, plus its operational cost.

Passing requires detecting the stale source, old boot, and missing node independently. A passing JSON result alone does not demonstrate reconciliation.

## Misconceptions to challenge

"Last writer wins" can replace a correct inventory with an old delayed event. "The monitoring process is up" does not mean every expected source is represented. "All timestamps are UTC" describes a representation, not clock accuracy. "The BMC is authoritative" is incomplete until the field, identity, and observation interval are named.

## Retrieval and transfer questions

1. Why is hostname alone unsafe as an action target after replacement?
2. An event has source time 505, offset +10, uncertainty 3; now is 520 and maximum age is 25. Does the conservative freshness test pass?
3. Ten of twelve expected nodes report zero errors. What fleet-health statement is justified?
4. Two events have corrected intervals [100, 104] and [103, 107]. Can you conclude which happened first?
5. What evidence would distinguish a collector backlog from a currently hot component?

## Reasoned answers - read after attempting

1. A reusable name can bind a previous asset's queued action to new hardware. Require stable asset identity and the intended incarnation, then recheck at execution.
2. Corrected time is 495; oldest plausible time is 492. Conservative age is 28, so it fails. The best-case age of 22 is insufficient to establish the requirement.
3. Ten reporting nodes had zero recorded errors during their valid observation windows. Two nodes are unknown. There is no justified twelve-node healthy claim.
4. No. The intervals overlap. A causal request/response or scoped sequence record may resolve the order; choosing the midpoint does not.
5. Compare source and observation times, queue/drop counters, source sequence continuity, independent fresh measurement, and the asset's current incarnation. A backlog predicts old event times with recent arrivals; real heat requires valid current measurements.

## Four-week study plan

| Week | Nine-hour allocation | Reviewable result |
|---|---|---|
| 1 | Concepts 2h; primary sources 1h; field-authority map 4h; recall 2h | Reconciliation contract |
| 2 | Timing calculations 2h; fault lab 4h; competing hypotheses 2h; review 1h | Original failure evidence |
| 3 | Corrected snapshot and reinjection 4h; platform mapping 3h; defense 2h | G3-E01 draft |
| 4 | Remediation 4h; changed-input replay 3h; archive 2h | Assessed bundle and limitations |

Weeks 1-3 are the active unit; week 4 is reserved for consolidation and reassessment. Continue to [Month 14](14-reliability.md). Retain your signal contract for [Month 19](../practicum/19-inherit.md).
