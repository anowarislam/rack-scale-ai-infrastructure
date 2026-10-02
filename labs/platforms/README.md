# Platform labs: evidence before claims

Read [month 7](../../curriculum/07-workload-contract.md) and the [Kubernetes](../../tracks/kubernetes/README.md) or [Slurm](../../tracks/slurm/README.md) lesson before the corresponding lab. The theory explains why each state matters. These labs supply observable healthy, broken, and recovered states.

| Route | Executes now with | Establishes | Does not establish |
|---|---|---|---|
| [L0](l0/queue_recovery.py) | Python 3.9+ standard library | Transparent placement reasoning, checkpoint integrity, process recovery | Native scheduler behavior, GPUs, HA, RDMA |
| [Kubernetes](kubernetes/README.md) | Docker, checksum-verified local kind/kubectl, image access | Real Pod/Job/RBAC/placement/retry behavior in a disposable CPU cluster | GPU isolation, physical topology, production security, storage disaster recovery |
| [Slurm](slurm/runbook.md) | Dedicated Linux VM, compiled pinned Slurm, MUNGE | Real allocations, steps, queueing, explicit requeue, completion evidence | Database history when SlurmDBD is absent, cgroup isolation when disabled, HA from one host |

No lab targets the user's current Kubernetes context or a shared Slurm cluster. Do not replace the provided guards with broad deletion commands. Runtime validation status and exact author-environment limitations are in [VALIDATION.md](VALIDATION.md).

## Laptop path

From repository root:

```sh
python3 -m unittest discover -s labs/platforms/l0 -p 'test_*.py' -v
python3 labs/platforms/l0/queue_recovery.py --output .cache/platform-evidence/placement.json
python3 labs/platforms/workload.py --directory .cache/platform-evidence/restart --steps 12 --fail-after 5
# The previous command deliberately exits 75. The next command is a new process.
python3 labs/platforms/workload.py --directory .cache/platform-evidence/restart --steps 12
```

Expected placement: same-domain healthy ADMITTED, fragmented same-domain PENDING, relaxed-domain ADMITTED across `a` and `b`. Expected recovery: step 5/total 55 before failure, resume from 5, step 12/total 650 after recovery. These are deterministic assertions, not timing benchmarks.

Use a new output directory for a fresh run. Retain failed checkpoints for inspection. The code rejects inconsistent arithmetic and changed target identity. It assumes a single writer and does not prove distributed checkpoint consistency or crash durability after power loss.

For each run use [the evidence template](../../assessments/evidence-template.md). Include command, working directory, code revision or content hashes, environment, time, observed output, invariant, deviations, and claim ceiling. Author tests are verification of course artifacts; they do not pass a learner's G2 outcome.
