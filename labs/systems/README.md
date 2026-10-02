# Systems labs: make a prediction, change one thing, verify

These are deterministic teaching models plus a tiny training/recovery workload. Every fixture value is synthetic. They do not contact hardware, a network, or a remote service. The optional CUDA backend in `training.py` is the sole exception: selecting it explicitly runs a small workload on an already available GPU. Read [the hardware workbook](hardware-workbook.md) first.

Python 3.11 or newer is the baseline; the author tested Python 3.11.11. L0 uses only the standard library. No install command is necessary. Run commands from the repository root. Scenario writes are restricted to a child of this repository's `learner-work/`; fixtures are never modified. The tools are for one learner process at a time, not concurrent writers or hostile shared workspaces.

## The learning loop

1. Read the associated chapter and predict the initial outcome.
2. Initialize a broken case and inspect observations before checking the answer.
3. Capture the failed check. A failure is expected evidence, not a reason to suppress output.
4. Write competing hypotheses and choose a discriminating change.
5. Configure one allowed input, observe again, and check its consequences.
6. Compare with a separately initialized healthy control.
7. Reset the broken attempt and reproduce the original result.
8. Submit your own output and explanation. A supplied answer key is not your evidence.

All six scenarios fit the single assessed bundle in their chapter. The training exercise is reused in G1-E04 and G1-E06, not counted as a seventh G1 assessment.

| Scenario | Chapter/bundle | Allowed inputs | Main question |
|---|---|---|---|
| `domains` | 01 / G1-E01 | `secondary` | Does any serving replica survive this feed loss? |
| `inventory` | 02 / G1-E02 | `recorded_serial`, `cpu_numa` | Do identity and locality need separate fixes? |
| `gpu` | 03 / G1-E03 | `microbatch` | Does memory demand fit the reserved budget? |
| `fabric` | 04 / G1-E04 | `rank2_count`, `resume_step` | Are the collective and checkpoint both valid? |
| `telemetry` | 05 / G1-E05 | `collector`, `source_offset_s`, `role` | Are observations fresh, plausible, and appropriately scoped? |
| `workload` | 06 / G1-E06 | `arrivals_per_s` | Does useful completion survive offered load? |

## Exact CLI workflow

```bash
python3 labs/systems/lab.py list
python3 labs/systems/lab.py init gpu --workspace learner-work/systems/gpu-attempt
python3 labs/systems/lab.py observe --workspace learner-work/systems/gpu-attempt
python3 labs/systems/lab.py check --workspace learner-work/systems/gpu-attempt
```

`observe` shows the facts, allowed controls, current configuration, and derived measurements. `check` adds invariant results. It exits 1 for the expected initial failure; do not run this line under a shell policy that aborts your whole notebook before you capture it. Exit 0 means all modeled checks passed. Exit 2 means invalid input, an unavailable file, a boundary violation, or incompatible fixture/schema state.

Change a number using a JSON number:

```bash
python3 labs/systems/lab.py configure --workspace learner-work/systems/gpu-attempt --key microbatch --value 4
python3 labs/systems/lab.py check --workspace learner-work/systems/gpu-attempt
```

String values require JSON quotes inside shell quotes. For example, after initializing a domains case, the syntax for a candidate placement is:

```bash
python3 labs/systems/lab.py configure --workspace learner-work/systems/domains-attempt --key secondary --value '"node-c"'
```

Create and inspect a separate control:

```bash
python3 labs/systems/lab.py init gpu --control healthy --workspace learner-work/systems/gpu-control
python3 labs/systems/lab.py check --workspace learner-work/systems/gpu-control
python3 labs/systems/lab.py reset --workspace learner-work/systems/gpu-attempt
python3 labs/systems/lab.py check --workspace learner-work/systems/gpu-attempt
```

The control should pass; reset should restore the original failure. Reset changes only `state.json` and appends an action to `history.jsonl`. It preserves your notes and captured outputs. Init refuses a non-empty directory. A source-fixture digest in `.systems-lab.json` prevents silently evaluating an old attempt against changed fixtures; after a course update, retain the old attempt and initialize a new one.

To save output, redirect it into your initialized attempt directory using a new filename:

```bash
python3 labs/systems/lab.py observe --workspace learner-work/systems/gpu-attempt > learner-work/systems/gpu-attempt/observation-before.json
```

