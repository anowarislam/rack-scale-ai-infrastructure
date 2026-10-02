# Engineer or principal capstone: put the invariant at the correct boundary

Own one technical decision that reduces recurrence of the Meridian failure while preserving safe recovery. Use your existing specialty intervention; do not redesign the entire fleet control plane. Your audience is an engineering reviewer who must decide whether the change's scope and evidence justify its adoption in the stated environment.

## What the reader needs from you

Start with the failure mechanism and the required guarantee. If an old qualification can authorize a new asset state, the guarantee is "only current qualification may authorize admission." The location of the fix follows the guarantee. A dashboard warning can help diagnosis but cannot enforce admission by itself. A check in a client can be bypassed by another client. A guard at the authoritative transition boundary can enforce the modeled invariant, provided its check and mutation are atomic.

For a performance specialty, the same logic applies differently: identify the resource whose contention creates exposed wait, and intervene in the request pattern you actually control. Do not tune an unrelated network merely because the slow timer is named collective.

## Worked exemplar fragments

**Problem and decision, synthetic:** "The repaired worker was promoted using checks from generation 4 after recovery had created generation 7. I placed the generation binding in the qualification acceptance transition. A reporting-only fix would reveal the mismatch after admission; this transition can reject it before admission. The current implementation is a single-process L0 model, so durable distributed enforcement remains unverified."

**Evidence fragment:** "Before the guard, the local test double accepted the old qualification. After the guard, the same event leaves generation and state unchanged, and the current-generation positive control still reaches ready. A duplicate applied request also leaves generation unchanged. This supports the tested invariant; it does not establish a measured production incident reduction."

**Counterfactual fragment:** "If only a collector backlog caused the symptom, a generation guard would not restore observability. I therefore also require current source and observation times in the admission evidence. This is an existing qualification input, not a second new intervention."

**Tradeoff fragment:** "Binding to all volatile fields could invalidate qualification unnecessarily. The tested model uses a logical configuration generation. A real integration must define which changes increment that generation and test that policy. I will not claim a production-safe mapping from this local model alone."

These fragments expose mechanism, location, evidence, alternative, and limit. They do not rely on the title principal to establish authority.

## Build and defend

1. Reproduce the failure with your existing specialty baseline. Write the expected wrong state before running.
2. Explain the required invariant and compare at least two intervention locations. Choose one with the necessary authority.
3. Implement or configure the bounded change in the permitted environment. Preserve unrelated behavior.
4. Validate the original failure, a changed-input case, and a fault-free control. Include correctness and recovery, not just error disappearance.
5. Provide a handoff that another operator actually uses. Record its gaps and correct them.
6. Incorporate Month 23's changed demand or evidence without expanding technical claims. Explain what your fix cannot solve, such as a capacity deficit.

Final artifact: a short engineering decision record with causal map, minimal change, test/result table, recovery path, operational owner, and explicit environment/version boundary. Attach raw evidence separately. At Month 24, reproduce one result and defend a competing hypothesis.

## Assessment and remediation

The reviewer checks whether the chosen boundary can enforce the guarantee, whether observations distinguish the claimed mechanism, whether negative and positive cases pass, and whether recovery leaves the stated invariants true. A solution at the wrong layer fails even if its code is elegant. Remedy by tracing the authorization path and rerunning a discriminating test, not adding more dashboard panels.

L0 can establish the local implementation. A native platform or physical behavior claim requires that actual environment. Influence without authority can be course-observed during review and handoff; it is not proof of years of principal-level impact. No real service mutation or public change submission is authorized by this packet.
