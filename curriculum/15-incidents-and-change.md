# Month 15: Restore service and make the next change safer

The first incident decision is about protecting the service while preserving options. It need not wait for a complete root-cause narrative. The second is about who is allowed to change what. **G3-E03** assesses **G3-O05**, leading a bounded incident role, and **G3-O06**, selecting and verifying a recovery mode. Read [Month 14](14-reliability.md) before using rates to justify an incident decision.

## Separate impact, mechanism, and cause

Impact describes what users cannot do: a training run lost progress, requests missed a latency objective, or capacity could not be admitted. A symptom is an observation: a queue grew or a link reported retries. A mechanism explains a path: retries consumed workers, delaying otherwise healthy requests. A root-cause claim also explains why the mechanism was triggered and why defenses did not contain it.

Keep these separate in the incident record. "A new release caused latency" is too early if the only evidence is that the release and latency happened together. The same observations can fit increased request length, a shared dependency slowdown, a changed measurement window, or a bad rollout. A useful hypothesis predicts an observation that another explanation would not.

A mitigation reduces current impact. A corrective action reduces recurrence. A rollback may mitigate without explaining the initiating fault. Conversely, a correct root-cause document does not restore service. During an incident, decide what evidence is necessary for the next safe action, not what evidence would finish a paper.

## An operating structure that preserves attention

Verified public fact: Google's incident process separates command, operational work, communications, and planning, with a live incident state and explicit handoff. Adopt the responsibilities, then fit the staffing to the exercise. [Managing Incidents](https://sre.google/sre-book/managing-incidents/)

For this course, one incident commander maintains impact, priorities, ownership, and next decision time. One operations lead controls the mutation ledger. Investigators can inspect independently but propose changes to that lead. The communications owner states what is known, unknown, and next. The planning owner tracks dependencies, recovery state, and relief. One person may initially hold several roles; the record must make that visible.

A useful incident update is short: "Checkout inference latency exceeds the 2-second exercise objective for 18% of eligible requests. We stopped the canary and are validating the control pool. Storage and request-mix hypotheses remain open. Next update in 10 minutes." This is a synthetic example, not a production claim. It reports scope without inventing a restoration time. The 18% denominator is requests in the stated observation window; a p99 would instead describe a percentile of that window's latency distribution.

## Worked example 1: a fleet average hides a bad canary

**Synthetic calculation.** A service has a request-success objective of 99.9% over one million eligible requests. Its budget is `1,000,000 * (1 - .999) = 1,000` failed requests. This is an accounting allowance for the objective, not spare GPU capacity and not permission to ignore harmful failures.

A canary serves 500 requests and fails 10: 2%. The control serves 49,500 and fails 49: about 0.099%. The overall rate is `59/50,000 = 0.118%`. The global dashboard looks only slightly worse than the objective, while the canary group is much worse. At an unchanged 2% error rate, 10,000 additional canary requests would produce an expected 200 errors; this expectation is conditional, not a guaranteed outcome.

Decision steps:

1. Check that both groups use the same eligibility rule, time interval, and error definition.
2. Confirm telemetry coverage and that the canary label follows the serving instance, not just the deployment request.
3. Stop expansion because current evidence shows potentially harmful divergence.
4. Examine whether request size or backend assignment differs between groups.
5. Restore the previous supported configuration if its state compatibility and capacity are verified. Then re-run a comparable control workload.

