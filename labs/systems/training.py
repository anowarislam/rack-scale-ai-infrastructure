#!/usr/bin/env python3
"""Bounded linear regression and checkpoint recovery; Python control or optional CUDA."""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
DATA = [(-1.0, -1.0), (-0.5, 0.0), (0.5, 2.0), (1.0, 3.0)]
DATA_SHA = hashlib.sha256(json.dumps(DATA).encode("ascii")).hexdigest()


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("ascii")


def workspace(value):
    path = Path(value).resolve()
    boundary = (ROOT / "learner-work").resolve()
    if path == boundary or not path.is_relative_to(boundary):
        raise ValueError("output must be a child of this repository's learner-work/")
    return path


def publish(path, state):
    name = f"checkpoint-{state['step']:04d}.json"
    payload = encode(state)
    for target in (path / name, path / (name + ".tmp"), path / "manifest.json", path / "manifest.json.tmp"):
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise ValueError("refusing non-regular checkpoint artifact")
    temporary = path / (name + ".tmp")
    with temporary.open("wb") as out:
        out.write(payload)
        out.flush()
        os.fsync(out.fileno())
    os.replace(temporary, path / name)
    manifest = {"file": name, "sha256": hashlib.sha256(payload).hexdigest()}
    with (path / "manifest.json.tmp").open("wb") as out:
        out.write(encode(manifest))
        out.flush()
        os.fsync(out.fileno())
    os.replace(path / "manifest.json.tmp", path / "manifest.json")
    # This is a process-interruption model, not a power-loss durability proof.


def restore(path):
    manifest_path = path / "manifest.json"
    if manifest_path.is_symlink():
        raise ValueError("manifest must not be a symlink")
    manifest = json.loads(manifest_path.read_bytes())
    name = manifest["file"]
    if not isinstance(name, str) or Path(name).name != name or not name.startswith("checkpoint-"):
        raise ValueError("invalid checkpoint filename")
    checkpoint = path / name
    if checkpoint.is_symlink():
        raise ValueError("checkpoint must not be a symlink")
    payload = checkpoint.read_bytes()
    if hashlib.sha256(payload).hexdigest() != manifest["sha256"]:
        raise ValueError("checkpoint checksum mismatch")
    state = json.loads(payload)
    if state["schema"] != 1 or state["data_sha256"] != DATA_SHA or state["learning_rate"] != .1:
        raise ValueError("checkpoint belongs to a different training contract")
    if type(state["step"]) is not int or not 0 <= state["step"] <= 200:
        raise ValueError("invalid checkpoint step")
    if not all(type(state[key]) in (int, float) and math.isfinite(state[key]) for key in ("weight", "bias")):
        raise ValueError("invalid checkpoint parameters")
    return state


class PythonModel:
    def __init__(self, weight, bias):
        self.weight, self.bias = weight, bias

    def update(self):
        errors = [self.weight * x + self.bias - y for x, y in DATA]
        dw = sum(2 * error * x for error, (x, _) in zip(errors, DATA)) / len(DATA)
        db = sum(2 * error for error in errors) / len(DATA)
        self.weight -= .1 * dw
        self.bias -= .1 * db

    def parameters(self):
        return self.weight, self.bias


class CudaModel:
    def __init__(self, weight, bias):
        try:
            import torch
        except ImportError as error:
            raise ValueError("CUDA backend requires an already installed, approved PyTorch environment") from error
        if not torch.cuda.is_available():
            raise ValueError("PyTorch reports CUDA unavailable; no CPU fallback is permitted")
        self.torch = torch
        self.model = torch.nn.Linear(1, 1).to(device="cuda", dtype=torch.float64)
        with torch.no_grad():
            self.model.weight.fill_(weight)
            self.model.bias.fill_(bias)
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=.1, momentum=0)
        self.x = torch.tensor([[x] for x, _ in DATA], device="cuda", dtype=torch.float64)
        self.y = torch.tensor([[y] for _, y in DATA], device="cuda", dtype=torch.float64)
        torch.cuda.synchronize()

    def update(self):
        self.optimizer.zero_grad()
        loss = self.torch.nn.functional.mse_loss(self.model(self.x), self.y)
        loss.backward()
        self.optimizer.step()

    def parameters(self):
        self.torch.cuda.synchronize()
        return self.model.weight.item(), self.model.bias.item()


def run(output, steps=40, interrupt_at=None, resume=False, backend="python"):
    if resume:
        state = restore(output)
        if state["backend"] != backend:
            raise ValueError("resume must use the recorded backend; compare backends using separate runs")
    else:
        if output.exists() and any(output.iterdir()):
            raise ValueError("new training requires an empty output directory")
        state = {"schema": 1, "data_sha256": DATA_SHA, "learning_rate": .1,
                 "step": 0, "weight": 0.0, "bias": 0.0, "backend": backend}
    if not 1 <= steps <= 200 or steps <= state["step"]:
        raise ValueError("steps must exceed saved step and be at most 200")
    if interrupt_at is not None and not state["step"] < interrupt_at < steps:
        raise ValueError("interrupt-at must be between the saved step and the final step")
    model = (PythonModel if backend == "python" else CudaModel)(state["weight"], state["bias"])
    output.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    start_step, checkpoint_step = state["step"], state["step"]
    status = "COMPLETE"
    for step in range(start_step + 1, steps + 1):
        model.update()
        state["step"] = step
        state["weight"], state["bias"] = model.parameters()
        if step % 10 == 0 or step == steps:
            publish(output, state)
            checkpoint_step = step
        if step == interrupt_at:
            status = "INTERRUPTED"
            break
    predictions = [state["weight"] * x + state["bias"] for x, _ in DATA]
    loss = sum((prediction - y) ** 2 for prediction, (_, y) in zip(predictions, DATA)) / len(DATA)
    result = {"label": "L0_REFERENCE" if backend == "python" else "L1_CUDA_OBSERVATION",
              "status": status, "backend": backend, "start_step": start_step,
              "completed_step": state["step"], "checkpoint_step": checkpoint_step,
              "uncommitted_steps": state["step"] - checkpoint_step, "weight": state["weight"],
              "bias": state["bias"], "mse": loss, "predictions": predictions,
              "within_tolerance": max(abs(p - y) for p, (_, y) in zip(predictions, DATA)) <= .1}
    if backend == "cuda":
        result["elapsed_s"] = time.perf_counter() - started
        result["torch_version"] = model.torch.__version__
        result["torch_cuda_version"] = model.torch.version.cuda
        result["device"] = model.torch.cuda.get_device_name(0)
        result["timing_scope"] = "training plus per-step synchronization and checkpoint I/O; not a GPU benchmark"
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--interrupt-at", type=int)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--backend", choices=("python", "cuda"), default="python")
    args = parser.parse_args(argv)
    try:
        result = run(workspace(args.output), args.steps, args.interrupt_at, args.resume, args.backend)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 3 if result["status"] == "INTERRUPTED" else 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        print(json.dumps({"status": "ERROR", "message": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
