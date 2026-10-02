# Cloudflare: a rule can be correct and still exhaust the service

**Decision question:** A new inspection rule correctly allows and rejects every test request. Is that enough evidence to run it against all production traffic?

That assumes functional correctness bounds resource cost. It does not. A rule can compute the right answer but consume so much shared CPU that other requests never receive an answer. The model below makes that distinction explicit without reproducing the historical expression.

## Mechanism: the cost of searching alternatives

Consider a deliberately simple matcher for `^a*a*b$`. Here each `a*` accepts zero or more `a` characters, `b` requires a final literal character, and the anchors constrain the full input. The input contains only `a` characters, so the match must fail.

Our teaching matcher tries every allocation of the input between the two repetitions before concluding that no `b` exists. With `n` input characters, an attempted split can assign `i` characters to the first repetition and `j` to the second, where `i + j <= n`. It tests:

```text
(n + 1) + n + ... + 1 = (n + 1)(n + 2) / 2
```

possible allocations. Doubling a large input length therefore makes this modeled work approximately four times larger. This is quadratic growth, not exponential growth. Some expressions and algorithms have other behavior; no universal complexity claim follows from the word "regex."

This matcher is intentionally unoptimized. A real engine might reject the input quickly using a required-character check or another optimization. The lesson is to measure and bound the actual implementation on difficult failures, not to infer cost from short successful matches.

## Published account

**Reported by the operator:** Cloudflare attributes its July 2, 2019 outage to a WAF rule whose regular expression caused excessive backtracking and exhausted CPU used to serve HTTP/HTTPS traffic. The company reports 27 minutes of disruption. The account is an operator explanation, not an independently reproduced incident. [Cloudflare's detailed postmortem](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)

Deployment began at 13:42 UTC. The rule was in simulation mode, which prevented blocking decisions but still executed its matching logic. Functional tests passed; they did not test for runaway CPU. The rule-distribution path allowed rapid global propagation. [Cloudflare's testing and deployment account](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)

Engineers disabled the WAF globally at 14:07; CPU and traffic returned to expected levels by 14:09. Internal access dependencies complicated that operation. They tested removal of the offending rule and re-enabled the WAF at 14:52. Other protective mechanisms continued operating meanwhile. The report marks restoration of an excessive-CPU guard complete and proposes staged rule rollout. [Cloudflare's recovery and corrective actions](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)

## Worked example: turning steps into saturation

**Synthetic assumptions:** Use the simple matcher above with `n = 2,000`. Each attempted allocation costs 10 ns of CPU time. A service has 32 CPU cores and receives 20,000 requests/s. Every request needs 0.2 ms of baseline CPU, and 10% additionally incur this expensive failed match. Ignore scheduling overhead and assume perfect distribution across cores.

```text
Matcher attempts = 2,001 * 2,002 / 2 = 2,003,001
Added CPU per expensive request = 2,003,001 * 10 ns = 20.03001 ms
Baseline CPU demand = 20,000 * 0.0002 = 4 CPU-seconds/s
Added CPU demand = 2,000 * 0.02003001 = 40.06002 CPU-seconds/s
Total demand = 44.06002 CPU-seconds/s
```

The machine supplies at most 32 CPU-seconds each second. Demand exceeds that capacity by about 12.06 CPU-seconds/s. A correct matcher cannot compensate for missing compute capacity; queues, rejection, or missed deadlines must result if this load persists.

If the maximum examined input is halved to 1,000 characters in this model, attempts become `1,001 * 1,002 / 2 = 501,501`. Added demand falls to `2,000 * 0.00501501 = 10.03002 CPU-seconds/s`, for a total of 14.03002. That arithmetic explains why input limits can matter, but it does not establish that truncating a real security inspection is acceptable. The truncated suffix might contain the very evidence the rule must inspect.

## What would you do?

A shadow deployment does not affect allow/deny decisions, but its CPU per request rises sharply with long nonmatching inputs. The service's success-rate dashboard is still green. Do you expand it?

<details>
<summary>Reasoned answer</summary>

Stop expansion while bounding the resource cost. A green success rate at the present load does not prove spare capacity at the next load. Compare CPU time by input size and outcome, test intentionally difficult nonmatches, and establish per-evaluation and aggregate budgets. Decide explicitly what happens when the budget is exhausted: reject, bypass, or defer each has consequences. Repeat the workload with the rule disabled to separate the rule's cost from a simultaneous change in traffic.

</details>

## Tradeoffs and counterfactual

**Course judgment:** A safety function needs a resource-isolation argument as well as detection quality. Restricting pattern expressiveness can simplify cost bounds but may require a different detector. Time limits protect capacity only if cancellation actually interrupts the work; they also require a defined policy for unfinished inspection.

A staged rollout could limit simultaneous exposure if its stages have separate capacity and meaningful stop conditions. It would not prove safety for an input absent from the canary workload. Use staged exposure and adversarial cost testing for different purposes.

## Transfer to AI infrastructure

**Course inference:** The same analysis applies to tokenization, prompt filtering, admission webhooks, telemetry parsing, and request validation around expensive GPU work. A CPU preprocessor can starve an otherwise idle accelerator fleet. Shadow evaluation still consumes resources. Track cost by input shape and failure path, and reserve enough independent capacity to disable an expensive function.

Connect this to [workload contracts](../curriculum/07-workload-contract.md), [canary interpretation](../curriculum/15-incidents-and-change.md), and [telemetry trust](../curriculum/05-power-telemetry-security.md).

**Evidence limits:** The numerical matcher is invented. No production traffic replay, current WAF implementation, or independent incident reconstruction was tested.
