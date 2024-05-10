import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import List
import unittest


def run_process(args: List[str], log_file_path) -> subprocess.CompletedProcess:
    env = os.environ
    env["PYTHONUNBUFFERED"] = "True"
    with open(log_file_path, "at", encoding="utf-8") as fh:
        with subprocess.Popen(
            args,
            bufsize=1,
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
        ) as proc:
            while (ret_code:=proc.poll()) is None:
                line = proc.stdout.readline()
                sys.stdout.write(line)
                fh.write(line)

    return ret_code


class TestLogCapture(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmpdir = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmpdir.cleanup)
        cls.test_child_log_path = Path(cls.tmpdir.name) / "test_child-process.log"

        cmd = ["python", "child_process.py"]

        completed_proc = run_process(cmd, cls.test_child_log_path)

        print("Stream done")
        print(f"Process return code: {completed_proc}")

    def test_smoke(self):
        print("Test 1")

    def test_child_process_written_to_file(self):
        print("\n")
        print("Printing from test_child_process_written_to_file")
        with open(self.test_child_log_path, "r", encoding="utf-8") as fh:
            for line in fh:
                print(line.rstrip())
