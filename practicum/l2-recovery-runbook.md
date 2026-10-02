# L2 extension: recover two replicated CPU tasks on two hosts

This is the executable advanced route for [Month 21](21-recovery.md), and a software readiness workload for [Month 22](22-rack-readiness.md). Native two-host execution is **NOT_RUN** in the course build. Local unit checks validate the recorder and arithmetic only.

Use the Slurm Run/compare skills already taught to both primary-platform routes. Kubernetes-primary learners do not need to build a second platform: an environment owner must provide this ready two-host Slurm environment. The supplied single-VM Slurm lab, one-worker Kubernetes lab, or two container workers on one laptop do not satisfy this L2 route.

## What the workload proves

Two replicated independent tasks each compute the sum of squares from 1 to 100. There is no communication between tasks. A supervisor accepts the run only when both logical task results are present and correct. A logical task is identified by its rank, 0 or 1; an attempt is one execution of that task. These are different units of counting.

For one task, `100*101*201/6 = 338350`. The two-result aggregate is `676700`. During the fault run, task 0 completes while task 1 exits after committing step 20, whose total is `20*21*41/6 = 2870`. That checkpoint is progress, not a final result. On recovery, task 0 resumes at 100 without repeating its loop; task 1 resumes at 20 and computes steps 21 through 100. The supervisor counts one current result per rank, not all success messages across attempts.

The built-in fault is an ordinary process exit with status 75 after a completed checkpoint write. It demonstrates application-state recovery after a process failure. It does not demonstrate behavior during a partial write, a power loss, storage corruption, host loss, partition, or concurrent duplicate writers. It is not distributed training, a collective, or RDMA. The two-host requirement proves actual placement and participation, not communication performance or independent physical failure domains beyond the owner's recorded topology.

## Required environment and stop conditions

Before running, record all of these in the evidence template:

- Two **independently provisioned Linux compute hosts**, their Slurm node names, host identities, and physical or VM topology. Two aliases for one OS instance are insufficient. If they are VMs, record their underlying placement and do not infer physical independence.
- A named owner, two booked hosts, a dedicated or owner-approved isolated CPU partition, an approved account, a recovery owner, and a three-minute job limit. The exercise requests one CPU and 128 MiB per host. The owner confirms that this scope cannot displace or disturb unrelated work.
- Operational Slurm submission and job accounting. Record client/controller/daemon versions; the course reference is 25.05.3. The owner checks equivalent options against the installed version if it differs. No installation, daemon reconfiguration, privilege escalation, or physical operation is part of this procedure.
- Python 3.11 or newer on each host. The course files and one new writable exercise directory are visible at the **same absolute paths** from the submit host and both compute hosts, using an owner-supported shared filesystem and the same effective user identity. The owner confirms ordinary file visibility and atomic directory creation/rename semantics needed by the exercise. Record this storage dependency; the run does not qualify its failure behavior.
- Permission for the built-in process exit only. Stop on an unexpected host, unrelated workload impact, missing native accounting, malformed checkpoint, loss of observation, stalled I/O, unexpected exit, or an existing writer marker. Do not clear a marker while a prior process might remain alive.

