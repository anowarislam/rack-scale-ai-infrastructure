# Kubernetes CPU sandbox runbook

This lab creates only a uniquely named `rack-course-platform-*` kind cluster, with a private kubeconfig in `.cache/platform-kind`. It runs a transparent CPU calculation, demonstrates unschedulable placement and repair, retries an application from a PVC checkpoint, and queries narrow RBAC permissions. Read the [five lessons](../../../tracks/kubernetes/README.md) first.

**Status:** native execution was not completed in the author environment because official tool downloads timed out. The checked-in manifests and scripts are therefore a runnable reference with static validation, not a claimed native pass. See [validation evidence](../VALIDATION.md).

## Prerequisites and frozen reference

- Dedicated local Docker learning capacity; no current cluster is used. As a course planning estimate, allow 4 Docker CPUs, 6 GiB Docker memory, and several GiB free disk. These are not vendor-certified minima.
- macOS or Linux on amd64/arm64, Bash, curl, and Python 3.9+.
- kind v0.30.0 and kubectl v1.34.0 installed only into the repository's ignored tool directory using verified checksums.
- Network access to official release endpoints and container registries.
- Time to retain evidence and remove the course cluster afterward.

Node image: `kindest/node:v1.34.0@sha256:7416a61b42b1662ca6ca89f02028ac133a309a2a30ba309614e8ec94d976dc5a`, verified against the [official kind release](https://github.com/kubernetes-sigs/kind/releases/tag/v0.30.0). Workload image: `python:3.12.7-alpine3.20@sha256:5049c050bdc68575a10bcb1885baa0689b6c15152d8a56a7e399fb49f783bf98`, resolved as a multi-platform index from the Docker Official Image registry on 2026-10-02. Both references are historical lab pins. Their presence here is not a security/support recommendation for production. No GPU, CNI add-on, operator, or Helm chart is installed.

## Download tools without modifying global installations

Run from repository root. The snippet writes `.part` files and only makes them executable after comparing official SHA-256 values. Failed partial downloads must never be renamed to the final tool names.

```sh
python3 - <<'PY'
import hashlib, json, os, pathlib, platform, subprocess
dest = pathlib.Path('.cache/course-tools')
dest.mkdir(parents=True, exist_ok=True)
arch = {'arm64': 'arm64', 'aarch64': 'arm64', 'x86_64': 'amd64'}[platform.machine()]
system = {'Darwin': 'darwin', 'Linux': 'linux'}[platform.system()]
items = [
    ('kind', f'https://github.com/kubernetes-sigs/kind/releases/download/v0.30.0/kind-{system}-{arch}', '.sha256sum'),
    ('kubectl', f'https://dl.k8s.io/release/v1.34.0/bin/{system}/{arch}/kubectl', '.sha256'),
]
records = []
for name, url, suffix in items:
    part, sums = dest / (name + '.part'), dest / (name + '.checksum')
    for remote, local in [(url, part), (url + suffix, sums)]:
        subprocess.run(['curl', '-fLsS', '--max-time', '300', '-o', str(local), remote], check=True)
    expected = sums.read_text().split()[0]
    actual = hashlib.sha256(part.read_bytes()).hexdigest()
    if expected != actual:
        raise SystemExit(f'{name}: checksum mismatch; retained nonexecutable partial file')
    part.chmod(0o755)
    os.replace(part, dest / name)
    records.append({'name': name, 'url': url, 'sha256': actual})
(dest / 'verified-downloads.json').write_text(json.dumps(records, indent=2) + '\n')
PY
```

The script checks exact tool versions. A globally installed newer kubectl is not silently substituted. Kubernetes v1.34's [skew policy](https://v1-34.docs.kubernetes.io/releases/version-skew-policy/) is broader than this exact lab pin, but reproducible teaching benefits from one baseline.

## Healthy, broken, recovered

Execute one action at a time and preserve output:

```sh
bash labs/platforms/kubernetes/run.sh create
bash labs/platforms/kubernetes/run.sh apply
bash labs/platforms/kubernetes/run.sh pending
bash labs/platforms/kubernetes/run.sh repair
bash labs/platforms/kubernetes/run.sh recover
bash labs/platforms/kubernetes/run.sh rbac
bash labs/platforms/kubernetes/run.sh inspect
bash labs/platforms/kubernetes/run.sh evidence
```

| Action | Expected observation | Meaning |
|---|---|---|
| create | One Ready control plane and worker after startup | Local learning cluster exists; not HA |
| apply | `cpu-check` Complete; total 650 | Native batch execution plus transparent result |
| pending | Existing Pod, `PodScheduled=False`, unschedulable event | Deliberately nonexistent required label |
| repair | New Pod UID, Succeeded, output 650 | Correct workload placement contract |
| recover | Failed attempt exit 75; replacement resumes at 8; total 22140 | Process/Pod failure with persistent backing available |
| rbac | Allow list Pods; deny delete, Secrets, cross-namespace list | Authorization answers for the tested identity |
| evidence | JSON and logs under `.cache/platform-kind/evidence` | Raw evidence for learner review/redaction |

The wrapper supplies the private kubeconfig and explicit context on every kubectl call. It refuses cleanup without its ownership marker and its unique cluster-name pattern. `create` may pull images and consume local Docker resources; no host path containing user documents is mounted.

The recovery workload intentionally fails once after saving step 8. The second attempt begins after that step, so it does not repeat the injected exit. Re-running `recover` against an already Complete Job does not create a fresh experiment. Archive the evidence and rebuild the sandbox for a clean repeat; do not confuse idempotent apply with an independent trial.

## Troubleshooting by layer

| Symptom | Inspect first | Avoid concluding |
|---|---|---|
| Tool download timeout | Exact endpoint, bytes/time, checksum status | That a partial binary is usable |
| No cluster | Docker daemon, memory/disk, kind output | That workload YAML caused pre-cluster failure |
| Job has no Pod | Job events, quota/admission | That the kubelet rejected a nonexistent Pod |
| Pending Pod | Conditions, events, requested labels/resources | That more CPU fixes every filter |
| ImagePullBackOff | Registry reachability and exact digest | That scheduling failed |
| PVC Pending | StorageClass/provisioner and node topology | That a PVC implies replicated storage |
| Recovery begins at zero | Claim/subdirectory/identity and retained files | That final arithmetic proves state reuse |
| Forbidden | Exact identity, resource, verb, namespace | That cluster-admin is the proper repair |

If normal time bounds expire, stop and record the failure. Do not repeatedly create additional clusters to hide it.

## Cleanup and extension boundaries

Copy the redacted evidence you need, then:

```sh
bash labs/platforms/kubernetes/run.sh cleanup
```

This removes only the recorded course cluster, verifies its absence from kind's cluster list, and retains evidence/tools. It does not perform Docker-wide prune or delete any other kubeconfig. If creation partly failed, the retained ownership marker permits the same bounded cleanup.

For GPU work, use separately assigned Linux hardware with verified drivers, runtime, device plugin, exact versions, and recorded image digests. First compare host inventory, advertised allocatable resources, and devices visible inside a one-GPU allocation; then test unauthorized access and workload correctness under the active isolation design. Read the [official GPU scheduling rules](https://v1-34.docs.kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/) and [NVIDIA MIG scope](https://docs.nvidia.com/datacenter/cloud-native/kubernetes/latest/index.html). CPU kind does not establish those results. For executed HA, use the additional failure-domain and state-store prerequisites in [month 11](../../../tracks/kubernetes/11-operability.md).
