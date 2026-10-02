import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from queue_recovery import place, scenario

spec = importlib.util.spec_from_file_location("workload", Path(__file__).parents[1] / "workload.py")
workload = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workload)


class PlacementTests(unittest.TestCase):
    def test_fragmented_total_does_not_imply_feasibility(self):
        result = scenario()
        self.assertEqual(result["broken"]["state"], "PENDING")
        self.assertEqual(result["recovered"]["placement"], ["a", "b"])

    def test_pending_does_not_reserve_partial_resources(self):
        nodes = [{"name": "a", "domain": "x", "free": 3}]
        original = json.loads(json.dumps(nodes))
        self.assertEqual(place(nodes, 2, 2, True)["placement"], [])
        self.assertEqual(nodes, original)

    def test_no_overcommit(self):
        result = place([{"name": "a", "domain": "x", "free": 4}], 2, 2, True)
        self.assertEqual(result["remaining"], {"a": 0})

    def test_invalid_request(self):
        with self.assertRaises(ValueError):
            place([], 0, 1, False)


class CheckpointTests(unittest.TestCase):
    def test_resume_matches_uninterrupted_result(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            self.assertEqual(workload.run(path / "interrupted", 12, 5), 75)
            self.assertEqual(workload.run(path / "interrupted", 12), 0)
            self.assertEqual(workload.run(path / "control", 12), 0)
            resumed = json.loads((path / "interrupted/result.json").read_text())
            control = json.loads((path / "control/result.json").read_text())
            self.assertEqual(resumed["resumed_from"], 5)
            self.assertEqual(resumed["total"], control["total"])
            self.assertEqual(resumed["total"], 650)

    def test_corrupt_checkpoint_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "checkpoint.json").write_text(json.dumps(
                {"schema": 1, "target": 12, "completed": 5, "total": 999}))
            with self.assertRaises(ValueError):
                workload.run(path, 12)

    def test_changed_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            workload.run(directory, 12, 5)
            with self.assertRaises(ValueError):
                workload.run(directory, 13)


if __name__ == "__main__":
    unittest.main()
