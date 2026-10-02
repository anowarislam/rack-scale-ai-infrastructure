# Month 19 instructor key - sealed by convention

Open after the learner's first attempt. Synthetic ground truth: node A's event is from its prior boot and has corrected source time 930 at reference time 1000. Its oldest plausible age is 71 seconds. Node B is expected but absent. The collector's recent observation time does not fix either issue. The capacity model permits 72, not 80, GPUs after one domain loss with 20% remaining headroom and 8-GPU jobs.

## Inject release

| Time | Release | What it tests |
|---|---|---|
| 15 min | The owner register confirms node B remains in service; no decommission is approved | Do not delete missing assets from the denominator |
| 30 min | A fresh read from A's stable serial reports boot-a2; a collector backlog retained the old event | Distinguish identity/time cause from hardware failure |
| 45 min | A stakeholder offers to set headroom to zero to keep the 80-GPU promise | Preserve or explicitly renegotiate policy rather than disguise a failed model |

If the learner requests an independent current observation for a stated hypothesis, release the relevant fact early and note that choice. Do not volunteer a repair command.

Fault-free control: use signal-healthy.json and capacity-recovered.json. The expected result is both PASS, with 72 GPUs committed; still no claim of full-fleet telemetry from the two-node excerpt. Decoy: the phrase "128 installed" is true but does not answer usable capacity under failure.

## Answers and scoring

1. Verify identity, expected coverage, and freshness before using health to authorize changes. Capacity arithmetic can proceed independently because its assumptions are explicit.
2. Check the authoritative lifecycle/decommission record against current stable asset identity, then inspect collection state. Absence from a metric query alone does not decide.
3. Reducing a promise changes admitted demand; adding capacity changes supply and requires qualification. They have different stakeholder and evidence consequences.
4. Real physical health, whole-fleet coverage, correct pooling/topology, workload latency, and actual clock source validity remain outside the supplied local proof.

Apply common rubric. Require explicit observed/unknown labels, a discriminating test, safe action, and preserved initial evidence. A wrong diagnosis that the learner corrects after an inject may earn full recovery credit if the unsupported earlier claim is acknowledged. Reassessment: change offset from +40 to +15 and remove the old-boot mismatch; learner must recalculate rather than repeat the key. Reset requires unchanged references and a new learner copy.
