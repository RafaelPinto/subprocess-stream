import subprocess
import sys
from typing import List
import unittest


def run_process(args: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        stdout=sys.stdout,
        stderr=sys.stdout,
        encoding="utf-8",
        check=True,
    )


class TestLogCapture(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cmd = ["python", "child_process.py"]
        completed_proc = run_process(cmd)

        print("Stream done")
        print(completed_proc)

    def test_smoke(self):
        print("Test 1")
