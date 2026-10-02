"""L0 recorder tests with mock identities; no Slurm or multi-host claim.

The real checkpoint application runs. Only its artificial delay is removed.
"""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import l2_batch


class BatchRecordTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        original_run = l2_batch.subprocess.run

        def without_artificial_delay(command, **kwargs):
            command = list(command)
            command[command.index("--delay") + 1] = "0"
            return original_run(command, **kwargs)

        patcher = patch.object(l2_batch.subprocess, "run", side_effect=without_artificial_delay)
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_rank(self, directory, phase, rank):
        environment = {"SLURM_PROCID": str(rank), "SLURM_NTASKS": "2",
                       "SLURMD_NODENAME": f"MOCK-node-{rank}", "SLURM_JOB_ID": phase}
        with patch.dict(l2_batch.os.environ, environment), patch.object(
                l2_batch.socket, "gethostname", return_value=f"MOCK-host-{rank}"), contextlib.redirect_stdout(io.StringIO()):
            return l2_batch.worker(directory, phase)

    def run_pair(self, directory, phase):
        return [self.run_rank(directory, phase, rank) for rank in (0, 1)]

    def check(self, directory, phase):
        with contextlib.redirect_stdout(io.StringIO()):
            return l2_batch.check(directory, phase)

    def test_baseline_fault_recovery_reset_real_checkpoint_application(self):
        self.assertEqual(self.run_pair(self.root / "control", "baseline"), [0, 0])
        self.assertEqual(self.check(self.root / "control", "baseline"), 0)
        self.assertEqual(self.run_pair(self.root / "failure", "fault"), [0, 75])
        self.assertEqual(self.check(self.root / "failure", "fault"), 0)
        self.assertEqual(self.run_pair(self.root / "failure", "recovery"), [0, 0])
        self.assertEqual(self.check(self.root / "failure", "recovery"), 0)
        self.assertEqual(self.run_pair(self.root / "reset", "reset"), [0, 0])
        self.assertEqual(self.check(self.root / "reset", "reset"), 0)

    def test_incorrect_final_result_is_rejected(self):
        self.run_pair(self.root, "baseline")
        path = self.root / "rank-1/result.json"
        result = json.loads(path.read_text())
        result["total"] += 1
        path.write_text(json.dumps(result))
        with self.assertRaisesRegex(ValueError, "logical task result mismatch"):
            self.check(self.root, "baseline")

    def test_same_host_aliases_are_rejected(self):
        self.run_pair(self.root, "baseline")
        path = self.root / "rank-1/attempt-baseline.json"
        record = json.loads(path.read_text())
        record["hostname"] = "MOCK-host-0"
        path.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, "distinct hostnames"):
            self.check(self.root, "baseline")

    def test_existing_writer_blocks_without_starting_application(self):
        (self.root / "rank-0/.writer").mkdir(parents=True)
        with self.assertRaises(FileExistsError):
            self.run_rank(self.root, "fault", 0)
        self.assertFalse((self.root / "rank-0/checkpoint.json").exists())

    def test_duplicate_phase_preserves_original_attempt(self):
        self.run_pair(self.root, "baseline")
        original = (self.root / "rank-0/attempt-baseline.json").read_bytes()
        with self.assertRaises(FileExistsError):
            self.run_rank(self.root, "baseline", 0)
        self.assertEqual((self.root / "rank-0/attempt-baseline.json").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
