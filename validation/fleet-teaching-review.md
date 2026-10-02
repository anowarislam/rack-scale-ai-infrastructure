# Independent fleet and practicum teaching review

Review date: 2026-10-02. Reviewer: platform-course author, reviewing another author's work. Standard: [teaching acceptance](TEACHING-REVIEW.md). This is a substantive instructional and technical review, not a copy-edit or proof of native infrastructure operation.

**Final disposition: ACCEPTED after corrections.** The theory, examples, and role distinctions satisfy the instructional intent. All five findings are corrected and independently rechecked. The new two-host procedure resolves the topology gap, and six safe shell-mock cases verify its setup and launch guards. This accepts the authored package; no native or physical execution is inferred from passing local checks.

## Scope and method

Read all twelve monthly chapters: [13](../curriculum/13-fleet-truth.md), [14](../curriculum/14-reliability.md), [15](../curriculum/15-incidents-and-change.md), [16](../curriculum/16-lifecycle-automation.md), [17](../curriculum/17-capacity-and-readiness.md), [18](../curriculum/18-specialty-integration.md), [19](../practicum/19-inherit.md), [20](../practicum/20-performance.md), [21](../practicum/21-recovery.md), [22](../practicum/22-rack-readiness.md), [23](../practicum/23-portfolio.md), and [24](../practicum/24-defense.md). Read all six separate instructor keys and the practicum README.

Read all four specialty packets and their README: [rack lifecycle](../specialties/rack-lifecycle.md), [performance](../specialties/performance.md), [workload platform](../specialties/workload-platform.md), and [fleet automation](../specialties/fleet-automation.md). Read all three capstone packets and their README: [engineer](../practicum/capstones/engineer.md), [aspiring leader](../practicum/capstones/aspiring-leader.md), and [manager](../practicum/capstones/manager.md).

Compared questions with reasoned answers, scenario inputs with instructor-only facts, and monthly mappings with [G3/G4](../assessments/gates.md). Inspected the fleet evaluator, its tests, its relevant signal/lifecycle/capacity fixtures, and both performance scenario fixtures. Recomputed representative numerical examples without calling the fleet evaluator. Reopened official technical references for the mechanisms most likely to be misremembered.

The audience is a learner who has completed the preceding systems and platform material. The practicum is meant to combine those mechanisms under uncertainty. It is not required to introduce a new technology stack in each case. Local exercises establish model behavior; environment-specific operational claims require the corresponding recorded execution.

## Findings and closure requirements

| ID | Severity / confidence | Finding and consequence | Required correction | Status |
|---|---|---|---|---|
| FTR-01 | Medium / high | Month 21 requires two participating compute nodes but directs the learner to reuse the G2 environment and workload without an extension. The supplied CPU workloads are single-task, and the Slurm reference is one VM. Following the stated instructions cannot establish the required multi-node claim. | Supply a bounded executable two-compute-node CPU recovery procedure, with distinct placement, per-task identity, a safe process fault, correct restore, unique aggregate results, positive health checks, and reset. Explicitly distinguish replicated independent tasks from collective training and distinguish multiple containers on one laptop from the required L2 topology. | Closed: two-host runbook and recorder supplied; five application/record tests and six independent shell-mock cases pass. Native run remains NOT_RUN. |
| FTR-02 | Medium / high | Month 22 promises an initial checklist and maintenance plan but supplies neither. The instructor key assumes mixed configuration tuples and an 80-GPU commitment that are absent from the initial packet. The learner cannot independently evaluate the claimed starting evidence. | Add a concrete synthetic initial packet with configuration/evidence identifiers, current target, check scope, maintenance unavailability, and demand. Keep timed facts in the instructor key. Permit a defensible initial decision without inventing facts. | Closed: explicit CFG-A/B, evidence rows, roles, 90-minute domain removal, headroom and demand supplied. |
| FTR-03 | Medium / high | The initial Month 20 JSON includes baseline/regression checkpoint-writer counts that the key is supposed to reveal at minute 15. The field name `unrelated_switch_warning` also supplies the relevance conclusion. This weakens the independent evidence-request exercise. | Remove timed writer counts from the initial fixture. Use a neutral warning and raw path/port facts, or release the path check separately, so the learner derives relevance. Retain the phase trace needed for the first hypothesis. | Closed: counts removed; neutral warning identifies SW2/P9 and the recorded path identifies SW1/P1-P4. Relevance is derived. |
| FTR-04 | Low / high | Month 21's key says the healthy control needs no repair, but its referenced healthy fixture explicitly includes a planned repair transition. A learner following the actual event history could be marked wrong. | Say that no extra repair or quarantine is needed beyond the listed healthy maintenance cycle. | Closed: key now distinguishes the planned repair cycle from unnecessary extra repair. |
| FTR-05 | Low / high | Month 15 describes p99 exceeding two seconds "for 18% of eligible requests," mixing a distribution statistic with per-request classification. | State either the fraction of requests exceeding the threshold or the fraction of measurement windows whose p99 exceeds it. Keep the intended denominator explicit. | Closed: request fraction and p99 are distinguished explicitly. |

