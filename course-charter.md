# Rack-Scale AI Infrastructure Course — Design Charter

- Status: approved design baseline
- Design date: 2026-07-09
- Delivery boundary: private planning artifacts only
- Reference repository: anowarislam/ml-in-k8s at commit e3b39d479fa27d9a0cd9be2de7217b94addedc89, read-only

## Executive decision

Create a new, separate course-planning repository for a 24-month program:

- Months 1–18: a T-shaped core.
- Months 19–24: a spiral advanced practicum.
- Entry point: experienced infrastructure practitioner.
- Primary technical context: NVIDIA rack-scale GPU and AI infrastructure.
- Transfer model: standards-based Linux, Redfish, Kubernetes, Slurm, RDMA, telemetry, reliability, and engineering-leadership mechanisms.
- Audience exits: experienced infrastructure engineer, aspiring engineering leader, and current manager/director.
- Platform design: Kubernetes and Slurm are independently complete course tracks. Each learner reaches Build depth in a primary platform and Run/compare depth in the secondary platform.
- Specialty design: each learner selects one primary technical specialty.
- Lab design: L0 emulation, L1 single-node GPU, L2 controlled multi-node, and L3 supervised rack work. Physical RDMA is required only for outcomes that claim RDMA behavior.
- No award, certification, or claim of job equivalence.

The existing ml-in-k8s repository is useful reference material for chapter anatomy, dependency gates, progressive exercises, version metadata, and executable validation. It is not the target course and will not be modified.

## Problem statement

The target NVIDIA role is broader than an ML-on-Kubernetes curriculum. It combines rack-scale systems, fleet operations, incident response, roadmap and change management, operational readiness, reliability metrics, automation, telemetry, hardware/software/firmware/network collaboration, NPI feedback, executive communication, and people leadership.

The complementary principal-engineer profile adds rack SW/FW coordination, fabric and NVSwitch recovery, multi-component firmware orchestration, serviceability, health APIs, CSP integration, and influence without authority.

Primary role anchors:

- [NVIDIA Director, Engineering Operations and Site Reliability Engineering — Datacenter Server Systems, JR2020349](https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Director--Engineering-Operations-and-Site-Reliability-Engineering---Datacenter-Server-Systems_JR2020349)
- [NVIDIA Principal Software Engineer, Rack-Scale System Software — CSP Engagements, JR2020316](https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Principal-Software-Engineer--Rack-Scale-System-Software---CSP-Engagements_JR2020316)

Current public OpenAI and Anthropic material is an adjacent comparison lens. It is not evidence of NVIDIA requirements or of either company’s private stack.

## Claim ceiling

This program develops and assesses bounded competencies. It does not compress 12–15 years of production ownership, incidents, vendor work, organizational leadership, or accumulated judgment into two years.

The course may claim that a learner completed defined outcomes at a named fidelity level and produced specified evidence. It must not claim:

- readiness for a specific NVIDIA, OpenAI, or Anthropic role;
- equivalence to principal, senior-manager, or director experience;
- physical repair competence from emulation;
- fleet-scale realism from a single GPU;
- knowledge of confidential frontier-lab architecture;
- certification, endorsement, or affiliation with a referenced company.

## Evidence language

Every consequential claim uses one of four labels:

- Verified public fact: explicitly stated by a dated, official source within its stated scope.
- Strong inference: several official signals support the conclusion and few alternatives fit.
- Weak inference: plausible, but materially different explanations remain.
- Speculation or unknown: insufficient primary evidence; preserve the uncertainty.

Forward-looking announcements are labeled planned and are never presented as deployed facts.

## Audience and admission

### Shared entry baseline

Learners are expected to demonstrate:

- production Linux administration;
- shell, Git, scripting, and basic infrastructure automation;
- IP networking, DNS, storage, containers, and troubleshooting;
- experience operating or supporting distributed systems;
- ability to read code, logs, metrics, traces, and configuration;
- familiarity with incident and change workflows.

Missing fundamentals belong in a separate bridge, not inside the 24-month core.

### Depth vocabulary

- Read: explain, question, and identify assumptions or failure domains.
- Run: operate safely and diagnose bounded failures using evidence.
- Build: design, automate, test, recover, and hand off a system under ambiguity.
- Lead: establish mechanisms, direct cross-team execution, make risk decisions, and develop others.

Build permits configuration and integration of supported platform components, implementation of bounded external lifecycle services or reconcilers, validation tooling, diagnostic automation, dashboards, and safe-delivery mechanisms. It does not require modifying Kubernetes or Slurm internals, producing a production-grade custom operator/plugin, or maintaining a general-purpose control plane.

