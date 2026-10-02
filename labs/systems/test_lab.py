"""Behavioral checks for L0 models, file boundaries, and checkpoint recovery."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


lab = module("lab")
training = module("training")


class Models(unittest.TestCase):
    def setUp(self):
        self.specs, self.digest = lab.catalog()

    def test_broken_and_healthy_controls(self):
        for name, spec in self.specs.items():
            with self.subTest(name=name):
                self.assertEqual(lab.evaluate(name, spec, spec["broken"])["status"], "FAIL")
                self.assertEqual(lab.evaluate(name, spec, spec["healthy"])["status"], "PASS")

    def test_inventory_partial_fix_does_not_pass(self):
        spec = self.specs["inventory"]
        result = lab.evaluate("inventory", spec, {"recorded_serial": "SN-2302", "cpu_numa": 0})
        self.assertTrue(result["checks"][0]["pass"])
        self.assertFalse(result["checks"][1]["pass"])

    def test_collective_fix_does_not_accept_partial_checkpoint(self):
        spec = self.specs["fabric"]
        result = lab.evaluate("fabric", spec, {"rank2_count": 1024, "resume_step": 120})
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["metrics"]["checkpoint_complete"])

    def test_memory_boundary(self):
        spec = self.specs["gpu"]
        self.assertEqual(lab.evaluate("gpu", spec, {"microbatch": 7})["status"], "PASS")
        self.assertEqual(lab.evaluate("gpu", spec, {"microbatch": 8})["status"], "FAIL")

    def test_boolean_rejected_as_integer(self):
        with self.assertRaises(ValueError):
            lab.validate_config(self.specs["gpu"], {"microbatch": True})

    def test_queue_capacity_and_tail(self):
        spec = self.specs["workload"]
        broken = lab.evaluate("workload", spec, spec["broken"])["metrics"]
        healthy = lab.evaluate("workload", spec, spec["healthy"])["metrics"]
        self.assertEqual(broken["requests"], 80)
        self.assertEqual(broken["p99_latency_ms"], 7000)
        self.assertEqual(healthy["p99_latency_ms"], 800)
        self.assertGreater(healthy["goodput_requests_s"], broken["goodput_requests_s"])

    def test_fresh_collection_does_not_correct_clock_or_privilege(self):
        spec = self.specs["telemetry"]
        result = lab.evaluate("telemetry", spec, dict(spec["broken"], collector="live"))
        self.assertTrue(result["checks"][0]["pass"])
        self.assertFalse(result["checks"][1]["pass"])
        self.assertFalse(result["checks"][2]["pass"])


class Workspaces(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.patch = patch.object(lab, "ROOT", self.root)
        self.patch.start()
        self.path = self.root / "learner-work" / "attempt"

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def cli(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return lab.main(list(args))

    def test_cli_failure_recovery_and_reset(self):
        path = str(self.path)
        self.assertEqual(self.cli("init", "gpu", "--workspace", path), 0)
        self.assertEqual(self.cli("check", "--workspace", path), 1)
        self.assertEqual(self.cli("configure", "--workspace", path, "--key", "microbatch", "--value", "4"), 0)
        self.assertEqual(self.cli("check", "--workspace", path), 0)
        (self.path / "my-notes.md").write_text("keep")
        self.assertEqual(self.cli("reset", "--workspace", path), 0)
        self.assertEqual(self.cli("check", "--workspace", path), 1)
        self.assertEqual((self.path / "my-notes.md").read_text(), "keep")

    def test_invalid_config_is_not_written(self):
        path = str(self.path)
        self.cli("init", "gpu", "--workspace", path)
        before = (self.path / "state.json").read_bytes()
        self.assertEqual(self.cli("configure", "--workspace", path, "--key", "microbatch", "--value", "100000"), 2)
        self.assertEqual(before, (self.path / "state.json").read_bytes())

    def test_refuse_external_path_and_root(self):
        for path in (self.root / "outside", self.root / "learner-work"):
            with self.assertRaises(ValueError):
                lab.workspace_path(path)

    def test_refuse_state_symlink(self):
        self.path.mkdir(parents=True)
        outside = self.root / "outside.json"
        outside.write_text("{}")
        (self.path / "state.json").symlink_to(outside)
        with self.assertRaises(ValueError):
            lab.workspace_path(self.path)

    def test_fixture_drift_rejected(self):
        specs, digest = lab.catalog()
        lab.initialize(self.path, "gpu", "broken", specs, digest)
        with self.assertRaises(ValueError):
            lab.load_workspace(self.path, specs, "different")

    def test_reinitialization_preserves_existing(self):
        path = str(self.path)
        self.assertEqual(self.cli("init", "gpu", "--workspace", path), 0)
        self.assertEqual(self.cli("init", "inventory", "--workspace", path), 2)


class Checkpoints(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_interrupted_resume_matches_uninterrupted(self):
        baseline = training.run(self.root / "baseline")
        broken = training.run(self.root / "resume", interrupt_at=23)
        self.assertEqual(broken["status"], "INTERRUPTED")
        self.assertEqual(broken["checkpoint_step"], 20)
        self.assertEqual(broken["uncommitted_steps"], 3)
        recovered = training.run(self.root / "resume", resume=True)
        self.assertEqual(recovered["start_step"], 20)
        self.assertEqual(baseline["predictions"], recovered["predictions"])
        self.assertTrue(recovered["within_tolerance"])

    def test_checksum_detects_tampering(self):
        path = self.root / "corrupt"
        training.run(path, interrupt_at=23)
        (path / "checkpoint-0020.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "checksum"):
            training.restore(path)

    def test_unpublished_generation_is_ignored(self):
        path = self.root / "orphan"
        training.run(path, interrupt_at=23)
        (path / "checkpoint-0030.json").write_text("partial")
        self.assertEqual(training.restore(path)["step"], 20)

    def test_manifest_path_escape_rejected(self):
        path = self.root / "escape"
        training.run(path, interrupt_at=23)
        (path / "manifest.json").write_text(json.dumps({"file": "../secret", "sha256": "x"}))
        with self.assertRaisesRegex(ValueError, "filename"):
            training.restore(path)

    def test_backend_change_rejected(self):
        path = self.root / "backend"
        training.run(path, interrupt_at=23)
        with self.assertRaisesRegex(ValueError, "backend"):
            training.run(path, resume=True, backend="cuda")

    def test_bounded_steps_and_no_overwrite(self):
        path = self.root / "bounds"
        with self.assertRaises(ValueError):
            training.run(path, steps=100000)
        training.run(path)
        with self.assertRaises(ValueError):
            training.run(path)


if __name__ == "__main__":
    unittest.main()