FTR-01 through FTR-03 are authoring acceptance conditions. FTR-04 and FTR-05 are small corrections, not reasons to expand the curriculum. Findings were sent to the coordinator and author while review continued. This reviewer has not edited the author's lesson or scenario files.

The [two-host runbook](../practicum/l2-recovery-runbook.md) correctly defines replicated independent CPU tasks, two actual hosts, shared-storage assumptions, one controlled process exit, recovery, aggregation, native accounting, and reset. A follow-up check reproduced a setup-guard issue: under the prescribed non-errexit shell, failed standalone `test` commands did not prevent later file writes in an existing evidence directory. A safe local temporary-directory reproduction printed `WOULD_OVERWRITE_EVIDENCE`. The coordinator independently found the same issue. The final version adds explicit fail-closed setup, a recorded parameter boundary, and an atomic per-phase launch marker. Six independently executed mocks of the actual Markdown functions now pass: existing evidence preserved, existing allocation rejected, valid first launch plus duplicate rejection, changed target and invalid phase rejected, failed configuration discovery disables submission, and expected status 75 preserved. No native job was submitted by these reproductions.

The revised Month 22 packet can be solved before reading its key: it supplies the target and previous tuples, scoped evidence records, roles, maintenance removal, headroom rule, and demand. Its minute-15 inject now adds a requested compatibility-review result instead of merely repeating the visible version difference. The answer correctly distinguishes absent compatibility evidence from proof of incompatibility.

## Instructional assessment

| Material | Substantive assessment |
|---|---|
| Months 13-14 | Define identity, incarnation, source/observed time, exposure, censoring, event-rate uncertainty, and predictive value before relying on them. Examples explain why fresh ingestion, raw event counts, zero observed failures, and a sensitive detector can mislead. The fixed-exposure model and informative-censoring limitations are explicit. |
| Months 15-16 | Teach symptom versus mechanism, incident roles, handoffs, controlled changes, recovery modes, idempotency, generation checks, and qualification. The state transitions make the mutation boundary concrete. The local replay does not claim durable distributed-controller semantics. FTR-05 is the only identified explanation inconsistency. |
| Months 17-18 | Capacity arithmetic separates installed supply, failure-domain loss, headroom, job granularity, and team capacity. Readiness requires current evidence and actual closure. Specialty integration distinguishes an observed change from a causal effect and tests both unsafe and valid cases. |
| Months 19-20 | Recombine source trust, coverage, capacity, and critical-path reasoning. The slow-collective example shows how a late rank shifts apparent time to other ranks. Serial-phase and synthetic-data assumptions are explicit. FTR-03 concerns release timing, not the correctness of the performance explanation. |
| Months 21-22 | Correctly distinguish process restart, committed workload state, hidden health, current qualification, and readiness at a stated fidelity. The corrected FTR-01 and FTR-02 applications now provide the required runbook and initial scenario data. |
| Months 23-24 | Supply bounded resource/time constraints, changed evidence, decision versions, reproducibility, reviewer challenges, and transfer plans. These assess adaptation rather than recollection of a single canned answer. |
| Four specialties | Each is one intervention with characterize, intervene, validate, recover, and operationalize stages. Rack lifecycle guards promotion; performance changes checkpoint phasing; workload platform changes admission scope; fleet automation binds intent to state generation. These are narrow applications of earlier theory, not unexplained new technology surveys. |

