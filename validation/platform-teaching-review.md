# Independent platform teaching review

Review date: 2026-10-02 UTC. Reviewer: the systems-course author, reviewing another author's platform material. Scope: all eleven monthly platform theory chapters, their entrypoints, the relevant native runbooks and local exercises, and alignment with [teaching acceptance](TEACHING-REVIEW.md) and [G2](../assessments/gates.md).

**Disposition: no open blocking findings in the reviewed material.** One material recovery-procedure defect and several smaller factual or prerequisite issues were found, reported to the author, corrected, and checked again. This is a completed content review, not a learner gate pass or a claim that the native reference environments were executed.

## Audience, assumptions, and confidence

The intended reader has completed the systems foundation and needs to understand how workload requirements become placement, execution, recovery, and operating evidence. The review tested whether a reader could learn that causal chain from these chapters, rather than needing to infer it from linked reference documentation.

The assumption that the reader can follow both platforms within one course budget holds in the documents: primary Build and secondary Run/compare work share the stated 8-10 hours per week. They are not presented as two additive full-time tracks. The assumption that local resource-model success establishes native scheduling behavior is explicitly rejected by the text and exercises.

- **High confidence, directly inspected:** all eleven chapters explain their central mechanisms, supply worked cases and contrasting cases, provide reasoned answer keys, and map coherently to the six G2 bundles. The listed corrections are present in the final files reviewed.
- **High confidence, directly executed:** the representative local workload resumes correctly, rejects a changed target, and produces the checked arithmetic results. The corrected requeue documentation block fails closed in the tested mocked branches.
- **Documentary confidence, version scoped:** selected Kubernetes 1.34 and Slurm 25.05.3 semantics were checked against primary documentation. Rolling Slurm explanatory pages support concepts, not an assertion that every current option exists in the pinned baseline.
- **Unverified:** native Kubernetes construction, image startup, scheduling and RBAC behavior; native Slurm construction, authentication, allocation and requeue behavior; and all GPU, RDMA, HA and production-isolation claims. Static review and mocked commands cannot establish these results.

## Complete chapter coverage

Every chapter below was read in full, including exercises, weekly plans, questions, and separated answer keys. The observations identify what was assessed; they are not merely checks that headings exist.

| Chapter | Teaching chain assessed | Result after corrections |
|---|---|---|
| [07: workload contract](../curriculum/07-workload-contract.md) | Workload identity and shape lead to placement constraints; recovery requirements lead to checkpoint and retry responsibilities. Aggregate capacity and checkpoint-cost examples expose incorrect shortcuts. | Sound. The missing information needed for an exact fair-share or failure-loss prediction is not invented. |
| [Kubernetes 08: reference environment](../tracks/kubernetes/08-reference-environment.md) | API acceptance, controller reconciliation, scheduling, kubelet execution and application correctness are separate observations. CPU request/limit arithmetic supports the mechanism. | Sound. ConfigMap, affinity, taint and toleration prerequisites were clarified during review. |
| [Kubernetes 09: placement and fairness](../tracks/kubernetes/09-placement-and-fairness.md) | Feasibility precedes ranking; per-worker shape can fail despite enough total GPUs; admission rejection differs from scheduler Pending. | Sound. Labels are now described as metadata pairs, distinct from the Kubernetes annotations field. |
| [Kubernetes 10: recovery](../tracks/kubernetes/10-workload-recovery.md) | Replacement execution does not reconstruct application state; checkpoint identity and generation matter; training group recovery differs from an inference request retry. | Sound. Correct final output alone is explicitly insufficient evidence of checkpoint reuse. |
| [Kubernetes 11: operability](../tracks/kubernetes/11-operability.md) | Identity, authorization, resource isolation and recoverable controller state are distinct boundaries. Permission and quorum examples show why apparent redundancy is insufficient. | Sound. The native RBAC exercise and the higher-scope HA procedure have different evidence ceilings. |
| [Kubernetes 12: integration](../tracks/kubernetes/12-integration-and-comparison.md) | An evidence chain joins contract, object identity, placement, execution and useful results. Denominators distinguish allocated time, active rate and end-to-end goodput. | Sound. The comparison asks about native guarantees rather than matching command names. |
| [Slurm 08: reference environment](../tracks/slurm/08-reference-environment.md) | Controller, compute daemon, allocation, batch script and job step have distinct roles. Four tasks and one four-CPU task are not equivalent execution shapes. | Sound. The single-node CPU reference is not presented as GPU or multi-node evidence. |
| [Slurm 09: placement and fairness](../tracks/slurm/09-placement-and-fairness.md) | Allocation shape, queue policy and backfill have different responsibilities; fair share requires more information than two usage totals. | Sound. Slurm gang time slicing is explicitly distinguished from coordinated distributed-job admission. |
| [Slurm 10: recovery](../tracks/slurm/10-workload-recovery.md) | Requeue restarts the batch script; the application must restore committed state. The same job ID does not imply the same execution attempt. | Sound after the linked runbook guard correction below. |
| [Slurm 11: operability](../tracks/slurm/11-operability.md) | Authentication, process/resource containment, accounting and controller recovery establish different properties. Controller availability is not database restore. | Sound after correcting the minimal profile's TaskPlugin description. |
| [Slurm 12: integration](../tracks/slurm/12-integration-and-comparison.md) | Allocated CPU time differs from consumed CPU time; checkpoint savings can be outweighed by queue delay; evidence must connect allocation to result. | Sound. The accounting limitation of the minimal VM is explicit. |

