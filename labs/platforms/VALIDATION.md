# Platform artifact validation

Validation date: 2026-10-02. This report describes author verification of course artifacts. It is not a learner gate pass and does not establish hardware or production readiness.

## Executed successfully

| Check | Observed result | Scope |
|---|---|---|
| `python3 -m unittest discover -s labs/platforms/l0 -p 'test_*.py' -v` | 7 tests passed | Fragmentation, no partial allocation, no overcommit, invalid request, correct resume, corrupt-state rejection, changed-target rejection |
| `python3 labs/platforms/l0/queue_recovery.py --output .cache/platform-evidence/placement.json` | ADMITTED / PENDING / ADMITTED in the three constructed states | Transparent resource model only; not a native scheduler |
| Two separate CLI processes using `workload.py` | First exit 75 after step 5; second exit 0, resumed_from 5, total 650, correct true | Application process failure/recovery with retained local files |
| YAML parsing with locally available PyYAML 6.0.3 | 10 documents parsed | Syntactic/object checks, not API-server acceptance |
| Manifest invariants | Namespace scope, digest-pinned images, requests/limits, no privilege escalation verified | Static assertions over supplied workload objects |
| `bash -n` on Kubernetes wrapper and both Slurm batch scripts | Passed | Shell parsing only |
| Python AST parsing | Passed | Syntax only |
| Slurm runbook fail-closed shell tests | 4 tests passed | Actual documentation block with mocked commands: no checkpoint, non-running job, wrong environment, and successful one-time requeue |
| Official source audit | 40 source records written; exact Slurm defaults corrected against 25.05.3 manual | Documentary mechanism verification, not runtime compatibility |

Generated local evidence is retained in `.cache/platform-evidence/author-validation.json`, `.cache/platform-evidence/placement.json`, and `.cache/platform-evidence/cli-recovery-8ht8nx68/{failed.log,recovered.log,checkpoint.json,result.json}`. These files are ignored local output; the report records the conclusions independently. The integration coordinator also independently ran the seven tests and saved `validation/logs/platforms-tests.txt`.

## Native Kubernetes: NOT_RUN

Read-only inspection found Docker Desktop 4.93.0 / Docker Engine 29.8.1, Linux arm64 server, installed kind v0.33.0, and installed kubectl v1.37.1. These are observed host tool versions, not the lab baseline. No relevant cached `kindest/node`, Python, or Slurm images were found by a filtered `docker image ls` query.

The lab requires kind v0.30.0 and kubectl v1.34.0 for its historical Kubernetes v1.34.0 baseline. Official release downloads were attempted into the repository's ignored `.cache/course-tools` directory. Exact failures:

```text
kind-darwin-arm64:
curl: (28) Operation timed out after 60002 milliseconds with 540663 out of 10624850 bytes received

kubectl darwin/arm64 v1.34.0:
curl: (28) Operation timed out after 60006 milliseconds with 753339 out of 59775314 bytes received
```

A preceding Python download process was terminated when the network limitation was established. Partial downloads were left nonexecutable and renamed with `.part` suffixes. No checksum-verified executable was installed, no cluster was created, no user's kubeconfig/context was changed, and no existing workload was modified. Cleanup of a native cluster was therefore not applicable.

The official node-image digest was verified in kind's v0.30.0 release notes. The Python multi-platform image index digest was resolved by a read-only registry inspection. These metadata checks do not establish image pull, startup, PVC provisioning, admission, RBAC query results, scheduling timing, or Job recovery. All those native behaviors remain **NOT_RUN** here. The runbook provides the exact next commands once downloads are available.

## Native Slurm: NOT_RUN

`sbatch` and `slurmctld` were not found in the author environment. No Linux VM was created, no Slurm daemon/database was started, and no authentication key or system configuration was changed. The supplied VM instructions, configuration, and batch scripts remain unexecuted reference artifacts.

The versioned official 25.05.3 manual was used to check configuration semantics. This found an invalid assumption during authoring: `task/none` and `jobacct_gather/none` are not listed plugin values for that baseline. The final configuration leaves TaskPlugin and JobAcctGatherType unset, matching the documented defaults. Proctrack remains `proctrack/linuxproc`, with the explicit limitation that it is not the cgroup enforcement profile.

The optional SlurmDBD, cgroup, GPU, controller restart, and backup-controller exercises require their documented environments and remain **NOT_RUN**. The base VM intentionally has no database-backed accounting or historical fair-share demonstration. No `sacct` output is fabricated.

Independent review identified that the original interactive checkpoint-wait sequence could continue after a failed test. A safe mocked reproduction printed `MOCK_REQUEUE_CALLED` after a failed RUNNING check, confirming the defect. The final runbook uses explicit checkpoint-success state, early returns, and a guarded RUNNING check. `python3 -m unittest discover -s labs/platforms/slurm -p 'test_*.py' -v` passed all four tests against the actual Markdown code block. Those tests execute only mocks and establish shell control flow, not native Slurm behavior.

## Interpretation and next verification

The local Python behavior is verified. The YAML and shell checks passed within their static scope. Native platform behavior is unverified until a learner or reviewer runs the provided sequence in an isolated environment and records actual outputs. Exact image/source pins improve repeatability but do not substitute for runtime tests, security review, a supported bill of materials, or physical-system evidence.
