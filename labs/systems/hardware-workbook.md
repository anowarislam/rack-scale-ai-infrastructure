# Hardware workbook: turn L0 reasoning into bounded physical evidence

This workbook defines concrete L1 observation and workload procedures, followed by L2/RDMA/L3 escalation boundaries. Its commands were checked against the cited official documentation. The authoring environment did not have PyTorch or an NVIDIA GPU available for execution: **L1/L2/L3 procedures are NOT_RUN here**. Record your own outputs rather than copying expected patterns as evidence.

## Before using a device

The target is an owner-approved Linux host with one allocated NVIDIA GPU, a supported installed driver, and an already installed compatible CUDA-enabled PyTorch environment. Python 3.11 or newer is the course baseline. PyTorch APIs used by the tiny workload were checked against 2.8 documentation; that is an API reference scope, not a claim that 2.8 is the right supported deployment for every device in October 2026.

Record host/device identity, the owner's allocation, maintenance conditions, expected co-tenants, software versions, and an allowed workload duration. The workload uses four data points and a one-input/one-output linear layer, with at most 200 updates. It is bounded correctness work, not stress qualification. The operator must still check the allocation before running it. If the device is shared, select the assigned GPU through the owner's supported allocation mechanism; do not assume device index 0 is your physical allocation.

Do not install packages, change drivers, reboot, reset a GPU/BMC, change clocks or power caps, enable MIG, flash firmware, modify a switch, or remove cables as part of this workbook. If prerequisites are missing, retain the L0 results and record what is missing. A lab's physical fidelity does not grant change authority.

## L1-A: capture a read-only baseline

Run from the repository root on the allocated host. Save outputs in a new `learner-work/` attempt folder or your approved evidence store. Preserve units, command, exit code, and UTC time. Keep identifiers private if the environment requires that.

```bash
python3 --version
python3 -c 'import platform; print(platform.platform())'
nvidia-smi --version
nvidia-smi -L
nvidia-smi --help-query-gpu
nvidia-smi --query-gpu=uuid,pci.bus_id,name,memory.total,memory.used --format=csv
nvidia-smi -q -d MEMORY,ECC,POWER,TEMPERATURE,PERFORMANCE
nvidia-smi topo -m
```

