# Month 14: Measure reliability without fooling yourself

A fleet with fewer reported failures may have less observation time, a different workload, or a broken collector. This month, turn a count into a defensible statement. **G3-E02** covers **G3-O03**, exposure-normalized reliability, and **G3-O04**, uncertainty and alert quality. Use the [Month 13](13-fleet-truth.md) signal checks before trusting a denominator.

## Define the event and the opportunity

An incident is not automatically a component failure. A single rack outage can create hundreds of alerts. Repeated alerts can describe one unresolved failure. A corrected error can be an observation rather than lost service. Write an event definition before counting: the affected unit, qualifying symptom, episode boundary, deduplication rule, and source of adjudication.

Exposure is time or work during which the event could occur and be observed. Node-hours, GPU-hours, job-hours, and requests answer different questions. A four-GPU job running two hours contributes eight GPU-hours and two job-hours. You cannot divide job failures by GPU-hours and silently label the result a job-failure probability.

Verified public fact: under a homogeneous Poisson process or exponential model, the rate estimate is event count divided by total observed operating time; uncertainty depends on both. This is a conditional model result. A shared rack fault, changing hazard, or informative loss of observation can invalidate its assumptions. [NIST constant repair rate model](https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm)

For an availability claim, choose an explicit service measure. `successful eligible requests / eligible requests` is request success. `available minutes / observed minutes` is time availability. Neither equals component survival or training goodput. Keep planned maintenance in or out according to a recorded policy applied consistently to both comparison cohorts.

## The statistical model in plain language

A Poisson count model describes how many events occur during a stated exposure. Its parameter `mu` is the expected count. If the event rate is `lambda` per hour and observed exposure is `T` hours, then `mu = lambda*T`. A homogeneous process assumes the same rate throughout the modeled exposure. Independent increments means that, given the model, learning how many events occurred in one nonoverlapping interval does not change the distribution for another. A rack-wide outage affecting every node together is a reason to question that assumption.

An exponential lifetime model describes how long until the next event when the event hazard is constant. In this special setting it connects to the Poisson model: the chance of surviving time `T` without an event equals the chance that the count is zero. This connection is a modeling choice, not a discovery that real devices lack aging. For repaired systems, the events may repeat; for first-failure lifetimes, a failed unit stops contributing exposure unless the test design supplies a replacement.

The Poisson probability of exactly `k` events is `exp(-mu)*mu^k/k!`. Here `exp(x)` means e raised to x, and `k!` is the product 1 through k, with `0! = 1`. Summing the probabilities for counts 0 through k gives the probability of at most k events. The laptop calculator performs these sums and searches for rate values whose tail probabilities match the requested confidence level.

A 95% confidence procedure is one that covers the fixed true parameter in at least 95% of repeated equivalent experiments under its assumptions. It does not assign a 95% probability to the parameter being in this particular observed interval. More precise arithmetic cannot compensate for a false event model or an incorrect exposure ledger.

## Worked example: the count ranking reverses

**Synthetic calculation.** Cohort A records two failures over 3,000 node-hours; B records one over 200. A's rate is `2/3000*1000 = 0.667` events per 1,000 node-hours. B's is `1/200*1000 = 5`. A has more events but a lower observed rate. The rate ratio B/A is 7.5, which is a point estimate, not evidence of a precisely known sevenfold hardware difference.

For two observed events, a central 95% interval allocates 2.5% to each tail. At a mean count of about 0.2422, the probability of seeing at least two is 0.025: `1 - exp(-.2422)*(1 + .2422)`. This sets the lower limit. At a mean count of about 7.2247, the probability of seeing at most two is 0.025: `exp(-7.2247)*(1 + 7.2247 + 7.2247^2/2)`. This sets the upper limit. The count limits become rate limits by dividing by 3,000 hours, then multiplying by 1,000: approximately `[0.081, 2.408]` events per 1,000 hours. The lab searches for these count means numerically. The equivalent chi-square method in the source is another way to obtain the same limits; you do not need it to follow this calculation. Sparse events leave wide uncertainty. Do not interpret overlap alone as a formal test of equality, and do not infer causality from either interval. Cohort age, workload, firmware, placement, and collector coverage remain possible confounders.

Cohort C has zero events over 2,000 hours. Substituting `k = 0` into the count formula leaves `P(zero events) = exp(-rate * exposure)`, because `mu^0` and `0!` are both 1. Setting this probability to 0.05 gives a one-sided 95% upper rate bound of `-ln(.05)/2000`, or about 1.498 per 1,000 hours. Zero observed failures does not establish zero risk. The two-sided interval uses a different tail allocation and has a larger upper bound. Label which you report.

## Censoring: unfinished observation still contains information