The associated Kubernetes and Slurm track READMEs, [platform lab entrypoint](../labs/platforms/README.md), [Kubernetes runbook](../labs/platforms/kubernetes/README.md), [Slurm runbook](../labs/platforms/slurm/runbook.md), manifests, shell wrappers, batch scripts, reference configurations, local resource model, and [shared workload](../labs/platforms/workload.py) were also inspected. The local resource model is deliberately simpler than either native scheduler; the surrounding instruction explains that boundary.

## Findings and resolutions

| ID | Severity and confidence | Location and consequence | Required correction and verification | Status |
|---|---|---|---|---|
| P1 | Medium; high confidence; blocked acceptance of the recovery procedure | [Slurm runbook, controlled requeue](../labs/platforms/slurm/runbook.md): the original interactive sequence could continue after checkpoint-wait exhaustion or a failed RUNNING test. A standalone failing shell command does not prevent a later independent command from running. The exercise could therefore request requeue without its documented preconditions. | Put the operation inside explicit fail-closed control flow: record checkpoint readiness, return on timeout, guard the evidence query, return for non-RUNNING state, and retain the final environment guard. The author reproduced the original defect with mocks. The corrected actual Markdown block was independently exercised for four branches, all passing. The remaining state-change race before the controller request is now stated. | Resolved |
| P2 | Low; high confidence | [Slurm 11](../tracks/slurm/11-operability.md): the original `task/none` description did not match the pinned manual or the intended unset configuration. It could lead the reader to invent an invalid plugin value. | Describe TaskPlugin as unset in the trusted-user profile. Confirm the reference configuration and runbook also leave TaskPlugin and JobAcctGatherType unset. Checked against the exact 25.05.3 manual and re-read the corrected chapter. | Resolved |
| P3 | Low; high confidence | [Kubernetes 08](../tracks/kubernetes/08-reference-environment.md) and [09](../tracks/kubernetes/09-placement-and-fairness.md): ConfigMap and some placement terms appeared before enough explanation for a newcomer. The mechanism was otherwise correct. | Add compact definitions connecting ConfigMap to non-secret configuration, affinity to placement relationships, and taints/tolerations to admission onto a node. Re-read the additions and their examples. | Resolved |
| P4 | Low; high confidence | [Kubernetes 09](../tracks/kubernetes/09-placement-and-fairness.md): an intermediate correction called a label a key/value annotation, conflating two distinct metadata fields. | Use "key/value metadata pair used for selection." The final wording was checked directly. | Resolved |

The original P1 defect was not treated as a speculative race: the author supplied a safe shell-mock reproduction showing the requeue call after a failed RUNNING test. By the time the independent review attempted that old sequence, the corrected file had landed. The first regression assertion still expected the old behavior and failed; inspection showed the function had correctly aborted. The reviewer then exercised the four intended branches against the corrected block. That stale assertion failure is not counted as a passing test or hidden as a native result.

