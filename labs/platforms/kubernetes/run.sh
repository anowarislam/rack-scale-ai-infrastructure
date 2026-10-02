#!/usr/bin/env bash
# Only this script's private kubeconfig and uniquely named course cluster are used.
set -euo pipefail
LAB=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$LAB/../../.." && pwd)
STATE="$ROOT/.cache/platform-kind"
KIND="${COURSE_KIND_BIN:-$ROOT/.cache/course-tools/kind}"
KUBECTL="${COURSE_KUBECTL_BIN:-$ROOT/.cache/course-tools/kubectl}"
ACTION="${1:-help}"
if [[ "$ACTION" == help ]]; then
  echo 'Usage: bash labs/platforms/kubernetes/run.sh create|apply|pending|repair|recover|rbac|inspect|evidence|cleanup'
  exit 0
fi
[[ -x "$KIND" && -x "$KUBECTL" ]] || { echo 'Install verified local tools using README instructions.' >&2; exit 1; }
"$KIND" version | grep -q 'v0.30.0' || { echo 'Expected kind v0.30.0.' >&2; exit 1; }
"$KUBECTL" version --client -o json | python3 -c 'import json,sys; assert json.load(sys.stdin)["clientVersion"]["gitVersion"] == "v1.34.0"'
if [[ "$ACTION" == create ]]; then
  [[ ! -e "$STATE/cluster-name" ]] || { echo 'Existing course state: inspect or cleanup first.' >&2; exit 1; }
  mkdir -p "$STATE"
  CLUSTER="rack-course-platform-$(date +%s)-$$"
  printf '%s\n' "$CLUSTER" > "$STATE/cluster-name"
  printf '%s\n' 'rack-scale-course-owned-v1' > "$STATE/owner"
  "$KIND" create cluster --name "$CLUSTER" --kubeconfig "$STATE/kubeconfig" --config "$LAB/kind.yaml" --wait 120s
  echo "Created $CLUSTER with private kubeconfig: $STATE/kubeconfig"
  exit 0
fi
[[ -f "$STATE/owner" && "$(cat "$STATE/owner")" == rack-scale-course-owned-v1 ]] || { echo 'Missing course ownership marker.' >&2; exit 1; }
CLUSTER=$(cat "$STATE/cluster-name")
[[ "$CLUSTER" =~ ^rack-course-platform-[0-9]+-[0-9]+$ ]] || { echo 'Refusing non-course cluster name.' >&2; exit 1; }
k() { "$KUBECTL" --kubeconfig "$STATE/kubeconfig" --context "kind-$CLUSTER" "$@"; }
case "$ACTION" in
  apply)
    k apply -f "$LAB/namespace-rbac.yaml"
    k -n course-platform create configmap course-workload --from-file=workload.py="$LAB/../workload.py" --dry-run=client -o yaml | k apply -f -
    k apply -f "$LAB/workloads.yaml"
    k -n course-platform wait --for=condition=complete job/cpu-check --timeout=180s
    k -n course-platform logs job/cpu-check
    ;;
  pending)
    k apply -f "$LAB/pending.yaml"
    k -n course-platform wait --for=condition=PodScheduled=false pod/pending-example --timeout=60s
    k -n course-platform describe pod pending-example
    ;;
  repair)
    k -n course-platform delete pod pending-example --wait=true
    sed 's/course-invalid/course-local/' "$LAB/pending.yaml" | k apply -f -
    k -n course-platform wait --for=jsonpath='{.status.phase}'=Succeeded pod/pending-example --timeout=120s
    k -n course-platform logs pending-example
    ;;
  recover)
    k apply -f "$LAB/recovery.yaml"
    k -n course-platform wait --for=condition=complete job/checkpoint-recovery --timeout=180s
    k -n course-platform get pods -l job-name=checkpoint-recovery
    k -n course-platform logs -l job-name=checkpoint-recovery --all-containers=true --prefix=true --tail=-1
    ;;
  rbac)
    AS='system:serviceaccount:course-platform:reader'
    [[ "$(k -n course-platform auth can-i list pods --as="$AS")" == yes ]]
    [[ "$(k -n course-platform auth can-i delete pods --as="$AS" || true)" == no ]]
    [[ "$(k -n course-platform auth can-i get secrets --as="$AS" || true)" == no ]]
    [[ "$(k -n default auth can-i list pods --as="$AS" || true)" == no ]]
    echo 'PASS: allowed pod list; denied pod deletion, secret read, and cross-namespace pod list.'
    ;;
  inspect)
    k get nodes -o wide
    k -n course-platform get pods,jobs,pvc,resourcequota
    k -n course-platform get events --sort-by=.metadata.creationTimestamp
    ;;
  evidence)
    mkdir -p "$STATE/evidence"
    k version -o json > "$STATE/evidence/versions.json"
    k get nodes -o json > "$STATE/evidence/nodes.json"
    k -n course-platform get pods,jobs,pvc,resourcequota,events -o json > "$STATE/evidence/resources.json"
    k -n course-platform logs job/cpu-check > "$STATE/evidence/control.log"
    k -n course-platform logs -l job-name=checkpoint-recovery --all-containers=true --prefix=true --tail=-1 > "$STATE/evidence/recovery.log"
    echo "Evidence: $STATE/evidence (review/redact before sharing)"
    ;;
  cleanup)
    "$KIND" delete cluster --name "$CLUSTER" --kubeconfig "$STATE/kubeconfig"
    if "$KIND" get clusters 2>/dev/null | grep -Fxq "$CLUSTER"; then
      echo 'Cluster remains; ownership marker preserved.' >&2
      exit 1
    fi
    mv "$STATE/cluster-name" "$STATE/last-deleted-cluster"
    rm "$STATE/owner"
    echo 'Course cluster removed. Evidence and downloaded tools retained in .cache.'
    ;;
  *) echo "Unknown action: $ACTION" >&2; exit 2 ;;
esac
