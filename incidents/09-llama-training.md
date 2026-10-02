# Case 09: Llama training and the cost of losing progress

**Decision question:** If a distributed training job encounters frequent interruptions, should you spend the next engineering week preventing failures, shortening restart, or changing checkpoint frequency?

The tempting assumption is that a large interruption count proves an unusable cluster. That conclusion needs a denominator and a loss model. An interruption that costs two minutes and one that destroys a day of progress are different reliability outcomes.

## Published account

**Verified account, not a single outage:** Meta's *The Llama 3 Herd of Models*, arXiv v3 dated November 23, 2024, describes a 54-day pre-training snapshot with 466 interruptions: 47 planned and 419 unexpected. It reports over 90% effective training time and only three occasions requiring significant manual intervention. Effective training time means useful training time divided by elapsed time. The authors report reducing startup and checkpointing time and building tools for faster diagnosis and resolution. [Original paper, section 3.3.4 and Table 5](https://arxiv.org/html/2407.21783v3#S3.SS3.SSS4)

**Source limitation:** Table 5's counts sum to 419, but its first row prints 148 faulty-GPU interruptions alongside 30.1%; `148/419` is 35.3%. The PDF has the same discrepancy. Do not silently correct the authors' classification. This account supplies neither an individual-event timeline nor a transferable device failure rate. [Pinned PDF, page 13](https://arxiv.org/pdf/2407.21783v3)

## The mechanism: a fleet is not a bag of independent jobs

**Teaching model:** Suppose every training step needs results from all `n` workers before it can commit. If each worker independently survives a chosen interval with probability `s`, the whole group survives with probability `s^n`. The exponent comes from requiring every event to hold together. It does not apply when workers share a rack power source, a faulty image, or another common cause.

This distinction changes the unit of investigation. Device failure frequency measures one population. Job interruption frequency measures the failure boundary of a computation. Useful progress also depends on recovery. A perfectly detected hardware failure can still cause large loss if the only valid checkpoint is old. A rapid restart can still be wrong if workers restore incompatible generations.

Keep three quantities separate: work committed, work recomputed, and wall time spent unable to compute. GPU activity alone cannot tell them apart. A dashboard that counts recomputation as productive work overstates the training result even when every device is busy.

## Worked example: derive a checkpoint interval

**Synthetic assumptions:** A job has mean useful-compute time `M = 600 minutes` between interruptions. A committed checkpoint pauses useful work for `C = 2 minutes`. Recovery adds `R = 8 minutes`. Checkpoints occur every `T` minutes of useful compute. Failures are rare relative to an interval and approximately uniform within it; ignore failure during checkpoint and recovery, and assume unchanged restart throughput.

Checkpoint overhead per useful minute is `C/T`. Uniform failure location means mean lost progress is `T/2`, so interruption overhead per useful minute is approximately `(T/2 + R)/M`. Adding them gives:

```text
overhead relative to useful compute = C/T + T/(2M) + R/M
```

This ratio is not directly the fraction of elapsed time wasted. If overhead is `w` per useful minute, useful fraction is approximately `1/(1+w)` under the same model.

| Interval T | Checkpoint overhead | Interruption overhead | Total overhead w |
|---|---:|---:|---:|
| 20 minutes | 10.00% | 3.00% | 13.00% |
| 49 minutes | 4.08% | 5.42% | 9.50% |
| 120 minutes | 1.67% | 11.33% | 13.00% |

The middle choice gives approximately `1/1.095 = 91.3%` useful time. Differentiating the terms that depend on `T` gives `-C/T^2 + 1/(2M) = 0`, hence `T = sqrt(2CM)`, or about 49 minutes. Equivalently, at that point checkpoint overhead equals expected recomputation overhead. The result follows from invented assumptions, not a fit to Meta's snapshot.

**Question:** If an engineering change halves recovery time to four minutes, should this model's best checkpoint interval double?

<details>
<summary>Reasoned answer</summary>

No. The recovery term changes from `8/600` to `4/600`, reducing overhead by about 0.67 percentage points at every interval. It does not change the minimum of the `T`-dependent terms. Changes to checkpoint cost or interruption frequency do change that minimum. Real restart improvements may also change the failure process or checkpoint design; that would require a new model rather than extending this result by intuition.

</details>

## Tradeoffs and transfer

**Inference for AI operations:** Prioritize the largest measured source of lost useful work, subject to correctness. Faster diagnosis helps only the interval it shortens. Better hardware isolation helps only the failures it contains. Faster checkpointing can permit more frequent saves without spending the gain on storage pauses.

The counterfactual is informative: a replacement device with half the failure frequency might provide less benefit than a modest restart improvement if recovery dominates loss. Conversely, reducing restart time cannot rescue checkpoints that are incomplete or mathematically inconsistent. Measure the terms before choosing.

A practical decision record should identify the failure boundary, valid checkpoint generation, lost steps, detection delay, replacement delay, restore time, and time until prior progress is regained. Compare policies using equivalent workload and exposure, then test whether shared failures invalidate the independence assumption.

Connect this to [exposure and reliability denominators](../curriculum/14-reliability.md), [checkpoint and collective correctness](../curriculum/04-fabric-storage.md), and [recovering useful application state](../tracks/kubernetes/10-workload-recovery.md). Those lessons help turn a restart into evidence of recovery. This case does not evaluate current Meta hardware, reproduce its training run, or establish a production checkpoint policy.
