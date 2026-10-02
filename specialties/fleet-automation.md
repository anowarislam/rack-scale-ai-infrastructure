# Specialty: make retry intent safe against changed state

**One intervention:** add or strengthen the request-ID plus expected-generation guard in a bounded lifecycle processor. Scope ends at local state transition decisions; no remote hardware executor is added.

## Characterize

Write down the unsafe baseline: a repeated repair request increments generation and repeats its side effect; a delayed request can overwrite a newer qualification state. The desired invariant is that the same applied intent has one effect and an obsolete state precondition has none.

**Synthetic worked example:** request `repair-4` first changes drained generation 2 to repairing generation 3. Its response is lost. Retrying exactly `repair-4` must return its prior meaning without creating generation 4. A different request `repair-5`, still expecting generation 2, must be rejected as stale. Reusing `repair-4` with a new action must be rejected as conflicting intent. These are three different cases.

**Counterexample:** deduplicating only on payload hash merges two legitimately distinct intents with identical parameters. Deduplicating only on ID accepts stale new requests. You need both intent identity and a state precondition, plus an atomic authority in a real implementation.

Verified public fact: AWS's documented design uses caller-provided identifiers, preserves intent parameters, and treats changed parameters for the same token as an error. The lab borrows this interface principle without claiming AWS infrastructure equivalence. [Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

## Intervene

Use a copied learner version of [the lifecycle lab](../labs/fleet/fleet_lab.py). First make the unsafe behavior observable in a deliberately local test double, then restore the guards in your learner implementation. Never weaken the supplied reference implementation or alter an external system. Keep an event ledger with result, state, generation, and request ID.

## Validate

Run the healthy, contention, failed qualification, and recovery fixtures. Add one changed-order test and one ID-reuse test with different parameters. Measure counts of applied transitions and rejected unsafe attempts, not elapsed script speed. Final generation must equal successful transitions, not number of delivered events. A valid retry must not be counted as a new application.

Use a fault-free control with six unique, current requests: it must reach available generation 6. Use the recovery path to reach generation 9 without deleting the original failed check. Have a peer construct one sequence whose result you predict before running.

## Recover and operationalize

Reset by replaying immutable input into a fresh process; there is no persistent service state. Archive the faulty learner implementation separately from the reference and label it unsafe. Provide schema, guard tests, behavior for unknown/expired tokens, and a production-gap record.

L0 can establish the bounded implementation and tests. It cannot establish a durable, distributed, crash-safe exactly-once side effect. A real service must coordinate persistent intent records with state mutation and resolve uncertain external completion. Do not hide that requirement behind the phrase "idempotent API."

Assessment requires all tested unsafe requests to leave state unchanged, positive requests to progress, a correct recovery explanation, and a usable handoff. Merely copying the reference source is practice, not independently assessed Build depth.
