---
title: Rack-scale AI infrastructure
description: A theory-first course in AI infrastructure, from systems foundations and worked examples to platforms, fleet operations, and an integrated practicum.
hide:
  - navigation
  - toc
---

<div class="course-home" markdown="1">

<section class="course-hero" markdown="1">
<div class="course-hero-copy" markdown="1">

<p class="course-kicker">A course in systems, platforms, and operations</p>

# Rack-scale AI infrastructure

<p class="course-deck">Understand the mechanisms.<br>Work the examples.<br>Defend your decisions.</p>

Follow a workload from its first process to the rack around it. Build a foundation in CPUs, GPUs, networks, and storage, then bring those ideas together in workload platforms and fleet operations.

<div class="course-actions" markdown="1">

[Start learning](Learning-Guide.md){ .course-button }
[Explore the course](#the-learning-path){ .course-text-link }

</div>

<p class="course-pace">Self-paced. A 24-month route, with progress based on evidence.</p>

</div>

<aside class="course-example" aria-label="A synthetic worked example from chapter 1" markdown="1">
<p class="course-example-label">Inside chapter 01 <span>Worked example</span></p>
<h2>Two replicas.<br>One shared failure.</h2>
<p>Each replica can serve 60 requests per second. Both depend on the same power feed.</p>
<div class="course-feed" aria-hidden="true">Feed A</div>
<div class="course-nodes" aria-hidden="true">
<div><span>Node A</span><strong>60 <small>req/s</small></strong></div>
<div><span>Node B</span><strong>60 <small>req/s</small></strong></div>
</div>
<dl class="course-calculation">
<div><dt>Nominal capacity</dt><dd>120 <small>req/s</small></dd></div>
<div><dt>After feed A fails</dt><dd>0 <small>req/s</small></dd></div>
</dl>
<p class="course-example-note">Count the shared dependencies, not just the replicas. Synthetic teaching model.</p>

[Read the full worked example](01-System-Map.md#a-failure-domain-is-a-set-of-things-one-event-can-affect){ .course-example-link }

</aside>

</section>

<section class="course-first-session" aria-labelledby="first-session" markdown="1">

<div markdown="1">
<p class="course-kicker">Begin here</p>

## Your first study session { #first-session }

Start with the guide, check your foundations, then draw the path from a request to the hardware that serves it. Allow about 90 minutes; take more time where you need it.

</div>
<ol class="course-first-links" markdown="1">
<li markdown="1">
<span>01</span>
<div markdown="1">

[Read the learning guide](Learning-Guide.md)
<small>How to study, practice, and keep evidence.</small>

</div>
</li>
<li markdown="1">
<span>02</span>
<div markdown="1">

[Try the fundamentals diagnostic](00-Fundamentals-Bridge.md)
<small>Linux, networking, containers, and quantitative reasoning.</small>

</div>
</li>
<li markdown="1">
<span>03</span>
<div markdown="1">

[Open chapter 1: the system map](01-System-Map.md)
<small>Trace dependencies and reason about a failure.</small>

</div>
</li>
</ol>

</section>

<section class="course-path" aria-labelledby="the-learning-path" markdown="1">

<div class="course-section-intro" markdown="1">
<p class="course-kicker">The learning path</p>

## Four stages. One connected system. { #the-learning-path }

Work in prerequisite order. The month numbers provide a pacing plan; the four assessment gates test what you can explain and demonstrate.

</div>

<div class="course-stage" markdown="1">
<div class="course-stage-number" aria-hidden="true">01</div>
<div class="course-stage-title" markdown="1">
<p class="course-stage-period">Months 1-6</p>

### Understand the system

</div>
<div class="course-stage-body" markdown="1">

Trace failure domains through server topology, GPU runtimes, fabrics, storage, and telemetry. Connect those mechanisms to training and inference workloads.

[Start with the system map](01-System-Map.md){ .course-text-link }

</div>
</div>

<div class="course-stage" markdown="1">
<div class="course-stage-number" aria-hidden="true">02</div>
<div class="course-stage-title" markdown="1">
<p class="course-stage-period">Months 7-12</p>

### Build a workload platform

</div>
<div class="course-stage-body" markdown="1">

Begin with the shared workload contract, then choose **Kubernetes or Slurm as your primary track**. Use the other platform's secondary route to run, investigate, recover, and compare within the same study budget.

[Workload contract](07-Workload-Contract.md) / [Kubernetes track](Kubernetes-Track.md) / [Slurm track](Slurm-Track.md)

</div>
</div>

<div class="course-stage" markdown="1">
<div class="course-stage-number" aria-hidden="true">03</div>
<div class="course-stage-title" markdown="1">
<p class="course-stage-period">Months 13-18</p>

### Reason about the fleet

</div>
<div class="course-stage-body" markdown="1">

Work with fleet truth, reliability, incidents, lifecycle automation, and capacity. Choose one specialty and follow a bounded intervention from its initial hypothesis through recovery and verification.

[Begin fleet operations](13-Fleet-Truth.md) / [Choose a specialty](Specialties.md)

</div>
</div>

<div class="course-stage" markdown="1">
<div class="course-stage-number" aria-hidden="true">04</div>
<div class="course-stage-title" markdown="1">
<p class="course-stage-period">Months 19-24</p>

### Integrate, recover, and defend

</div>
<div class="course-stage-body" markdown="1">

Apply the mechanisms to an unfamiliar synthetic fleet. Investigate performance, recover from compound failures, evaluate readiness, and defend one role-family capstone with reproducible evidence.

[Explore the practicum](Practicum.md) / [View the capstones](Capstones.md)

</div>
</div>

<p class="course-path-footer" markdown="1">[See the full study calendar](Study-Calendar.md) <span aria-hidden="true">/</span> [Read the four assessment gates](Assessment-Gates.md)</p>

</section>

<section class="course-method" aria-labelledby="how-learning-works" markdown="1">

<div class="course-section-intro" markdown="1">
<p class="course-kicker">Theory comes first</p>

## Learn it well enough to explain it. { #how-learning-works }

The lesson explains the mechanism. Worked examples expose the assumptions. Practical work tests your explanation.

</div>

<div class="course-method-grid">
<div><span>01 / Read</span><h3>Build the model</h3><p>Trace what depends on what. Draw the mechanism before reaching for commands.</p></div>
<div><span>02 / Work</span><h3>Follow the example</h3><p>Do the calculation yourself. Change one assumption and predict the result.</p></div>
<div><span>03 / Explain</span><h3>Test your reasoning</h3><p>Answer without the key. Find the gap, then try again with a different input.</p></div>
<div><span>04 / Apply</span><h3>Keep the evidence</h3><p>Run a bounded experiment. Record what happened, why, and what it cannot prove.</p></div>
</div>

</section>

<section class="course-practice" aria-labelledby="practice-with-purpose" markdown="1">
<div markdown="1">
<p class="course-kicker">From the page to practice</p>

## Start local. Make precise claims. { #practice-with-purpose }

Local Python exercises let you test reasoning with synthetic data. Native platforms, GPUs, and multi-node systems require their own environments and evidence. Study can continue while an environment-dependent outcome remains pending.

The 8-10 hour weekly budget is an initial estimate, with theory and worked examples taking priority. Hardware access and actual execution are recorded separately from course completion.

</div>
<div class="course-resource-links" markdown="1">

[Systems labs](Systems-Labs.md)

[Hardware workbook](Hardware-Workbook.md)

[Progress template](Progress-Template.md)

[Sources and evidence](Sources-and-Evidence.md)

</div>
</section>

<footer class="course-home-footer" markdown="1">

This course is public self-study material. It does not award a credential or authorize changes to shared systems. [View source and validation records]({{REPOSITORY}}/blob/{{SOURCE_COMMIT}}/DELIVERY-STATUS.md).

</footer>

</div>
