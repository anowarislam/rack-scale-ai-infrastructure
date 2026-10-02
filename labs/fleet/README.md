# Laptop fleet exercises

These are synthetic L0 exercises for [months 13-18](../../curriculum/13-fleet-truth.md) and the [practicum](../../practicum/README.md). Python 3.11 or later is sufficient; only the standard library is used. The program reads local JSON and makes no network or infrastructure calls. It writes only the explicitly requested output file, if one is supplied.

## Run and interpret

Run from the repository root:

```sh
python3 labs/fleet/fleet_lab.py signal labs/fleet/fixtures/signal-fault.json
python3 labs/fleet/fleet_lab.py reliability labs/fleet/fixtures/reliability.json
python3 labs/fleet/fleet_lab.py lifecycle labs/fleet/fixtures/lifecycle-fault.json
python3 labs/fleet/fleet_lab.py capacity labs/fleet/fixtures/capacity-fault.json
python3 -m unittest discover -s labs/fleet -p 'test_*.py' -v
```

The command shape is `python3 labs/fleet/fleet_lab.py SUBCOMMAND INPUT.json [--output OUTPUT.json]`. Exit 0 means the specific evaluator's PASS condition holds. Exit 1 means FAIL or BLOCKED as described below; the three supplied fault commands intentionally return 1. Exit 2 means invalid input or command usage. An expected exit 1 is exercise evidence, not a failed installation.

| Subcommand | What PASS means | What PASS does not mean |
|---|---|---|
| `signal` | Every expected synthetic identity is represented; units, incarnation, order, and freshness checks pass | Temperatures are safe, the observed machine is healthy, or physical identity was inspected |
| `reliability` | Calculations completed on valid inputs | A cohort is reliable or statistical assumptions hold; preserve warnings |
| `lifecycle` | Final state and generation match `expected_final` | All submitted requests were accepted; inspect rejected-request history |
| `capacity` | Declared demand fits normal and every single-domain-loss count scenario with the declared headroom | Topology, memory, service latency, or two-domain failures are safe |

## The learner's task is to change and explain

Do not submit the reference healthy outputs as your own work. Copy a fault fixture to a learner-owned path. Predict its result, run it, diagnose the specific failed invariant, then create a new observation or event sequence that represents recovery. Keep the original. Re-run and explain the result. Finally reintroduce a different fault and demonstrate detection.

Reference controls are `signal-healthy.json`, `signal-clock-corrected.json`, `lifecycle-healthy.json`, and `capacity-recovered.json`. `lifecycle-contention.json` is expected to PASS even though its event history contains rejected stale and conflicting requests; those rejections are the protection being tested. Reference recovered paths exist for self-study comparison after an attempt.

## Input semantics

Every file must declare `synthetic: true`. Times in the signal fixture are artificial seconds in one scenario, not real UTC timestamps. The source offset is source clock minus reference clock. `clock_uncertainty_s` defines the possible error around the corrected event time; the validator uses the oldest plausible event for freshness. It checks every supplied reading; feed it an intended current observation batch, not a full historical archive.

Reliability observations contain one aggregate row per asset per cohort: observed operating exposure, nonnegative event count, and termination reason. Exposure is supplied by the learner's ledger; the calculator cannot detect overlapping or falsely included hours from aggregate rows. A `lost_observation` reason emits a warning about potentially informative censoring. The model is a fixed-exposure homogeneous Poisson count model. Exact interval calculations are conditional on that model; they are not a goodness-of-fit test.

Lifecycle events are ordered deliveries. `expected_generation` is checked against current state; applied IDs are remembered for that process invocation. The same applied ID with identical content is a duplicate; changed content is a conflict. Rejected IDs are not persisted, and there is no disk-backed transaction, authentication, live admission check, or external side effect. Qualification check values are synthetic assertions, not real probes. The exercise asks you to identify these gaps.

Capacity inputs are homogeneous GPUs in named failure domains, a demand divisible by the job gang size, and post-failure headroom fraction. The program reserves headroom after each modeled loss and rounds admission down to whole jobs. It assumes surviving resources can be pooled for this workload; the learner must test that assumption separately.

## Reset and abort

Each invocation starts from the input file and keeps no persistent service state. Reset by using a fresh learner copy of the reference fixture. Preserve evidence you intend to submit. Abort a run if you discover real credentials or asset identifiers in a file and replace it with synthetic/redacted data before continuing. No exercise requires administrator permissions, a cloud account, firmware access, or a production context.
