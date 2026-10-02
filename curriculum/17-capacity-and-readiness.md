# Month 17: Decide what the fleet can safely promise

Installed GPUs are not a service commitment. A commitment needs a workload definition, usable topology, a failure scenario, and an operating team that can restore the system. **G3-E05** assesses **G3-O09**, capacity under loss and headroom, and **G3-O10**, closure of readiness and new-product-introduction findings. Bring the state machine from [Month 16](16-lifecycle-automation.md).

## Follow capacity from hardware to useful work

Start with installed resources. Remove assets that are not qualified, are reserved for another purpose, or cannot be used by this workload. Avoid subtracting the same failed asset twice because it also appears on a maintenance list. The resulting pool is allocatable capacity. Admission then reserves some of that pool for a workload according to policy. Delivered goodput is the correct useful work the service actually completes per time interval.

These are different quantities. A workload can have allocated GPUs and make little useful progress because of repeated restarts, storage waits, or incorrect output. Another workload can have adequate aggregate GPU memory but fail because its individual workers do not fit on any device. Treat resource capacity as a vector: accelerators, per-device memory, host memory, network topology, storage throughput/capacity, power/cooling envelope, and control-plane limits. A scalar GPU count is one useful projection, not the whole vector.

Verified public fact: Google's overload discussion warns that request count alone can misrepresent resource demand when request costs differ. The same measurement question applies to AI work: declare model, input/output shape, correctness, and latency before treating two requests as equivalent. [Handling Overload](https://sre.google/sre-book/handling-overload/)

Headroom is deliberately uncommitted capacity for a stated purpose. State its denominator. Reserving 20% of capacity after a failure is different from keeping 20% of normal capacity unused and then absorbing the failure. Neither number is an industry-wide safe default. The 20% used below is an exercise policy.

## Worked example 1: 128 installed GPUs support a 72-GPU promise

**Synthetic calculation.** Four independent exercise domains contain 32 homogeneous qualified GPUs each. Jobs require gangs of 8 GPUs from the permitted pool. The policy is to survive the loss of any one domain while retaining 20% headroom in what remains.

1. Installed and qualified capacity is `4 * 32 = 128` GPUs.
2. Normal headroom leaves `128 * .8 = 102.4` GPUs for admission.
3. Whole jobs matter: `floor(102.4 / 8) = 12` jobs, or 96 GPUs.
4. Loss of one domain leaves `128 - 32 = 96` GPUs.
5. Headroom then leaves `96 * .8 = 76.8`; rounding down to gangs gives `floor(76.8/8)*8 = 72` GPUs.
6. A promise of 80 GPUs fails the declared scenario by 8. A promise of 72 exactly satisfies this simplified count model.

The lab enumerates each domain loss rather than assuming the domains have equal size. A larger domain changes the worst case. Passing the arithmetic still leaves topology placement, memory, workload performance, and correlated failures outside the model.

**Counterexample.** A 16-GPU job requiring one connected 16-GPU island cannot run on two disconnected 8-GPU islands merely because the sum is 16. Before using the pool arithmetic, establish that the assumed pooling is valid for the workload. Reducing the gang size in the spreadsheet does not change the application.

## Worked example 2: repair throughput defeats the spare plan

**Synthetic flow calculation.** A fleet has six assets awaiting repair. Over each of the next four weeks, five additional assets enter the queue and three complete qualification. The backlog grows by `5 - 3 = 2` per week: 8, 10, 12, then 14. A delivery of four spares can cover four replacements; it does not remove the continuing deficit in return-to-service throughput.

Suppose a bounded intervention reduces repeated diagnostic handoffs so qualified completions rise from three to five per week. Backlog stops growing at six, but does not disappear. At six completions per week it shrinks by one per week. These are arithmetic scenarios with fixed rates, not a fitted arrival process. Actual variability, parts delays, skill constraints, and shared-cause failures require measurement.

Now inspect team capacity. A specialist has 40 scheduled hours, 18 hours of measured interruptions, and 10 hours of recurring work. Only 12 remain. A 16-hour intervention does not fit without moving four hours, obtaining help, or changing the schedule. Calling it "top priority" does not create those hours.

**Counterexample.** Hiring another generalist may not improve return-to-service throughput if the bottleneck is a vendor-only part or one qualified signoff. Locate the limiting stage before recommending staffing. The exercise does not establish a universal engineer-to-GPU ratio.

## Readiness is evidence that someone can operate the service