These are query forms from the [NVIDIA SMI reference](https://docs.nvidia.com/deploy/nvidia-smi/index.html). Check the installed help when a field is unsupported. Preserve `N/A` as unsupported/unavailable rather than converting it to zero. `topo -m` can have limited information on a single-GPU or virtualized system; that is a boundary, not a reason to invent topology.

Identify the same GPU by UUID and PCI address across outputs. Interpret the displayed CUDA/UMD capability separately from the application's build. Collect the latter explicitly:

```bash
python3 - <<'PY'
import torch
print("torch", torch.__version__)
print("build CUDA", torch.version.cuda)
print("CUDA available", torch.cuda.is_available())
print("visible device count", torch.cuda.device_count())
if torch.cuda.is_available():
    print("allocated logical device 0", torch.cuda.get_device_name(0))
PY
```

A missing import or unavailable CUDA is a failed prerequisite, not a passed workload. Consult the exact installed stack's [driver installation guidance](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/index.html) and [compatibility requirements](https://docs.nvidia.com/deploy/cuda-compatibility/latest/why-cuda-compatibility.html) with the owner. This workbook does not automatically repair that environment.

For a Linux PCI view, read only the attributes associated with the observed GPU address. Do not write to `/sys`, whose device controls can change or remove devices. The [kernel PCI sysfs guide](https://docs.kernel.org/PCI/sysfs-pci.html) documents this distinction. A recorded BDF is a current location; it is not a substitute for asset identity.

If authorized kernel logs are available, search the relevant interval for exact `NVRM: Xid` messages and preserve surrounding context. NVIDIA's [Xid guide](https://docs.nvidia.com/deploy/xid-errors/latest/working-with-xid-errors.html) describes those messages. If access is denied, mark kernel-log coverage unavailable. Do not request elevated privileges merely to make a workbook checklist green.

## L1-B: execute and verify a tiny GPU workload

First run the standard-library reference on the same host:

```bash
python3 labs/systems/training.py --output learner-work/systems/l1-reference
```

Then run the allocated CUDA device:

```bash
python3 labs/systems/training.py --backend cuda --output learner-work/systems/l1-baseline
```

The CUDA path refuses to silently fall back to CPU. Expect `L1_CUDA_OBSERVATION`, `COMPLETE`, 40 completed steps, finite predictions, and `within_tolerance: true`. Compare its four predictions to targets `[-1, 0, 2, 3]`, and to the reference. The supplied maximum absolute error tolerance is 0.1; record actual differences. If output is non-finite or outside tolerance, retain the failure and investigate rather than increasing tolerance without a reason.

The implementation uses a float64 `Linear(1,1)` model, plain SGD with learning rate 0.1 and no momentum, and mean squared error. Relevant official APIs are [Linear](https://docs.pytorch.org/docs/2.8/generated/torch.nn.Linear.html), [SGD](https://docs.pytorch.org/docs/2.8/generated/torch.optim.SGD.html), and [MSE loss](https://docs.pytorch.org/docs/2.8/generated/torch.nn.functional.mse_loss.html). It synchronizes before collecting parameters. Elapsed time includes repeated synchronization and checkpoint I/O, so it is not a measure of GPU peak throughput. See [CUDA timing semantics](https://docs.pytorch.org/docs/2.8/notes/cuda.html).

Repeat the read-only GPU queries after the workload. A short workload may finish between telemetry samples; absence of a visible utilization peak does not negate its actual device execution, and a peak would not prove numerical correctness. Use application output plus allocation identity, rather than one utilization graph.

**Stop conditions:** unexpected loss of device visibility, workload error, non-finite results, owner-reported service impact, or an existing site-defined power/thermal alarm. Stop this application and preserve evidence. Do not improvise resets or cooling changes. There is no universal temperature threshold in this workbook.

## L1-C: interrupt, recover, and verify meaning

```bash
python3 labs/systems/training.py --backend cuda --output learner-work/systems/l1-recovery --interrupt-at 23
python3 labs/systems/training.py --backend cuda --output learner-work/systems/l1-recovery --resume
```

The first command intentionally exits 3 after the controlled application stop. Record completed step 23 and committed step 20. The second should resume at 20 and finish at 40. Compare its final parameters and predictions to the uninterrupted CUDA baseline. Record actual differences, software versions, dataset hash, and checkpoint hash. The same program does not establish bitwise reproducibility across hardware or versions; [PyTorch's reproducibility notes](https://docs.pytorch.org/docs/2.8/notes/randomness.html) explain that limit.

This is application-level failure and recovery on a GPU host. It does not establish recovery from power loss, a GPU reset, a driver crash, filesystem corruption, or loss of an entire node. Those need their own authorized and validated experiments.

For G1-O06 submit baseline CUDA correctness. For G1-O12 submit interruption/recovery comparison and a system path that names process, allocation, device, checkpoint storage, and telemetry. Attach these to the existing monthly bundles; do not fabricate a passed outcome if hardware access remains unavailable.

## L1-D: optional management-plane observation

If the owner provides a read-only Redfish role and an approved authenticated client, begin with `GET /redfish/v1/` and follow the returned links to the relevant Systems, Chassis, and Managers resources. Record HTTP status, service identity, resource IDs, source times, and returned hardware identity. Do not assume a hardcoded member such as `Systems/1` exists. Compare management identity with the host inventory.

Redfish defines `GET` as read-only; actions and writes are separate operations. Use the exact implementation's documentation and the [Redfish 1.22.0 specification](https://www.dmtf.org/sites/default/files/standards/documents/DSP0266_1.22.0.html). Preserve TLS certificate verification and use the site's credential mechanism. Do not paste tokens into learner evidence. A BMC read cannot certify all host behavior, just as a working host process cannot certify the BMC recovery path.

## Escalation boundaries

| Level and proposed work | What must already be established | Acceptable evidence | What remains out of scope |
|---|---|---|---|
| L1 passive DCGM observations | Owner-approved deployed DCGM and understood field meanings | Current device/field data with missing/unsupported fields retained | Running diagnostics by calling them passive reads |
| L1 DCGM diagnostic window | Allocated compatible device, owner-reviewed mode, resource impact, stop conditions | Exact mode, version, complete result, workload/control comparison | Treating one diagnostic PASS as whole-hardware qualification |
| L2 two or more GPU nodes | Separate allocation, topology, identities, compatible runtime, bounded workload and recovery plan | Per-rank output, correctness, transport, synchronized timing context | Claiming one host demonstrates multi-node behavior |
| L2 physical RDMA | Actual RDMA NICs/fabric, owner-approved addressing/configuration, known selected transport, vendor-supported checks | Observed RDMA path, per-port/link evidence, bounded correctness/bandwidth test | Inferring RDMA from a passing TCP connection or simulator |
| L3 rack observation/service | Facility and product procedure, qualified supervisor, explicit task authorization, stop-work authority | Signed/supervised observations for the specific work performed | Unsupervised electrical work, firmware writes, cooling changes, physical repair claims from L0 |

DCGM's [diagnostic guide](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html) describes modes and prerequisites; a diagnostic may perform active work. Do not launch it on an occupied device just because a command is easy to copy. The present version also describes a single-node NCCL test plugin; its success does not prove multi-node fabric behavior.

For an approved L2 communication exercise, the [official NCCL tests repository](https://github.com/NVIDIA/nccl-tests) documents test arguments and multi-process use. An already built `all_reduce_perf` can be scoped to small message sizes and iterations according to its installed help, then launched through the environment's approved scheduler or MPI mechanism. This workbook intentionally does not provide a universal multi-node launch command: rank allocation, device mapping, network selection, security, and available process managers are not known here. Those are concrete missing prerequisites to resolve with the L2 owner, not a reason to guess a launcher.

Before any physical RDMA claim, use the [DOCA RDMA guide](https://networking-docs.nvidia.com/doca/archive/3-5-0/rdma-aware-networks-programming-guide) for concepts and the exact NIC/switch software documentation for operations. The [NCCL networking guide](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/networking_troubleshooting.html) distinguishes low-level tests from application tuning. Record negative results as well as successes. Neither this workbook nor an official example supersedes owner allocation or product/facility safety procedures.

## Evidence and limits

Your packet needs original commands/output, UTC time and clock context, physical and logical identity, software versions, workload input/hash, baseline, failed/stop result, recovery, correctness comparison, and a statement of what was not tested. Use [the shared evidence template](../../assessments/evidence-template.md).

The author verified documentation and L0 behavior. No physical GPU, NCCL, RDMA, BMC, DCGM, power, thermal, or rack-service result is supplied as if observed. If your evidence covers one tiny workload on one device, claim exactly that; it is a useful completed result within its boundary.
