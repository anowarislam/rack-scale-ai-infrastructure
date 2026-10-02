"""Single-writer checkpoint exercise, using only Python's standard library.

This is application state, not a scheduler, distributed checkpoint, or benchmark.
"""
import argparse
import json
import os
from pathlib import Path
import time


def sum_squares(n):
    return n * (n + 1) * (2 * n + 1) // 6


def run(directory, steps, fail_after=0, delay=0):
    if steps < 1 or delay < 0 or not 0 <= fail_after <= steps:
        raise ValueError("steps must be positive; delay and fail_after must be valid")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    checkpoint = directory / "checkpoint.json"
    state = {"schema": 1, "target": steps, "completed": 0, "total": 0}
    if checkpoint.exists():
        state = json.loads(checkpoint.read_text())
        if (set(state) != {"schema", "target", "completed", "total"}
                or state["schema"] != 1 or state["target"] != steps
                or type(state["completed"]) is not int
                or not 0 <= state["completed"] <= steps
                or state["total"] != sum_squares(state["completed"])):
            raise ValueError("checkpoint identity or arithmetic is invalid; preserve evidence")
    resumed = state["completed"]
    print(json.dumps({"event": "start", "resumed_from": resumed,
                      "target": steps}), flush=True)
    for step in range(resumed + 1, steps + 1):
        state.update(completed=step, total=state["total"] + step * step)
        temporary = directory / "checkpoint.tmp"
        with temporary.open("w") as stream:
            json.dump(state, stream, sort_keys=True)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, checkpoint)
        print(json.dumps({"event": "checkpoint", **state}), flush=True)
        if step == fail_after:
            print(json.dumps({"event": "injected_failure", "exit_code": 75}), flush=True)
            return 75
        time.sleep(delay)
    result = {"event": "complete", "resumed_from": resumed,
              "completed": steps, "total": state["total"],
              "correct": state["total"] == sum_squares(steps)}
    (directory / "result.json").write_text(json.dumps(result, sort_keys=True) + "\n")
    print(json.dumps(result), flush=True)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True)
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--fail-after", type=int, default=0)
    parser.add_argument("--delay", type=float, default=0)
    args = parser.parse_args()
    raise SystemExit(run(args.directory, args.steps, args.fail_after, args.delay))
