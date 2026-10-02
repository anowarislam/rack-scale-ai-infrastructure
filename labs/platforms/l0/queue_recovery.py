"""Deterministic placement model. It does NOT execute Kubernetes or Slurm."""
import argparse
import json
from pathlib import Path


def place(nodes, slots, units_per_slot, same_domain):
    """Return an all-or-nothing placement without mutating available capacity."""
    if slots < 1 or units_per_slot < 1:
        raise ValueError("resource requests must be positive integers")
    candidates = sorted({n["domain"] for n in nodes}) if same_domain else [None]
    for domain in candidates:
        remaining = {n["name"]: n["free"] for n in nodes}
        placement = []
        for _ in range(slots):
            node = next((n for n in nodes
                         if (domain is None or n["domain"] == domain)
                         and remaining[n["name"]] >= units_per_slot), None)
            if node is None:
                break
            remaining[node["name"]] -= units_per_slot
            placement.append(node["name"])
        if len(placement) == slots:
            return {"state": "ADMITTED", "placement": placement,
                    "remaining": remaining}
    return {"state": "PENDING", "reason": "no complete feasible placement",
            "placement": []}


def scenario():
    fragmented = [{"name": "a", "domain": "rack-a", "free": 3},
                  {"name": "b", "domain": "rack-b", "free": 3}]
    repaired = [{"name": "a", "domain": "rack-a", "free": 4},
                {"name": "b", "domain": "rack-b", "free": 2}]
    return {"fidelity": "L0 model only", "resource_units": "synthetic slots",
            "request": {"slots": 2, "units_per_slot": 2, "same_domain": True},
            "healthy": place(repaired, 2, 2, True),
            "broken": place(fragmented, 2, 2, True),
            "recovered": place(fragmented, 2, 2, False),
            "tradeoff": "relaxing domain changes the workload contract"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(scenario(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result)
    print(result, end="")
