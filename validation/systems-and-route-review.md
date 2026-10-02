# Independent systems and learner-route review

Review date: 2026-10-02 UTC. Reviewer: fleet/practicum author, reviewing the systems author's chapters and the coordinator's learner integration. Standard: [teaching acceptance](TEACHING-REVIEW.md).

**Disposition: accepted for the reviewed authoring scope after correction of SR-01.** The seven systems lessons explain the mechanisms needed for their examples and exercises. The entrypoint, route guide, calendar, and gates give a newcomer a usable study and assessment path. No remaining material teaching, arithmetic, or navigation inconsistency was found in this scope. This is a document review with independent numerical and targeted source checks; it is not evidence of learner mastery or physical-system execution.

## Scope and method

Read all of [00: bridge](../curriculum/00-bridge.md), [01: system map](../curriculum/01-system-map.md), [02: server control](../curriculum/02-server-control.md), [03: GPU runtime](../curriculum/03-gpu-runtime.md), [04: fabric and storage](../curriculum/04-fabric-storage.md), [05: power, telemetry, and security](../curriculum/05-power-telemetry-security.md), and [06: workloads](../curriculum/06-workloads.md), including questions and separated answers. Read the [systems lab instructions](../labs/systems/README.md) and [hardware workbook](../labs/systems/hardware-workbook.md).

Read [README](../README.md), [LEARNING-GUIDE](../LEARNING-GUIDE.md), [CALENDAR](../CALENDAR.md), [gates](../assessments/gates.md), and the [course map](../course-map.json). Checked the map's months, week types, exercise identifiers, and atomic outcome identifiers independently using Python. Reviewed the relevant systems source-ledger entries when checking citations.

The intended reader is new to rack-scale AI, with the bridge available for missing command-line, networking, container, permission, and numerical prerequisites. The test was whether that reader could learn the causal explanation from the lesson, reproduce its examples, distinguish a counterexample, attempt its questions, and understand what evidence the practical work can establish. Counting headings or source links was not treated as proof of teaching quality.

## Material finding and resolution

| ID | Severity and confidence | Finding | Correction and verification |
|---|---|---|---|
| SR-01 | Medium; high confidence | Chapter 04 and source record SYS-20 initially labeled the rolling NCCL networking page as 2.32.3. Independent web retrieval and direct HTML title inspection identified that page as 2.31.2. The collective-operations page separately identified itself as 2.32.3. A learner could incorrectly infer one pinned source release. | Systems author corrected chapter 04, SYS-20, and the source ledger's negative findings. Reopened the files and the two primary pages: networking is recorded as 2.31.2, collectives as 2.32.3, both observed 2026-10-02; no common pinned release is inferred. Closed. |

The finding concerned source provenance, not a demonstrated error in the collective or networking mechanism taught. The cause of the publisher's page-version mismatch was not investigated, and no cause is asserted. The earlier suspicion that SYS-19 also needed correction was rejected after checking its actual page title; SYS-19's 2.32.3 scope was supported.

## Chapter-by-chapter teaching assessment

| Lesson | Definitions and causal chain | Worked cases, answers, and claim boundaries |
|---|---|---|
| 00 | Introduces process, command, path, identity/permissions, address/name/port, configuration, container, and units before later lessons need them. A successful command is distinguished from a healthy service. | Permission-versus-integrity reasoning and bit/byte and tensor-size calculations are explicit. The bridge diagnoses gaps rather than presuming all beginners have Linux experience. It does not claim container isolation is equivalent to a VM or physical host. |
| 01 | Traces a request through workload, scheduler, host, accelerator, data, and shared physical dependencies. Defines failure domains and falsifiable hypotheses before asking for an experiment. | The replica example separates count, surviving capacity, and demand. The canary example explains why node percentage can understate job impact. Questions require applying the dependency map; answers do not infer availability from two replicas. |
| 02 | Explains CPU/memory placement, NUMA distance, PCIe topology, asset identity, and host-versus-management authority. Firmware change is taught as a state and compatibility transition. | Serial timing has clear units and an explicit no-overlap assumption. The identity example has two distinct faults rather than one vague unhealthy node. The locality counterexample correctly retains contention and actual placement as things to observe. |
| 03 | Defines tensor shape, representation, operations, driver, runtime, framework, memory components, and asynchronous timing. Separates initialization failure from capacity and numerical behavior. | Matrix arithmetic is shown before the throughput bound. Memory-fit reasoning separates fixed and variable terms. The answers do not treat a container image as a host driver, an SMI version field as the application's toolkit, or a synthetic memory PASS as GPU validation. |
| 04 | Defines scale-up, scale-out, storage, rank, collective agreement, transport, and committed checkpoint state. Explains why time inside a collective can include waiting for another rank. | The ring example is a stated teaching algorithm, not a claim that every NCCL run selects it. Count/data-type mismatch cannot be fixed by bandwidth. Checkpoint generation and completion are separated. The source-version issue is now corrected. |
| 05 | Defines power versus energy, surviving-feed capacity, measurement location, gauge/counter behavior, source versus collection time, and observation versus change authority. | Energy, N-1 load, clock offset, uncertainty, and stale data are reasoned explicitly. The lesson supplies no universal thermal limit and does not turn passive access into authorization for a reset or diagnostic. Answers retain missing measurements rather than converting them to healthy zeroes. |
| 06 | Defines model, prediction, loss, gradient, learning rate, batch, synchronization, serving queue, throughput, goodput, percentile, and recovery semantics. Gives a complete small training update before discussing distribution. | The full derivative/update example is reproducible. The queue example states the 1,500-ms goodput criterion and nearest-rank percentile convention, and explains the finite-run denominator. DDP's input partitioning responsibility is stated correctly. The queue model does not claim to simulate transformer/KV-cache performance. |

