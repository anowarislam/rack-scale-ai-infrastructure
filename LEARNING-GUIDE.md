# How to use this course

Start at month 1 after the bridge diagnostic. Work in prerequisite order; advance on evidence, not on elapsed calendar time. The 24-month schedule is a pacing plan, not a requirement to wait two years before progressing.

## What "zero to hero" means here

The course starts with systems vocabulary and the path from a workload request to physical resources. It develops diagnosis, recovery, automation, reliability, and operational judgment through increasingly integrated exercises. The bridge supplies prerequisite practice when Linux, networking, containers, or numerical reasoning are unfamiliar.

The achievable endpoint is a portfolio of demonstrated, bounded skills at the environments you actually used. Reading cannot substitute for operating a GPU, recovering a real cluster, or handling a real organizational responsibility. Record those differences in your evidence. The course does not award a credential or promise a specific job level.

## Your first study session

1. Open [the bridge](curriculum/00-bridge.md). Try its diagnostic before looking at answers. Study and practice the topics you cannot explain or perform unaided.
2. Open [month 1](curriculum/01-system-map.md). Draw the request-to-hardware path in your own words before comparing it to the lesson.
3. Work through the first lesson's examples on paper. Explain why each step follows. Change one assumption and predict what happens before looking at the solution.
4. Copy [the progress template](assessments/progress-template.md) into a local `learner-work/` directory. Record what you can explain unaided and where the explanation breaks down.
5. End by stating one mechanism you understand, one inference you still need to test, and your next question. When ready, use [the systems lab instructions](labs/systems/README.md) and [an evidence packet](assessments/evidence-template.md) to test the mental model.

Allow a first 90-minute session for diagnosis and orientation. Setup or prerequisite gaps can take longer; log actual time rather than interpreting the estimate as a pass/fail test.

## A repeatable study week

Budget 8-10 hours for scheduled core weeks: roughly 3-4 for theory and drawing the mechanisms, 2 for worked examples and independent questions, 2 for a bounded practical experiment, and 1-2 for review and remediation. These are design estimates, not measured completion times. Theory and examples come first. Stop when the agreed evidence is good enough; do not keep adding optional technologies.

For each lesson:

1. Read the objectives and prerequisite check.
2. Explain the mechanism on paper, including where the explanation could be wrong.
3. Work the numerical example yourself before reading its result.
4. Predict the healthy behavior and at least two plausible fault causes.
5. Run the exercise, change one relevant variable, recover, and verify a positive postcondition.
6. Answer the checkpoint questions without the key. Use the key to locate a gap, then retest with a changed input.
7. Save a small evidence packet and update your progress. At a gate, defend it to a reviewer.

The command output matters less than the causal explanation: what did the experiment distinguish, what action followed, and what proves recovery?

## Choose depth without doubling the workload

The common systems core is months 1-6. Month 7 introduces workload contracts. In months 8-12, select Kubernetes or Slurm as your primary track. Build and troubleshoot it in depth. Use the other track's secondary route for a workload, scheduling/admission analysis, failure/recovery, accounting/evidence review, and a comparison memo. Do not complete both Build routes concurrently inside the core-hour budget.

In months 13-18, select one of [four bounded specialties](specialties/README.md). A second specialty is enrichment after the core. In the practicum, choose the capstone that matches the evidence you want to produce: technical engineering, aspiring leadership, or management decision-making. Each has a different deliverable; none implies equivalent real-world experience.

## Learn from real failures alongside the theory

Use the [failure casebook](incidents/README.md) to see why plausible designs and recovery plans can fail. Begin with [the reading method](incidents/reading-method.md), then the Meta network, GitLab recovery, and OpenAI control-plane cases. Each case separates the published account from an original worked example and gives you a decision question before the answer.

Choose one case that matches your current lesson and use it within a theory or review session. The casebook is optional enrichment, not an extra mandatory track. Later, use the [incident-review workshop](incidents/review-workshop.md) to compare mechanisms and write corrective actions with testable completion criteria.

## Calendar and hardware planning

The [calendar](CALENDAR.md) contains 96 scheduled weeks plus eight unscheduled break weeks. Months 1-18 each reserve the fourth week for validation and remediation. Months 19-22 apply known mechanisms in compound scenarios. Months 23-24 emphasize capstone defense, correction, and transfer.

The bridge sits before this budget. Its duration depends on the diagnostic. If you already have the baseline skills, demonstrate them and proceed. If you do not, complete the bridge exercises; skipping them makes later debugging harder.

L0 exercises run locally with Python. Arrange L1 access before the systems gate, access to both native schedulers before the platform gate, and a controlled multi-node environment before claiming the L2 practicum outcomes. Only use supervised, authorized rack work for L3 claims. Before spending money, read the exact hardware workbook and define the evidence you need. A specific cloud or equipment purchase is not required by this course.

You can study later lessons while waiting for hardware. Keep the relevant outcome `pending-environment`. A clean simulation result does not close that item.

## When you get stuck

- If you cannot explain a term, return to its first lesson and draw a concrete example.
- If a command fails, save the exact output and environment version before changing anything.
- If two explanations fit, choose the smallest safe observation that distinguishes them.
- If setup consumes the lab period, use the local simulation to continue learning and keep native execution pending.
- If a safety, authorization, or recovery prerequisite is missing, stop that operation and use the analysis path.
- If an exercise appears wrong, preserve a minimal reproduction. Correct the material and rerun its validation before trusting the answer key.

Use [the four gates](assessments/gates.md) to decide when to advance. Bring your evidence and the precise point of uncertainty to a reviewer, rather than only asking whether the material "looks right."