Verified public fact: canary evaluation benefits from separating canary and control populations; shared dependencies can contaminate both, so a relative comparison also needs absolute service checks. [Canarying Releases](https://sre.google/workbook/canarying-releases/)

**Counterexample.** Both groups worsen together after the storage backend slows. A small difference between groups does not mean the release is safe, and rollback may not remove the shared bottleneck. The absolute success objective and dependency evidence prevent that false conclusion.

## Recovery is a choice among different state transitions

| Mode | What it means | Evidence needed before selection | Verification afterward |
|---|---|---|---|
| Rollback | Return to a prior supported version/configuration | Backward data compatibility, retained artifact, sufficient old-version capacity | Old version actually serving, state readable, workload correct |
| Forward recovery | Apply a supported correction from the current state | Diagnosed mechanism, validated fix, bounded expansion | Fix present and relevant invariant restored |
| Rebuild | Recreate the environment from known inputs | Durable state outside the rebuilt unit, identity and restoration plan | Correct identity, restored state, clean admission |
| Quarantine | Keep the affected asset out of service | Safe exclusion path, remaining service capacity | No new work assigned; evidence retained |
| Vendor recovery | Delegate recovery to authorized procedure/people | Exact BOM, support case, qualified actor, preserved evidence | Documented returned state and independent qualification |
| Irreversible outcome | A prior state cannot be recovered by approved means | Specific missing path or incompatible state | Honest loss record, containment, residual-risk decision |

A rollback plan that has never considered stored state is a command, not a recovery plan. A quarantine that leaves a scheduler accepting work is incomplete. A rebuild that reuses an old identity without revoking queued actions can create a second incident.

## Worked example 2: fastest restart is not least loss

**Synthetic decision.** A job writes a recoverable checkpoint every 20 minutes. At minute 57, a node fails. Checkpoints at minutes 20 and 40 are committed; a minute-55 upload is only a partial object. The apparent newest file would lose just two minutes, but it is not a validated checkpoint. The safe baseline loses 17 minutes of work and requires 8 minutes to restore, for 25 minutes until prior progress is regained if processing speed is unchanged.

A corrected binary can read the minute-40 checkpoint in 8 minutes. The prior binary cannot read its schema. A five-minute rollback is therefore not the faster valid recovery path; it would still need data conversion or an older checkpoint. Choose forward recovery only after its artifact and checkpoint compatibility are established. Otherwise quarantine the failing resource and restart a compatible worker from minute 40.

Recovery checks include checkpoint commit marker, shard completeness, workload progress, output correctness, duplicate side effects, and the absence of renewed assignment to the quarantined node. A successful process exit alone proves none of these.

**Counterexample.** If the change only altered a stateless routing configuration and the old route remains qualified, rollback may be both fast and reversible. The correct choice follows state compatibility, not a blanket preference for rollbacks or rollforwards.

## Bounded exercise: a 45-minute incident

Use [the failed lifecycle fixture](../labs/fleet/fixtures/lifecycle-fault.json) as the affected asset record. Three participants take command, operations, and observer roles; a solo learner can rehearse all three but cannot claim independently assessed leadership.

At minute 0, the observer reports failed qualification on a recently repaired node. At minute 10, the observer states that a stakeholder wants immediate promotion. At minute 20, the remaining pool is declared adequate for one hour but not indefinitely. At minute 30, telemetry qualification becomes available. These are exercise injects, not facts to discover from the JSON.

1. Declare impact and authority; write a mutation ledger before proposing a change.
2. Run the failed fixture and identify the actual blocking invariant.
3. Choose a mode from the table. Record why two alternatives are not currently justified.
4. Create your own recovery event sequence, preserving the failed events. Execute it locally and inspect the state history.
5. At minute 40, hand command to the observer with explicit acceptance. At minute 45, decide whether the incident can close and what remains as a problem item.

Use the [lab guide](../labs/fleet/README.md). All actions are local JSON simulation. No physical changes, live firmware operations, or external messages are authorized by the exercise.

## Evidence and scoring

Submit the impact timeline, hypothesis table, mode decision, failed and recovered transcripts, role handoff, and two corrective actions with owner roles, due points, and objective closure evidence. An action such as "improve monitoring" is not closed by a ticket: specify a missing-source test and show it firing. The [common rubric](../assessments/gates.md) applies. If you bypass qualification to obtain green output, the action/recovery dimension fails.

## Questions

1. What is the difference between restoring availability and proving root cause?
2. Why can a global 0.118% error rate conceal a dangerous rollout?
3. Which facts decide whether rollback is possible after a data-format change?
4. When does quarantining a node fail to contain the incident?
5. Can a solo incident rehearsal establish longitudinal people leadership?

## Reasoned answers

1. Restoration shows that service postconditions hold again. Root cause requires an explanatory causal chain and discriminating evidence. Either can occur before the other.
2. The canary's 2% failure rate is diluted by a much larger control group. Preserve group denominators and absolute objectives.
3. Whether the old version can read/write the current state, whether conversion is supported, which checkpoints are valid, and what artifacts/capacity remain available.
4. When admission still assigns work there, existing work is not safely handled, dependencies keep routing through it, or the surviving pool overloads.
5. No. It provides course practice and may demonstrate a bounded technical decision. Sustained coaching, delegation, and organizational outcomes need observed follow-through over time.

## Four-week study plan

| Week | Nine-hour allocation | Result |
|---|---|---|
| 1 | Mechanisms 3h; worked examples 3h; incident record practice 3h | Recovery decision table |
| 2 | Scenario preparation 2h; role exercise 3h; analysis 4h | Failed/recovered sequence |
| 3 | Counterfactuals 3h; corrective actions 3h; peer defense 3h | G3-E03 draft |
| 4 | Remediation 4h; changed inject replay 3h; archive 2h | Assessed bundle |

Continue to [Month 16](16-lifecycle-automation.md).
