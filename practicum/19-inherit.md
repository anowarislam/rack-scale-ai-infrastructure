# Month 19: inherit Meridian without inheriting its assumptions

**G4-E01: G4-O01 and G4-O02.** Reconstruct an unfamiliar system and discriminate among explanations before changing it. This packet is fully runnable as L0; read-only inspection of your actual primary platform adds only the corresponding observed evidence.

## Rehearsal: how to turn a handoff into questions

A handoff says, "All workers are healthy; there are 32 GPUs free." Treat both clauses as hypotheses. First ask which workers are expected. Then ask what healthy means, who measured it, and when. Finally ask whether the 32 GPUs meet the incoming workload's topology, memory, and failure-reserve requirements. A statement can be accurate at the inventory layer and insufficient at the service layer.

**Worked example 1.** An inventory lists eight nodes; six emit recent heartbeats. Dividing six healthy nodes by six reporters produces 100%, but the expected-asset coverage is `6/8 = 75%`. The other two are unknown. If one missing node is intentionally decommissioned, reconcile that change first: only a justified seven-node expected set gives `6/7`, about 85.7%. Removing a missing node merely to improve the ratio is not reconciliation.

**Worked example 2.** A collector received an event two seconds ago, but source-time correction puts it 70 seconds in the past. A 30-second freshness policy fails. Restarting a healthy worker would target the wrong layer if the issue is a collector backlog. A current independent observation can distinguish the hypotheses without a disruptive change.

**Counterexample.** The event may also come from a previous boot on a reused hostname. A recent independent read that still targets only the hostname can repeat the identity mistake. Carry stable identity and incarnation through the check.

The theory is in [Month 13](../curriculum/13-fleet-truth.md). Verified public fact: monitoring a component internally and testing the service from outside answer different questions. Use both kinds of observation when defining health. [Google SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)

## Student brief and initial artifacts

You take over Meridian. The written handoff claims that 128 installed GPUs across four 32-GPU domains support an 80-GPU commitment while preserving 20% headroom after any single-domain loss. It also says the included two-node telemetry excerpt is current. The fleet uses your chosen primary platform; the actual platform version remains something you must record from G2 evidence, not infer from this story.

Initial artifacts:

- [Signal excerpt](../labs/fleet/fixtures/signal-fault.json).
- [Capacity commitment](../labs/fleet/fixtures/capacity-fault.json).
- The statement above, treated as an unverified handoff.
- Your existing primary platform architecture and workload contract.

You may read and calculate freely. You may change only learner-owned local fixture copies. Request further evidence by naming the hypothesis and the result that would change your decision. The instructor has [the separate key](instructor/19-key.md).

## Execute the investigation

```sh
python3 labs/fleet/fleet_lab.py signal labs/fleet/fixtures/signal-fault.json
python3 labs/fleet/fleet_lab.py capacity labs/fleet/fixtures/capacity-fault.json
```

Predict the failures before running. Build a map from workload to scheduler, nodes, accelerator/network/storage dependencies, management plane, and owner roles. Mark unsupported edges unknown. The two-node excerpt does not establish full-fleet coverage.

During a 60-minute episode, updates arrive at minutes 15, 30, and 45. At each update, revise the fact/hypothesis table and next action. Do not discard a superseded observation; annotate why its interpretation changed. Finish by proposing one safe baseline and one deferred decision.

Then create a corrected synthetic observation and a supportable capacity commitment in learner copies. Preserve the original records and the rationale for each changed field. Re-run the validators and explain what their PASS results do and do not establish.

## Evidence, abort, and reset

Submit the initial failure transcript, annotated topology/ownership map, authority/coverage table, hypothesis tests, corrected snapshot provenance, capacity calculation, and a 150-word incoming-operator handoff. Label missing ownership or authorization as unresolved; a name invented to fill a box is not evidence.

Abort any attempt to mutate an actual platform. If actual read-only evidence contains credentials or direct asset identifiers, stop copying it into the public exercise and use a restricted/redacted record. Reset by starting from clean local fixture copies; verify reference fixture hashes did not change.

Objective checks: evaluate source freshness, incarnation, and expected-asset coverage correctly; calculate the maximum commitment under the supplied model; distinguish full-fleet state from the excerpt; preserve uncertainty about causes not observed. A claim of "all 128 GPUs verified healthy" fails the evidence criterion.

## Questions before the debrief

1. Which claim in the handoff should be tested first, and why?
2. What single observation most efficiently distinguishes missing collection from decommissioning?
3. Why is correcting the commitment different from adding physical capacity?
4. What uncertainty remains after both local validators pass?

Answers and acceptable alternatives are in the instructor key; attempt them before opening it.

## Four weeks, two application units

Weeks 1-2: 9h/week on handoff analysis, source/identity checks, system map, timed episode, and initial evidence. Weeks 3-4: 9h/week on corrected local state, changed-input replay, peer handoff, and G4-E01 review. No new survey topic is introduced. Carry the baseline into [Month 20](20-performance.md).