The TaskPlugin and accounting defaults were checked in the [Slurm 25.05.3 configuration manual](https://raw.githubusercontent.com/SchedMD/slurm/slurm-25-05-3-1/doc/man/man5/slurm.conf.5). Its scope supports the pinned configuration; it does not validate the host's cgroup delegation or installed build. The labels and placement correction is consistent with [Kubernetes 1.34 node assignment](https://v1-34.docs.kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) and [taints and tolerations](https://v1-34.docs.kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/): toleration permits consideration, while affinity can express placement preference or requirement.

## Independent numerical and executable checks

The following checks used Python 3.11.11. Temporary local directories were used for representative workload runs; they are reviewer tests, not learner evidence.

| Check | Independent result | Interpretation |
|---|---|---|
| Sum of squares through 5, 8, 12, 20, 40 and 100 | 55, 204, 650, 2870, 22140 and 338350 | Matches the checkpoint and final-output values used in the chapter/runbook examples. |
| Checkpoint useful-time fraction | `200 / (200 + 10) = 0.952380...`; `20 / (20 + 10) = 0.666666...` | The 95.2% and 66.7% examples use consistent seconds and denominators. |
| Recovery components | `20 + 90 + 15 + 5 = 130 s` | Detection, queue, restore and validation sum correctly; replayed computation is not silently included. |
| Allocated CPU time and consumption | `8 CPUs * 30 min = 240 CPU-min = 4 CPU-h`; `60 / 240 = 25%` | Allocation and consumption have different meanings despite compatible units. |
| Queue delay outweighs checkpoint gain | `25 - ((20 - 2) - 4) = 11 min` | The constructed end-to-end regression follows from the stated 14-minute net recovery saving and 25-minute additional wait. |
| Resource-model placement | Broken state PENDING; healthy state ADMITTED; recovered allocation uses nodes `a` and `b` | The example's fragmentation conclusion follows from per-worker constraints, not just a total GPU count. |
| Workload failure and recovery in separate CLI processes | `--steps 12 --fail-after 5` exited 75; restart exited 0 with `resumed_from: 5`, `total: 650`, `correct: true` | Demonstrates actual local application interruption and checkpoint reuse. It does not demonstrate scheduler recovery. |
| Changed workload target | Restart with `--steps 13` rejected the existing checkpoint with `checkpoint identity or arithmetic is invalid` | Negative control verifies that a plausible checkpoint cannot silently cross workload identity. |
| Corrected Slurm requeue documentation block, independent shell mocks | Missing checkpoint: exit 1 and no requeue. Non-RUNNING state: exit 1 and no requeue. Failed environment guard: exit 1 and no requeue. Ready/RUNNING/valid environment: exit 0 and exactly one requeue call. | Tests shell control flow with mocked commands; no Slurm controller is contacted. |
| Added regression test module, independently rerun | `python3 -m unittest discover -s labs/platforms/slurm -p 'test_*.py' -v`: 4 tests passed | Executes the actual Markdown function rather than a separately rewritten copy. |

For the selected exercises, the supplied inputs were sufficient to derive the expected answer. Where exact outcomes require unavailable policy or runtime information, the answer keys identify that missing information rather than producing a fictitious exact value. In particular, historical usage totals alone do not establish exact fair-share ordering, and Pod acceptance alone does not establish application success.

## Selected primary-source verification

These pages were inspected during the review on 2026-10-02. They support the checked mechanisms, not an exhaustive audit of every linked page.

- The [Kubernetes 1.34 Job documentation](https://v1-34.docs.kubernetes.io/docs/concepts/workloads/controllers/job/) supports the warning that a program can be started more than once even with a single intended completion. The recovery text correctly retains application responsibility for safe repeated execution.
- The [Kubernetes 1.34 volume documentation](https://v1-34.docs.kubernetes.io/docs/concepts/storage/volumes/) supports the distinction between container restart and Pod removal for `emptyDir`. The chapters do not present Pod-local storage as durable across replacement Pods.
- The [Kubernetes 1.34 version-skew policy](https://v1-34.docs.kubernetes.io/releases/version-skew-policy/) supports the need to reason about specific component pairs during an upgrade. The text does not reduce upgrade safety to comparing one cluster version string.
- The [Slurm 25.05.3 sbatch manual](https://raw.githubusercontent.com/SchedMD/slurm/slurm-25-05-3-1/doc/man/man1/sbatch.1) supports the central requeue lesson: a new execution starts the batch script from its beginning while retaining the job ID. The checkpoint mechanism remains application owned.
- Slurm's [gang scheduling explanation](https://slurm.schedmd.com/gang_scheduling.html) describes time slicing through suspension/resumption; [multifactor priority documentation](https://slurm.schedmd.com/priority_multifactor.html) explains the accounting dependency for historical fair-share operation. These sources support the explicit limitations of the minimal CPU VM and the comparison with distributed-job admission.

## G2 alignment and remaining limits

The sequence maps one shared contract exercise and five monthly platform exercises to G2-E01 through G2-E06, with two outcomes each. It does not inflate the number of assessed bundles by counting both tracks separately. G2-E02 continues to require native workload observations on both platforms; the local model cannot satisfy it. G2-E04 requires evidence of restored useful state rather than a successful process exit alone. G2-E05 separates actual access-denial observations from a written HA or upgrade procedure. These distinctions are consistent in the chapters, runbooks and gate.

No incorrect worked numeric result was found among the independently checked examples. No claim that the native references had successfully run was found in the reviewed chapters or [platform validation report](../labs/platforms/VALIDATION.md). That report records failed Kubernetes tool downloads and absent Slurm commands, then marks native behavior NOT_RUN. The supplied pinned versions are historical teaching references, not a verified current production-support recommendation.

This review did not execute either native platform, reproduce the author's download failures, audit every external citation, assess every possible scheduler configuration, conduct a security penetration test, or validate GPU/RDMA behavior. It did not test a real control-plane outage or restore a real accounting database. It also did not conduct a longitudinal teaching study with new learners. Course content is complete within this reviewed scope; learner mastery and native operational results still require the stated observations and defenses.
