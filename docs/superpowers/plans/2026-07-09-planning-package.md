# Rack-Scale AI Infrastructure Planning Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Produce the complete private planning package defined by course-charter.md without creating course chapters, executable labs, deployment manifests, or infrastructure.

**Architecture:** The package uses stable IDs and one-way traceability: official sources and explicit design inferences feed competencies; competencies feed roadmap outcomes and module specifications; modules feed lab/decision plans; validation maps evidence back to outcomes. Human-readable Markdown remains authoritative for decisions and explanations, while YAML provides machine-checkable source, competency, dependency, BOM, and traceability records.

**Tech Stack:** Markdown, YAML, Mermaid, Git, ripgrep, Ruby 2.6 standard YAML parser, and independent subagent document review.

## Global Constraints

- Work only in /Users/anowarislam/rack-scale-ai-infrastructure-course.
- Do not modify /tmp/ml-in-k8s-audit.OBIYTF or any ml-in-k8s checkout.
- The repository remains private and has no remote unless the user later requests one.
- Deliver planning artifacts only; no executable lab, deployable manifest, container image, infrastructure code, course chapter, or production configuration.
- Preserve the 18-month T-shaped core plus 6-month spiral practicum.
- Preserve the experienced-infrastructure admission baseline.
- Preserve the five competency pillars and three audience exits.
- Kubernetes and Slurm are independently complete catalog tracks; a learner builds a primary platform and runs/compares the secondary.
- Every learner selects one bounded specialty focus.
- L0–L3 describes environment fidelity only; topology, accelerator count, RDMA, operation risk, actor, and support posture remain orthogonal attributes.
- L3 is necessary but never sufficient authorization for disruptive or physical activity.
- No award, certification, company endorsement, or job-readiness claim.
- NVIDIA target roles and products anchor target relevance; standards, law, facility rules, and version-specific vendor documentation govern normative claims.
- OpenAI and Anthropic reconstructions remain optional, requirement-ineligible hypotheses with atomic confidence labels, alternatives, and falsifiers.
- Use minimal rights-safe excerpts. Never copy full job postings, proprietary manuals, support artifacts, secrets, private topology, or direct asset identifiers.
- Use stable IDs: SRC-*, COMP-P*-*, MOD-01 through MOD-06, OUT-*, LAB-*, DEC-*, and RISK-*.
- No unresolved completion markers or unsupported success claims.
- Commit each independently reviewable task without attribution trailers.

---

### Task 1: Repository Index and Decision Records

**Files:**
- Create: README.md
- Create: decisions/0001-t-shaped-plus-spiral.md
- Create: decisions/0002-evidence-hierarchy.md
- Create: decisions/0003-platform-track-parity.md
- Create: decisions/0004-lab-level-claims.md
- Modify: course-charter.md only if a factual inconsistency is discovered

**Interfaces:**
- Consumes: accepted decisions in course-charter.md.
- Produces: DEC-0001 through DEC-0004 and the navigation entrypoint used by every later artifact.

- [ ] **Step 1: Create README.md**

Use these exact top-level sections:

1. Purpose
2. Current Status
3. Claim Ceiling
4. Planning Package Map
5. Accepted Architecture
6. Evidence Rules
7. What Is Not In This Repository
8. Review Order

State that the status is design-baseline until all planning-package acceptance checks pass. Link course-charter.md and every approved artifact path. State explicitly that ml-in-k8s at commit e3b39d479fa27d9a0cd9be2de7217b94addedc89 is read-only reference material.

- [ ] **Step 2: Create DEC-0001**

Record the decision for an 18-month T-shaped core plus 6-month spiral practicum. Include context, options considered, decision, consequences, validation, and revisit triggers. Rejected options must include one linear spine, spiral-only delivery, and extending ml-in-k8s.

- [ ] **Step 3: Create DEC-0002**

Record the two-axis evidence model:

- target-role relevance;
- claim authority.

State that role relevance never overrides law, facility rules, standards, safety manuals, or support matrices.

- [ ] **Step 4: Create DEC-0003**

Record independently complete Kubernetes and Slurm catalog tracks, primary Build depth, and secondary Run/compare depth. Include the exact secondary minimum: representative workload, platform-native scheduling/admission analysis, failure and recovery, accounting/evidence review, and comparison memo.