The [version-pinned Slurm 25.05.3 srun manual](https://raw.githubusercontent.com/SchedMD/slurm/slurm-25-05-3-1/doc/man/man1/srun.1) defines exact node/task counts, per-node task limits, failure handling, and task exit propagation. This run uses two nodes and two tasks, at most one task per node. `--kill-on-bad-exit=0` lets the other task finish; `--wait=0` avoids a short site wait setting terminating it after the first task exits. `srun` returns the highest task exit code for this ordinary synchronous run. These are command semantics, not evidence that the local cluster enforces the intended isolation.

## 1. Freeze paths and establish the baseline

Run from the authorized submit host, outside any existing Slurm allocation. Replace the example values with the owner-approved values; do not use the example hosts as targets. The environment must already be configured to contact the approved cluster. Use a shell without `errexit` for the expected status-75 exercise, and preserve every exit code.

```sh
export L2_COURSE=/shared/your-user/rack-scale-ai-infrastructure-course
export L2_ROOT=/shared/your-user/course-l2-unique-run-001
export L2_PARTITION=approved_cpu_partition
export L2_NODES=approved_host_a,approved_host_b
export L2_ACCOUNT=approved_account
L2_READY=
setup_l2() {
    L2_READY=
    test -z "${SLURM_JOB_ID:-}" || return 1
    test -f "$L2_COURSE/labs/platforms/workload.py" || return 1
    test ! -e "$L2_ROOT" || return 1
    mkdir -m 700 "$L2_ROOT" || return 1
    mkdir "$L2_ROOT/control" "$L2_ROOT/failure" "$L2_ROOT/reset" || return 1
    srun --version > "$L2_ROOT/client-version.txt" || return 1
    scontrol show config > "$L2_ROOT/cluster-config.txt" || return 1
    scontrol show nodes "$L2_NODES" > "$L2_ROOT/nodes-before.txt" || return 1
    : > "$L2_ROOT/.setup-complete" || return 1
    L2_READY="$L2_COURSE|$L2_ROOT|$L2_PARTITION|$L2_NODES|$L2_ACCOUNT"
}
setup_l2
```

Setup returns nonzero at the first failed prerequisite or write and leaves submission disabled. Preserve any partially created directory and diagnose the failure; use a new unique directory for a fresh attempt. Keep configuration evidence private to the authorized reviewers. Inspect the cluster identity, partition, host inventory, versions, and sharing policy with the owner before submitting. An existing directory is evidence, not a place to start a fresh baseline.

Define this small submission function in that shell. It writes only inside your new exercise directory and submits only the named CPU workload. The Python recorder invokes the existing checkpoint application and records Slurm job ID, node name, hostname, application progress, and exit code for each rank.

```sh
launch_l2() {
    test "$#" -eq 2 || return 2
    local l2_phase="$1" l2_case="$2" l2_exit
    test "${L2_READY:-}" = "$L2_COURSE|$L2_ROOT|$L2_PARTITION|$L2_NODES|$L2_ACCOUNT" || return 2
    test -f "$L2_ROOT/.setup-complete" || return 2
    case "$l2_phase:$l2_case" in
        baseline:control|fault:failure|recovery:failure|reset:reset) ;;
        *) return 2 ;;
    esac
    test -d "$L2_ROOT/$l2_case" && test ! -L "$L2_ROOT/$l2_case" || return 2
    mkdir "$L2_ROOT/$l2_case/.launch-$l2_phase" || return 2
    date -u '+%Y-%m-%dT%H:%M:%SZ' > "$L2_ROOT/$l2_case/$l2_phase-client-start.txt" || return 2
    srun --partition="$L2_PARTITION" --account="$L2_ACCOUNT" \
      --nodelist="$L2_NODES" --nodes=2 --ntasks=2 --ntasks-per-node=1 \
      --cpus-per-task=1 --mem=128M --time=00:03:00 --immediate=30 \
      --kill-on-bad-exit=0 --wait=0 --label \
      --job-name="course-l2-$l2_phase" \
      python3 "$L2_COURSE/practicum/l2_batch.py" worker \
      --directory "$L2_ROOT/$l2_case" --phase "$l2_phase" \
      > "$L2_ROOT/$l2_case/$l2_phase-native.log" 2>&1
    l2_exit=$?
    printf '%s\n' "$l2_exit" > "$L2_ROOT/$l2_case/$l2_phase-exit.txt" || return 2
    date -u '+%Y-%m-%dT%H:%M:%SZ' > "$L2_ROOT/$l2_case/$l2_phase-client-end.txt" || return 2
    return "$l2_exit"
}
launch_l2 baseline control
python3 "$L2_COURSE/practicum/l2_batch.py" check \
  --directory "$L2_ROOT/control" --expected baseline
```

Expected submission exit: 0. Expected checker: two complete logical tasks, aggregate 676700, two distinct node names and hostnames. Inspect both attempt JSON files and application logs; compare their node identities to the owner's inventory. Save native accounting for the job ID in those records:

```sh
L2_JOB=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["job_id"])' \
  "$L2_ROOT/control/rank-0/attempt-baseline.json")
sacct -j "$L2_JOB" --format=JobIDRaw,JobName,State,ExitCode,NodeList --parsable2 \
  > "$L2_ROOT/control/baseline-accounting.txt"
```

If accounting has not arrived, wait within the approved window and collect it again; absence is not a successful native check. Inspect step/task records as well as the allocation record. Before proceeding, predict the fault-run checkpoint, missing result, task exit codes, and allocation result.

## 2. Observe the bounded failure

```sh
launch_l2 fault failure
python3 "$L2_COURSE/practicum/l2_batch.py" check \
  --directory "$L2_ROOT/failure" --expected fault
```

Expected submission exit: 75; expected checker exit: 0 because it verifies the **expected failed state**, not a successful workload. Its aggregate 338350 contains only the completed task. Task 1 has a valid step-20 checkpoint and no final result. Preserve `fault-native.log`, `fault-exit.txt`, each attempt record and log, and copies of both checkpoint files before recovery overwrites current progress:

```sh
cp "$L2_ROOT/failure/rank-0/checkpoint.json" "$L2_ROOT/failure/rank-0/checkpoint-at-fault.json"
cp "$L2_ROOT/failure/rank-1/checkpoint.json" "$L2_ROOT/failure/rank-1/checkpoint-at-fault.json"
```

Save the fault job's native accounting using the same command as above with `failure/rank-0/attempt-fault.json`. Execute each named phase only once in a run directory; a new independent attempt uses a new directory. Do not overwrite earlier native logs by repeating a phase.

Do not resubmit yet if `srun` has not returned, the native job is not terminal, an application child might still run, or a `.writer` directory remains. The recorder releases that marker only after reaping the child; an abnormal recorder failure deliberately leaves it for investigation. Directory creation is a bounded exclusion guard, not a distributed lease service or automatic stale-lock recovery.

Write the recovery decision: committed state is intact; both attempts have ended; one task needs remaining computation; resubmission will reuse the same logical task directories. Explain why deleting task 1's directory would change the experiment into a from-scratch restart.

## 3. Recover and verify hidden state

```sh
launch_l2 recovery failure
python3 "$L2_COURSE/practicum/l2_batch.py" check \
  --directory "$L2_ROOT/failure" --expected recovery
```

Expected submission exit: 0. Inspect recovery `resumed_from` values of 100 and 20, completed values of 100, distinct hosts, preserved failed-attempt records, and one canonical `result.json` per rank. The checker must report aggregate 676700. It does not add task 0's earlier and later success messages; doing so would incorrectly produce three logical results.

Save native accounting for the recovery job. Compare actual application duration, client submission-to-return interval, and native scheduling times separately. Host wall clocks must be evaluated before cross-host subtraction; the recorder's per-process duration uses a monotonic clock. This workload's delay is artificial, so durations are exercise observations rather than a hardware benchmark.

Check hidden health: current host/boot identity and observation delivery using the owner's read-only monitoring; job terminal state; absence of active exercise writers; valid checkpoint arithmetic; preserved original fault; no unrelated job changes. An available host or zero allocation exit alone does not establish these conditions.

## 4. Reset and hand back the environment

```sh
launch_l2 reset reset
python3 "$L2_COURSE/practicum/l2_batch.py" check \
  --directory "$L2_ROOT/reset" --expected reset
scontrol show nodes "$L2_NODES" > "$L2_ROOT/nodes-after.txt"
```

The fresh reset case must start both tasks from 0 and match the baseline. Save its accounting, verify every exercise job is terminal, compare before/after node state with the owner, and archive evidence before deleting anything. Remove only the approved run directory after evidence retention is satisfied; no daemon, partition, host, or firmware state was changed by this procedure.

For an abort, stop new submissions. If an exercise job is still running, the owner may use `scancel` with its **recorded exact job ID**, then verify termination and retained state. Never cancel all jobs for a user or partition. Hand the state and reason to the recovery owner; do not remove writer markers or checkpoints to make a check pass.

Submit the authorization/topology record, four cases' native logs and accounting, original fault checkpoints, per-rank application/attempt records, aggregate checks, clock limitations, reset result, and a claim boundary. A local replay with invented Slurm environment variables is labeled **L0 recorder testing**. Only observed participation by the two provisioned hosts with native evidence supports this L2 CPU batch recovery claim.
