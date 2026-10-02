# Slurm CPU reference on one dedicated Linux VM

This is a real Slurm setup procedure and real batch scripts, not a Slurm emulator. It was **NOT_RUN** on the author's macOS environment, where Slurm executables were absent. The shared Python application was tested locally. Use the [theory track](../../../tracks/slurm/README.md) to understand the mechanisms before executing these steps.

## Scope, prerequisites, and version boundary

Use a new disposable Ubuntu 24.04 LTS Linux VM with systemd, at least 2 virtual CPUs, 2 GiB RAM, 10 GiB free disk, network access, and an ordinary sudo-enabled learner account. These are course planning values, not a SchedMD support certification. Record the actual architecture, VM image/source hash, OS/kernel, package versions, and resources. CPU-only amd64/arm64 are intended; build/runtime compatibility remains unverified until the run succeeds on your recorded VM.

The VM must contain no other Slurm cluster, no production data, and no shared users. It will be renamed `course-node`; packages, a service account, configuration, and course directories will be added. A running MUNGE service will be used. Snapshot the empty VM first so disposal is the complete cleanup path. Do not run these administrator commands on the user's laptop or on a shared/login node.

Reference: Slurm **25.05.3**, official tag `slurm-25-05-3-1`, resolved commit **`1c0b066e1e0432a94b0149cf40d23b882e137942`** from [SchedMD's release](https://github.com/SchedMD/slurm/releases/tag/slurm-25-05-3-1) and [commit](https://github.com/SchedMD/slurm/commit/1c0b066e1e0432a94b0149cf40d23b882e137942). Build dependencies are resolved by the VM's package repository, so record their actual versions; the course does not claim an immutable VM/package matrix. The checked-in configuration is verified against the [25.05.3 manual](https://raw.githubusercontent.com/SchedMD/slurm/slurm-25-05-3-1/doc/man/man5/slurm.conf.5). Current online docs can describe later releases; installed matching man pages take precedence for exact options.

Copy this repository into the VM and enter its root. First inspect:

```sh
uname -a
cat /etc/os-release
id
command -v slurmctld || true
command -v slurmd || true
```

If Slurm already exists or the VM is not exclusively yours, stop and use a clean VM. Do not overwrite an existing configuration.

## Construct the reference

These steps mutate only the dedicated VM. Set its hostname and ensure `course-node` resolves locally (the loopback mapping is suitable only for this single-VM lab):

```sh
sudo hostnamectl set-hostname course-node
getent hosts course-node || printf '127.0.1.1 course-node\n' | sudo tee -a /etc/hosts
sudo mkdir -p /etc/slurm-course
printf 'dedicated-rack-course-v1\n' | sudo tee /etc/slurm-course/COURSE_SANDBOX
sudo apt-get update
sudo apt-get install -y build-essential git pkg-config munge libmunge-dev libhwloc-dev libdbus-1-dev libmariadb-dev
sudo systemctl enable --now munge
munge -n | unmunge
```

Expected MUNGE result: successful decode and the invoking UID/GID. Do not print or copy `/etc/munge/munge.key`. The package supplies its local service/key handling. If authentication fails, inspect MUNGE service status, permissions, and clock before proceeding.

Build the exact source. Use this only after reviewing the source/provenance boundary above:

```sh
mkdir -p .cache/slurm-build
git clone --depth 1 --branch slurm-25-05-3-1 https://github.com/SchedMD/slurm.git .cache/slurm-build/source
test "$(git -C .cache/slurm-build/source rev-parse HEAD)" = 1c0b066e1e0432a94b0149cf40d23b882e137942
cd .cache/slurm-build/source
./configure --prefix=/opt/slurm/25.05.3 --sysconfdir=/etc/slurm-course
make -j2
sudo make install
cd ../../..
export PATH=/opt/slurm/25.05.3/bin:/opt/slurm/25.05.3/sbin:$PATH
export SLURM_CONF=/etc/slurm-course/slurm.conf
slurmctld -V
```

Expected version: `slurm 25.05.3`. The source includes its generated configure script. Keep configure/make output and `config.log` if compilation fails; do not declare the build complete from `configure` alone. Record packages with `dpkg-query -W > .cache/slurm-build/packages.txt` and source identity with `git -C .cache/slurm-build/source rev-parse HEAD`.

Create dedicated state directories and service identity:

```sh
getent passwd slurm || sudo useradd --system --user-group --home-dir /var/lib/slurm-course --shell /usr/sbin/nologin slurm
sudo install -d -o slurm -g slurm /var/lib/slurm-course/controller /var/log/slurm-course /run/slurm-course
sudo install -d -o root -g root /var/lib/slurm-course/worker
slurmd -C > .cache/slurm-build/detected-node.txt
```

Generate a node line from detected topology, reserving 512 MiB of the reported memory for the VM. Do not copy the template's example CPU topology as if it were detected:

```sh
python3 - <<'PY'
from pathlib import Path
source = Path('labs/platforms/slurm/slurm.conf').read_text()
line = next(s for s in Path('.cache/slurm-build/detected-node.txt').read_text().splitlines() if s.startswith('NodeName='))
fields = dict(token.split('=', 1) for token in line.split() if '=' in token)
fields['NodeName'] = 'course-node'
fields['RealMemory'] = str(int(fields['RealMemory']) - 512)
assert int(fields['RealMemory']) >= 512, 'VM needs more memory'
keys = ['NodeName', 'CPUs', 'Boards', 'SocketsPerBoard', 'CoresPerSocket', 'ThreadsPerCore', 'RealMemory']
measured = ' '.join(f'{key}={fields[key]}' for key in keys) + ' State=UNKNOWN'
rendered = '\n'.join(measured if row.startswith('NodeName=') else row for row in source.splitlines()) + '\n'
Path('.cache/slurm-build/slurm.conf').write_text(rendered)
PY
sudo install -m 0644 .cache/slurm-build/slurm.conf /etc/slurm-course/slurm.conf
```

Review the rendered file. `TaskPlugin` and `JobAcctGatherType` are intentionally unset in this trusted-user learning profile. AccountingStorageType is unset. The completion plugin writes a simple record; it is not SlurmDBD.

Start the daemons in two separate terminals, each on this VM. Keep their output visible:

```sh
# Terminal A; foreground controller. It uses SlurmUser=slurm.
sudo /opt/slurm/25.05.3/sbin/slurmctld -D -f /etc/slurm-course/slurm.conf
```

```sh
# Terminal B; foreground node daemon.
sudo /opt/slurm/25.05.3/sbin/slurmd -D -f /etc/slurm-course/slurm.conf
```

In terminal C, repeat the PATH/SLURM_CONF exports. `/run/slurm-course` is volatile; recreate it with the same ownership if you reboot the VM.

## Guard every mutation and establish healthy state

Define this shell function in terminal C. It checks environment, marker, and controller identity before any job/control mutation:

```sh
course_guard() {
  test "$(hostname -s)" = course-node &&
  test "$SLURM_CONF" = /etc/slurm-course/slurm.conf &&
  test "$(cat /etc/slurm-course/COURSE_SANDBOX)" = dedicated-rack-course-v1 &&
  test "$(scontrol show config | awk '$1 == "ClusterName" {print $3}')" = rack-course
}
course_guard || { echo 'Wrong environment; stop.'; return 1 2>/dev/null || exit 1; }
scontrol ping
sinfo -N -l
scontrol show node course-node
```

Expected: controller responds and the node is IDLE after registration. If not, compare the exact registration error with measured topology, local name resolution, MUNGE decode, and state-directory permissions. Do not force the node to IDLE without fixing the reported cause.

## Scheduling, pending state, and release

Run from `labs/platforms/slurm`, because the batch script intentionally resolves the adjacent application by its submission directory:

```sh
cd labs/platforms/slurm
mkdir -p evidence
course_guard && HOLD_JOB=$(sbatch --parsable hold.sbatch)
HOLD_JOB=${HOLD_JOB%%;*}
printf '%s\n' "$HOLD_JOB" > evidence/hold-job-id.txt
squeue -j "$HOLD_JOB" -o '%.18i %.8T %R'
```

Wait until the hold job reports RUNNING before submitting the next job. It ends after about 90 seconds, so record the pending state promptly:

```sh
course_guard && WORK_JOB=$(sbatch --parsable job.sbatch)
WORK_JOB=${WORK_JOB%%;*}
printf '%s\n' "$WORK_JOB" > evidence/work-job-id.txt
squeue -j "$WORK_JOB" -o '%.18i %.8T %R'
scontrol show job "$WORK_JOB" > evidence/pending-job.txt
course_guard && scancel "$HOLD_JOB"
```

Expected: work is PENDING while the exclusive hold allocation owns the node, then runs after release. Depending on scheduling cycle/policy, the pending reason may show Resources or Priority. Preserve the actual reason. This demonstrates contention/release; it does not establish backfill effectiveness from one sample.

## Requeue and verify application state

While WORK_JOB runs, wait until at least five steps are committed. The following loop has a bound; it does not silently wait forever:

```sh
course_requeue_when_ready() {
  course_guard || return 1
  [[ "${WORK_JOB:-}" =~ ^[0-9]+$ ]] || { echo 'Missing numeric course Job ID.'; return 1; }
  checkpoint_ready=false
  for attempt in $(seq 1 30); do
    if python3 - "$WORK_JOB" <<'PY'
import json, pathlib, sys
p = pathlib.Path('evidence') / ('job-' + sys.argv[1]) / 'checkpoint.json'
try:
    n = json.loads(p.read_text())['completed']
except (FileNotFoundError, json.JSONDecodeError):
    raise SystemExit(1)
raise SystemExit(0 if 5 <= n < 100 else 1)
PY
    then checkpoint_ready=true; break; fi
    sleep 1
  done
  if [[ "$checkpoint_ready" != true ]]; then
    echo 'No eligible checkpoint within 30 seconds; requeue aborted.'
    return 1
  fi
  scontrol show job "$WORK_JOB" > evidence/before-requeue.txt || return 1
  if [[ "$(squeue -h -j "$WORK_JOB" -o '%T')" != RUNNING ]]; then
    echo 'Job is no longer RUNNING; requeue aborted.'
    return 1
  fi
  course_guard && scontrol requeue "$WORK_JOB"
}
course_requeue_when_ready
```

If the function reports failure, stop and use a fresh job; do not claim an interruption occurred. A state change can still race with the final controller request, so preserve its return status and the actual transition. After successful requeue, inspect `course-$WORK_JOB.out`. Expected: a restarted attempt, a positive `resumed_from`, and ultimately total 338350. Verify the output independently after the job completes:

```sh
python3 - "$WORK_JOB" <<'PY'
import json, pathlib, sys
result = json.loads((pathlib.Path('evidence') / ('job-' + sys.argv[1]) / 'result.json').read_text())
assert result['correct'] and result['total'] == 338350
assert 0 < result['resumed_from'] < 100, result
print('PASS: native job application restored state and produced 338350')
PY
sudo tail -n 20 /var/log/slurm-course/job-completion.log
```

If the result file is not present yet, use `squeue` and inspect the output; do not turn FileNotFoundError into success. `SLURM_RESTART_COUNT` and log append mode help separate attempts. The application writes a checkpoint every step, so the exact restored step can vary with interruption timing.

## Accounting: make availability explicit

The base setup has no SlurmDBD, no database-backed associations, and no full job-accounting collector. Preserve `scontrol show config`, current job details while retained, the completion file, and application output. State **SlurmDBD accounting NOT_CONFIGURED**. Do not claim that `sacct` returned authoritative history, and do not compute observed CPU consumption from requested CPU count.

For an extended exercise, require an instructor-provided isolated MariaDB/MySQL service supported by the selected Slurm release, a least-privilege database account, secure credential delivery, a matching SlurmDBD build, protected `slurmdbd.conf`, consistent identities, and an empty course-only database. Configure `AccountingStorageType=accounting_storage/slurmdbd`, `AccountingStorageHost`, and `JobAcctGatherType=jobacct_gather/linux` in the controller profile. The SlurmDBD profile needs the correct `AuthType`, `DbdHost`, `SlurmUser`, `StorageType=accounting_storage/mysql`, `StorageHost`, `StorageLoc`, `StorageUser`, and privately provided `StoragePass` where required. Never commit that credential file.

After the database daemon is healthy, add the course cluster/account/user using `sacctmgr` in that isolated environment and verify associations. For example, with the configured course cluster and current learner user, an authorized administrator can use:

```sh
course_guard && sudo env SLURM_CONF="$SLURM_CONF" /opt/slurm/25.05.3/bin/sacctmgr add cluster rack-course
course_guard && sudo env SLURM_CONF="$SLURM_CONF" /opt/slurm/25.05.3/bin/sacctmgr add account course Description=course Organization=course
course_guard && sudo env SLURM_CONF="$SLURM_CONF" /opt/slurm/25.05.3/bin/sacctmgr add user "$USER" Account=course Cluster=rack-course
sacctmgr show associations format=Cluster,Account,User
```

These commands intentionally retain interactive confirmation and require existing secure database provisioning. Set the learner's default association or submit `--account=course` explicitly. Then run a fresh job and inspect `sacct -j JOB_ID --format=JobID,State,ExitCode,Elapsed,AllocCPUS,TotalCPU,MaxRSS`; replace `JOB_ID` with the recorded integer. Explain batch/application step rows, absent fields, and collection timing. Before testing fair share, also configure a reviewed multifactor priority profile and nonzero fair-share weight. Enabling database storage alone does not select a fair-share policy. See [accounting](https://slurm.schedmd.com/accounting.html), [sacctmgr](https://slurm.schedmd.com/sacctmgr.html), and [SlurmDBD configuration](https://slurm.schedmd.com/slurmdbd.conf.html).

## Isolation, restart, and HA boundaries

For a bounded filesystem test, create two course-only users on the disposable VM, a private mode-0700 directory owned by one, and attempt a read as the other. Record the expected Permission denied. This is ordinary Linux file isolation, not proof of cgroup/device isolation. For example:

```sh
course_guard && sudo useradd --create-home course-other
mkdir -p evidence/private
chmod 700 evidence/private
printf 'synthetic checkpoint\n' > evidence/private/test.txt
sudo -u course-other cat "$PWD/evidence/private/test.txt"
# Expected nonzero exit and Permission denied.
```

The hardened cgroup profile replaces `TaskPlugin` with `task/cgroup` and `ProctrackType` with `proctrack/cgroup`, using the provided `cgroup.conf.example` only after validating cgroup v2/systemd delegation for the VM and matching Slurm build. Test CPU/memory containment with conservative limits before claiming it. No GPU exists in this VM; GPU isolation needs real GRES inventory, a compatible driver/library build, device controls, and actual allowed/denied access checks.

To test single-controller state persistence, submit a fresh delayed job, record its ID and checkpoint, then gracefully stop only foreground terminal A. Leave the node daemon running. Restart the same controller command against the same StateSaveLocation; verify the same job, observed application progress, and new submission. Preserve timestamps and logs. This tests a restart, not backup-controller failover. Do not use `slurmctld -c`, erase state files, or infer continuity without observations.

For real HA, provision a separate primary/backup controller environment with shared persistent controller state, matching configuration and identities, protected authentication, correct SlurmctldHost entries, dedicated nodes, and a separate failure plan. Baseline jobs and state; stop only the assigned primary; observe backup takeover, job state, running-step continuity, and new submission; restore the primary and verify ownership. Abort on shared-state failure, unplanned dual ownership, or collateral impact. Database HA remains a separate dependency. Use the release-specific [upgrade guide](https://slurm.schedmd.com/upgrades.html) for compatibility and restore planning; never assume old binaries can read state transformed by new daemons.

## Cleanup

After preserving evidence, cancel only recorded live course Job IDs and verify they are gone:

```sh
course_guard && scancel "$WORK_JOB"
course_guard && scancel "$HOLD_JOB"
squeue -u "$USER"
```

Already completed IDs may produce an invalid-job message; record that status rather than broadening the cancellation. Stop foreground terminals A and B gracefully. Dispose of or revert the dedicated VM using its recorded VM identity. Do not run broad `scancel -u`, remove another cluster's state, or copy MUNGE/database secrets into evidence. If retaining the VM, review the created users/services and remove only course-owned resources with the environment owner.