Leadership outcomes carry one evidence class:

- Course-observed: behavior visible in a scenario, review, or submitted follow-through cycle.
- Workplace-evidenced: longitudinal evidence from a real operating context.
- Transfer objective: important professional behavior that the course can prepare but cannot establish.

### Exit expectations

Experienced infrastructure engineer:

- Run across all five competency pillars.
- Build the primary scheduler platform.
- Build one technical specialty.
- Diagnose hidden cross-layer failures.
- Lead a bounded technical incident workstream.

Aspiring engineering leader:

- Run across the stack.
- Build one credible technical anchor.
- Lead incidents, changes, readiness reviews, NPI closure, roadmaps, and mentoring.
- Produce evidence of follow-through, not only meeting artifacts.

Manager or director:

- Read and challenge the full stack.
- Run critical scenarios.
- Retain one credible technical anchor.
- Lead fleet health, capacity, risk, vendors, organizational design, executive communication, and technical-leader development.
- Treat simulated leadership work as practice, not proof of longitudinal management performance.

Incident command, risk decisions, delegation, and executive communication can be course-observed. Sustained coaching, succession, organization design, and leader development remain workplace-evidenced or transfer objectives.

## Five competency pillars

### 1. Rack and hardware systems

Server internals, CPU and memory topology, PCIe, asset identity, BMC and Redfish, boot and firmware, GPU, NVLink and NVSwitch, high-speed fabric, storage, power and thermal operational interfaces, RAS, platform security, and safe serviceability.

### 2. Cluster and workload platforms

Linux, provisioning, Kubernetes, Slurm, topology-aware allocation, accelerator exposure, HA, upgrades, distributed training and inference, checkpointing, correctness, utilization, latency, throughput, and recovery.

### 3. Fleet reliability and operations

Telemetry, time integrity, health scoring, statistical reliability, lifecycle, incident command, change safety, operational readiness, capacity and spares, NPI feedback, serviceability, vendor escalation, and repair-item closure.

### 4. Automation and developer leverage

State machines, reconcilers, APIs, idempotency, concurrency, inventory and control planes, CI, hardware-in-loop validation, safe delivery, observability platforms, reproducible builds, evidence capture, and paved paths.

### 5. Leadership and execution

Engineering judgment, cross-functional and vendor execution, roadmaps, executive reporting, operating models, team design, hiring, coaching, delegation, on-call sustainability, succession, and technical-leader development.

Cross-cutting requirements:

- safety, security, privacy, and access control;
- quantitative reasoning, statistics, cost, and capacity;
- evidence, reproducibility, version boundaries, and support status;
- clear technical, incident, and executive communication.

## Program architecture

Complete curriculum catalog:

~~~mermaid
flowchart TD
    A["Shared systems and workload-management core"] --> K["Complete Kubernetes track"]
    A --> S["Complete Slurm track"]
    K --> F["Fleet operations and specialty catalog"]
    S --> F
    F --> C["Three role-family capstone designs"]
    C --> P["Spiral practicum scenario bank"]
~~~

Individual learner route:

~~~mermaid
flowchart TD
    A["Admission diagnostic and lab charter"] --> B["Months 1–6: shared systems core"]
    B --> C["Month 7: shared workload-management semantics"]
    C --> P["Months 8–12: primary platform Build path"]
    C --> Q["Months 8–12: secondary platform Run/compare package"]
    P --> G2["Platform Gate G2"]
    Q --> G2
    G2 --> F["Months 13–18: fleet operations and one bounded specialty"]
    F --> E["Role-family capstone proposal"]
    E --> R["Months 19–24: spiral advanced practicum"]
    R --> Z["Evidence, limitations, remediation, and workplace transfer"]
~~~

The T-shaped horizontal bar is shared systems, fleet operations, automation, cross-platform comparison, and leadership judgment. The vertical stem combines the primary platform and one specialty.

The secondary-platform minimum is not a survey. It includes: one deployed representative workload; one platform-native scheduling or admission analysis; one failure and recovery exercise; one accounting or evidence review; and one comparison memo covering topology, fairness, identity, change, and recovery. It does not require building platform internals.

## Twenty-four-month roadmap

The planning calendar contains 96 scheduled course weeks and 8 unscheduled break weeks across 24 months. Of the scheduled weeks, 70 introduce or build new mechanisms, 18 are reserved for remediation, validation, hardware contingency, or reassessment, and 8 are reserved for capstone defense and transfer. Learner effort is planned at 8–10 hours per scheduled week, for a provisional 768–960-hour envelope. Pilot data may reduce mandatory scope; it must not silently increase the envelope.

Hard scope budgets:

