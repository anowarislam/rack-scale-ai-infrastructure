# Slurm: months 8-12

Choose Slurm as your primary Build track when you need to construct and operate a batch allocation system. Choose it as the secondary Run/compare track when Kubernetes is primary. A complete Slurm path teaches its own model: job allocations, steps, partitions, associations and QOS, GRES/TRES, queue policy, persistent controller state, and optional database accounting. It is not Kubernetes vocabulary translated into different commands.

Read [month 7](../../curriculum/07-workload-contract.md), then:

1. [Month 8: Reference environment](08-reference-environment.md)
2. [Month 9: Placement and fairness](09-placement-and-fairness.md)
3. [Month 10: Workload recovery](10-workload-recovery.md)
4. [Month 11: Operability](11-operability.md)
5. [Month 12: Integration and comparison](12-integration-and-comparison.md)

The [dedicated Linux VM runbook](../../labs/platforms/slurm/runbook.md) contains an actual configuration and representative CPU jobs. Its reference source release is Slurm 25.05.3, tag `slurm-25-05-3-1`, resolved official commit `1c0b066e1e0432a94b0149cf40d23b882e137942`. This is a historical teaching baseline; the course does not claim a current supported production matrix. The setup was not executed on the author's macOS machine: native Slurm validation is **NOT_RUN**. The same application checkpoint code is executed by the laptop tests, which does not substitute for a native job.

One weekly budget covers both platforms: roughly 5 hours primary study/build, 2 hours secondary study/run, and 1-3 hours evidence and remediation, totaling 8-10. Each chapter's four weeks refers to the same month as the other track. Do not add both calendars. The central course calendar controls reserved remediation and defense weeks.

The primary learner constructs, explains, and changes the reference. The secondary learner runs it, diagnoses one native scheduling decision, recovers a failure, reviews real evidence or accounting, and writes the comparison. Actual database fair-share, GPU isolation, and HA are additional environment-dependent demonstrations, never claims inferred from a single CPU VM. All work feeds [G2's six bundles and twelve outcomes](../../assessments/gates.md).