External references substantiate or extend the explanations. For the assessed core reasoning in these chapters, no material case was found where a link replaces a missing derivation. Advanced physical transport and service procedures are appropriately deferred to an authorized exact environment; that is different from omitting the mathematical or conceptual explanation.

## Independent numerical checks

Used standard-library Python with integer arithmetic, `fractions.Fraction`, and a separately written earliest-free-worker queue using `heapq`. The checks did not call the course evaluator or reuse its result calculations. The following representative results match the text within its stated rounding.

| Calculation | Independent result and interpretation |
|---|---|
| Bridge transfer, 80 GB over 40 Gb/s | `40/8 = 5 GB/s`; ideal 16 s. At measured 2 GB/s, 40 s. Line rate and end-to-end rate are different inputs. |
| Bridge tensor, 2048 x 4096 x 4 bytes | 33,554,432 bytes = 32 MiB; ten payloads = 320 MiB. |
| Two 60-request/s replicas, demand 80 | Normal capacity 120; utilization 2/3. One surviving replica has a 20-request/s deficit even after separating the feed fault domain. |
| Serial preprocessing, 18 + 24 + 12 ms; copy reduced to 12 ms | 54 -> 42 ms; 18.5185 -> 23.8095 batches/s; throughput gain 28.5714%, not a doubling. |
| Matrix work, 2 x 256 x 4096 x 4096 | 8,589,934,592 FLOP; at the assumed 50 TFLOP/s, compute-only lower bound 0.17179869184 ms. |
| 24,576 MiB total, 2,048 reserve, 6,144 fixed, 2,304 per microbatch item | Usable 22,528 MiB; maximum integer microbatch 7 in this model. Microbatch 8 exceeds that usable budget by 2,048 MiB. |
| Ring with four ranks and 2 GB per rank | Six quarter-array payloads = 3 GB transferred per rank. At assumed 10 GB/s, 0.3 s communication; with 0.1 s compute, 0.4 s. Halving compute gives 0.35 s, or 14.2857% throughput gain. |
| 80-GB checkpoint at 4 GB/s, after 600 s compute | 20 s write; `20/620 = 3.2258%` wall-time fraction. Expected half-interval lost work is conditional on the stated uniform-within-interval assumption. |
| 8 kW for 10 min versus 6 kW for 15 min | 1.333333 versus 1.5 kWh; lower-power case uses 12.5% more energy for the fixed task. |
| 34-kW load after loss of one usable 40-kW feed | 6-kW nominal headroom under the given synthetic transfer/capacity assumptions; two 20-kW feeds would not meet the same single-feed condition. |
| Source timestamp 1008, clock 12 s ahead, collection 998 | Corrected event time 996; delivery 2 s; with +/-1-s offset uncertainty, event interval 995-997. Collection timestamp alone cannot recover source freshness. |
| Initial linear-model training step | Gradients `dw=-2.5`, `db=-2`; at learning rate 0.1, `w=.25`, `b=.2`; mean squared error falls from 3.5 to 2.5540625. |
| Eight arrivals each integer second for ten seconds, two 0.4-s workers | 80 complete by 16 s; ten meet the 1.5-s criterion; goodput 0.625/s; nearest-rank p99 7,000 ms. |
| Four arrivals on the same schedule | 40 complete by 9.8 s; all meet the criterion; finite-window goodput 4.0816327/s; p99 800 ms. |
| 98 requests at 100 ms plus two at 3,000 ms | Mean 158 ms; nearest-rank p99 3,000 ms. A low mean does not imply the tail objective holds. |