An operational readiness review (ORR) answers: can this specific service be introduced or changed with its risks understood and owned? It is not a meeting whose completion makes the service ready. Verified public fact: AWS describes ORR as both a review process and a checklist informed by incidents and used through the workload lifecycle. [AWS Well-Architected OPS07-BP02, 2024-06-27 edition](https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/ops_ready_to_support_const_orr.html)

For this course, review six evidence groups:

| Group | Decision question | Concrete evidence |
|---|---|---|
| Workload | What outcome and load envelope are promised? | Correctness, demand, SLO and admission contract |
| Dependencies | What shared failure can defeat the promise? | Topology, ownership, failure-domain map |
| Detection | Will both workload failure and lost observation be detected? | Positive and negative probes, delivery test |
| Recovery | Can the named actor restore the stated postconditions? | Timed rehearsal, mode, artifacts, state compatibility |
| Operations | Can the team sustain routine and incident work? | Coverage, workload, escalation, handoff and relief |
| Change | What blocks expansion or invalidates approval? | Exact BOM, ring plan, aborts, expiry and re-review triggers |

A finding contains a specific gap, owner role, due point, closure test, and status. "Vendor aware" is an escalation state, not closure. New product introduction (NPI) adds unfamiliar combinations and incomplete operating history. Feed each field finding back into a reproducible case: affected configuration, symptom, timestamps, minimal reproduction, expected/observed behavior, workaround boundaries, and test needed to accept a correction.

A patch received from a vendor is evidence of an offered fix. A local reproduction that no longer fails is evidence for that scenario. A successful soak broadens observation time. None alone proves all fleet configurations are fixed. Record the exact closure scope and reopen trigger.

## Apply the model and conduct a review

```sh
python3 labs/fleet/fleet_lab.py capacity labs/fleet/fixtures/capacity-fault.json
python3 labs/fleet/fleet_lab.py capacity labs/fleet/fixtures/capacity-recovered.json
```

1. Predict both results by hand. Explain why normal capacity can pass while failure capacity fails.
2. Copy the fault fixture and enlarge one domain from 32 to 48 GPUs. Enumerate losses before running. Decide whether the extra installed capacity actually improves the worst-case promise.
3. Preserve the 20% post-failure headroom policy. Propose a reduced commitment or a topology-valid capacity change; do not "repair" the failure by silently changing policy.
4. Conduct a 30-minute ORR with one peer or recorded role rehearsal. Inject one missing telemetry-delivery test and one unverified checkpoint restore. Record a conditional decision and exact conditions.
5. Create an NPI case for the telemetry gap. Demonstrate one closure test with the signal lab, then reintroduce the fault and show detection. Distinguish this local regression from a vendor acceptance test.

Evidence: capacity assumptions and formulas, scenario table, original/fixed transcripts, a readiness decision, findings with closure evidence, and a residual-risk note. The common rubric requires proof that at least one finding was closed and one unsupported claim was withheld. A checklist entirely marked green without linked evidence does not pass.

## Questions

1. Why does headroom need a named denominator and purpose?
2. If a 32-GPU domain becomes 48 GPUs, what is the surviving capacity after that largest domain fails?
3. Why does a spare purchase not necessarily close a repair-throughput gap?
4. What distinguishes NPI issue tracking from verified closure?
5. Does the capacity calculator's PASS establish an inference latency objective?

## Reasoned answers

1. Otherwise the percentage can refer to normal, remaining, installed, or usable capacity and produce different commitments. Its purpose determines which scenario must preserve it.
2. The total becomes 144 and the largest loss removes 48, leaving 96. The worst-case count promise remains 72 with the same headroom and gang size.
3. Spares add finite inventory; a sustained arrival/completion imbalance keeps consuming it. The repair bottleneck must also be addressed or the commitment reduced.
4. Tracking names a case and owner. Closure demonstrates an agreed postcondition on the affected configuration and states its observation window and limits.
5. No. It checks homogeneous pooled resource counts. Tail latency requires a defined workload and measured service behavior, including queues and dependencies.

## Four-week study plan

| Week | Nine-hour allocation | Result |
|---|---|---|
| 1 | Capacity concepts 3h; examples 3h; workload assumptions 3h | Commitment model |
| 2 | Failure enumeration 3h; repair/team flow 3h; sensitivity 3h | Tested scenario table |
| 3 | ORR 3h; NPI closure loop 4h; defense 2h | G3-E05 draft |
| 4 | Remediation 4h; changed-domain replay 3h; archive 2h | Assessed bundle |

Continue to [Month 18](18-specialty-integration.md).
