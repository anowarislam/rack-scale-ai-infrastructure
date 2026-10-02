# Month 20 instructor key - sealed by convention

Ground truth: rank 1 waits 280ms on synchronous checkpoint work before entering the collective. Other ranks spend 320ms in the collective, including waiting for rank 1. Every regressed step is `80+280+40 = 400ms` on rank 1 or `80+0+320 = 400ms` elsewhere. Baseline is 120ms. The supplied switch warning is outside the recorded traffic path.

| Time | Inject | Expected response |
|---|---|---|
| 15 min | Four neighboring checkpoint jobs start together; one started in baseline | Investigate shared destination concurrency, not just NIC counters |
| 30 min | An independent small collective control is unchanged; compute kernel durations are unchanged | Weaken pure compute and network-service hypotheses without claiming all fabric faults excluded |
| 45 min | A stakeholder proposes disabling checkpointing entirely | Reject invalidating recovery to improve speed; choose one phase-offset intervention |

Release 20-trial-results.json only after the learner states a mechanism and guardrails. Aggregate baseline rate is `3000/1200 = 2.5` useful units/s; staggered rate is `3000/420 = 7.142857...`. Rate improvement is 185.7%; elapsed reduction for equal work is 65%. Three designed pairs provide mechanism evidence inside the scenario, not a fitted confidence interval or a population performance promise.

Fault-free control: with one checkpoint writer, baseline and staggered conditions both complete 1,000 units in 120 seconds and restore successfully. A 20% compute slowdown in a separate changed-input defense raises compute from 80 to 96ms; checkpoint staggering does not remove that compute cost. Decoy: the switch warning and the largest collective timer.

Answers: (1) it can be waiting for a late participant; (2) when phases overlap or use different measurement scopes; (3) useful work includes correctness and preserved recovery objectives; (4) a large claimed gain despite unchanged overlap suggests another variable or a measurement error.

Require a valid reversal/control and explicit uncertainty. Remediate a network-first diagnosis by giving a new trace with equal arrival times and longer communication on every rank; the learner must update the diagnosis rather than memorize "collectives mean storage." Reset removes exercise-only phase offsets and verifies checkpoint restore. No real hardware result is asserted by this key.
