# Kubernetes: months 8-12

Use Kubernetes as your primary Build track when you want to construct and operate a declarative workload platform. Use the same chapters as your secondary Run/compare track when Slurm is primary. The primary learner explains and changes the reference design; the secondary learner runs a representative workload, investigates a native scheduling decision, recovers a failure, reviews evidence, and compares behavior. Neither path is satisfied by reading alone.

Start with [the shared workload contract](../../curriculum/07-workload-contract.md). Then read in order:

1. [Month 8: Reference environment](08-reference-environment.md)
2. [Month 9: Placement and fairness](09-placement-and-fairness.md)
3. [Month 10: Workload recovery](10-workload-recovery.md)
4. [Month 11: Operability](11-operability.md)
5. [Month 12: Integration and comparison](12-integration-and-comparison.md)

The concepts are taught in the chapters; [the sandbox runbook](../../labs/platforms/kubernetes/README.md) supplies exact operational commands. Examples use Kubernetes v1.34.0, kind v0.30.0, and a digest-pinned Python image. These are historical laboratory versions, not a recommendation for production or a claim of current support. Source scope and retrieval are recorded in [the platform ledger](../../evidence/platform-sources.json).

Each chapter's four weeks divide one **8-10 hour total weekly budget**: approximately 5 hours primary theory/build, 2 hours secondary theory/run, 1 hour evidence, and up to 2 hours review/remediation. If Kubernetes is secondary, swap the primary and secondary allocations. The two tracks' tables describe the same twenty weeks, not forty weeks. The central course calendar controls reserved remediation and defense weeks. Repeated lab runs and questions are practice inside [G2's six bundles](../../assessments/gates.md), not extra mandatory assessments.

The CPU sandbox can establish real API/controller/scheduler behavior at its recorded topology. It cannot establish GPU isolation, NCCL performance, physical rack recovery, or a production security boundary. Those need the explicitly bounded extensions described in months 9-11.
