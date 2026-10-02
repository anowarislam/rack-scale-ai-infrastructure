# Evidence packet template

Copy this file into `learner-work/` for each assessed exercise. That directory is ignored by Git. Keep raw logs with secrets, internal hostnames, serial numbers, tokens, or personal information outside the course repository. A template is not evidence of completion.

## Identity and claim

- Exercise ID:
- Learner:
- Date and UTC time range:
- Primary platform / secondary platform:
- Claimed outcomes:
- Work performed: executed / observed / simulated / analyzed.
- Fidelity: L0 / L1 / L2 / L3.
- Environment, accelerator count, topology, and RDMA mode:
- Versions, immutable image digests where applicable, and relevant source dates:
- Operation risk, authorized actor, support posture, and environment owner:

## Before touching the system

- Observed symptom and a healthy comparison:
- At least two competing hypotheses:
- Evidence that would distinguish them:
- Expected blast radius:
- Authorization and isolation check:
- Abort conditions and recovery owner:
- Recovery mode: rollback / forward recovery / rebuild / quarantine / vendor recovery / irreversible.

## Experiment and result

Record the smallest useful experiment. Include the exact command or action, input revision, exit status, observed output, and UTC time. Explain what each observation rules in or out. Keep synthetic examples labeled synthetic.

| Step | Action / observation | Result | What this establishes | What it cannot establish |
|---|---|---|---|---|
| 1 | | | | |

## Recovery and positive health

- Change made and why it addresses the supported cause:
- Independent postcondition check:
- Workload correctness, not only process liveness:
- Monitoring path and clock-integrity check:
- Residual fault or competing explanation:
- Cleanup / reset result:
- Redacted evidence filenames and checksums:

## Reasoning and review

- Verified facts:
- Inferences and their alternatives:
- Unknowns and what would resolve them:
- Claim ceiling:
- Reviewer, rubric scores, and reasons:
- Remediation action and reassessment result:
- Next exercise this evidence enables:

Do not fill missing observations with expected output from an answer key. Expected output helps diagnose your result; it is not your result.
