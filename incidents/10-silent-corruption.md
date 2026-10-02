# Case 10: When a successful computation returns the wrong answer

**Decision question:** A computation completes, its output checksum matches, and a retry returns the same result. What evidence would justify publishing that result?

The hidden assumption is that successful execution plus intact storage proves correct computation. It proves less: the process finished, and the stored bytes match whatever was checksummed. A wrong value can be copied, checksummed, and replicated perfectly.

## Published account

**Verified account, not a single outage:** Google's Hochschild and colleagues published *Cores that don't count* at HotOS 2021. They describe a valid library change exposing incorrect computation on a subset of machines by exercising previously uncommon instructions. Their observations include intermittent, workload-sensitive failures associated with particular CPU cores. One example encrypted and decrypted successfully on the same faulty core but failed when decrypted elsewhere. [Original conference paper, sections 1-2](https://sigops.org/s/conferences/hotos/2021/papers/hotos21-s01-hochschild.pdf)

**Source limitation:** This is a fleet study and research agenda, not a dated outage reconstruction or a GPU failure-rate measurement. Exact rates are withheld, and the authors describe limited visibility into underlying hardware causes. Proposed defenses are not all reported as deployed guarantees. [Google Research publication record](https://research.google/pubs/cores-that-dont-count/)

## The mechanism: preserve bytes or verify meaning?

**Teaching model:** Let a correct calculation be `y = f(x)`. A faulty execution produces `z`, where `z != y`, and then computes a checksum of `z`. Storage later returns `z` with that checksum. The integrity check passes because the stored value was preserved. Nothing in this sequence compared the computation with `f(x)`.

Redundancy moves the question to independence. Two executions can share the input error, program bug, defective execution unit, or wrong validation rule. Repeating an operation is valuable evidence only against faults the repetition could expose. Copying one answer to three replicas offers no independent computation at all.

An invariant supplies another route. Instead of recomputing every operation, check a property that any correct answer must satisfy. The property should be cheaper to evaluate and sufficiently independent of the path being checked. A weak invariant catches some errors; it is not a proof against every possible wrong answer.

## Worked example: a check with a visible blind spot

**Synthetic arithmetic:** Let `A = [[2,1],[1,3]]` and `x = [4,5]`. Correct multiplication produces `y = [13,19]`. Check the sum of output elements. The column sums of `A` are `[3,4]`, so the expected sum is `3*4 + 4*5 = 32`.

The corrupted result `[13,18]` sums to 31 and is rejected. But `[14,18]` sums to 32 and passes. Its errors cancel under this particular check. Add a differently weighted check using weights `[1,2]`. The expected value is `(1*2 + 2*1)*4 + (1*1 + 2*3)*5 = 51`; the wrong result yields `14 + 2*18 = 50`. This check catches the error the first one missed.

To reason precisely about detection probability, change to an explicitly artificial model: all arithmetic is exact modulo the prime 101. Choose both weights independently and uniformly from 0 through 100, after the incorrect output is fixed. For any nonzero error vector, hold one weight fixed. Exactly one value of the other weight cancels the error, because the corresponding nonzero error component has a multiplicative inverse. Thus the chance of missing that fixed error is `1/101`, about 0.99%.

Two independent weight vectors reduce that chance to `1/101^2`, about 0.0098%, provided the checker itself is correct and the error cannot adapt to the weights. These are probabilities in the constructed modular model. Floating-point rounding, correlated checker faults, and adaptive errors violate its assumptions; these numbers are not detection guarantees for real training.

**Question:** Would running the same weighted check twice with the same weights give the squared miss probability?

<details>
<summary>Reasoned answer</summary>

No. A fixed error that passes the first deterministic check passes the identical check again. There is only one random selection, not two independent chances to reveal the error. A different execution location might expose an intermittent checker defect, but that is a separate hypothesis. State what was varied and which failure mechanism that variation tests.

</details>

## Tradeoffs and transfer

**Inference for AI operations:** Treat numerical validity as a separate acceptance condition from process completion and transport integrity. For a training pipeline, possible checks include known small computations, independently derived aggregate properties, and bounded replay of suspicious work on another qualified resource. Each needs a documented tolerance and scope. A plausible loss curve alone cannot certify every intermediate result.

The counterfactual is a system that checks every operation through a wholly independent implementation. It could increase detection coverage but consume substantial computation, introduce another implementation to qualify, and still share an incorrect specification. Select checks according to consequence: a corrupted published checkpoint and a discarded exploratory batch need not have identical acceptance rules.

When investigating, preserve the exact input, binary, device or core identity, operating conditions, observed output, expected property, and replay location. A failure following one resource across controlled replays weakens a pure input-bug explanation; a failure following the input across independently qualified resources weakens a resource-specific explanation. Neither observation alone resolves all causes.

Use [GPU execution and diagnostic boundaries](../curriculum/03-gpu-runtime.md) to separate discovery from computation, and [fleet identity and observation provenance](../curriculum/13-fleet-truth.md) to keep replay evidence comparable. This case does not diagnose a particular processor, measure contemporary corruption prevalence, or show that any proposed check suffices for an actual model.