Record the exit code in your notes immediately when a command fails. Output is deterministic for the same fixture and configuration. Real collection times belong in your evidence record; the fixture's synthetic timestamps must not be reported as real observation times.

## Local training and real checkpoint files

The training workload fits `y = weight*x + bias` to four known points with full-batch SGD. It writes a checkpoint every ten steps and a manifest naming the last complete checkpoint. It does not download data. The reference backend is ordinary Python arithmetic; it is labeled `L0_REFERENCE`, even though its files and process are real.

Run an uninterrupted baseline, saving stdout outside the initially empty output directory:

```bash
python3 labs/systems/training.py --output learner-work/systems/train-baseline
python3 labs/systems/training.py --output learner-work/systems/train-recovery --interrupt-at 23
```

The second command intentionally exits 3 and reports `INTERRUPTED`, `completed_step: 23`, `checkpoint_step: 20`, and `uncommitted_steps: 3`. This is a controlled application stop, not a GPU reset, machine crash, or power failure.

```bash
python3 labs/systems/training.py --output learner-work/systems/train-recovery --resume
```

Expected: `COMPLETE`, `start_step: 20`, `completed_step: 40`, and `within_tolerance: true`. Compare `weight`, `bias`, and `predictions` with the uninterrupted baseline. In the same Python environment these should match exactly. `within_tolerance` means all four predictions are within 0.1 of their known targets; it is not a model-quality or generalization score.

Inspect `manifest.json` and the referenced payload. It contains dataset identity, learning rate, backend, and progress. Explain why files for unreferenced generations do not supersede the manifest. Then deliberately corrupt a separate disposable case:

```bash
python3 labs/systems/training.py --output learner-work/systems/train-corrupt --interrupt-at 23
python3 - <<'PY'
from pathlib import Path
p = Path("learner-work/systems/train-corrupt/checkpoint-0020.json")
p.write_text('{}\n', encoding="ascii")
PY
python3 labs/systems/training.py --output learner-work/systems/train-corrupt --resume
```

Expected: exit 2 and `checkpoint checksum mismatch`. Do not repair this by editing the hash to match damaged data. The checksum is useful only if metadata remains trustworthy. Preserve the failed case, then create a new attempt to recover from a valid checkpoint. No recursive cleanup command is supplied; outputs are tiny and retaining failed evidence is valuable.

Publication uses local temporary files, `fsync` on file content, and `os.replace` for the manifest. This does not validate directory fsync, physical power-loss durability, network-filesystem semantics, multiprocess coordination, or object-store publication. The tests establish process-interruption behavior in the local model only.

## Review expectations and solution boundary

Machine checks reject invalid types, out-of-range controls, incomplete state, and failed model invariants. They do not grade causal explanations or demonstrate that a chosen input was supported by evidence. For example, several clock offsets can satisfy a broad plausibility range; only the measured offset is justified by the fixture. A reviewer must inspect the reasoning as well as PASS.

<details>
<summary>Recovery key: use after your independent attempt</summary>

| Scenario | One supported recovery | Initial failure preserved by reset |
|---|---|---|
| domains | `secondary = "node-c"` | zero survivors after `feed-a` loss |
| inventory | `recorded_serial = "SN-2302"`, `cpu_numa = 1` | identity mismatch and remote modeled path |
| gpu | `microbatch = 4` (1 through 7 fit) | memory estimate exceeds reserved budget |
| fabric | `rank2_count = 1024`, `resume_step = 100` | mismatched collective and unpublished partial checkpoint |
| telemetry | `collector = "live"`, `source_offset_s = 12`, `role = "telemetry-reader"` | stale observation, implausible time, excessive role |
| workload | `arrivals_per_s = 4` | p99 7,000 ms and low deadline-qualified goodput |

Changing a control is not an observation of real infrastructure. A passing model does not establish physical capacity, RDMA, GPU health, or a production-safe change.

</details>

## Maintainer verification

```bash
python3 -m unittest discover -s labs/systems -p 'test_*.py' -v
```

The suite covers broken/healthy states, partial fixes, boundary memory values, queue measurements, type validation, reset preservation, path protection, fixture drift, corrupt checkpoints, ignored unpublished generations, and resumed/uninterrupted equivalence. It does not execute the optional CUDA backend. Refer to the repository's current validation record for actual execution results; running these tests does not complete a learner gate.
