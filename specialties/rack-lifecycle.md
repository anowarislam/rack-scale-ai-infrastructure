# Specialty: current qualification before rack promotion

**One intervention:** introduce a promotion validator that requires matching asset identity, current incarnation, complete telemetry coverage, and a passing workload qualification record. The learner builds the validator at L0 by combining existing signal and lifecycle checks. No firmware writing is part of this intervention.

The causal hypothesis is simple: promotion is unsafe when the proof refers to an earlier asset or state. A validator at the promotion boundary can block that class of error. A dashboard added elsewhere might show the discrepancy without preventing admission, so the location of the guard matters.

## Characterize

Draw the current path from change request through drain, qualification, and admission. Name who owns each assertion. Record the candidate set, expected asset set, current boot IDs/generations, observation window, qualification ID, and workload correctness criterion. Read [Month 13](../curriculum/13-fleet-truth.md) and [Month 16](../curriculum/16-lifecycle-automation.md).

Start with two synthetic assets. Candidate A has matching serial and boot but a stale event. Candidate B has fresh telemetry from the wrong serial. Neither is promotable. A validator that merely counts two received records would accept both and fail the requirement.

## Intervene

Create a small local wrapper around the fleet lab functions. It must refuse to create a passing `accept_checks` event unless signal validation passes and the workload result identifies the same generation. The result should name every failing requirement. Keep the interface small: input evidence, target generation, decision, and reasons. Do not add a scheduler, inventory database, or remote executor.

Verified public fact: Redfish represents asynchronous operations with task state; acceptance is different from completion. If you map this validator to real hardware later, task completion and independent qualification remain separate inputs. [DMTF Redfish 1.20.2](https://www.dmtf.org/sites/default/files/standards/documents/DSP0266_1.20.2.html)

## Validate

Use six designed cases: valid evidence, missing asset, stale event, wrong boot, wrong serial, and workload result from an earlier generation. Expected unsafe admissions are zero; the valid case must pass. Report six-case coverage, not a population error rate. Add one benign control: source clock +40s with a documented +40s correction should pass when its corrected freshness is valid.

**Worked interpretation:** five unsafe candidates and one valid candidate produce six decisions. If all are rejected, unsafe admissions are zero but valid acceptance is also zero. That is not a complete success: the guard has become a permanent outage. Safety and serviceability both require testing.

## Recover

Return to the prior validator implementation in a copied local fixture, then replay the preserved failure to show why it was inadequate. Reinstall your guard in the local wrapper and show the positive case. On real hardware, recovery means keeping admission closed until the authorized owner can establish trustworthy evidence; bypassing the guard is not the default fallback.

## Operationalize and assess

Provide the wrapper, tests, evidence contract, known false-rejection cases, owner, and a rule that any identity or qualification-schema change triggers revalidation. A peer runs your six cases without help. Apply the common rubric to reasoning, guard correctness, positive control, recovery, and handoff.

L0 establishes validator behavior on synthetic evidence. L3 can add supervised observation or execution of an approved rack promotion workflow on a recorded BOM, with qualified service actors and independent signoff. L1/L2 read-only inventory does not establish real firmware or physical service competence. The choice of L0 must remain visible in the final claim.
