# Learn from real failures

Study a failure until you can explain why a plausible safeguard did not stop it. Then change one condition and decide whether the same failure could still happen. That is the purpose of this casebook: turn incident reports into a working understanding of dependencies, state, overload, recovery, and correctness.

The collection contains **13 cases: 11 incident reviews and two published fleet studies**. It covers several distinct failure mechanisms; it is not a census of the industry or a ranking of providers. A company that publishes detailed reports gives us more to learn from. Inclusion says nothing about its current reliability relative to another company.

Start with [how to read a postmortem](reading-method.md), then choose a case below. Each case provides a concise published account, a mechanism to reason about, an original worked example, a decision question with a reasoned answer, and links back to the course. The numerical teaching examples are synthetic. They are not reconstructions of undisclosed production measurements.

## A first route through the cases

If you are new to the subject, read these three in order:

1. [Meta: losing the network and the recovery path](01-meta-network.md). Draw the dependencies before studying the recovery.
2. [GitLab: a backup is not a demonstrated restore](07-gitlab-backups.md). Separate data loss from service downtime.
3. [OpenAI: telemetry overloads a Kubernetes control plane](05-openai-control-plane.md). Ask how an apparently auxiliary service can interrupt the main service.

Spend one session on each. A suggested 60-90 minutes includes reading, drawing the mechanism, working the example, and answering before opening the disclosure. This is a study estimate, not a measured completion time. If a prerequisite is unfamiliar, follow the linked lesson and return.

## Choose the failure mechanism you want to understand

The questions in this table are our teaching lens, not quotations from the reports. Read each case's published account for the historical claims and their limits.

| Case | Question to take into the report | Connect it to the course |
|---|---|---|
| [01. Meta network outage](01-meta-network.md) | Can you recover when the path used to operate the system shares its failure? | [System map](../curriculum/01-system-map.md), [fabric](../curriculum/04-fabric-storage.md) |
| [02. GitHub network partition](02-github-partition.md) | Does restoring connectivity make divergent state safe to use? | [Storage](../curriculum/04-fabric-storage.md), [recovery decisions](../curriculum/15-incidents-and-change.md) |
| [03. Cloudflare regular expression](03-cloudflare-regex.md) | Can a small rule change create unbounded work across a fleet? | [Workloads](../curriculum/06-workloads.md), [change safety](../curriculum/15-incidents-and-change.md) |
| [04. Fastly latent software bug](04-fastly-latent-bug.md) | What does a successful rollout fail to tell you about untested states? | [Workload contract](../curriculum/07-workload-contract.md), [readiness](../curriculum/17-capacity-and-readiness.md) |
| [05. OpenAI control-plane overload](05-openai-control-plane.md) | What happens when observers become a major source of work? | [Kubernetes operability](../tracks/kubernetes/11-operability.md), [fleet truth](../curriculum/13-fleet-truth.md) |
| [06. Amazon S3 service disruption](06-s3-recovery.md) | Can a repair tool remove more capacity than the system can rebuild quickly? | [Lifecycle automation](../curriculum/16-lifecycle-automation.md), [capacity](../curriculum/17-capacity-and-readiness.md) |
| [07. GitLab database recovery](07-gitlab-backups.md) | Which exact data can your recovery procedure actually recover? | [Storage](../curriculum/04-fabric-storage.md), [compound recovery](../practicum/21-recovery.md) |
| [08. Cloudflare power and control-plane outage](08-cloudflare-power.md) | Which supposedly separate services still share a physical dependency? | [Power and telemetry](../curriculum/05-power-telemetry-security.md), [rack lifecycle](../specialties/rack-lifecycle.md) |
| [09. Llama 3 training fleet study](09-llama-training.md) | How does a rare component failure become frequent job interruption at scale? | [GPU runtime](../curriculum/03-gpu-runtime.md), [reliability](../curriculum/14-reliability.md) |
| [10. Silent data corruption study](10-silent-corruption.md) | What if the process succeeds but its result is wrong? | [Server control](../curriculum/02-server-control.md), [fleet truth](../curriculum/13-fleet-truth.md) |
| [11. Amazon EBS recovery storm](11-ebs-remirroring.md) | Can a locally sensible repair consume the capacity needed for fleet recovery? | [Fabric and storage](../curriculum/04-fabric-storage.md), [capacity](../curriculum/17-capacity-and-readiness.md) |
| [12. Google Cloud network incident](12-google-network.md) | How can control-plane maintenance outgrow its intended scope? | [System map](../curriculum/01-system-map.md), [lifecycle automation](../curriculum/16-lifecycle-automation.md) |
| [13. OpenAI data isolation incident](13-openai-data-isolation.md) | Can successful responses violate the boundary between users? | [Power, telemetry, and security](../curriculum/05-power-telemetry-security.md), [workload contract](../curriculum/07-workload-contract.md) |

## Use the cases while learning the core

After months 1-6, use cases 1, 3, 7, 8, and 10 to practice dependency maps, bounded resource use, durable state, and correctness. At the platform gate, compare cases 2, 4, 5, and 13: being scheduled, reachable, or able to return a response is not a complete service contract. During months 13-18, use cases 6, 9, 11, and 12 to examine fleet rates, automation, and recovery capacity.

These readings are optional companions to the existing 24-month route. Use one in a theory or review session instead of silently adding a second workload. They do not add assessment gates or establish native-hardware experience. The [incident-review workshop](review-workshop.md) gives you paired comparisons and a complete synthetic review exercise when you are ready to integrate the ideas.

## What this collection does and does not establish

The primary sources are public operator reports and original research papers. We verify what those sources state; we do not have their private logs or an independent reconstruction of the events. The two fleet studies describe populations and observations, not a single outage timeline. Their observed rates cannot be treated as current rates for your fleet.

This is broad mechanism coverage, not an exhaustive list. It does not provide dedicated historical cases for every cooling failure, firmware defect, kernel bug, supply-chain compromise, malicious attack, or model-quality regression. Nor can a few public reports establish how common a failure is. Use the [review method](reading-method.md) to evaluate a new report without forcing it into the wrong analogy.

Source scope and access records are in the [network/software ledger](../evidence/incident-network-sources.json), [recovery/isolation ledger](../evidence/incident-recovery-sources.json), and [hardware/fleet ledger](../evidence/incident-hardware-sources.json). The [evidence guide](../evidence/README.md) explains how source claims differ from execution evidence.