Verified public fact: right-censored data record that a unit survived until observation ended, without claiming its future failure time. Interval-censored data bound a failure between observations. [NIST censoring](https://www.itl.nist.gov/div898/handbook/apr/section1/apr131.htm)

A unit entering late contributes only its observed exposure. A healthy unit administratively removed after 90 hours contributes those 90 hours. If a failing device loses telemetry and is removed from analysis, the missingness may depend on its condition. Label that uncertainty and recover evidence; do not fix it by increasing the statistical confidence level.

Verified public fact: the Kaplan-Meier estimator multiplies survival fractions at failure times and adjusts the population still at risk as units leave observation. It does not require choosing an exponential lifetime distribution. [NIST Kaplan-Meier procedure](https://www.itl.nist.gov/div898/handbook/apr/section2/apr215.htm)

**Synthetic survival calculation.** Four units start together. One fails at 10h, one is administratively censored at 15h, one fails at 20h, and one is censored at 25h. At 10h, survival becomes `3/4`. At 15h there is no failure, so survival stays `3/4`, but the risk set drops to two. At 20h survival becomes `(3/4)*(1/2) = 3/8`. The curve is an estimate for this cohort, not a known fleet law. If the 15h removal was due to suspected degradation, independent-censoring reasoning is doubtful.

## Alerts and the base-rate trap

**Synthetic calculation.** In 10,000 independent assessment windows, suppose 1% truly need intervention. A detector has sensitivity 90% and false-positive rate 5%. It detects 90 of the 100 true cases, but also flags 495 of the 9,900 negative cases. Only `90/(90+495) = 15.38%` of alerts are true positives. "90% sensitive" is not "90% of alerts are correct."

These probabilities are teaching inputs, not measured industry rates. Correlated alert windows make the independence assumption questionable. Evaluate incident-level deduplication, operator workload, missed harm, and time to detect, not just classification accuracy. Verified public fact: Google's SRE workbook treats precision, recall, detection time, and reset time as distinct alerting properties. [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)

## Investigation procedure and exercise

```sh
python3 labs/fleet/fleet_lab.py reliability labs/fleet/fixtures/reliability.json
python3 labs/fleet/fleet_lab.py reliability labs/fleet/fixtures/reliability-censored.json
```

1. Before running, predict the rate ordering and both zero-event upper bounds. Define the population, event, exposure unit, and window.
2. Reproduce the two tail probabilities in the worked example using a calculator or Python's `math.exp`, then convert their count means to rates. Explain how the lab searches for those endpoints; the source's chi-square formulation is optional enrichment. The numerical test suite checks reference quantiles; it does not establish that your fleet fits the model.
3. Copy the fixture. Add a late entrant observed for 50h with zero failures. Predict the changed denominator and recompute.
4. Change one termination reason to `lost_observation` and shorten its exposure to the last confirmed observation. Preserve the uncertainty warning in your recommendation.
5. Build a Pareto table for five synthetic causes with counts `[8, 5, 4, 2, 1]`, then add downtime minutes `[8, 100, 12, 240, 3]`. Explain why the priority changes when harm, not event count, is the objective.
6. Recommend either collect more data, run a controlled investigation, or intervene now. State the cost of waiting and the evidence that would reverse your decision. A safety-critical event may justify containment despite statistical uncertainty.

Submit one bundle with raw inputs, definitions, calculations, model assumptions, censored observations, alert confusion matrix, and the decision. Passing requires a correct denominator, an uncertainty statement tied to assumptions, and a changed-input replay. It does not require declaring one cohort intrinsically worse.

## Misconceptions

MTBF is not a replacement schedule. A confidence interval is not the probability that this fixed computed interval contains the parameter. A Pareto chart does not identify root causes. Large exposure does not repair selection bias. Ten repeated alerts from one incident are not ten independent failures.

## Questions

1. How much observed exposure do four GPUs supply during a two-hour job, and why may that be the wrong denominator for job success?
2. Why does a zero-failure run still have a finite upper rate bound?
3. What happens to the Kaplan-Meier risk set at an administrative censoring time?
4. If prevalence falls with sensitivity and false-positive rate fixed, what happens to positive predictive value?
5. Why can a confidence interval be numerically correct yet operationally misleading?

## Reasoned answers

1. Eight GPU-hours. Job success is an event about the job; dividing job failures by GPU exposure changes the quantity and requires a justified model relating them.
2. A nonzero rate can produce zero events by chance. The bound identifies a rate for which that observation would be sufficiently unlikely under the declared model and tail probability.
3. The unit leaves future risk sets without causing a downward survival step. Removing it retroactively from earlier risk sets would discard valid exposure.
4. It decreases because true cases become rarer while false alerts still arise from the larger negative population. Derive this from `p*sensitivity / (p*sensitivity + (1-p)*FPR)`.
5. The calculation may assume independent stationary events and valid exposure while the data contain common-cause failures, cohort differences, or missing observations tied to failure.

## Four-week study plan

| Week | Nine-hour allocation | Result |
|---|---|---|
| 1 | Definitions 2h; NIST reading 2h; hand calculations 3h; recall 2h | Measurement contract |
| 2 | CLI and changed exposures 4h; censoring and survival 3h; review 2h | Reproducible analysis |
| 3 | Alert matrix 2h; harm-based prioritization 2h; decision and defense 5h | G3-E02 draft |
| 4 | Remediation 4h; unseen cohort 3h; archive 2h | Assessed bundle |

Continue to [Month 15](15-incidents-and-change.md). The interval calculations are a worked model, not a distribution fitted to an actual rack fleet.
