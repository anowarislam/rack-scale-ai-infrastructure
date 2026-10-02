# Deliver the course

Decision date: 2026-10-02. Decision owner: the user; delivery coordination: the main agent.

## Decision

Build a complete private self-study course in this repository. The user's current request to finish the course supersedes the planning-only delivery boundary in the July charter and implementation plan. Preserve those documents as design history. They are not instructions to produce another planning package before teaching can begin.

The delivered course includes lessons, worked examples, exercises, answer guides, local software labs, native-platform and hardware workbooks, assessment gates, specialty choices, and the six-month practicum. Markdown is the delivery format. There is no dependency on building a website or publishing a repository.

The user further clarified that theory, with examples, is the most important part. Lessons are therefore the primary product. Each must teach the problem, prerequisite vocabulary, causal mechanism, worked examples with intermediate reasoning, contrasting cases, and explanatory answers. A source link, command list, or outline cannot substitute for the explanation. Labs reinforce and test the mental model. Additional tooling has lower priority than repairing a thin explanation.

## What went wrong

Verified at the start of this delivery: the repository had two content files, `course-charter.md` and `docs/superpowers/plans/2026-07-09-planning-package.md`, plus `.gitignore`. Its two commits recorded a design and a plan for a planning package. No lessons, exercises, course entrypoint, or executable labs existed. The plan explicitly prohibited chapters and executable labs.

Inference: the planning-only contract explains the mismatch between the user's desired learning material and the artifacts present. The repository alone does not establish what happened in prior conversations or whether other copies contain additional work.

## Preserved choices

- Eighteen months of core learning followed by six months of integrated practice.
- Both Kubernetes and Slurm in the catalog; one primary platform and a meaningful secondary comparison.
- One bounded specialty and one of three role-family capstones.
- Four gates, with at most twelve mandatory outcomes and six assessed exercise bundles per gate.
- Ninety-six scheduled weeks: seventy building/applying mechanisms, eighteen for remediation or validation, and eight for capstone defense and transfer. Eight additional break weeks are unscheduled.
- Eight to ten hours per scheduled week, as a design estimate to be measured by the learner, not a pilot-validated promise.
- Distinct fidelity and authorization axes. Laptop evidence does not prove GPU, RDMA, physical-rack, or production-management competence.

## Changed choices

- Course delivery replaces the planning-only restriction.
- A fundamentals bridge supports learners new to parts of the assumed infrastructure baseline. Bridge effort is additional and depends on diagnostic results; the 768-960-hour core estimate excludes it.
- Implemented lessons and a machine-readable course map replace the proposed directory of module specifications. Building duplicate planning documents is not a prerequisite to delivery.
- Current documentation sources support technical teaching. The historical job postings are context, not a required claim that a learner is ready for a particular job.
- Private-stack reconstruction is optional enrichment outside the mandatory course. It does not delay the course or become an answer key.

## Completion has separate meanings

1. **Course authored:** every mandatory lesson, lab procedure, answer guide, gate, specialty, and capstone is available and linked.
2. **Local software validated:** automated checks and runnable laptop exercises pass in the recorded environment.
3. **Native and hardware validated:** the relevant platform/GPU/multi-node/rack procedures have been run with a recorded version manifest and evidence. Absence of that environment is recorded as NOT_RUN, never a pass.
4. **Learner completed:** the learner has produced and defended the evidence for each claimed outcome. Writing the course cannot establish this.

The status report must name the attained states independently. No certification, employer endorsement, job equivalence, or blanket production-readiness claim follows from any of them.

## Acceptance and maintenance

The coordinator integrates three independently authored workstreams, runs local validation, and commissions a separate review after authoring. Material findings must be resolved or explicitly retain a release limitation. Assessment and navigation must let a new reader start without the previous conversation.

Instructional review asks whether a reader new to the topic can explain the mechanism, reproduce the worked example, predict a changed case, and understand why an incorrect answer fails. Reviewers must identify unstated prerequisites, unexplained terms, skipped reasoning, and examples that merely restate definitions. Coverage counts and passing code tests do not establish teaching quality.

Before a native or hardware session, record exact component versions, image digests where relevant, topology, permissions, and recovery conditions. Recheck the applicable official documentation when a version changes. Shared production and physical equipment remain outside self-service laptop exercises.

## Revisit triggers

Revisit pacing if actual study time exceeds the budget, bridge gaps block progress, lab availability delays a gate, platform support changes, or an independent review finds a missing prerequisite. Reduce optional work before adding mandatory hours. A lower-fidelity substitute changes the claim; it does not silently satisfy a higher-fidelity outcome.
