#!/usr/bin/env python3
"""Deterministic L0 teaching models. No hardware, network, or subprocess access."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).with_name("fixtures") / "scenarios.json"
OWNED = (".systems-lab.json", "state.json", "history.jsonl")


def catalog():
    raw = FIXTURE.read_bytes()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def workspace_path(value):
    path = Path(value).resolve()
    boundary = (ROOT / "learner-work").resolve()
    if path == boundary or not path.is_relative_to(boundary):
        raise ValueError("workspace must be a child of this repository's learner-work/")
    for name in OWNED:
        target = path / name
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise ValueError(f"refusing non-regular lab file: {name}")
    return path


def validate_config(spec, config):
    if not isinstance(config, dict) or set(config) != set(spec["controls"]):
        raise ValueError("configuration keys do not match this scenario")
    for key, rule in spec["controls"].items():
        value = config[key]
        expected = {"integer": int, "string": str}[rule["type"]]
        if type(value) is not expected:
            raise ValueError(f"{key} must be {rule['type']}")
        if "choices" in rule and value not in rule["choices"]:
            raise ValueError(f"{key} must be one of {rule['choices']}")
        if "minimum" in rule and not rule["minimum"] <= value <= rule["maximum"]:
            raise ValueError(f"{key} is outside the bounded lab range")


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="ascii")


def record(path, event):
    with (path / "history.jsonl").open("a", encoding="ascii") as out:
        out.write(json.dumps(event, sort_keys=True) + "\n")


def initialize(path, name, control, specs, digest):
    if path.exists() and any(path.iterdir()):
        raise ValueError("init requires a new or empty workspace; use reset for an existing lab")
    path.mkdir(parents=True, exist_ok=True)
    marker = {"schema": 1, "scenario": name, "control": control, "fixture_sha256": digest}
    write_json(path / OWNED[0], marker)
    write_json(path / "state.json", {"config": specs[name][control]})
    record(path, {"action": "init", "control": control, "scenario": name})
    return marker


def load_workspace(path, specs, digest):
    marker = json.loads((path / OWNED[0]).read_text(encoding="ascii"))
    if marker.get("schema") != 1 or marker.get("fixture_sha256") != digest:
        raise ValueError("fixture/schema changed; preserve evidence and initialize a new workspace")
    name = marker.get("scenario")
    if name not in specs or marker.get("control") not in ("broken", "healthy"):
        raise ValueError("invalid lab marker")
    state = json.loads((path / "state.json").read_text(encoding="ascii"))
    if set(state) != {"config"}:
        raise ValueError("state may contain only config")
    validate_config(specs[name], state["config"])
    return marker, state["config"]


def nearest_rank(values, fraction):
    return sorted(values)[max(0, math.ceil(len(values) * fraction) - 1)]


def evaluate(name, spec, config):
    """Compute measurements and invariant checks from inputs, never a state label."""
    validate_config(spec, config)
    facts = spec["facts"]
    checks = []

    def check(code, ok, requirement):
        checks.append({"code": code, "pass": bool(ok), "requirement": requirement})

    if name == "domains":
        placements = [facts["primary"], config["secondary"]]
        survivors = [node for node in placements if facts["nodes"][node]["feed"] != facts["failed_feed"]]
        metrics = {"replicas_before": len(placements), "replicas_after_feed_loss": len(survivors),
                   "surviving_nodes": survivors, "failed_feed": facts["failed_feed"]}
        check("SURVIVOR", len(survivors) >= 1, "at least one serving replica survives the selected feed loss")
        check("DISTINCT_NODE", len(set(placements)) == 2, "replicas occupy distinct nodes")
    elif name == "inventory":
        local = config["cpu_numa"] == facts["gpu_numa"]
        metrics = {"identity_agrees": config["recorded_serial"] == facts["os_serial"] == facts["bmc_serial"],
                   "copy_time_ms": facts["local_copy_ms"] if local else facts["remote_copy_ms"],
                   "local_memory_path": local}
        check("IDENTITY", metrics["identity_agrees"], "OS, BMC, and inventory identify the same chassis")
        check("LOCALITY", local, "this experiment's CPU allocation matches the GPU NUMA node")
    elif name == "gpu":
        used = facts["fixed_mib"] + facts["per_sample_mib"] * config["microbatch"]
        usable = facts["capacity_mib"] - facts["reserve_mib"]
        metrics = {"estimated_peak_mib": used, "usable_budget_mib": usable,
                   "budget_headroom_mib": usable - used, "driver_visible": facts["driver_visible"]}
        check("DEVICE_VISIBLE", facts["driver_visible"], "the synthetic driver enumerates the target device")
        check("MEMORY_BUDGET", used <= usable, "estimated peak stays within capacity minus reserve")
    elif name == "fabric":
        counts = list(facts["rank_counts"])
        counts[2] = config["rank2_count"]
        checkpoint = facts["checkpoints"][str(config["resume_step"]) ]
        complete = checkpoint["published"] and checkpoint["valid_shards"] == facts["world_size"]
        metrics = {"rank_counts": counts, "resume_step": config["resume_step"],
                   "checkpoint_complete": complete,
                   "transfer_lower_bound_s": facts["checkpoint_gb"] / facts["storage_gb_s"]}
        check("COLLECTIVE_SHAPE", len(set(counts)) == 1, "all ranks use the same element count for this collective")
        check("CHECKPOINT_COMMIT", complete, "resume uses a published generation with all valid shards")
    elif name == "telemetry":
        sample = facts["samples"][config["collector"]]
        age = facts["now_s"] - sample["observed_s"]
        corrected_event = sample["source_s"] - config["source_offset_s"]
        delivery = sample["observed_s"] - corrected_event
        metrics = {"observed_age_s": age, "corrected_delivery_s": delivery,
                   "temperature_c": sample["temperature_c"], "sample_count": sample["sample_count"],
                   "clock_uncertainty_s": facts["clock_uncertainty_s"]}
        check("FRESHNESS", 0 <= age <= facts["max_age_s"], "observed sample age is within the experiment freshness budget")
        check("TIME_INTEGRITY", 0 <= delivery <= facts["max_delivery_s"], "corrected event ordering is plausible")
        check("LEAST_PRIVILEGE", config["role"] == "telemetry-reader", "collector has only the observation role")
    elif name == "workload":
        latencies = []
        queue = [0] * facts["workers"]
        # One arrival batch each second. Deterministic FCFS service on the earliest free worker.
        for batch in range(facts["batches"]):
            arrival = batch * 1000
            for _ in range(config["arrivals_per_s"]):
                worker = min(range(len(queue)), key=queue.__getitem__)
                finish = max(arrival, queue[worker]) + facts["service_ms"]
                queue[worker] = finish
                latencies.append(finish - arrival)
        duration_s = max(queue) / 1000
        good = sum(value <= facts["deadline_ms"] for value in latencies)
        metrics = {"requests": len(latencies), "duration_s": duration_s,
                   "throughput_requests_s": round(len(latencies) / duration_s, 4),
                   "goodput_requests_s": round(good / duration_s, 4),
                   "deadline_success_fraction": good / len(latencies),
                   "p99_latency_ms": nearest_rank(latencies, .99),
                   "p50_latency_ms": nearest_rank(latencies, .50)}
        check("TAIL_DEADLINE", metrics["p99_latency_ms"] <= facts["deadline_ms"], "p99 end-to-end latency meets the synthetic deadline")
        check("GOODPUT", metrics["deadline_success_fraction"] >= .99, "at least 99 percent of completed requests meet the deadline")
    else:
        raise ValueError("unknown scenario")
    return {"label": "SYNTHETIC_L0", "scenario": name, "exercise": spec["exercise"],
            "metrics": metrics, "checks": checks, "status": "PASS" if all(x["pass"] for x in checks) else "FAIL",
            "claim_ceiling": "model invariants only; no physical performance or hardware health evidence"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    init = sub.add_parser("init")
    init.add_argument("scenario")
    init.add_argument("--control", choices=("broken", "healthy"), default="broken")
    for item in (init, *[sub.add_parser(name) for name in ("observe", "check", "configure", "reset")]):
        item.add_argument("--workspace", required=True)
        if item.prog.endswith(" configure"):
            item.add_argument("--key", required=True)
            item.add_argument("--value", required=True, help="JSON value, e.g. 4 or '\"node-c\"'")
    args = parser.parse_args(argv)
    try:
        specs, digest = catalog()
        if args.command == "list":
            result = {name: {"exercise": spec["exercise"], "question": spec["question"]} for name, spec in specs.items()}
        else:
            path = workspace_path(args.workspace)
            if args.command == "init":
                if args.scenario not in specs:
                    raise ValueError(f"unknown scenario: {args.scenario}")
                result = initialize(path, args.scenario, args.control, specs, digest)
            else:
                marker, config = load_workspace(path, specs, digest)
                name = marker["scenario"]
                spec = specs[name]
                if args.command == "configure":
                    if args.key not in config:
                        raise ValueError("unknown configuration key")
                    old = config[args.key]
                    config[args.key] = json.loads(args.value)
                    validate_config(spec, config)
                    write_json(path / "state.json", {"config": config})
                    record(path, {"action": "configure", "key": args.key, "old": old, "new": config[args.key]})
                    result = {"config": config}
                elif args.command == "reset":
                    config = spec[marker["control"]]
                    write_json(path / "state.json", {"config": config})
                    record(path, {"action": "reset", "control": marker["control"]})
                    result = {"reset": "state only; evidence and history preserved", "config": config}
                else:
                    result = evaluate(name, spec, config)
                    result["fixture_sha256"] = digest
                    result["config"] = config
                    if args.command == "observe":
                        result.pop("checks")
                        result.pop("status")
                        result["facts"] = spec["facts"]
                        result["controls"] = spec["controls"]
        print(json.dumps(result, indent=2, sort_keys=True))
        return int(args.command == "check" and result["status"] == "FAIL")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"status": "ERROR", "message": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
