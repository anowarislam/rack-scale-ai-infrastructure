# Month 6: turn computation into useful work

A GPU can be busy while a job makes little useful progress. A server can complete more requests per second while almost every user misses a deadline. To operate AI infrastructure, you need to connect the machine's activity to the workload's objective. This chapter teaches a complete tiny training loop, explains how training and inference stress a system differently, and closes Systems Gate G1 with recovery evidence.

**Prerequisites:** months 1-5. You should understand tensor shape, memory budgets, rank agreement, checkpoint publication, and trustworthy timing. **Assessed bundle:** G1-E06. G1-O11 compares throughput, goodput, latency, and correctness. G1-O12 recovers and verifies an integrated workload. Actual L1 execution is required for the gate's single-GPU workload claim; L0 is preparation and local mechanism evidence.

## Training changes a model; inference uses one

A model is a function with adjustable parameters. Training chooses those parameters using examples and an objective. Inference uses the current parameters to produce outputs. The infrastructure cares about both the mathematical result and how the work moves through memory, devices, communication, and storage.

Our tiny model predicts `prediction = weight * x + bias`. Training data contains four pairs:

| x | Target y |
|---|---|
| -1.0 | -1.0 |
| -0.5 | 0.0 |
| 0.5 | 2.0 |
| 1.0 | 3.0 |

These values follow `y = 2*x + 1`, so we know the desired parameters. That makes correctness visible; this is not a realistic language-model dataset or a generalization study.

A training step has four parts. The **forward pass** computes predictions. The **loss** measures prediction error. The **backward pass** computes gradients of that loss with respect to parameters. The **optimizer** changes parameters using those gradients. A **learning rate** controls the update size. PyTorch's automatic differentiation constructs gradients from recorded operations, while its SGD optimizer applies configured updates; the course CUDA backend uses these mechanisms. See [autograd fundamentals](https://docs.pytorch.org/tutorials/beginner/introyt/autogradyt_tutorial.html), [PyTorch 2.8 Linear](https://docs.pytorch.org/docs/2.8/generated/torch.nn.Linear.html), and [SGD](https://docs.pytorch.org/docs/2.8/generated/torch.optim.SGD.html).

## Worked example 1: calculate one full training step

Start with `weight = 0` and `bias = 0`. All predictions are zero. Errors, defined as prediction minus target, are `[1, 0, -2, -3]`. Mean squared error is `(1^2 + 0^2 + (-2)^2 + (-3)^2) / 4 = 14/4 = 3.5`.

For this model and loss, the gradient of bias is twice the mean error: `2 * (1 + 0 - 2 - 3) / 4 = -2`. The gradient of weight also accounts for each x: `2 * ((1 * -1) + (0 * -0.5) + (-2 * 0.5) + (-3 * 1)) / 4 = -2.5`.

SGD subtracts learning rate times gradient. At learning rate 0.1:

```text
new weight = 0 - 0.1 * (-2.5) = 0.25
new bias   = 0 - 0.1 * (-2.0) = 0.20
```

New predictions are `[-0.05, 0.075, 0.325, 0.45]`. New errors are `[0.95, 0.075, -1.675, -2.55]`, and new loss is `(0.9025 + 0.005625 + 2.805625 + 6.5025) / 4 = 2.5540625`. The loss decreased, but the model is not yet accurate. Repeating the update moves weight toward 2 and bias toward 1. The Python reference workload computes the same equations directly; the CUDA backend runs a linear layer and autograd.

This example explains why a correct process exit is insufficient. A script could run successfully while using the wrong sign for the gradient, the wrong targets, or a stale checkpoint. Verify the known predictions and loss as well as execution. Conversely, one decreasing loss is not proof of a useful production model; real model quality requires separate evaluation data and criteria.

## Batches, distribution, and synchronization

A **batch** is a set of examples used together. A **step** here means one optimizer update. An **epoch** is a pass through a defined dataset. These words are not interchangeable. Log exact definitions, especially when a loader repeats or shards data.

