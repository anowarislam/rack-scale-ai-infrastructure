# Fastly: the last code deployment is not the whole change

**Decision question:** Software has served normally for weeks. A permitted configuration update now causes failures. Which state must you examine before declaring the configuration wrong or the binary safe?

The hidden assumption is that a quiet period validates every behavior of the deployed code. It validates only the combinations actually exercised. This case treats change as an interaction among code, configuration, and runtime state.

## Mechanism: dormant behavior becomes reachable

Define the service result in this teaching model as `F(binary, configuration, input, runtime_state)`. A binary release changes one argument; a configuration activation changes another. The same code can therefore produce a different outcome without any new deployment.

Configuration validity is also a narrower contract than implementation safety. A parser can accept a permitted value while later code mishandles the resulting state. Rejecting every triggering value after an incident might contain the immediate problem, but it does not explain why an accepted state escaped its intended boundary.

Investigate both **introduction** and **activation**. Introduction places the defect in a version or shared component. Activation makes the faulty behavior reachable through an input, option, ordering, or state transition. Their timestamps can be far apart. Looking only at recent binary deployments can miss the first; looking only at the last user action can misassign responsibility for the second.

The model deliberately leaves the implementation open. A memory error, failed assertion, wrong result, or resource leak could fit this abstract pattern. The published evidence below does not identify which occurred.

## Published account

**Reported by the operator:** Fastly says a software rollout that began May 12, 2021 introduced a dormant defect. On June 8, a customer's valid configuration change activated it under particular conditions. The company reports that 85% of its network returned errors. This is Fastly's explanation, not an independent code-level finding. [Fastly's outage summary](https://www.fastly.com/blog/summary-of-june-8-outage)

The summary records disruption at 09:47 UTC and detection a minute later. Engineers identified the relevant configuration at 10:27 and subsequently disabled it. Fastly says 95% of the network was operating normally within 49 minutes; its timeline separately records the incident as mitigated at 12:35. Those statements use different recovery milestones and should not be collapsed into a single all-services recovery time. [Fastly's recovery account](https://www.fastly.com/blog/summary-of-june-8-outage)

Deployment of a permanent bug fix began at 17:25. The report says Fastly would investigate why quality assurance had not detected the defect and how to improve remediation. It does not demonstrate completion of those later process changes. [Fastly's stated follow-up](https://www.fastly.com/blog/summary-of-june-8-outage)

## Worked example: many passing tests can miss a rare state

**Synthetic assumptions:** Each independently selected activation scenario has probability `p = 0.0001` of exercising a faulty interaction. The probability is invented and constant; production frequency is unknown. Tests correctly detect the defect whenever they exercise it.

The probability that one test misses the interaction is `1 - p = 0.9999`. Independence gives:

```text
P(all n tests miss) = (1 - p)^n
For n = 1,000: 0.9999^1,000 = about 0.9048
For n = 30,000: 0.9999^30,000 = about 0.0498
```

A thousand successful random tests still leave about a 90.5% chance of missing this particular interaction under the assumptions. Thirty thousand reduce that miss probability to about 5%. This is the probability of the test process missing a defect assumed to exist, not a posterior probability that released software is defective.

Now challenge the assumptions. Repeating the same request against the same state 30,000 times does not provide 30,000 independent chances to exercise a configuration interaction. Nor does a large request count guarantee that a reload, expiration, or recovery transition occurred at all.

Suppose the synthetic design has four configuration profiles, three cache states, two activation orders, and three supported binary variants. Even a simplified cross-product contains `4 * 3 * 2 * 3 = 72` combinations. This is not a complete test plan; it exposes why coverage should name states and transitions. Prioritize boundary combinations using the architecture, then retain random tests to search beyond that model. Neither approach proves absence of defects.

## What would you do?

A configuration disable restores a failing service, but the same software remains installed everywhere. Is the incident resolved, and what can you safely claim?

<details>
<summary>Reasoned answer</summary>

Claim verified mitigation only for the observed service and workload. Preserve the triggering configuration and version identities, prevent unreviewed reactivation, and test the suspected interaction in an isolated environment. Check that the disable has converged across serving instances. A permanent correction needs evidence that the triggering case now works and that relevant neighboring states still behave correctly. Do not infer that every other configuration is safe because one was disabled, or that a valid customer action absolves the implementation of handling its allowed input.

</details>

## Tradeoffs and counterfactual

**Course judgment:** Control configuration activation with the same attention to exposure and rollback as executable releases. A narrow disable can restore service faster than a fleet-wide binary rollback, but leaves dormant code in place. Binary rollback may cover more triggers, while introducing compatibility and rollout risks. Choose using the known interaction and recoverable state.

A counterfactual with isolated activation cells could reduce affected scope, provided a cell cannot push the triggering state into shared infrastructure. A canary is not a boundary merely because it has a label. Inspect where configuration is stored, distributed, and interpreted.

## Transfer to AI infrastructure

**Course inference:** Treat model metadata, tokenizer settings, feature flags, request templates, scheduler policies, and driver options as inputs to a versioned behavior contract. Record configuration and runtime generations alongside binary versions. Test transitions such as model reload and resumed jobs, not just steady requests. Preserve a route to disable the trigger without depending on the affected serving path.

Use [fleet identity and freshness](../curriculum/13-fleet-truth.md), [state-aware recovery](../curriculum/15-incidents-and-change.md), and [automation under races](../curriculum/16-lifecycle-automation.md) to extend the exercise.

**Evidence limits:** The report omits the trigger's technical details and code defect. No customer identity, fault subtype, or later remediation completion is inferred.
