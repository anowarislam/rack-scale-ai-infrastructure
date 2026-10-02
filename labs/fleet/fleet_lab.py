#!/usr/bin/env python3
"""Synthetic L0 fleet exercises. Reads JSON; never contacts infrastructure."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def number(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    if not math.isfinite(value) or value < minimum:
        raise ValueError(f"{name} must be finite and >= {minimum}")
    return value


def integer(value, name, minimum=0):
    number(value, name, minimum)
    if int(value) != value:
        raise ValueError(f"{name} must be an integer")
    return int(value)


def require_synthetic(data):
    if not isinstance(data, dict) or data.get("synthetic") is not True:
        raise ValueError("input must explicitly declare synthetic: true")


def signal(data):
    """Validate identity, coverage, clock correction, freshness, and units."""
    now = number(data["now_s"], "now_s")
    max_age = number(data["max_age_s"], "max_age_s")
    inventory, serials, issues = {}, set(), []
    for row in data["inventory"]:
        asset, serial = row["asset_id"], row["serial"]
        if asset in inventory or serial in serials:
            issues.append(f"duplicate inventory identity: {asset}/{serial}")
        inventory[asset] = row
        serials.add(serial)
    if not inventory:
        raise ValueError("inventory must not be empty")
    seen, sequences = set(), {}
    for row in data["readings"]:
        asset = row["asset_id"]
        if asset not in inventory:
            issues.append(f"unknown asset: {asset}")
            continue
        seen.add(asset)
        expected = inventory[asset]
        if row["serial"] != expected["serial"]:
            issues.append(f"serial mismatch: {asset}")
        if row["boot_id"] != expected["boot_id"]:
            issues.append(f"old boot: {asset}")
        if row["unit"] != "C":
            issues.append(f"unit mismatch: {asset}")
        number(row["value"], "temperature", minimum=-273.15)
        key = (asset, row["boot_id"])
        seq = integer(row["sequence"], "sequence")
        if key in sequences and seq <= sequences[key]:
            issues.append(f"duplicate or reordered sequence: {asset}")
        sequences[key] = seq
        event = number(row["event_time_s"], "event_time_s")
        observed = number(row["observed_time_s"], "observed_time_s")
        offset = number(row["clock_offset_s"], "clock_offset_s", minimum=-1e9)
        uncertainty = number(row["clock_uncertainty_s"], "clock_uncertainty_s")
        corrected = event - offset
        # Reject if the oldest plausible event exceeds the freshness bound.
        if now - corrected + uncertainty > max_age:
            issues.append(f"stale source event: {asset}")
        if corrected - uncertainty > now or observed > now:
            issues.append(f"future timestamp: {asset}")
        if corrected - uncertainty > observed:
            issues.append(f"event later than observation: {asset}")
        if now - observed > max_age:
            issues.append(f"stale collection: {asset}")
    for asset in sorted(set(inventory) - seen):
        issues.append(f"missing telemetry: {asset}")
    return {"status": "FAIL" if issues else "PASS", "issues": issues,
            "inventory_count": len(inventory), "observed_count": len(seen),
            "claim": "L0 signal contract only; temperatures are not safety clearance"}


def poisson_cdf(k, mean):
    if k < 0:
        return 0.0
    if mean == 0:
        return 1.0
    return min(1.0, math.fsum(math.exp(i * math.log(mean) - mean - math.lgamma(i + 1))
                              for i in range(k + 1)))


def invert_poisson_cdf(k, probability):
    low, high = 0.0, max(1.0, k + 1.0)
    while poisson_cdf(k, high) > probability:
        high *= 2
    for _ in range(80):
        mid = (low + high) / 2
        if poisson_cdf(k, mid) > probability:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def reliability(data):
    """Fixed-exposure Poisson intervals; no assumed real-world failure model."""
    confidence = number(data.get("confidence", 0.95), "confidence")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between zero and one")
    alpha = 1 - confidence
    results = []
    for cohort in data["cohorts"]:
        exposure, events, warnings, assets = 0.0, 0, [], set()
        for row in cohort["observations"]:
            asset = row["asset_id"]
            if asset in assets:
                raise ValueError("one observation per asset per cohort is required")
            assets.add(asset)
            exposure += number(row["exposure_hours"], "exposure_hours")
            events += integer(row["events"], "events")
            if row.get("end_reason") not in ("administrative", "failure", "lost_observation"):
                raise ValueError("end_reason must label administrative, failure, or lost_observation")
            if row["end_reason"] == "lost_observation":
                warnings.append(f"{asset}: potentially informative censoring; model may not apply")
        if exposure <= 0 or events > 10000:
            raise ValueError("positive total exposure and <= 10000 events required")
        lower = 0.0 if events == 0 else invert_poisson_cdf(events - 1, 1 - alpha / 2) / exposure
        upper = invert_poisson_cdf(events, alpha / 2) / exposure
        result = {"name": cohort["name"], "events": events, "exposure_hours": exposure,
                  "rate_per_1000h": events / exposure * 1000,
                  "two_sided_rate_interval_per_1000h": [lower * 1000, upper * 1000],
                  "warnings": warnings}
        if events == 0:
            result["one_sided_zero_event_upper_per_1000h"] = -math.log(alpha) / exposure * 1000
        results.append(result)
    alarm = data.get("alarm")
    alarm_result = None
    if alarm is not None:
        p = number(alarm["prevalence"], "prevalence")
        sensitivity = number(alarm["sensitivity"], "sensitivity")
        fpr = number(alarm["false_positive_rate"], "false_positive_rate")
        if max(p, sensitivity, fpr) > 1:
            raise ValueError("alarm inputs must be probabilities")
        tp, fp = p * sensitivity, (1 - p) * fpr
        alarm_result = {"true_positive_fraction": tp, "false_positive_fraction": fp,
                        "positive_predictive_value": tp / (tp + fp) if tp + fp else None}
    return {"status": "PASS", "model": "independent homogeneous Poisson events, fixed exposure",
            "confidence": confidence, "cohorts": results, "alarm": alarm_result,
            "claim": "computed model result, not evidence that model assumptions hold"}


TRANSITIONS = {("available", "begin_drain"): "draining",
               ("draining", "confirm_empty"): "drained",
               ("drained", "repair"): "repairing",
               ("repairing", "qualify"): "qualifying",
               ("qualifying", "accept_checks"): "ready",
               ("ready", "promote"): "available",
               ("repairing", "quarantine"): "quarantined",
               ("qualifying", "quarantine"): "quarantined",
               ("quarantined", "resume_repair"): "repairing"}


def lifecycle(data):
    state = data.get("initial_state", "available")
    if state not in {item for pair in TRANSITIONS for item in pair[:1]}:
        raise ValueError("unknown initial state")
    generation = integer(data.get("initial_generation", 0), "initial_generation")
    applied, history = {}, []
    for event in data["events"]:
        event_id, action = event["event_id"], event["action"]
        encoded = json.dumps(event, sort_keys=True)
        expected = integer(event["expected_generation"], "expected_generation")
        target = TRANSITIONS.get((state, action))
        if event_id in applied:
            code = "DUPLICATE" if applied[event_id] == encoded else "ID_REUSE_CONFLICT"
        elif expected != generation:
            code = "STALE_GENERATION"
        elif target is None:
            code = "INVALID_TRANSITION"
        elif action == "confirm_empty" and integer(event.get("workloads", 1), "workloads") != 0:
            code = "WORKLOADS_PRESENT"
        elif action == "accept_checks" and (
            event.get("check_generation") != generation or
            not all(event.get("checks", {}).get(k) is True for k in ("workload", "telemetry", "inventory"))
        ):
            code = "QUALIFICATION_FAILED"
        elif action == "resume_repair" and event.get("recovery_authorized") is not True:
            code = "RECOVERY_NOT_AUTHORIZED"
        else:
            state, generation, code = target, generation + 1, "APPLIED"
            applied[event_id] = encoded
        history.append({"event_id": event_id, "action": action, "result": code,
                        "state": state, "generation": generation})
    final = {"state": state, "generation": generation}
    return {"status": "PASS" if final == data["expected_final"] else "BLOCKED",
            "final": final, "history": history,
            "claim": "single-process event replay with optimistic concurrency; no durable controller"}


def capacity(data):
    headroom = number(data["headroom_fraction"], "headroom_fraction")
    if headroom >= 1:
        raise ValueError("headroom_fraction must be less than one")
    demand = integer(data["demand_gpus"], "demand_gpus")
    gang = integer(data["gang_size"], "gang_size", 1)
    if demand % gang:
        raise ValueError("demand_gpus must be a multiple of gang_size")
    domains = data["domains"]
    if not domains or len({d["name"] for d in domains}) != len(domains):
        raise ValueError("nonempty uniquely named domains required")
    total = sum(integer(d["gpus"], "gpus") for d in domains)
    scenarios = []
    for lost in [None] + domains:
        remaining = total - (lost["gpus"] if lost else 0)
        # A tiny tolerance avoids losing an exactly integral capacity to float noise.
        jobs = math.floor((remaining * (1 - headroom) + 1e-9) / gang)
        admitted = jobs * gang
        scenarios.append({"lost_domain": lost["name"] if lost else "none",
                          "remaining_gpus": remaining, "admissible_gpus": admitted,
                          "margin_gpus": admitted - demand})
    worst = min(scenarios, key=lambda s: s["margin_gpus"])
    return {"status": "PASS" if worst["margin_gpus"] >= 0 else "FAIL",
            "total_gpus": total, "demand_gpus": demand, "scenarios": scenarios,
            "worst_margin_gpus": worst["margin_gpus"],
            "claim": "homogeneous pooled GPU counts only; no topology, memory, or latency guarantee"}


HANDLERS = {"signal": signal, "reliability": reliability, "lifecycle": lifecycle, "capacity": capacity}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exercise", choices=HANDLERS)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text())
        require_synthetic(data)
        result = HANDLERS[args.exercise](data)
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as error:
        print(json.dumps({"status": "INVALID_INPUT", "error": str(error)}, indent=2))
        return 2
    rendered = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        # Explicit output is the sole write; never replace the supplied fixture.
        if args.output.resolve() == args.input.resolve():
            parser.error("output must differ from input")
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
