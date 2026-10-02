"""Execute the runbook's actual shell block with mocks; never invoke Slurm."""
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


class RequeueGuardTests(unittest.TestCase):
    def run_guard(self, checkpoint_status, state, guard_status=0):
        document = Path(__file__).with_name("runbook.md").read_text()
        block = next(block for block in re.findall(r"```sh\n(.*?)\n```", document, re.S)
                     if block.startswith("course_requeue_when_ready()"))
        mocks = f"""
course_guard() {{ return {guard_status}; }}
python3() {{ return {checkpoint_status}; }}
squeue() {{ printf '%s\\n' '{state}'; }}
scontrol() {{ if [[ "$1" == requeue ]]; then echo MOCK_REQUEUE_CALLED; fi; }}
seq() {{ printf '1\\n2\\n'; }}
sleep() {{ :; }}
WORK_JOB=42
"""
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "evidence").mkdir()
            return subprocess.run(["bash"], input=mocks + block, text=True,
                                  capture_output=True, cwd=directory)

    def test_checkpoint_timeout_never_requeues(self):
        result = self.run_guard(1, "RUNNING")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("No eligible checkpoint", result.stdout)
        self.assertNotIn("MOCK_REQUEUE_CALLED", result.stdout)

    def test_nonrunning_job_never_requeues(self):
        result = self.run_guard(0, "COMPLETED")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("no longer RUNNING", result.stdout)
        self.assertNotIn("MOCK_REQUEUE_CALLED", result.stdout)

    def test_wrong_environment_never_requeues(self):
        result = self.run_guard(0, "RUNNING", guard_status=1)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertNotIn("MOCK_REQUEUE_CALLED", result.stdout)

    def test_ready_running_job_requeues_once(self):
        result = self.run_guard(0, "RUNNING")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("MOCK_REQUEUE_CALLED"), 1)


if __name__ == "__main__":
    unittest.main()
