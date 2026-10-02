"""Two-task CPU recovery recorder/checker; launching Slurm is the learner's action.

Reuses labs/platforms/workload.py. Passing local record checks is not L2 proof.
The owner must establish two independently provisioned hosts and storage scope.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def worker(root, phase):
    rank = int(os.environ["SLURM_PROCID"])
    if rank not in (0, 1) or int(os.environ["SLURM_NTASKS"]) != 2:
        raise ValueError("exactly two tasks, ranks 0 and 1, are required")
    directory = root / f"rank-{rank}"
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory / ".writer"
    lock.mkdir()  # No automatic stale-lock removal; stop and inspect on collision.
    record_path = directory / f"attempt-{phase}.json"
    record = {
        "phase": phase, "rank": rank, "node": os.environ["SLURMD_NODENAME"],
        "hostname": socket.gethostname(), "job_id": os.environ["SLURM_JOB_ID"],
        "started_utc": utc_now(), "status": "running",
    }
    with record_path.open("x") as stream:
        json.dump(record, stream)
    script = Path(__file__).resolve().parents[1] / "labs/platforms/workload.py"
    command = [sys.executable, str(script), "--directory", str(directory),
               "--steps", "100", "--delay", "0.1"]
    if phase == "fault" and rank == 1:
        command += ["--fail-after", "20"]
    start = time.monotonic()
    with (directory / f"attempt-{phase}.log").open("x") as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
    # Only a reaped child permits releasing the writer marker.
    log = [json.loads(line) for line in
           (directory / f"attempt-{phase}.log").read_text().splitlines()]
    checkpoint = json.loads((directory / "checkpoint.json").read_text())
    record.update(status="exited", exit_code=result.returncode,
                  ended_utc=utc_now(), duration_s=time.monotonic() - start,
                  resumed_from=log[0]["resumed_from"],
                  completed=checkpoint["completed"])
    record_path.write_text(json.dumps(record, sort_keys=True) + "\n")
    lock.rmdir()
    print(json.dumps(record, sort_keys=True), flush=True)
    return result.returncode


def check(root, expected):
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    require({p.name for p in root.glob("rank-*")} == {"rank-0", "rank-1"},
            "need exactly the two logical task directories")
    phase = expected
    records, total = [], 0
    for rank in (0, 1):
        directory = root / f"rank-{rank}"
        require(not (directory / ".writer").exists(), "writer still active or unresolved")
        record = json.loads((directory / f"attempt-{phase}.json").read_text())
        require(record["status"] == "exited" and record["rank"] == rank,
                "task identity or terminal record mismatch")
        require(record["phase"] == phase, "attempt phase mismatch")
        desired_completed = 20 if expected == "fault" and rank == 1 else 100
        desired_exit = 75 if desired_completed == 20 else 0
        desired_resume = (100 if rank == 0 else 20) if expected == "recovery" else 0
        require(record["exit_code"] == desired_exit, "unexpected task exit code")
        require(record["completed"] == desired_completed, "unexpected completed step")
        require(record["resumed_from"] == desired_resume, "unexpected resume point")
        checkpoint = json.loads((directory / "checkpoint.json").read_text())
        require(checkpoint == {"schema": 1, "target": 100,
                               "completed": desired_completed,
                               "total": sum(i * i for i in range(1, desired_completed + 1))},
                "checkpoint invariant mismatch")
        if desired_completed == 20:
            require(not (directory / "result.json").exists(),
                    "failed task must not have a final result")
        else:
            result = json.loads((directory / "result.json").read_text())
            require(result == {"event": "complete", "resumed_from": desired_resume,
                               "completed": 100, "total": 338350, "correct": True},
                    "logical task result mismatch")
            total += result["total"]  # One canonical result per logical task.
        if expected == "recovery":
            prior = json.loads((directory / "attempt-fault.json").read_text())
            require(prior["exit_code"] == (0 if rank == 0 else 75),
                    "original failed attempt evidence is missing or wrong")
            require(prior["completed"] == (100 if rank == 0 else 20),
                    "original progress evidence is wrong")
        records.append(record)
    require(len({r["node"] for r in records}) == 2, "tasks did not record distinct Slurm nodes")
    require(len({r["hostname"] for r in records}) == 2, "tasks did not record distinct hostnames")
    require(len({r["job_id"] for r in records}) == 1, "tasks belong to different allocations")
    require(total == (338350 if expected == "fault" else 676700), "aggregate mismatch")
    print(json.dumps({"status": "PASS", "check": "arithmetic_and_record_checks",
                      "phase": expected, "completed_logical_tasks": 1 if expected == "fault" else 2,
                      "aggregate": total, "nodes": [r["node"] for r in records],
                      "claim": "host independence and native records require separate review"},
                     sort_keys=True))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("worker", "check"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--directory", type=Path, required=True)
        sub.add_argument("--phase" if command == "worker" else "--expected",
                         choices=("baseline", "fault", "recovery", "reset"), required=True)
    args = parser.parse_args()
    try:
        return worker(args.directory.resolve(), args.phase) if args.command == "worker" else check(
            args.directory.resolve(), args.expected)
    except (ValueError, KeyError, OSError) as error:
        print(json.dumps({"status": "BLOCKED", "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
