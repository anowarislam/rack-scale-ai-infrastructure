# Month 5: decide whether the evidence is trustworthy

Your dashboard shows a cool GPU, no errors, and low power. The last collected sample is five minutes old. Is the machine healthy? You do not yet know. This chapter connects power and thermal reasoning to the integrity of the observations that guide operations.

**Prerequisites:** months 1-4; units, failure domains, and counters. **Assessed bundle:** G1-E05. G1-O09 detects misleading telemetry and timing. G1-O10 applies power, thermal, and access boundaries. This is an observation and decision exercise. It authorizes no electrical work, cooling changes, interlock bypass, or physical service.

## Power is a rate; energy is an amount

A watt is a joule per second. A kilowatt is 1,000 watts. A kilowatt-hour is the energy used by one kilowatt sustained for one hour. Lower instantaneous power does not necessarily mean less energy to finish a job: the job may take longer.

A component's rated power, an enforced power limit, measured instantaneous draw, and whole-server input draw are different quantities. GPU readings do not automatically include CPU, memory, networking, storage, fans, or conversion losses. Likewise, adding power-supply nameplate capacities does not tell you the measured workload load or usable facility capacity.

**Worked example 1: power and time trade off.** Configuration A finishes a fixed correct training task in 10 minutes at a measured average server input of 8 kW. Its energy is `8 kW * (10/60 h) = 1.333 kWh`. Configuration B uses 6 kW but takes 15 minutes: `6 * (15/60) = 1.5 kWh`. B reduces average power by 25% yet uses 12.5% more energy per completed task. B may still be preferable under a power ceiling. State whether the objective is peak load, task energy, throughput, cost, or deadline success; there is no universal winning number.

The constant-average inputs are synthetic. For varying power, approximate energy by summing `power_i * interval_i` over measured intervals, taking care with units and missing samples. Multiplying one instantaneous reading by a day's duration is an unverified assumption about the entire day.

## Redundancy is constrained by the failure state

Consider a synthetic rack whose combined load is 34 kW. Two independent feeds normally share that load equally, 17 kW each. Suppose each feed's approved usable capacity is 40 kW. If the documented wiring and PSU behavior allow the whole load to transfer to one feed, surviving-feed load becomes 34 kW and remaining headroom is `40 - 34 = 6 kW`.

That conclusion requires the explicit wiring/PSU assumption. Without it, dividing normal load by two tells you little about behavior after a feed fails. Also account for approved transient demand, cooling, other loads, derating, and facility policy. This is capacity reasoning, not branch-circuit design. Qualified facilities staff own the physical electrical calculation and work.

**Counterexample:** two 20 kW usable feeds can each carry 17 kW normally, but a transfer of all 34 kW to one exceeds its capacity by 14 kW. A normal-state dashboard can look safe while the redundancy objective is already impossible.

Real systems have product-specific constraints. For example, the DGX H100/H200 guide documents its PSU redundancy and behavior under reduced PSU availability, and separately states environmental limits. Those values apply to that product configuration; this course deliberately does not substitute them for your platform's limits. Read the [product power and environmental specifications](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html) and the exact approved local plan.

## Temperature is evidence about a location and time

A temperature reading needs a sensor location, units, timestamp, and product-specific meaning. GPU temperature is not inlet-air temperature. A coolant reading is not automatically a component-junction reading. A single average can hide a local hotspot or missing sensor.