- No more than 12 mandatory atomic outcomes and 6 assessed exercises per gate.
- No mandatory unit longer than 3 active weeks.
- Every mandatory unit must feed a gate, produce reviewable evidence, and recur in the spiral practicum.
- Each specialty lane is an umbrella; the learner selects one bounded focus with one measurable intervention.
- New material displaces existing material. It never creates a fifth gate or extends the learner-hour envelope without a new design decision.

| Month | Theme | Observable outcome |
|---|---|---|
| 1 | Entry diagnostic, system-of-systems map, safety, evidence, claim boundaries | Rack-to-workload failure-domain map and individual bridge decision |
| 2 | CPU, memory, NUMA, PCIe, asset identity, BMC/OOB, boot, firmware | Reconcile OS, BMC, and inventory views; design a safe change |
| 3 | GPU, driver/runtime boundary, PCIe, NVLink-class scale-up, RAS | Trace the host-to-GPU path and diagnose a bounded L1 fault |
| 4 | Ethernet/InfiniBand-class fabrics, RDMA, collectives, storage and checkpoints | Distinguish compute, scale-up, scale-out, and storage bottlenecks |
| 5 | Power, thermal, telemetry integrity, identity, secrets, supply chain | Reconcile signals and identify unsafe or misleading conclusions |
| 6 | Distributed training and inference integration | Run bounded L1 workloads and pass Systems Gate G1 |
| 7 | Shared workload-management contract | Express resource, topology, fairness, identity, data, and recovery needs without false platform equivalence |
| 8 | Primary platform construction; secondary orientation | Build a primary reference environment and run a secondary workload |
| 9 | Scheduling, admission, topology, priority, fairness, fragmentation | Diagnose and correct misplaced or pending work |
| 10 | Training/inference lifecycle, data, checkpoint and restart | Interrupt, recover, and validate representative workloads |
| 11 | Tenancy, security, observability, upgrades, node and control-plane recovery | Recover a platform failure and produce a bounded change plan |
| 12 | Primary integration and secondary Run/compare | Pass Platform Gate G2 and explain consequential differences |
| 13 | Asset truth, desired/observed state, telemetry time integrity | Define authoritative fleet state and scope one specialty |
| 14 | Statistical reliability and health-signal quality | Use exposure denominators, uncertainty, censoring, and false-rate reasoning |
| 15 | Incident response, problem analysis, and safe change | Lead an incident role and choose rollback, forward recovery, quarantine, or irreversibility |
| 16 | Lifecycle automation and CI | Model qualification, drain, repair, promotion, refresh, and decommission as tested state transitions |
| 17 | Capacity, ORR, NPI, and specialty intervention | Produce a capacity model, run readiness/NPI review, and execute a bounded intervention |
| 18 | Specialty validation and role-family capstone proposal | Operationalize one specialty and pass Integrated Core Gate G3 |
| 19 | Spiral: inherit and baseline an unfamiliar system | Reconstruct topology, ownership, workload, SLOs, security, and evidence gaps |
| 20 | Spiral: cross-layer performance | Diagnose training-goodput or inference-tail regression across system layers |
| 21 | Spiral: controlled failure, change, and recovery | Execute an L2 scenario, recover, and prove hidden health |
| 22 | Spiral: supervised rack ORR/NPI/serviceability | Exercise the integrated rack boundary at L3 when authorized; otherwise retain L2 claim ceiling |
| 23 | Spiral: fleet capacity, incident, and leadership | Resolve a compound portfolio scenario and deliver the role-family capstone |
| 24 | Defense, remediation, and workplace transfer | Reproduce evidence, close remediation, state unsupported claims, and define a transfer plan |

### Gates

- G1 Systems: full hardware/workload path, L0/L1 diagnosis, and safe-change plan.
- G2 Platform: primary Build, secondary Run/compare, workload recovery, and platform-native diagnosis.
- G3 Integrated core: lifecycle, statistical reliability, incidents/change, capacity/ORR/NPI, automation, and one specialty.
- G4 Practicum evidence: integrated diagnosis, recovery, role-family execution, and explicit fidelity ceiling. This is a learning review, not a credential.

## Module-specification boundaries

### Shared systems core

Purpose: establish the cross-layer model from request and scheduler through server, accelerator, fabric, storage, management plane, power, and facility boundaries.

Required groups:

1. Failure domains, safety, and evidence.
2. Server, NUMA, PCIe, BMC/OOB, boot, firmware, inventory, and platform security.
3. GPU, driver/runtime, memory, NVLink-class scale-up, topology, and RAS.
4. Scale-out fabric, RDMA, collectives, congestion, storage, and checkpoints.
5. Power, thermal behavior, telemetry integrity, and security.
6. Distributed training/inference mechanisms and cross-layer diagnosis.

