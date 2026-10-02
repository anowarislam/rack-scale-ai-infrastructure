# Month 20: find the layer that is making useful work wait

**G4-E02: G4-O03 and G4-O04.** Diagnose a cross-layer regression and validate one measurable intervention. Carry forward the trusted observation rules from month 19. All provided traces are synthetic L0 evidence; actual performance claims require an observed workload on the recorded hardware.

## A slow collective is not automatically a slow network

A distributed step completes when its required participants complete. If one rank arrives late at a collective operation, other ranks can spend time inside the collective waiting for it. A profiler that labels this interval "collective" is measuring where time was spent, not necessarily the cause of the delay.

**Worked example 1.** Two ranks normally compute for 80ms and communicate for 40ms, for a 120ms step. Rank 1 now spends 200ms waiting on a checkpoint before entering the collective. Rank 0 enters after its 80ms compute and spends 240ms in the collective: 200ms waiting for rank 1 plus 40ms communication. Both finish at 320ms. The longest measured collective is on the rank whose network did not become slower. Inspect arrival times and the late rank's preceding work.

This decomposition assumes serial phases in the example. In a real trace, compute, communication, and I/O may overlap. Summing overlapping durations overstates elapsed time; reconstruct the critical path and compare it with wall-clock step time.

**Worked example 2.** A change lowers mean step time from 300ms to 200ms. Elapsed time falls by `(300-200)/300`, about 33.3%. Throughput for the same useful work rises by `300/200 - 1 = 50%`. Those percentages answer different questions. If the new run skips required work, neither is a valid goodput gain.

**Counterexample.** A compute-bound workload with no exposed I/O wait will not improve because another job's checkpoint is staggered. A no-contention control should expose this. The [performance specialty](../specialties/performance.md) develops the same mechanism in more depth.

## Student brief

Meridian's fixed four-rank training workload now takes longer, while a dashboard reports increased collective time. A recent configuration change altered checkpoint start times for neighboring jobs. A switch warning also appeared that day. Your job is to diagnose the regression without treating either coincidence as causal proof.

Open [the synchronized phase trace](fixtures/20-performance.json). Units and the serial-phase assumption are declared in the file. The dataset and model IDs are synthetic labels, not cryptographic hashes. Preserve the output correctness result as one observation, not a guarantee about every future run.

```sh
python3 -m json.tool practicum/fixtures/20-performance.json
python3 labs/fleet/fleet_lab.py signal labs/fleet/fixtures/signal-clock-corrected.json
```

Use the second command to remind yourself that source-time correction may be legitimate. Do not modify clock offsets to make the performance story fit.

## Investigation procedure

1. Predict the slow rank and the exposed wait from the trace. Check that each serial phase sum equals step wall time.
2. Keep at least three hypotheses open: network service slowdown, a late rank due to checkpoint I/O, and changed compute demand. State a discriminating observation for each.
3. Request evidence from the instructor by naming the hypothesis it tests. Updates are scheduled at minutes 15, 30, and 45 of a 60-minute episode.
4. Propose one intervention with a predicted intermediate effect, a goodput metric, and correctness/recovery guardrails. Explain why it acts at the required layer.
5. After the proposal, analyze the released trial results. Compute useful units over total elapsed time for each condition. Keep raw pairs; do not submit only a percentage.
6. Reverse or reset the intervention in the scenario and compare with a fault-free control. State whether the observations support your mechanism and what alternatives remain.

The trial results file is [here](fixtures/20-trial-results.json), but keep it closed until step 4 on an independent attempt. The [instructor key](instructor/20-key.md) has release conditions and control facts.

## Actual workload extension

For an L2 performance claim, replay this experimental design on the dedicated primary platform environment using a fixed validated workload. Record exact model/data/configuration identities, node/GPU topology, software, run order, clocks, warm-up, and the observed phase timeline. Change only one approved checkpoint phase policy. Do not infer that the synthetic gain will occur on your machine.

If your selected specialty is different, the practicum still requires this diagnostic analysis; it does not require building a second specialty. An L0 conclusion is "identified the cause in the supplied model and analyzed the intervention." It is not a measured multi-node speedup.

## Evidence, aborts, and recovery

Submit the critical-path reconstruction, competing hypotheses, evidence requests, one-variable intervention, baseline/trial/control results, correctness and restore checks, and the exact fidelity claim. Abort on incorrect output, loss of reliable timing, unbounded checkpoint backlog, or impact outside the authorized environment. Recovery restores the prior phase policy, stops only exercise-owned work, and verifies usable checkpoints and admission state.

Objective checks: phase sums are correct; the late rank is identified from preceding work; rate and elapsed-time percentages use correct denominators; the switch warning is tested against the actual path; the conclusion does not overclaim a real network or hardware defect. Apply the common rubric; a fast but incorrect workload fails.

## Questions for defense

1. Why can the highest collective duration occur on an otherwise healthy rank?
2. When is adding phase times invalid?
3. Why report correctness and checkpoint recovery alongside speed?
4. What result in the no-contention control would weaken your proposed mechanism?

Answers follow the first attempt in the separate key.

## Four-week application plan

Weeks 1-2: 9h/week for trace theory, reconstruction, baseline/control design, and the timed investigation. Weeks 3-4: 9h/week for one intervention, result analysis, recovery, and a changed-trace defense. Proceed to [Month 21](21-recovery.md).