Thermal control can change fan behavior, clocks, or power to keep components within their operating envelope. A slower workload can therefore be a consequence of environmental conditions, but low clocks alone do not identify thermal throttling: idle state, power limits, workload behavior, and other conditions remain alternatives. NVIDIA SMI documents separate power, temperature, clock, and clock-event observations; their availability varies. See the [SMI observation reference](https://docs.nvidia.com/deploy/nvidia-smi/index.html).

Use observation to narrow the cause. Compare workload demand, temperatures, event reasons, power, and performance over aligned intervals. Stop when an approved limit or local stop condition is reached. Never create a thermal fault by obstructing airflow or disabling protection. The [DGX safety guidance](https://docs.nvidia.com/dgx/dgxh100-user-guide/safety.html) is one official example of why physical integration and service are qualified-person tasks.

## A metric is a measurement plus context

A **gauge** represents a sampled value, such as temperature. A **counter** accumulates events, such as bytes or errors, until its defined reset condition. A **rate** derived from a counter is the counter increase divided by elapsed time. A **histogram** groups observations into ranges; its resolution affects percentile estimates. Always name the instrument and aggregation before treating a number as a physical truth.

Suppose an error counter increases from 100 to 160 over 30 s. The observed rate is `(160 - 100) / 30 = 2 errors/s`. If instead it changes from 100 to 10 after a restart, the negative difference is not "minus three errors per second." Determine reset behavior and treat the interval appropriately. Absence of a counter field is unknown, not zero.

Telemetry also depends on a pipeline: sensor or process, exporter, collector, network, storage, query, and dashboard. Each can fail independently. **Meta-monitoring** means observing that pipeline itself: last successful collection, sample counts, scrape errors, queue backlog, dropped records, and alert delivery. A monitor's process being alive does not prove the data is current or correctly attributed.

## Two timestamps answer two questions

OpenTelemetry distinguishes the time an event occurred at its source from the time the collection system observed it. These can differ due to transport delay and clock differences. See [the OpenTelemetry log data model](https://opentelemetry.io/docs/specs/otel/logs/data-model/). Wall-clock synchronization protocols such as NTP estimate clock relationships rather than make every timestamp exact; see [NTPv4, RFC 5905](https://www.rfc-editor.org/rfc/rfc5905.html). For a local duration, use a monotonic clock that is not interpreted as a calendar timestamp.

**Worked example 2: correct the order without inventing certainty.** The collector's current time is 1,000 s in the teaching clock. A cached sample was observed at 700 s, so collection age is `1000 - 700 = 300 s`. A dashboard showing its 42 C value as current is misleading regardless of how reassuring 42 looks.

A live sample was observed at 998 s and carries source time 1,008 s. A separate clock observation says the source is 12 s ahead, with uncertainty of 1 s. Corrected source time is `1008 - 12 = 996 s`, so estimated delivery delay is `998 - 996 = 2 s`. With that uncertainty, the source event time lies approximately in `[995, 997]`. It is reasonable to call the sample recent under this lab's 30 s freshness budget. It is not reasonable to infer physical thermal safety because the fixture supplies no platform temperature limit.

Without the offset correction, delivery delay would appear to be -10 s. A negative apparent delay is a signal to inspect clocks, timestamp interpretation, or data corruption, not proof that time ran backward. If two corrected event-time uncertainty intervals overlap, do not claim their causal order from timestamps alone; use request IDs or other ordering evidence.

## Observation authority is not change authority

**Authentication** identifies an actor; **authorization** determines what that actor may do. A telemetry collector needs observation access to specific resources. It does not inherently need firmware-update or reset permissions. **Least privilege** means granting only the necessary actions and scope. Network location alone should not be taken as proof of trust; this distinction is central to [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final).

Treat secrets and diagnostic bundles as data with owners. Record versions, image digests, and provenance without pasting tokens into command histories, screenshots, or reports. Verify certificates instead of bypassing verification to make an endpoint appear reachable. Software supply-chain reasoning asks who produced a package, how integrity is checked, whether its version is supported in this configuration, and who can alter the deployment artifact. A hash verifies matching bytes against a trusted reference; it does not by itself prove a trustworthy publisher.

For the exercise, select the provided `telemetry-reader` role. This is a synthetic permission label, not a claim that every product ships that exact role. In a real system, map required operations to the product's supported roles and test permitted and denied operations in the authorized scope.

| Observation | Candidate causes | Evidence that separates them | Decision boundary |
|---|---|---|---|
| Cool dashboard, workload stopped | Stale data; wrong device label; real cool idle state | Sample age, device identity, collector status | No health clearance from stale samples |
| Low clocks and slow job | Thermal/power policy; low demand; application stall | Aligned demand, event reasons, temperature and power | No cooling changes from one number |
| Event appears after its consequence | Clock offset; batching; wrong source timestamp | Source/observed times, offset uncertainty, request IDs | Preserve uncertain ordering |
| Collector has admin privileges | Convenience configuration; overly broad role | Required API reads versus granted actions | Reduce scope through approved access change |

## Four-week study route

| Week | Study and read | Apply | Review | Total |
|---|---|---|---|---|
| 1 | 3 h: power/energy and redundancy reasoning | 4 h: calculate both failure-state capacity and task energy | 2 h: list missing physical assumptions | 9 h |
| 2 | 3 h: sensors, counters, and timestamp semantics | 4 h: reproduce stale-data and clock failures | 2 h: explain uncertainty without a false health claim | 9 h |
| 3 | 2 h: access/provenance boundaries | 5 h: repair collection choices and write a safe decision | 2 h: role and evidence review | 9 h |
| 4 | 2 h: reread weak areas | 4 h: G1-E05 packet and control comparison | 3 h: defense and remediation | 9 h |

## G1-E05: repair the measurement before trusting it

Initialize the `telemetry` scenario. Observe and check the initial state. Calculate sample age and apparent delivery delay by hand. Change only the collector selection and rerun: the sample becomes fresh, but time interpretation and excessive privilege still fail. Use the stated offset evidence and required role to repair those independently. Compare with the healthy control, then reset and show that the failure is reproducible.

Submit the before/after numbers, competing explanations, clock uncertainty, permission decision, and a short stop/go note: "The signal pipeline meets these modeled checks; physical thermal health remains unknown because ..." Complete the sentence using the missing evidence. A passing L0 check is not a thermal qualification. Real read-only observations may be attached from the hardware workbook, with their exact time and device context.

## Checkpoint questions

1. Why can a lower-power run consume more energy?
2. Why is normal operation insufficient evidence of feed redundancy?
3. If an error counter decreases, what must you check before deriving a rate?
4. What remains unknown after the telemetry lab passes?

<details>
<summary>Answer key and misconception check</summary>

1. Energy depends on power integrated over time; the slower run can lose despite lower power.
2. The surviving feed may need to carry redistributed load. Wiring, transfer behavior, and failure-state capacity must be established.
3. Reset/restart, wrap behavior, identity changes, and collection errors. A raw negative delta is not a useful error rate.
4. Actual hardware conditions, product limits, calibration, longer observation windows, and all unsimulated pipeline behavior. The lab checks freshness, plausible ordering, and modeled access only.

The supplied model passes with `collector` set to `live`, `source_offset_s` set to 12, and `role` set to `telemetry-reader`. Offset values other than 12 can satisfy the broad plausibility invariant; only 12 is supported by the supplied clock measurement. Passing a permissive check never replaces evidence-based parameter choice.

</details>

**Next:** [Month 6: training, inference, and integrated recovery](06-workloads.md).