The separated answers explain the mechanisms and allow defensible alternatives. Publicly readable keys are honestly described as sealed by convention; key-assisted attempts are practice. Outside FTR-03, the review found no timed answer copied into the initial student inputs. Worked warm-up examples disclose general mechanisms, which is appropriate teaching rather than answer leakage.

## Distinct role-family capstones

The [engineer route](../practicum/capstones/engineer.md) asks where a guarantee can actually be enforced. It compares intervention locations, uses a causal counterfactual, bounds the implementation, tests negative and valid cases, and requires another operator to use the handoff. This is substantive engineering reasoning rather than a blank design template.

The [aspiring-leader route](../practicum/capstones/aspiring-leader.md) defines responsibility, authority, and accountability; traces technical dependencies; gives concrete delegation and acceptance examples; and requires two work cycles with an observed result. The coaching example challenges the mistaken equivalence between a running process and a recovered workload. It explicitly separates solo practice, course-observed coordination, and sustained leadership evidence.

The [manager route](../practicum/capstones/manager.md) combines capacity arithmetic with delivery time and specialist hours. Its example explains why an economically plausible purchase cannot solve the immediate launch gap. It requires a revised recommendation, technical evidence review, closure, deferred work, and reversal triggers. It does not claim that a course exercise proves longitudinal management, hiring, or succession competence.

Months 15-18 and 23 supply the incident-role, dependency, readiness, and operating-decision mechanisms used by these capstones. No material promised-content gap was found in these three paths. Broadening them into a generic people-management curriculum is unnecessary for the stated charter.

## Independent numerical checks

The following were recomputed using Python's standard library from the supplied inputs. The reliability interval check used the even-degree chi-square CDF and numerical quantiles, independently of `fleet_lab.invert_poisson_cdf`.

| Example | Independent result | Assessment |
|---|---|---|
| Source time 970, offset +40, now 1000, uncertainty 1 | Corrected time 930; conservative age 71 seconds | Matches Month 13. A two-second collection age does not make the source current. |
| Source 505, offset +10, now 520, uncertainty 3 | Conservative age 28 seconds | Exceeds the question's 25-second bound. |
| 2 events / 3000 hours versus 1 / 200 hours | 0.666667 versus 5 events per 1000 hours; ratio 7.5 | Raw counts reverse the rate ordering. |
| Two-event central 95% Poisson interval | Count bounds 0.2422092785 and 7.2246876677; rate bounds 0.0807364 and 2.4082292 per 1000 hours at 3000-hour exposure | Matches Month 14 within rounding. |
| Zero events / 2000 hours, one-sided 95% bound | 1.4978661 events per 1000 hours | Distinct from the upper bound of a central 95% interval. |
| Four-unit survival example | `(3/4) * (1/2) = 0.375` after the second failure | Correctly removes the censored unit from the later risk set. |
| 1% prevalence, 90% sensitivity, 5% false-positive rate, 10000 units | 90 true positives and 495 false positives; precision 15.3846% | Matches the detector example. |
| Canary 10/500, control 49/49500 | 2% versus 0.0989899%; pooled 0.118% | Pooling conceals the severity in the changed cohort. |
| Four 32-GPU domains, 20% remaining headroom, 8-GPU jobs | Normal admissible 96; after one domain loss 72 | An 80-GPU commitment is short by eight under the loss case. |
| Five 24-GPU domains, one loss, 25% headroom | 72 GPUs, nine 8-GPU jobs | Matches Month 22. |
| Add a fifth 32-GPU domain to the four-domain fleet | 96 admissible after one equal-domain loss | Matches the manager example under its count-only assumptions. |
| Replace one 32-GPU domain with 16 | Total 112; loss of a largest domain leaves 80; admissible 64 | Matches the changed-input defense. |
| Four 20-GB checkpoints / 200 seconds at 2 GB/s | Average 0.4 GB/s; synchronous burst needs 40 seconds; each isolated checkpoint needs 10 seconds | Offsetting helps bursts, not an average demand exceeding service capacity. |
| Four 120-GB checkpoints / 200 seconds | Average 2.4 GB/s, above 2 GB/s | Staggering cannot stabilize this sustained overload. |
| Performance trace | Each baseline serial phase sum is 120 ms; each regression sum is 400 ms | Rank 1's 280-ms pre-collective wait explains 320-ms collective durations elsewhere in this model. |
| Performance trial aggregates | 2.5 versus 7.142857 useful units/s; rate gain 185.7143%; equal-work elapsed reduction 65% | Correct denominators; no population confidence claim follows from three designed pairs. |
| Replay from step 200 after failure at 280, 0.2 s/step plus 12 s initialization | 28 seconds, excluding scheduler delay | Matches Month 21. |