- [ ] **Step 5: Create DEC-0004**

Record L0–L3 environment fidelity plus the orthogonal lab attributes:

- environment;
- accelerator count and topology;
- RDMA mode;
- operation risk;
- actor;
- support posture.

State that L3 never grants authority by itself.

- [ ] **Step 6: Validate navigation and decision completeness**

Run:

~~~bash
rg -n '^## (Context|Decision|Consequences|Validation|Revisit Triggers)$' decisions/*.md
rg -n 'course-charter.md|DEC-0001|DEC-0002|DEC-0003|DEC-0004' README.md decisions/*.md
git diff --check
~~~

Expected: each decision contains all five required headings; README links the charter and four decisions; git diff reports no whitespace errors.

- [ ] **Step 7: Commit**

~~~bash
git add README.md decisions course-charter.md
git commit -m "docs: record course architecture decisions"
~~~

### Task 2: Evidence Ledger and Role Alignment

**Files:**
- Create: evidence/source-ledger.yaml
- Create: evidence/nvidia-director-alignment.md
- Create: evidence/nvidia-principal-alignment.md
- Create: evidence/frontier-transfer-signals.md

**Interfaces:**
- Consumes: DEC-0002.
- Produces: SRC-* records and rights-safe role requirement IDs referenced by COMP-* records.

- [ ] **Step 1: Define source-ledger.yaml**

Each source record must include:

- source_id;
- title;
- publisher;
- source_type;
- canonical_url;
- target_relevance;
- claim_authority;
- authoritative_scope;
- publication_or_update_date when available;
- accessed_at;
- version_or_revision;
- applicability;
- lifecycle;
- rights_and_snapshot_policy;
- limitations;
- review_due;
- owner_role.

Seed the ledger with the exact NVIDIA Director JR2020349 and Principal JR2020316 pages plus the official standards/product sources already cited in the research notes for Redfish, Linux RAS, Kubernetes device allocation, Slurm GRES, NCCL, DCGM, NVIDIA GPU/Network Operators, and DGX rack safety.

Use this exact initial source set:

- https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Director--Engineering-Operations-and-Site-Reliability-Engineering---Datacenter-Server-Systems_JR2020349
- https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Principal-Software-Engineer--Rack-Scale-System-Software---CSP-Engagements_JR2020316
- https://redfish.dmtf.org/schemas/Redfish_Release_History.pdf
- https://docs.kernel.org/6.11/admin-guide/RAS/main.html
- https://docs.kernel.org/PCI/pci-error-recovery.html
- https://docs.kernel.org/networking/devlink/devlink-health.html
- https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/
- https://docs.nvidia.com/deploy/xid-errors/working-with-xid-errors.html
- https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/
- https://slurm.schedmd.com/gres.html
- https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting.html
- https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-driver-upgrades.html
- https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/platform-support.html
- https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html
- https://docs.nvidia.com/dgx/dgxgb200-user-guide/networking.html
- https://docs.nvidia.com/dgx/dgxh100-service-manual/safety.html

- [ ] **Step 2: Create the director map**

Map rights-safe requirement IDs to:

- observable operating behavior;
- pillar and competency IDs reserved for Task 3;
- planned module;
- learning evidence;
- course-observed, workplace-evidenced, or transfer-objective class;
- coverage status;
- limitations and non-equivalence.

Include fleet operations, incidents, roadmaps, change, readiness, reliability metrics, telemetry, NPI, executive reporting, cross-functional execution, and leader development.

- [ ] **Step 3: Create the principal map**

Map rack SW/FW coordination, error propagation, fabric/NVSwitch recovery, firmware sequencing and recovery, health APIs, serviceability, CSP integration, left-shift validation, and influence without authority.

- [ ] **Step 4: Create frontier-transfer-signals.md**

Define allowed and prohibited use of official OpenAI/Anthropic signals. Make clear that convergence in public signals is not proof of private architecture or an industry standard.

- [ ] **Step 5: Validate YAML and rights-safe boundaries**

Run:

~~~bash
ruby -e 'require "yaml"; YAML.load_file("evidence/source-ledger.yaml"); puts "source-ledger: OK"'
rg -n 'JR2020349|JR2020316|direct|inference|limitation|non-equivalence' evidence/*.md
rg -n -i 'full job posting|private stack is|industry standard' evidence && exit 1 || true
git diff --check
~~~

Expected: Ruby prints source-ledger: OK; both role maps contain direct/inference and limitation language; prohibited overclaims are absent.

- [ ] **Step 6: Commit**

~~~bash
git add evidence
git commit -m "docs: add evidence ledger and role alignment"
~~~

### Task 3: Competency and Audience Model

**Files:**
- Create: competencies/competency-matrix.yaml
- Create: competencies/audience-depth.md
- Create: competencies/prerequisites.md
- Create: competencies/specialty-lanes.md

**Interfaces:**
- Consumes: SRC-* and role requirement IDs.
- Produces: COMP-P1-* through COMP-P5-* and the depth assignments consumed by roadmap and modules.

- [ ] **Step 1: Create competency-matrix.yaml**

For every atomic competency include:

- competency_id;
- name;
- pillar;
- source_claim_ids;
- design_inference flag;
- outcome;
- non_goals;
- prerequisites;
- engineer_depth;
- aspiring_leader_depth;
- manager_director_depth;
- leadership_evidence_class;
- minimum_lab_fidelity;
- orthogonal_lab_requirements;
- planned_module_id;
- planned_evidence;
- owner_role;
- status.

Cover all five approved pillars. Keep mandatory atomic outcomes within the gate budgets in the charter.

- [ ] **Step 2: Create audience-depth.md**

Define Read, Run, Build, and Lead. Include the allowed Build deliverables and the course-observed/workplace-evidenced/transfer-objective distinction.

- [ ] **Step 3: Create prerequisites.md**

Define the admission diagnostic for Linux, networking, storage, containers, Git/IaC, scripting, distributed systems, and operations. State that gaps route to a separate bridge and do not expand the core.

- [ ] **Step 4: Create specialty-lanes.md**

Define the four launch umbrellas and require one bounded focus:

1. rack lifecycle and serviceability;
2. accelerator/fabric/storage performance;
3. primary-platform scheduling and control;
4. fleet reliability and developer leverage.

For each, define characterize, intervene, validate/recover, and operationalize.

- [ ] **Step 5: Validate identifiers and scope**

Run:

~~~bash
ruby -e 'require "yaml"; d=YAML.load_file("competencies/competency-matrix.yaml"); ids=d.fetch("competencies").map{|x| x.fetch("competency_id")}; abort("duplicate") unless ids.uniq.size==ids.size; puts "competencies: #{ids.size} unique"'
rg -n 'Read|Run|Build|Lead|course-observed|workplace-evidenced|transfer objective' competencies/*.md
rg -n -i 'second specialty|all specialties required' competencies && exit 1 || true
git diff --check
~~~

Expected: Ruby reports a unique competency count; depth and evidence classes are defined; no second specialty is required.

- [ ] **Step 6: Commit**

~~~bash
git add competencies
git commit -m "docs: define competency and audience model"
~~~

### Task 4: Roadmap and Dependency Graph

**Files:**
- Create: roadmap/24-month-roadmap.md
- Create: roadmap/t-shaped-core.md
- Create: roadmap/spiral-practicum.md
- Create: roadmap/dependencies.yaml

**Interfaces:**
- Consumes: COMP-* depth assignments and DEC-0001/DEC-0003.
- Produces: G1–G4, month-level outcomes, and prerequisite edges consumed by module specs.

- [ ] **Step 1: Write 24-month-roadmap.md**

Use the month-by-month sequence and four gates from course-charter.md. Include:

- 96 scheduled weeks and 8 unscheduled breaks;
- 70 new-mechanism weeks;
- 18 remediation/validation/hardware-contingency weeks;
- 8 capstone/defense weeks;
- 8–10 hours per scheduled week;
- 768–960 total planned hours;
- maximum 12 mandatory outcomes and 6 assessed exercises per gate.

- [ ] **Step 2: Write t-shaped-core.md**

Map months 1–18 to the horizontal breadth, primary platform vertical stem, one specialty, and role-family capstone proposal.

- [ ] **Step 3: Write spiral-practicum.md**

Define months 19–24 with the operating loop:

Observe → Build → Break → Detect → Decide → Recover → Verify → Review → Automate.

State that no new survey domain enters during the spiral.

- [ ] **Step 4: Create dependencies.yaml**

Represent stable IDs for:

- admission;
- G1 systems;
- shared workload semantics;
- primary Kubernetes and Slurm Build paths;
- secondary Run/compare packages;
- G2 platform;
- fleet operations;
- specialty;
- G3 integrated core;
- role capstone proposal;
- spiral cycles;
- G4 evidence review.

- [ ] **Step 5: Validate YAML and gate budgets**

Run:

~~~bash
ruby -e 'require "yaml"; d=YAML.load_file("roadmap/dependencies.yaml"); puts "nodes=#{d.fetch("nodes").size} edges=#{d.fetch("edges").size}"'
rg -n '768.?960|G1|G2|G3|G4|12 mandatory|6 assessed' roadmap/*.md
git diff --check
~~~

Expected: YAML prints non-zero node and edge counts; roadmap files contain hours, gates, and budgets.

- [ ] **Step 6: Commit**

~~~bash
git add roadmap
git commit -m "docs: add 24-month roadmap and dependencies"
~~~

### Task 5: Module Specifications

**Files:**
- Create: module-specs/module-template.md
- Create: module-specs/01-shared-systems-core.md
- Create: module-specs/02-platform-tracks.md
- Create: module-specs/03-fleet-operations.md
- Create: module-specs/04-specialty-lanes.md
- Create: module-specs/05-role-family-capstones.md
- Create: module-specs/06-spiral-practicum.md

**Interfaces:**
- Consumes: COMP-*, OUT-*, G1–G4, and roadmap dependencies.
- Produces: MOD-01 through MOD-06 and planned exercise/evidence contracts consumed by validation.

- [ ] **Step 1: Create module-template.md**

Require these headings:

1. Metadata
2. Purpose
3. Outcomes
4. Prerequisites
5. Audience Depth
6. Module Groups
7. Planned Exercises
8. Evidence
9. Failure, Detection, and Recovery
10. Lab Fidelity and Authorization
11. Non-Goals
12. Sources
13. Validation and Staleness

Template variables must be visibly marked as schema variables, not unresolved completion markers.

- [ ] **Step 2: Write MOD-01**

Cover system map, server/NUMA/PCIe/BMC/OOB/firmware, GPU/NVLink/RAS, fabric/RDMA/storage, power/thermal, security, and distributed training/inference integration.

- [ ] **Step 3: Write MOD-02**

Specify the complete Kubernetes and Slurm catalog tracks plus the individual primary and secondary routes. Include platform-native HA, scheduling, fairness, accounting, topology, identity, security, upgrades, incidents, and recovery.

- [ ] **Step 4: Write MOD-03**

Cover asset truth, lifecycle, statistical reliability, incidents, change, ORR, capacity, spares, NPI, and lifecycle automation/CI.

- [ ] **Step 5: Write MOD-04**

Define the four specialty umbrellas and one bounded focus contract.

- [ ] **Step 6: Write MOD-05**

Define separate developer/principal, aspiring-leader, and manager/director capstones with evidence classes.

- [ ] **Step 7: Write MOD-06**

Define inherited-system reconstruction, performance regression, controlled failure/change/recovery, supervised rack ORR/NPI, fleet/leadership cycle, and defense/remediation.

- [ ] **Step 8: Validate module anatomy and IDs**

Run:

~~~bash
for f in module-specs/0*.md; do
  rg -q '^## Purpose$' "$f" &&
  rg -q '^## Outcomes$' "$f" &&
  rg -q '^## Non-Goals$' "$f" || exit 1
done
rg -n 'MOD-0[1-6]|OUT-' module-specs/*.md
git diff --check
~~~

Expected: every module contains required headings; MOD-01 through MOD-06 and OUT-* IDs are present.

- [ ] **Step 9: Commit**

~~~bash
git add module-specs
git commit -m "docs: specify course modules and capstones"
~~~

### Task 6: Lab Fidelity, Safety, and BOM Planning

**Files:**
- Create: lab-planning/lab-levels.md
- Create: lab-planning/operating-charter.md
- Create: lab-planning/bom-template.yaml
- Create: lab-planning/safety-and-authorization.md

**Interfaces:**
- Consumes: COMP-* minimum fidelity, MOD-* exercise plans, and DEC-0004.
- Produces: lab profiles, authorization profiles, and BOM fields referenced by traceability.

- [ ] **Step 1: Write lab-levels.md**

Define L0–L3 claim ceilings and the orthogonal classification fields. Include representative L0 Redfish/scheduler simulations, L1 GPU diagnostics, L2 multi-node scheduler and optional physical-RDMA labs, and L3 supervised rack evidence.

- [ ] **Step 2: Write operating-charter.md**

Define access, concurrency, OOB, credentials, maintenance, recovery modes, EHS, qualified service, spares, warranty/support, lab SLOs, incident ownership, and lower-tier fallback.

- [ ] **Step 3: Create bom-template.yaml**

Include schema version, validity, scope, owners, support assertions, hardware profile, firmware components and recoverability, software versions, immutable image digests, network/topology, time integrity, authorization/safety profiles, evidence stores, validators, known issues, change triggers, and release-lock digest.

- [ ] **Step 4: Write safety-and-authorization.md**

Define eligible, conditionally eligible, and always-prohibited operations plus actor classes. State that local law, facility rules, manuals, support terms, and stop-work authority prevail.

- [ ] **Step 5: Validate YAML and prohibited-action language**

Run:

~~~bash
ruby -e 'require "yaml"; YAML.load_file("lab-planning/bom-template.yaml"); puts "bom-template: OK"'
rg -n 'necessary but never sufficient|always prohibited|qualified service|stop-work|branch-circuit|thermal' lab-planning/*.md
git diff --check
~~~

Expected: Ruby prints bom-template: OK; high-risk and prohibited boundaries are explicit.

- [ ] **Step 6: Commit**

~~~bash
git add lab-planning
git commit -m "docs: define lab fidelity and operating controls"
~~~

### Task 7: Validation and Traceability

**Files:**
- Create: validation/completeness-contract.md
- Create: validation/traceability-matrix.yaml
- Create: validation/review-rubrics.md
- Create: validation/staleness-policy.md

**Interfaces:**
- Consumes: SRC-*, COMP-*, MOD-*, OUT-*, planned LAB-*, gate IDs, BOM and authorization profiles.
- Produces: machine-checkable coverage rows and review rules used in the final integration review.

- [ ] **Step 1: Write completeness-contract.md**

Require the 13 completeness fields from course-charter.md, including evidence authority, claim ceiling, platform-native design, failure/detection/recovery/irreversibility, positive health, meta-monitoring, time integrity, evaluator mode, evidence handling, reset/replay, and staleness.

- [ ] **Step 2: Create traceability-matrix.yaml**

Each row must contain:

- outcome_id;
- competency_ids;
- source_claim_ids;
- audience depth;
- primary_or_secondary;
- module_id;
- planned_exercise_id;
- required_lab_profile;
- failure_families;
- evaluator_mode;
- evidence_fields;
- claim_ceiling;
- owner_role;
- status;
- unresolved_gap.

- [ ] **Step 3: Write review-rubrics.md**

Define the 0–3 scale and blocking dimensions. Define machine-only, human-only, and combined evaluation. Include leadership dimensions for sensemaking, stop/go, delegation, communication, safety/change discipline, alignment, follow-through, and coaching without blame.

- [ ] **Step 4: Write staleness-policy.md**

Define validation triggers for source changes, role removal, software releases, support expiry, hardware/BOM change, license or safety change, and public export.

- [ ] **Step 5: Validate YAML and orphan references**

Run:

~~~bash
ruby -e 'require "yaml"; YAML.load_file("validation/traceability-matrix.yaml"); puts "traceability: OK"'
rg -n 'machine|human|both|0|1|2|3|blocking' validation/review-rubrics.md
rg -n 'positive health|meta-monitor|time integrity|irreversible|claim ceiling' validation/*.md
git diff --check
~~~

Expected: Ruby prints traceability: OK; evaluator modes, scale, and completeness controls are present.

- [ ] **Step 6: Commit**

~~~bash
git add validation
git commit -m "docs: add validation and traceability model"
~~~

### Task 8: Frontier-Stack Hypothesis Appendix

**Files:**
- Create: research/frontier-stack-hypotheses.md
- Modify: evidence/source-ledger.yaml with the primary OpenAI and Anthropic sources used by the appendix

**Interfaces:**
- Consumes: SRC-* records and the optional-use boundary in evidence/frontier-transfer-signals.md.
- Produces: requirement-ineligible HYP-OAI-* and HYP-ANT-* records for comparative seminars.

- [ ] **Step 1: Define the hypothesis record**

For each atomic proposition include company, layer, tense, evidence IDs, source scope, confidence label, rationale, competing hypotheses, falsifier, negative findings, freshness, course relevance, allowed use, requirement_eligible=false, publication status, owner, and review date.

- [ ] **Step 2: Add the OpenAI reconstruction**

Cover compute/hardware, orchestration, networking, storage/data, training runtime, inference runtime, observability, developer productivity, security, reliability/incidents, and management. Use only primary official sources from the research pass. Keep scheduler, Slurm, frameworks, storage backends, serving internals, topology, SLOs, and decision rights explicitly unknown unless an atomic source supports them.

Begin with these exact official sources:

- https://openai.com/careers/software-engineer-compute-infrastructure-san-francisco/
- https://openai.com/careers/software-engineer-frontier-clusters-infrastructure-san-francisco/
- https://openai.com/index/mrc-supercomputer-networking/
- https://openai.com/careers/software-engineer-compute-storage-san-francisco/
- https://openai.com/careers/training-performance-engineer-san-francisco/
- https://openai.com/careers/software-engineer-observability-san-francisco/
- https://openai.com/careers/software-engineer-hardware-health-san-francisco/
- https://openai.com/careers/head-of-data-center-rack-and-cluster-san-francisco/
- https://openai.com/index/scaling-kubernetes-to-7500-nodes/

- [ ] **Step 3: Add the Anthropic reconstruction**

Cover the same layers. Preserve the verified public Kubernetes signal and heterogeneous accelerator signal while leaving production Slurm use, training framework, fabric, checkpoint format, storage backend, serving engine, SLOs, topology, and org decision rights unknown.

Begin with these exact official sources:

- https://job-boards.greenhouse.io/anthropic/jobs/5211241008
- https://job-boards.greenhouse.io/anthropic/jobs/5139038008
- https://job-boards.greenhouse.io/anthropic/jobs/5177143008
- https://job-boards.greenhouse.io/anthropic/jobs/4938432008
- https://job-boards.greenhouse.io/anthropic/jobs/5257650008
- https://job-boards.greenhouse.io/anthropic/jobs/5113224008
- https://job-boards.greenhouse.io/anthropic/jobs/5110511008
- https://job-boards.greenhouse.io/anthropic/jobs/5120512008
- https://www.anthropic.com/news/anthropic-amazon-compute
- https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services

- [ ] **Step 4: Add the rubber-duck method**

For every inferred mechanism require:

1. public observation;
2. confidence label;
3. reconstruction;
4. why it is plausible;
5. competing explanation;
6. falsifier;
7. course relevance;
8. non-private-stack disclaimer.

- [ ] **Step 5: Validate requirement ineligibility and source coverage**

Run:

~~~bash
rg -n 'Verified public|Strong inference|Weak inference|Speculation|Unknown|Competing|Falsifier' research/frontier-stack-hypotheses.md
rg -n 'requirement_eligible: false|requirement-ineligible' research/frontier-stack-hypotheses.md
ruby -e 'require "yaml"; YAML.load_file("evidence/source-ledger.yaml"); puts "source-ledger: OK"'
git diff --check
~~~

Expected: every evidence class, alternatives, falsifiers, and requirement-ineligible boundary are present.

- [ ] **Step 6: Commit**

~~~bash
git add research evidence/source-ledger.yaml
git commit -m "docs: add frontier stack hypothesis map"
~~~

### Task 9: Risk and Publication Readiness

**Files:**
- Create: risks.md
- Create: publication-readiness.md

**Interfaces:**
- Consumes: all prior planning artifacts.
- Produces: RISK-* records and private-to-public gates used by final review.

- [ ] **Step 1: Write risks.md**

For every seed risk in course-charter.md include:

- risk_id;
- category;
- failure scenario;
- causal assumption;
- leading indicator;
- affected artifacts;
- probability or unscored;
- impact;
- current verified control;
- control gap;
- owner role;
- mitigation;
- contingency;
- stop condition;
- residual risk;
- verification evidence;
- status.

- [ ] **Step 2: Write publication-readiness.md**

Define artifact states private-restricted, private-reusable, public-candidate, and public-approved. Define publish/transform/omit/seek-permission disposition and gates for provenance, licenses, trademarks, non-affiliation, privacy, secrets, export, current evidence, public-safe diagrams/fault bundles, accessibility, correction, takedown, and incident ownership.

- [ ] **Step 3: Validate risk mechanics and publication gates**

Run:

~~~bash
rg -n 'Owner|Stop condition|Residual risk|Leading indicator|Contingency' risks.md
rg -n 'private-restricted|private-reusable|public-candidate|public-approved|publish|transform|omit|seek permission' publication-readiness.md
git diff --check
~~~

Expected: risk records have mechanisms and stop conditions; all four publication states and four dispositions are defined.

- [ ] **Step 4: Commit**

~~~bash
git add risks.md publication-readiness.md
git commit -m "docs: add risk and publication readiness plans"
~~~

### Task 10: Integration, Reader Testing, and Planning-Complete Review

**Files:**
- Modify: README.md
- Modify: course-charter.md only for confirmed inconsistencies
- Modify: any planning artifact that fails traceability or reader testing

**Interfaces:**
- Consumes: every planning artifact.
- Produces: a planning-complete package or an explicit list of unmet acceptance criteria.

- [ ] **Step 1: Run structural validation**

Run:

~~~bash
find . -type f -not -path './.git/*' -print | sort
ruby -e 'require "yaml"; Dir["**/*.{yaml,yml}"].each{|f| YAML.load_file(f); puts "YAML OK #{f}"}'
git diff --check
rg -n -i 'T[O]DO|T[B]D|FIXME|PLACEHOLDER|coming soon' . --glob '!docs/superpowers/plans/*'
~~~

