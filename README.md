# Rack-scale AI infrastructure: from foundations to integrated practice

Read the [course website](https://anowarislam.github.io/rack-scale-ai-infrastructure/) on GitHub Pages. This repository holds the canonical lesson sources, runnable exercises, and validation records. See [website publishing](docs/pages-publishing.md) for the update workflow.

Start with [the learning guide](LEARNING-GUIDE.md), then [the fundamentals bridge](curriculum/00-bridge.md) and [month 1: how the system fits together](curriculum/01-system-map.md). The course prioritizes **theory, worked examples, and reasoned answers**. Practical exercises test the explanations.

You will learn how CPUs, GPUs, memory, networks, storage, workload platforms, and fleet operations interact; how to diagnose failures across those boundaries; and how to make and defend operational decisions. The route develops a primary Kubernetes or Slurm platform, one technical specialty, and an integrated capstone.

For the exact delivered and tested state, read [DELIVERY-STATUS.md](DELIVERY-STATUS.md) and [validation results](validation/RESULTS.md). Course material being available does not mean you have passed its assessments. Your progress begins with your own evidence.

## Read the course

| Stage | What the theory develops | Start here |
|---|---|---|
| Bridge | Processes, files, permissions, networking, configuration, containers, units, and basic quantitative reasoning | [00: prerequisites](curriculum/00-bridge.md) |
| Months 1-6 | Failure domains; server and GPU mechanisms; scale-up and scale-out; storage; telemetry; training and inference | [01: the system map](curriculum/01-system-map.md) |
| Month 7 | Resources, placement, fairness, identity, correctness, and recovery as a workload contract | [07: workload contract](curriculum/07-workload-contract.md) |
| Months 8-12 | Native scheduler mechanisms and operational differences, with one primary and one secondary path | [Kubernetes](tracks/kubernetes/README.md) or [Slurm](tracks/slurm/README.md) |
| Months 13-18 | Fleet truth, statistical reliability, incidents, lifecycle automation, capacity, readiness, and one intervention | [13: fleet truth](curriculum/13-fleet-truth.md), then [specialties](specialties/README.md) |
| Months 19-24 | Integrated diagnosis, performance, recovery, rack readiness, portfolio decisions, and defense | [Practicum](practicum/README.md) |

The [calendar](CALENDAR.md) links the complete sequence. The [course map](course-map.json) records all 24 months, four gates, and their outcomes in a machine-checkable form. Read one primary platform track in depth; use the other track's secondary package instead of doubling the workload.

## What each lesson should give you

A problem worth solving, the vocabulary and prerequisites to understand it, a stepwise explanation, worked cases with the assumptions exposed, a contrasting or failing case, independent questions, and an answer guide explaining why the result follows. External sources substantiate claims; the explanation belongs in the lesson itself.

For example, counting two replicas is insufficient to establish availability. You must trace their shared failure domains, calculate the capacity left after the specified fault, and ask whether that capacity meets demand. The later fleet and capstone work repeatedly applies the same habit: define the claim, expose the assumptions, test the causal explanation, and name the remaining uncertainty.

## Study and assess

Allow 8-10 hours per scheduled week as an initial estimate, with theory and worked examples taking priority. The full calendar has 96 scheduled weeks and eight flexible break weeks. The bridge is additional when needed. Move faster only when you can explain the material and meet the evidence requirements; reading quickly is not the same as demonstrating the outcomes.

- [Learning guide](LEARNING-GUIDE.md): first session, weekly method, hardware planning, and getting unstuck.
- [Four assessment gates](assessments/gates.md): what counts as demonstrated and how to remediate.
- [Progress template](assessments/progress-template.md): copy into `learner-work/` to track your own route.
- [Evidence template](assessments/evidence-template.md): record predictions, observed results, recovery, and limitations.
- [Teaching acceptance](validation/TEACHING-REVIEW.md): how explanations and examples are reviewed.

## Practical work

Begin with local Python exercises when you reach the relevant lesson. They use synthetic data and do not establish physical GPU, RDMA, or rack behavior.

| Area | Instructions | Purpose |
|---|---|---|
| Systems | [Local exercises](labs/systems/README.md) | Test failure domains, identity, runtime boundaries, checkpoint and telemetry reasoning |
| Physical systems | [Hardware workbook](labs/systems/hardware-workbook.md) | Collect actual evidence in an appropriate authorized GPU or multi-node environment |
| Platforms | [Platform labs](labs/platforms/README.md) | Compare local models with native Kubernetes and Slurm behavior |
| Fleet | [Fleet labs](labs/fleet/README.md) | Calculate reliability and capacity; test data integrity and lifecycle invariants |
| Advanced recovery | [Two-host CPU exercise](practicum/l2-recovery-runbook.md) | Practice application recovery and evidence collection across two participating compute hosts |

L0-L3 describe environment fidelity, not permission to act. A laptop exercise is self-service. Native deployments require an isolated environment. Physical, disruptive, and service operations retain the charter's owner, supervision, and recovery requirements. The course does not authorize work on shared production or physical equipment.

## Check the course files

With Python 3.11 or later, run from this directory:

```bash
python3 tools/validate_course.py
python3 -m unittest discover -s labs/systems -p 'test*.py'
python3 -m unittest discover -s labs/platforms/l0 -p 'test*.py'
python3 -m unittest discover -s labs/platforms/slurm -p 'test*.py'
python3 -m unittest discover -s labs/fleet -p 'test*.py'
python3 -m unittest discover -s practicum -p 'test*.py'
```

The first command checks navigation, source-record shape, calendar accounting, and gate mappings. Unit tests check local exercise behavior. Neither establishes teaching quality, native-platform compatibility, or learner mastery. The [recorded results](validation/RESULTS.md) state what was actually run.

## Sources and design history

[Source ledgers](evidence/README.md) record the scope and limitations of public documentation. Synthetic examples remain labeled. Private company architectures and job-readiness claims are outside this course.

This repository began as a planning-only charter. [The delivery decision](decisions/0005-deliver-the-course.md) supersedes that restriction and records the shift to a theory-first course. The [original charter](course-charter.md) and [original planning plan](docs/superpowers/plans/2026-07-09-planning-package.md) remain as history. They are not additional prerequisites to studying or completing the course.

The course is publicly available for self-study. No employer endorsement, professional certification, or job equivalence is claimed.