## Primary-source verification

Reopened the following on 2026-10-02. These support the mechanisms, not any assertion that the synthetic fleet reflects an actual vendor population.

- [NIST constant repair-rate model](https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm): checked exposure-normalized rate, fixed-time interval conditions, and the zero-event bound. The lesson appropriately limits the model and does not treat zero failures as zero risk.
- [NIST Kaplan-Meier procedure](https://www.itl.nist.gov/div898/handbook/apr/section2/apr215.htm): checked risk-set removal and the survival product used in the four-unit example.
- [OpenTelemetry Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/): checked origin `Timestamp` versus collection `ObservedTimestamp`. The page identifies the model as stable; this does not supply deployment-specific clock accuracy.
- [DMTF Redfish DSP0266 1.20.2](https://www.dmtf.org/sites/default/files/standards/documents/DSP0266_1.20.2.html): checked ETags and conditional modification, plus asynchronous acceptance versus task completion. The course does not assume every device implements the optional behavior identically.
- [Slurm 25.05.3 srun source manual](https://raw.githubusercontent.com/SchedMD/slurm/slurm-25-05-3-1/doc/man/man1/srun.1): checked highest task-exit propagation, explicit non-killing behavior for a failed task, zero wait meaning no early peer timeout, and task-per-node limits. [The same release's task launcher](https://raw.githubusercontent.com/SchedMD/slurm/slurm-25-05-3-1/src/slurmd/slurmstepd/task.c) confirms that it sets `SLURMD_NODENAME` for the launched task. These validate the extension's stated command semantics, not its execution on an available cluster.

Source checks were targeted at questionable or precision-sensitive claims. They were not an independent audit of every external link or every sentence in all cited source documents.

## Executed checks and limits

Ran `python3 -m unittest discover -s labs/fleet -p 'test_*.py' -v`: **22 tests passed**. Inspected tests rather than relying only on their pass result. They exercise rate normalization and intervals, source freshness, clock correction, units, identity conflicts, guarded transitions, duplicate/stale intent, failed qualification, and correlated-domain capacity.

Ran `python3 -m unittest discover -s practicum -p 'test_l2_batch.py' -v`: **5 tests passed**. These execute the real checkpoint application with its artificial delay removed and mock node identities. They cover baseline/failure/recovery/reset, corrupt final arithmetic, same-host aliases, active-writer exclusion, and duplicate-phase evidence preservation. They are L0 recorder tests, not native Slurm or L2 execution.

A separate exact-ID check confirmed each of the twelve chapters maps to its expected single G3/G4 exercise and two outcomes, with no additional or mismatched IDs.

No Kubernetes, Slurm, GPU, RDMA, physical rack, firmware, or external messaging action was executed as part of this review. The supplied two-node extension remains a procedure until executed on its stated environment. L2/L3 `NOT_RUN` does not by itself make the authored theory incomplete; missing executable instructions for a required application do, which is why FTR-01 was tracked and corrected separately.

The review does not award learner mastery, independent leadership assessment, production readiness, vendor support, or workplace outcomes. All material authoring findings are closed. The accepted package teaches the necessary mechanisms, provides solvable scenarios and bounded executable applications, and states the remaining environment requirements without treating them as completed evidence.