Expected: every YAML file parses; no whitespace errors; no unresolved completion markers outside the implementation plan.

- [ ] **Step 2: Verify scope boundaries**

Run:

~~~bash
find . -type f -perm -111 -not -path './.git/*'
find . -type f \( -name '*.sh' -o -name '*.py' -o -name '*.tf' -o -name 'Dockerfile' \)
git -C /tmp/ml-in-k8s-audit.OBIYTF status --short
~~~

Expected: no executable or implementation files; no output from the reference repository status.

- [ ] **Step 3: Verify traceability coverage**

Use a read-only validation pass to confirm:

- every COMP-* is mapped to a module;
- every mandatory OUT-* maps to a planned exercise and evidence;
- every planned exercise declares fidelity and evaluator mode;
- every G1–G4 outcome stays within its budget;
- both platform tracks cover the shared outcome families with native mechanisms;
- role maps remain distinct;
- frontier hypotheses are requirement-ineligible.

Record any failure in the owning artifact and fix it before continuing.

- [ ] **Step 4: Run independent reader tests**

Give fresh reviewers only the repository and ask:

1. What can this course honestly claim?
2. What path does one learner take through Kubernetes and Slurm?
3. What distinguishes environment fidelity from operation authorization?
4. How does a source become a competency and then a planned exercise?
5. What is verified versus inferred about OpenAI and Anthropic?
6. In what order should the planning package be implemented?
7. What prevents course scope and hardware risk from expanding silently?

Require correct answers without conversation context. Fix ambiguity before continuing.

- [ ] **Step 5: Update README status**

Set status to planning-complete only if every acceptance criterion in course-charter.md passes. Otherwise state the exact unmet criteria and retain design-baseline.

- [ ] **Step 6: Final verification**

Run:

~~~bash
git status --short
git log --oneline --decorate -10
git diff --check HEAD
git -C /tmp/ml-in-k8s-audit.OBIYTF status --short
~~~

Expected: only intentional final edits are pending; history shows scoped commits; no whitespace error; ml-in-k8s remains clean.

- [ ] **Step 7: Commit the integration result**

~~~bash
git add README.md course-charter.md evidence competencies roadmap module-specs lab-planning validation research risks.md publication-readiness.md
git commit -m "docs: complete rack-scale course planning package"
~~~

- [ ] **Step 8: Report boundaries**

Report:

- files created;
- validations run and exact results;
- planning-complete status;
- remaining feasibility gates;
- current commit;
- confirmation that no remote was created and ml-in-k8s was not modified.
