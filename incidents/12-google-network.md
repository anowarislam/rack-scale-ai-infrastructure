# Case 12: Separate locations, shared maintenance authority

**Decision question:** Three network controllers run in separate failure domains. What must be true before that arrangement protects a service from a maintenance mistake?

The implicit assumption is that physical separation creates operational independence. It protects against some physical events. It does not stop one sufficiently broad command, identity, or automation bug from reaching every replica.

## Published account

**Verified operator account:** Google's detailed report, posted June 6, describes the June 2, 2019 network incident. Two maintenance-related misconfigurations combined with an automation bug to deschedule network control jobs across multiple physical locations. Forwarding continued briefly, then BGP route withdrawal reduced network capacity. Congestion hindered response tools, and recovery required rebuilding and distributing configuration. Google reported halting the automation; planned safeguards included rejecting broad descheduling requests and persisting configuration to avoid reconstruction. [Official report, Root Cause and Remediation](https://status.cloud.google.com/incident/cloud-networking/19009)

The report gives region-dependent packet-loss durations of 3 hours 19 minutes to 4 hours 25 minutes. **Source limit:** The page header, live updates, and detailed report have different end-time statements; this case does not collapse them into one universal restoration timestamp. The published account is evidence of the described mechanism, not access to Google's private topology or a claim about its current controls. [Official detailed report and updates](https://status.cloud.google.com/incident/cloud-networking/19009)

## The mechanism: draw the authority graph

**Teaching model:** Draw one graph for dependencies that carry traffic and another for dependencies that can change traffic. A controller replica in another building may add a new power boundary while remaining inside the same mutation boundary. Ask which actor can stop all replicas, replace all configurations, revoke their credentials, or prevent recovery.

The graph must also include the recovery path. If operator access, artifact retrieval, identity verification, and configuration distribution all depend on the impaired network, the repair procedure contains a cycle: fix the network to regain the tools needed to fix the network. An emergency route breaks that cycle only if its dependencies are sufficiently separate and usable under the stated failure.

Continuing to forward with the last configuration can buy time. It is not unlimited independence from control. Existing routes, topology, credentials, and safety assumptions may cease to be valid. A deliberately bounded continuation period is therefore a recovery deadline, not an assurance that control-plane loss is harmless.

## Worked example: replicas cannot cancel a common cause

**Synthetic probability model:** During one maintenance window, each of three controllers independently fails with probability `p = 0.01`, conditional on no common-cause event. A separate event disables all controllers with probability `q = 0.002`. These are invented probabilities, not measurements from Google.

Without the common cause, the probability of all three failing is `p^3 = 0.000001`. With it, the mutually exclusive possibilities are a common failure, or no common failure followed by three individual failures:

```text
P(all unavailable) = q + (1-q)*p^3
                   = 0.002000998
                   = 0.2000998%
```

The common-cause term dominates. Adding two more replicas changes the individual term to `p^5`; it barely changes the total because `q` remains. The lesson is mathematical and conditional: adding replicas helps the failure mechanisms that the replicas make independent.

**Synthetic recovery deadline:** Suppose existing forwarding remains safe and useful for ten minutes after controller loss. Detection takes two minutes, emergency access four, state reconstruction twelve, and distribution five. If these steps are sequential, recovery takes `2+4+12+5 = 23 minutes`, leaving a 13-minute gap beyond the continuation window.

Persisting usable state reduces reconstruction to two minutes, but the new total is still 13 minutes. Reducing emergency access to one minute brings it to ten, exactly at the deadline with no margin. A fifteen-minute safe continuation window would provide five minutes of modeled margin. These improvements act on different terms; a fast component does not prove a fast complete recovery path.

**Question:** Does this example justify extending the continuation window indefinitely?

<details>
<summary>Reasoned answer</summary>

No. The example assumes forwarding stays safe and useful for the selected window. Extending it requires evidence that stale state cannot cause an unacceptable routing or policy outcome during the extension. Alternatively, reduce the complete recovery path or provide a qualified independent control mechanism. A longer timer that outlasts its safety assumptions exchanges one failure mode for another.

</details>

## Tradeoffs and transfer

**Inference for AI infrastructure:** A GPU fleet can span racks while sharing a controller, firmware campaign, credential authority, or image promotion. A maintenance plan should identify both the resources touched and the authority capable of expanding that scope. A placement diagram alone is insufficient evidence of containment.

A canary limits exposure only if the operation is actually confined to it. In the teaching model, enforce scope at the receiving boundary as well as in the submitting tool: a broad request should not become safe merely because the operator intended a small one. Separate authorization does add operational complexity, and manual recovery can be slower; test the whole route before relying on it.

The counterfactual is five controllers managed by the same unrestricted deletion path. That improves independent-process resilience while retaining the common failure. Another design with fewer replicas but independently enforced maintenance boundaries may be safer for this specific hazard, though weaker against unrelated hardware failures. Choose according to the failure being controlled.

Use [fabric dependencies](../curriculum/04-fabric-storage.md), [incident recovery modes](../curriculum/15-incidents-and-change.md), and [state-transition invariants](../curriculum/16-lifecycle-automation.md) to draft a bounded maintenance exercise. Record controller availability, forwarded traffic, operator access, recoverable configuration, and verified scope rejection separately. This case does not audit Google's present architecture or prove a particular AI platform's independence.