Non-goals: board or ASIC design, custom BMC development, live electrical work, thermal abuse, ML theory, and command memorization.

### Platform tracks

Purpose: make Kubernetes and Slurm independently complete while giving each learner deep primary competence and meaningful secondary comparison.

Shared outcome families:

- resources and accelerator exposure;
- placement, topology, admission, and fairness;
- identity, tenancy, security, data, and accounting;
- distributed training and inference;
- telemetry, upgrades, HA, incident response, and recovery.

Kubernetes remains platform-native: API server, etcd, scheduler, controllers, admission, CRDs/operators, namespaces, RBAC, device allocation, desired-state convergence, and version skew.

Slurm remains platform-native: controller and execution daemons, partitions, QOS, associations, GRES/TRES, cgroups, topology, backfill, reservations, accounting, job steps, prolog/epilog, requeue, state persistence, and upgrade compatibility.

False friends such as the different meanings of gang scheduling must be called out explicitly.

Non-goals: identical command sets, identical learner hours, platform interchangeability, or repeatedly reimaging one supported rack to manufacture symmetry.

### Fleet operations

Purpose: turn working platforms into a safely operable fleet.

Required groups:

1. Asset identity, desired/observed state, telemetry, time integrity, and data quality.
2. Bring-up, qualification, drain, repair, change, refresh, and decommission.
3. Exposure-normalized reliability, uncertainty, Pareto/survival reasoning, signal validation, and drift.
4. Incident command, recovery, communications, and follow-through.
5. Change automation, CI, compatibility matrices, rings, stop conditions, ORR, NPI, capacity, and spares.

### Specialty lanes

Launch with no more than four:

1. Rack lifecycle, firmware, serviceability, RAS, power/thermal interfaces, and platform security.
2. Accelerator, scale-up, RDMA fabric, storage, and workload performance.
3. Workload-platform scheduling and control using the primary Kubernetes or Slurm track.
4. Fleet reliability, lifecycle automation, CI, and developer leverage.

Every specialty follows characterize, intervene, validate, recover, and operationalize. A second specialty is outside the core.

### Role-family capstones

Developer or principal:

- diagnose, recover, and reduce recurrence for a cross-layer failure;
- deliver a technical intervention and automation;
- defend causal evidence and claim boundaries.

Aspiring leader:

- lead a multi-team incident, change, readiness, or NPI cycle;
- establish milestones, owners, dependencies, risk decisions, and follow-through.

Manager or director:

- make and defend a capacity, NPI, reliability, staffing, platform, or change-safety portfolio decision;
- establish operating mechanisms and communicate residual risk.

### Spiral practicum

Purpose: revisit the complete system with increasing ambiguity, fidelity, and consequence. It introduces no new survey domains.

Operating loop:

Observe → Build → Break → Detect → Decide → Recover → Verify → Review → Automate

The practicum uses calibrated compound scenarios, changing evidence, decoys, fault-free controls, and role-specific outputs.

## Lab-level model

L0–L3 is a course taxonomy, not an industry standard.

| Level | What it may establish | Default boundary |
|---|---|---|
| L0 emulation | API semantics, state machines, scheduler policy reasoning, validation, and safe failure handling | No claims about physical performance, RDMA, PCIe/NVLink, real firmware, optics, power, or thermal behavior |
| L1 single GPU | Actual driver/runtime/device behavior, single-node isolation, DCGM/kernel evidence, and workload correctness | No multi-node/fabric claims; no real firmware writes, BMC reset, or physical service |
| L2 controlled multi-node | Multi-node scheduler/control-plane behavior, node lifecycle, checkpoint recovery, and observed network behavior on the recorded topology. Physical RDMA is required only for RDMA claims | Dedicated environment only; no physical hotplug, firmware writes, shared-production faults, PDU, facility, or thermal manipulation |
| L3 supervised rack | Physical inventory/topology reconciliation, vendor-approved service/firmware workflow, rack diagnosis, and operational handoff on the exact BOM | Supervised and separately authorized; no unsupervised firmware, hotplug, power, energized service, thermal override, or production fault injection |

Lower-tier fallback visibly lowers the claim. It never silently counts as equivalent completion.

Managers may satisfy an L3 learning objective through supervised observation, risk decisions, and evidence review. The portfolio must distinguish executed, observed, simulated, and analyzed work.

L0–L3 is only the environment-fidelity axis. Every lab also declares:

- environment: emulated, single-node, multi-node, or rack;
- accelerator count and topology;
- RDMA: none, software-emulated, or physical;
- operation risk: sandbox, controlled write, disruptive, or qualified service;
- actor: learner, asset owner, instructor under dual control, or qualified service person;
- support posture: vendor-supported, documented exception, or emulation-only.

A physical BMC lab on a non-GPU server and a multi-node CPU scheduler-HA lab are therefore classifiable without pretending they establish GPU or RDMA competence.

## Lab operating charter

No L2 or L3 work may run without:

- named environment owner and lab SRE;
- booking, exclusive locking, concurrency limits, and learner isolation;
- frozen supported BOM and private asset overlay;
- isolated OOB management network;
- least-privilege, just-in-time credentials and audited break-glass access;
- synchronized UTC time and evidence redaction;
- maintenance window, blast radius, abort conditions, and recovery owner;
- explicit recovery mode: rollback, forward recovery, rebuild, quarantine, vendor recovery, or documented irreversibility;
- positive-health, meta-monitoring, post-change, cleanup, and reset checks;
- facility/EHS and qualified-service ownership;
- sacrificial equipment and spares where destructive or irreversible risk exists;
- warranty, support, insurance, licensing, and export gates;
- lab SLOs, incident severity, escalation, and rescheduling rules.

The course never includes branch-circuit work, deliberate overheating, fan/interlock bypass, unsafe lifting, energized chassis service, or unauthorized physical intervention.

## Authorization model

Operations are classified as:

- self-service sandbox;
- just-in-time ticket and asset-owner approval;
- supervised dual control;
- qualified-service execution with learner observation;
- prohibited course activity.

Environment level alone never grants authority.

L3 is necessary but never sufficient for a high-risk operation. Asset eligibility, current vendor procedure, site/facility approval, operation-specific authorization, qualified personnel, dual control, recovery preconditions, and a valid maintenance window must all be satisfied.

| Operation class | Eligibility | Permitted actor |
|---|---|---|
| Mock API, VM, namespace, and assigned workload actions | Eligible under the lab profile | Learner |
| Real telemetry and approved non-disruptive configuration | Conditionally eligible | Learner or asset owner under just-in-time authorization |
| Node reboot, dedicated switch-port action, or disruptive host change | Conditionally eligible | Asset owner or instructor under dual control |
| BMC reset or configuration write | Conditionally eligible only on explicitly approved assets | Qualified instructor or asset owner under dual control |
| Firmware update, approved hotplug, PDU outlet action, or instructor-seeded physical fault | Conditionally eligible only when the vendor/site procedure permits it | Qualified service, facility, or vendor-authorized person; learner observes, plans, or validates |
| Forced downgrade or recovery flash | Ineligible unless an asset-specific vendor recovery procedure explicitly authorizes it | Qualified vendor/service person |
| Main rack power, branch circuits, thermal/fan/interlock override, energized chassis service, deliberate overheating | Always prohibited as course activity | No course actor |

Course approval can never override local law, facility rules, warranty/support terms, the current hardware manual, or stop-work authority.

## Validation and traceability

~~~mermaid
flowchart LR
    S["Official source or stated design inference"] --> C["Atomic competency"]
    C --> M["Module outcome"]
    M --> L["Lab or decision exercise"]
    L --> A["Observable assessment"]
    A --> E["Redacted evidence"]
    E --> R["Revalidation and staleness control"]
~~~

A competency counts as complete only when it has:

1. evidence level, source, access date, and applicability;
2. director or principal alignment kept distinct;
3. admission prerequisites;
4. precise outcome, non-goals, and claim ceiling;
5. audience and primary/secondary depth;
6. platform-native design;
7. lab level, supported BOM, and authorization profile;
8. happy path, failure, detection, diagnosis, recovery, and irreversible-change handling;
9. positive health, meta-monitoring, time integrity, and audit;
10. machine validation and/or calibrated human review;
11. sanitized evidence with raw-store restrictions;
12. clean reset and bounded replay;
13. owner, last-validated date, support expiry, and upgrade path.

Release checks reject:

- orphan competencies;
- modules without a gate outcome;
- labs without mapped outcomes;
- Build claims supported only by L0;
- unlabeled simulation claims;
- zero scores in safety, authorization, licensing, or evidence handling.

The review rubric uses a 0–3 scale:

- 0: unsafe, unsupported, or no usable evidence;
- 1: partial recognition without reliable diagnosis or recovery;
- 2: correct diagnosis, safe action, recovery, and evidence-backed verification;
- 3: anticipates blast radius, handles decoys, validates the monitoring path, and explains limits.

Claim honesty, safety, authorization, licensing, and evidence handling are blocking dimensions: a score of 0 blocks the lab regardless of the total.

Evaluation mode is outcome-specific:

- deterministic state, configuration, and invariant outcomes require machine validation;
- technical judgment, incident command, risk decisions, communication, and coaching require calibrated human review;
- Build and Lead outcomes require both machine evidence where applicable and human review of causal reasoning;
- consequential leadership scenarios use two reviewers or recorded adjudication.

Hidden-fault scenarios use seeded ground truth, controlled injectors, decoy signals, optional fault-free controls, bounded duration, abort signals, expected evidence, and clean reset. Pure randomization is prohibited because it creates unequal or ambiguous exercises.

Representative scenarios:

- telemetry loss plus clock drift corrupts an apparent causal timeline;
- correctable PCIe noise distracts from a workload configuration fault;
- one RDMA path degrades while NCCL continues slowly;
- checkpoint completion is reported before atomic commit;
- Redfish reports task completion while component inventory remains stale;
- Kubernetes admission/control dependencies block progress while the API server is healthy;
- Slurm jobs run while accounting or fair-share state becomes misleading;
- mixed-fleet firmware/driver rollout partially converges with no safe rollback;
- fabric degradation, checkpoint pressure, and monitoring blindness coincide;
- repeated cross-rack failures reveal an NPI/serviceability escape;
- executive pressure conflicts with a safe stop decision.

## Course operations and maintenance

Required ownership:

- program owner;
- release engineer;
- lab SRE;
- evidence steward;
- one subject owner plus backup per pillar;
- separate Kubernetes and Slurm track owners;
- safety/facility owner;
- security/licensing owner;
- publication steward.

Each term uses a frozen BOM containing:

- hardware and accelerator generation;
- OS and kernel;
- Kubernetes, Slurm, operators, and controllers;
- driver, CUDA, NCCL, DCGM, NIC, switch, BMC, BIOS, CPLD, and firmware;
- immutable image and package digests;
- license and redistribution status;
- vendor support status and expiry;
- known incompatibilities;
- tested upgrade and recovery path.

The value latest is prohibited in assessed labs.

Recommended cadence:

- every change: schemas, links, mappings, secrets, licenses, and impacted tests;
- weekly: issue triage, lab health, capacity, and incidents;
- monthly: version, source, cost, capacity, and owner review;
- before each cohort: rehearsal, safety approval, capacity proof, and recovery test;
- quarterly: role alignment, evidence, risk, platform parity, and deletion review;
- semiannually: supported release and architecture review;
- event-driven: safety/security event, vendor release, standard revision, posting removal, or API deprecation.

## Evidence model

Evidence is evaluated on two independent axes.

Target-role relevance:

1. The exact NVIDIA director and principal role sources.
2. Other official NVIDIA role and product-context sources.
3. Official OpenAI and Anthropic public signals as adjacent transfer evidence.
4. Emerging research, previews, and explicitly labeled hypotheses.

Claim authority:

1. Applicable law, site/facility rules, and qualified safety authority.
2. Ratified standards and version-specific vendor safety, support, and product documentation.
3. Official engineering disclosures and incident reports within their stated scope.
4. Job postings for stated responsibilities and desired experience.
5. Supported inference and explicitly labeled hypotheses.

The axes are not interchangeable. An NVIDIA job posting ranks highly for target-role relevance but does not override a safety manual, standard, support matrix, or facility rule. Multiple lower-authority citations do not become a normative claim.

A role posting is authoritative for what it asks for, not for actual task frequency or internal architecture. Product documentation is authoritative for the stated product and version, not for universal deployments. A standard is authoritative for normative behavior, not proof that a specific deployment implements it.

Negative findings record search scope and say no evidence found within this search scope. They never say a system or practice does not exist.

## Optional frontier-stack hypothesis map

Artifact: research/frontier-stack-hypotheses.md

Placement:

- optional seminar after G2 in month 12;
- optional rubber-duck reconstruction during month 19 or 23;
- removed before any mandatory work when calendar slack is consumed.

The map covers compute, scheduler, networking, storage, training runtime, inference runtime, observability, developer productivity, security, reliability, and management.

Each atomic hypothesis records:

- company and stack layer;
- claim tense: current, historical, planned, or target;
- evidence sources, dates, locators, and scope;
- verified/strong/weak/speculation label and rationale;
- competing explanations;
- falsifier;
- negative findings;
- freshness and review trigger;
- course relevance;
- requirement eligibility, default false;
- private/public disposition.

The detailed company-by-company reconstruction belongs only in the hypothesis artifact, where every atomic statement has a source ID, publication/access date, locator, scope, confidence label, competing explanation, and falsifier. The charter intentionally makes no company-stack implementation claim.