## Targeted primary-source verification

Reopened these primary sources on 2026-10-02 for facts where precise scope mattered:

- [Linux NUMA memory policy](https://docs.kernel.org/admin-guide/mm/numa_memory_policy.html): changing task policy affects later allocations; existing pages do not automatically move. This supports the chapter's distinction between policy intent and observed placement.
- [NVIDIA SMI reference](https://docs.nvidia.com/deploy/nvidia-smi/index.html): CUDA/UMD version expresses driver-supported capability and is not a reliable statement of the application's installed toolkit. The current reference deprecates the older CUDA Version label; the chapter's distinction remains correct across those labels.
- [NCCL collective operations](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html): checked agreement in count/type and the all-reduce/rank semantics. Observed page version 2.32.3.
- [NCCL networking troubleshooting](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/networking_troubleshooting.html): checked interface selection and low-level validation before tuning. Observed page version 2.31.2, recorded separately after SR-01.
- [PyTorch 2.8 DistributedDataParallel](https://docs.pytorch.org/docs/2.8/generated/torch.nn.parallel.DistributedDataParallel.html): synchronizes gradients; it does not itself partition input data across GPUs. The user's application owns that partitioning.
- [NVIDIA DOCA 3.5 RDMA programming guide](https://networking-docs.nvidia.com/doca/archive/3-5-0/rdma-aware-networks-programming-guide): checked the versioned transport terminology used to distinguish registered-memory/RDMA concepts from a passing socket workload. This does not verify a deployed NIC or fabric.

These checks found no further contradiction in the specific claims reviewed. They were not an independent full crawl of every external URL or verification of a particular hardware/software compatibility matrix.

## Learner integration and assessment consistency

The README gives a direct first action: learning guide, bridge diagnostic, then Month 1. The guide describes a first session, the weekly theory/example/experiment loop, how to preserve failed attempts, and how to move on using evidence. The route choices are explicit: one primary platform, one secondary minimum package, one specialty, and one role-family capstone. The secondary route is not represented as a second full Build workload.

Independent map inspection found **24 months, 96 unique scheduled weeks**, and week-type counts of **70 build/apply, 18 remediation, and 8 defense/transfer**. Each gate has **six distinct assessed bundles and twelve distinct atomic outcomes**. Months 1-18 reserve their fourth week for remediation; Months 19-22 are two bounded application units each; Months 23-24 provide the eight defense/transfer weeks. The calendar explicitly excludes diagnostic-dependent bridge work and places eight break weeks outside the 96 scheduled weeks. At 8-10 hours per scheduled week, the arithmetic is 768-960 hours.

Systems chapter bundle IDs and requirements agree with G1. L0 can establish model reasoning; G1-O06 and G1-O12 require the specified actual L1 workload evidence. The hardware workbook supplies bounded observation, CUDA correctness, controlled application interruption, recovery, and evidence requirements. It labels physical execution NOT_RUN and separates an optional management-plane read from a state-changing action. GPU/RDMA/rack claims cannot be obtained from the local models.

The guide permits continued study while an environment is pending but does not permit marking the higher-fidelity outcome passed. The gates distinguish course tests from learner work, key-assisted practice from independent evidence, and simulated leadership from longitudinal management. This is a coherent progression contract rather than a promise of certification or job equivalence.

## Boundaries of this acceptance

This review does not establish whether a new learner actually completes each week in 8-10 hours; that needs observed learner trials. It does not certify every technical statement in all external references, every behavior of the systems Python code, or full code security. The separate execution record covers local test results; passing those tests was not used as a substitute for reading and recomputing the lessons.

No GPU, CUDA runtime, native scheduler, NCCL, physical RDMA, BMC, DCGM diagnostic, power, thermal, or rack-service action was executed for this independent review. Compatibility and authorization remain properties of the eventual learner environment. The fleet/practicum author did not independently approve their own chapters through this report; those are reviewed in the [separate fleet review](fleet-teaching-review.md). This report's acceptance is limited to the systems theory and root learner integration named above.