Data parallelism gives each worker a model replica and different examples, then synchronizes gradients. PyTorch DistributedDataParallel synchronizes gradients but leaves input sharding to the application. This is a consequential boundary: replicating a process does not automatically partition data. See [PyTorch 2.8 DistributedDataParallel](https://docs.pytorch.org/docs/2.8/generated/torch.nn.parallel.DistributedDataParallel.html).

With four ranks, two examples per microbatch per rank, and four accumulation microsteps per optimizer update, the effective batch is `4 * 2 * 4 = 32 examples`, assuming equal contributions and intended normalization. If one worker repeats another's examples, the nominal count is still 32 but the information is different. If workers execute different numbers of collectives, the job may hang.

**Tensor parallelism** divides computations inside a layer across devices. **Pipeline parallelism** places different model stages on different workers, with microbatches flowing between them. These address different constraints from simple data replication and add different communication schedules. The [PyTorch tensor-parallel tutorial](https://docs.pytorch.org/tutorials/intermediate/TP_tutorial.html) illustrates why combining strategies requires explicit model and communication boundaries. This course uses those concepts to reason about placement; it does not claim that a tiny single-GPU probe reproduces distributed model training.

## Inference has a queue before it has a kernel

An arriving request can wait before computation starts. Its end-to-end latency includes admission, queueing, input preparation, model execution, and response delivery. A system that measures only kernel time can miss most of the user's wait.

In autoregressive language-model inference, a **token** is a unit of the model's input/output representation. Processing the existing prompt is commonly called **prefill**; generating additional tokens step by step is **decode**. The first token's delay and the time between later tokens capture different user experiences. A **key-value cache** reuses attention-related intermediate values from previously processed tokens; it trades memory for avoiding repeated work. This is explained by the library maintainers in [Transformers caching concepts](https://huggingface.co/docs/transformers/main/cache_explanation), whose main-branch API details are not a pinned deployment contract here.

Longer contexts and more concurrent sequences can increase cache memory. Larger batches can improve device efficiency while increasing waiting or memory pressure. Those are hypotheses to characterize with the actual serving engine; the course queue lab deliberately models neither a transformer nor KV-cache behavior. It isolates the simpler admission/service relationship first.

## Throughput, goodput, and tail latency answer different questions

**Throughput** is completed work divided by elapsed time, with the work unit stated: requests, tokens, examples, or steps. **Goodput** is useful completed work divided by elapsed time under an explicitly stated usefulness criterion. In our serving lab, a request counts as good only if its correct result arrives within 1,500 ms. In a training recovery review, you might count only valid retained progress and exclude repeated work. State the definition rather than imply a universal metric.

A percentile describes a distribution. This course uses the **nearest-rank** convention: sort N measurements and select item `ceil(p*N)` for percentile fraction p, with one-based indexing. With 100 latencies, p99 selects the 99th. Percentile conventions and histogram approximations can differ, so record yours.

**Worked example 2: a higher-throughput failure.** The queue lab has two workers, each taking 400 ms per request. Service capacity under the simplified continuous model is `2 / 0.4 s = 5 requests/s`. Send batches of eight requests at each integer second for ten seconds. Eight arrive while only five can be serviced per second on average, so unfinished work accumulates.

At time zero, the first eight finish in pairs at 0.4, 0.8, 1.2, and 1.6 s. Two already miss the 1.5 s deadline. Later arrivals wait behind earlier work. All 80 requests complete by 16 s, so observed throughput is `80 / 16 = 5 requests/s`. Only ten meet the deadline, yielding `10 / 16 = 0.625 good requests/s`; p99 latency is 7,000 ms.

Reduce arrivals to four per second, keeping the same service capacity. The first batch completes at 0.4 and 0.8 s, leaving room before the next batch. All 40 requests meet the deadline, and the last finishes at 9.8 s. This finite-run measurement gives `40 / 9.8 = 4.0816 good requests/s`, with p99 800 ms. The rate is slightly above four because the measured interval starts with an immediate batch and ends before a full tenth second. Long-run offered load remains four per second.

The lower-throughput run produces over six times the deadline-qualified goodput. This is why saturation is not an objective by itself. Possible remedies in a real system include admission control, more usable capacity, shorter service time, or a changed service objective; rejecting everything would meet latency for no work, so report demand and rejection rates too.

**Counterexample to averages:** 98 requests at 100 ms and two at 3,000 ms have mean `(98*100 + 2*3000)/100 = 158 ms`, which looks modest, while nearest-rank p99 is 3,000 ms. A mean-latency objective would hide the experience of those two users.

## Recovery must preserve meaning, not merely restart a process

The training workload saves a checkpoint every ten steps. Interrupting after step 23 leaves the published step-20 state. Resume must begin at 20, replay updates 21-23, and continue to 40. A process that skips directly to 24 without those parameter updates would silently lose training work. A process that loads step-20 parameters but records step 23 in metadata would misrepresent progress.

The checkpoint contains weight, bias, step, learning rate, dataset hash, and backend. The optimizer has no momentum, and data order is fixed, so there is no additional optimizer or random state in this particular model. A production trainer can need much more. The manifest checksum rejects altered content. The uninterrupted control supplies expected final predictions independent of a successful restart message.

For the Python backend, interrupted/resumed final predictions should equal the uninterrupted reference exactly in the same interpreter. For CUDA, compare with a stated tolerance and record exact versions. The course uses tolerance 0.1 against the four known targets and recommends a tighter observed baseline comparison when feasible. CPU/GPU bitwise identity across environments is not guaranteed by PyTorch's [reproducibility guidance](https://docs.pytorch.org/docs/2.8/notes/randomness.html).

| Symptom | Plausible layer | Evidence to distinguish | Positive recovery evidence |
|---|---|---|---|
| Busy GPU, no retained progress | Repeated failures/checkpoint loss; invalid results | Completed versus committed steps, correctness | Advancing valid committed state |
| High request throughput, poor experience | Queueing, deadlines, overload | Arrival/finish times, rejected work, tail distribution | Deadline-qualified goodput at stated demand |
| One rank waits indefinitely | Earlier peer failure, collective mismatch, transport | Earliest event across all ranks with time uncertainty | All ranks finish correct matching work |
| Restart succeeds, result changes | Wrong checkpoint, data order, optimizer state | State hashes, step, inputs, baseline output | Correctness matches stated tolerance |

## Four-week study route

| Week | Study and read | Apply | Review | Total |
|---|---|---|---|---|
| 1 | 3 h: training mathematics and distribution | 4 h: calculate first update and run reference workload | 2 h: explain state needed for resume | 9 h |
| 2 | 3 h: inference and queueing | 4 h: reproduce overloaded and recovered queue cases | 2 h: defend the goodput denominator | 9 h |
| 3 | 2 h: integration and hardware procedure | 5 h: approved L1 interruption/recovery and baseline comparison | 2 h: evidence review across system layers | 9 h |
| 4 | 2 h: address weak evidence | 4 h: prepare and defend G1-E06 and full G1 | 3 h: remediation or record pending fidelity | 9 h |

## G1-E06: integrate correctness, load, and recovery

Run the `workload` scenario with its broken arrival rate. Record p50, p99, throughput, goodput, completion count, and duration. Predict the effect of reducing arrivals before changing the configuration. Find at least one load that passes and one that fails; keep the denominator and deadline unchanged. Compare with the healthy control and reproduce the original failure with reset.

Next execute the training baseline, interruption, and resume procedure in [the lab README](../labs/systems/README.md). For the gate's L1 claim, repeat with the CUDA backend using [the hardware workbook](../labs/systems/hardware-workbook.md). Capture real identity, versions, memory observations, outputs, checkpoint metadata, and recovery. Do not inject hardware faults. The interruption is a controlled application stop.

Submit one integrated packet explaining the path from process to device, inputs, checkpoint storage, and observations. Include the first-update derivation, queue analysis, failed attempt, chosen recovery, known-result validation, a healthy control, and untested boundaries. Use [the gate rubric](../assessments/gates.md). A reviewer should be able to reconstruct what happened without trusting your narrative alone.

## Checkpoint questions

1. Why subtract the gradient rather than add it in this example?
2. What does DDP leave to the application that affects training correctness?
3. Why is five completed requests/s worse than 4.0816 in the supplied experiment?
4. Why does restarting from step 20 repeat three updates after an interruption at 23?
5. Does a passing CUDA probe establish model quality or multi-node performance?

<details>
<summary>Answer key and misconception check</summary>

1. The gradient points toward increasing local loss; a sufficiently suitable step in the negative direction seeks lower loss. Our first update demonstrably lowers MSE from 3.5 to 2.5540625. Arbitrarily large learning rates need not decrease it.
2. Input sharding and application behavior, including consistent collective participation and intended effective-batch semantics. Gradient synchronization does not fix duplicated or wrong data.
3. The five-per-second run has severe queueing: only 0.625 requests/s meet the stated deadline. The recovered run's completions all qualify. Compare useful outcomes, not device activity alone.
4. Only the step-20 parameters were published. Replaying 21-23 reconstructs lost uncommitted work before advancing. Metadata cannot substitute for missing computation.
5. No. It establishes bounded execution, correctness, and recovery on the recorded device/environment. Real model quality, sustained operation, distributed fabric behavior, and fleet reliability remain separate outcomes.

In the supplied queue, `arrivals_per_s` 4 matches the healthy control; explore 5 to see the effect of batch arrival timing at nominal capacity. Do not infer a real serving admission rate from this simplified model.

</details>

**Next:** complete the [G1 review](../assessments/gates.md), preserve pending L1 outcomes honestly, then enter the shared workload-management chapter for month 7. You now have the system model needed to ask a scheduler for the resources, topology, identity, and recovery behavior your workload actually needs.