The appendix never becomes an answer key. Its purpose is to teach observation, reconstruction, alternatives, falsifiers, and uncertainty.

## Private-to-public plan

Artifact states:

1. private-restricted;
2. private-reusable;
3. public-candidate;
4. public-approved.

Every artifact receives publish, transform, omit, or seek-permission disposition.

Public release requires:

- provenance and classification inventory;
- license and third-party rights review;
- nominative trademark and logo review;
- explicit non-affiliation language;
- security, privacy, secret, identifier, and export review;
- current sources and labeled inference;
- public-safe clean-room diagrams;
- synthetic, minimized, seeded fault bundles;
- reproducible build and supported-version checks;
- independent technical, evidence, safety, licensing, accessibility, and editorial approval;
- correction, takedown, and incident ownership.

Rumors, leaks, anonymous claims, employee social media, and procurement speculation are requirement-ineligible and do-not-publish.

## Risks and pre-mortem

This table seeds risks.md. Role owners are valid during planning; named assignees are required before feasibility approval.

| Failure | Early warning | Owner role | Mechanism | Stop condition | Residual risk |
|---|---|---|---|---|---|
| Course becomes an encyclopedia | Mandatory outcomes exceed a gate budget | Program owner | Delete anything without a gate, evidence packet, and spiral recurrence | Freeze additions until scope returns within budget | Medium |
| Learners finish shallow or drop out | Setup/remediation consumes reserved weeks | Program owner | Preserve scheduled remediation weeks and pilot actual time | Reduce mandatory scope before increasing hours | Medium |
| Hardware becomes a queue | Wait exceeds one lab cycle | Lab SRE | Booking, concurrency cap, spares, early access proof, and reduced-claim fallback | Stop enrollment or defer the affected fidelity claim | High until capacity is contracted |
| A learner strands equipment | Ad hoc firmware or power exception | Asset and safety owners | Authorization matrix, sacrificial assets, supervised L3, stop-work authority | Stop all affected write activity | Low after controls; impact remains high |
| Labs become stale | Support matrix expires mid-cohort | Release engineer | Frozen term BOM and event-driven validation | Quarantine stale write labs | Medium |
| Scheduler parity is cosmetic | One track lacks native HA/change/failure work | Track owners | Independent traceability and cross-track review | Block G2 release for both tracks | Medium |
| Leadership becomes theater | Artifacts lack consequences or closure | Leadership module owner | Timed decisions, observed delegation, owner tracking, and follow-through evidence | Remove unsupported Lead claim | Medium |
| Monitoring silently fails | Alerts pass while collection/delivery is broken | Lab SRE | Positive health, meta-monitoring, and telemetry fault injection | Quarantine the scenario | Low |
| Evidence leaks sensitive data | Raw identifiers or secrets enter the repository | Security/evidence owners | Private overlay, redaction, restricted raw store, retention policy | Stop collection and invoke incident handling | Low after controls; impact remains critical |
| Public release violates rights | Unresolved diagrams, binaries, or terms | Publication steward | Rights manifest, allowlisted export, independent publication gate | Block publication | Low |
| Frontier reconstruction becomes gossip | Speculation is presented as fact | Evidence steward | Atomic labels, alternatives, falsifiers, requirement-ineligible default | Remove the claim from learner material | Medium |
| One expert becomes a bottleneck | No owner backup or lab on-call | Program owner | Named owner and backup, train-the-trainer, enrollment gate | Reduce scope or enrollment | Medium |

## Scope cuts

The core excludes:

- second platform at Build depth;
- second specialty;
- ASIC or board design;
- custom CUDA-kernel and collective development;
- custom BMC firmware implementation;
- switch-OS/BGP/EVPN deep administration;
- parallel-filesystem implementation;
- Kubernetes operator or Slurm plugin development;
- facility electrical and liquid-cooling engineering;
- full ML theory, compliance, procurement, or people-management curricula;
- guessed private frontier-lab implementation details.

Those may become later specialties only when a gate, safe lab, owner, and evidence path exist.

## Planning-repository structure

~~~text
rack-scale-ai-infrastructure-course/
├── README.md
├── course-charter.md
├── evidence/
│   ├── source-ledger.yaml
│   ├── nvidia-director-alignment.md
│   ├── nvidia-principal-alignment.md
│   └── frontier-transfer-signals.md
├── competencies/
│   ├── competency-matrix.yaml
│   ├── audience-depth.md
│   ├── prerequisites.md
│   └── specialty-lanes.md
├── roadmap/
│   ├── 24-month-roadmap.md
│   ├── t-shaped-core.md
│   ├── spiral-practicum.md
│   └── dependencies.yaml
├── module-specs/
│   ├── module-template.md
│   ├── 01-shared-systems-core.md
│   ├── 02-platform-tracks.md
│   ├── 03-fleet-operations.md
│   ├── 04-specialty-lanes.md
│   ├── 05-role-family-capstones.md
│   └── 06-spiral-practicum.md
├── lab-planning/
│   ├── lab-levels.md
│   ├── operating-charter.md
│   ├── bom-template.yaml
│   └── safety-and-authorization.md
├── validation/
│   ├── completeness-contract.md
│   ├── traceability-matrix.yaml
│   ├── review-rubrics.md
│   └── staleness-policy.md
├── decisions/
│   ├── 0001-t-shaped-plus-spiral.md
│   ├── 0002-evidence-hierarchy.md
│   ├── 0003-platform-track-parity.md
│   └── 0004-lab-level-claims.md
├── research/
│   └── frontier-stack-hypotheses.md
├── risks.md
└── publication-readiness.md
~~~

No chapter content, manifests, executable labs, course images, or infrastructure deployment belong in this first planning package.

The planning repository will include a policy check that rejects executable files, deployable manifests, container images, credentials, direct asset identifiers, and writes or generated output outside this repository. Reuse from ml-in-k8s requires a provenance record, rights review, and an explicit copy decision; conceptual reference is not permission to copy.

## Artifact execution order and statuses

Ordered first tranche:

1. Source ledger and rights-safe director/principal role maps.
2. Competency matrix, audience depth, prerequisites, and specialty boundaries.
3. Four decision records.
4. Roadmap, dependency graph, and gate budgets.
5. Six module specifications.
6. Lab fidelity, authorization, operating charter, and BOM schema.
7. Validation, traceability, review, and staleness artifacts.
8. Risk register, frontier hypothesis map, and publication-readiness plan.
9. Cross-artifact consistency and reader review.

The first five items can begin only after their upstream records exist. Lab and validation policy may proceed in parallel once competency IDs, module IDs, and decision records are stable.

Repository statuses:

- Design baseline: this charter is internally approved and self-reviewed.
- Planning-complete: all listed planning artifacts exist, cross-reference stable IDs, and meet the acceptance criteria.
- Feasibility-confirmed: named owners, hardware capacity, safety/legal/licensing approvals, supported BOMs, and pilot resources are committed.
- Implementation-ready: feasibility is confirmed and the first content/lab implementation plan is approved.

Planning may use role-based owners. Feasibility-confirmed requires named assignees.

## Accepted design decisions

1. Separate folder; ml-in-k8s remains reference-only.
2. Private initially, structured for later public release.
3. Experienced-infrastructure entry baseline.
4. NVIDIA-centered and standards-based.
5. Five competency pillars.
6. Eighteen-month T-shaped core plus six-month spiral practicum.
7. Independently complete Kubernetes and Slurm tracks.
8. Primary platform Build; secondary platform Run/compare.
9. One specialty.
10. Separate role-family exits.
11. L0–L3 fidelity and strict claim ceilings.
12. Planning artifacts only.
13. No award or certification framework.
14. Frontier-stack reconstruction is optional, evidence-labeled, and requirement-ineligible.

## Planning-package acceptance criteria

The initial package is complete when:

- the charter and all four decision records are internally consistent;
- rights-safe NVIDIA role metadata, retrieval date, locator, content hash or restricted snapshot reference, and minimal quoted excerpts are mapped separately for director and principal profiles;
- every competency has an owner, audience depth, module, planned exercise, evidence type, and validation path;
- the 24-month roadmap maps to module specifications and four gates;
- both platform tracks meet the same outcome-family quality bar without false symmetry;
- each lab level states allowed and prohibited claims;
- lab operating, authorization, BOM, safety, evidence, staleness, and fallback policies are explicit;
- risks have triggers, owners, mitigations, and stop conditions;
- the frontier hypothesis map separates facts, inferences, alternatives, falsifiers, and unknowns;
- publication readiness can identify what to publish, transform, omit, or seek permission for;
- the package contains no unresolved TODO or TBD markers, copied proprietary content, secrets, or unsupported success claims; documented template variables in module-template.md and bom-template.yaml are permitted;
- no existing repository is modified.

## Implementation gates outside this design

The design is complete without assuming:

- cohort size or employer-supported time;
- faculty, lab-SRE, EHS, security, legal, and publication owners;
- guaranteed L1/L2/L3 hardware capacity;
- exact supported term BOM;
- licenses, warranty, insurance, export, and remote-access approvals;
- pilot-derived time, attrition, hardware-wait, and reviewer-consistency data.

Those are gates to course implementation, not reasons to invent details in the planning package.
