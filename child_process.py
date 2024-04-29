# child_process.py

import contextlib
import logging
import logging.handlers
import sys
from time import sleep
from typing import Generator, Optional, TextIO


logger = logging.getLogger(__name__)


LOG_FORMAT = "%(asctime)s %(levelname)s:%(name)s:%(lineno)d:%(message)s"


@contextlib.contextmanager
def set_logging(
    console_stream: Optional[TextIO] = None,
) -> Generator[None, None, None]:
    if console_stream is None:
        console_stream = sys.stderr

    console_handler = logging.StreamHandler(console_stream)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    root = logging.getLogger()
    root.addHandler(console_handler)
    old_level = root.level
    root.setLevel(logging.DEBUG)

    try:
        yield
    finally:
        root.setLevel(old_level)
        root.removeHandler(console_handler)
        console_handler.flush()
        console_handler.close()

if __name__ == "__main__":
    with set_logging():
        for i in range(5):
            logger.debug(f"Stderr: Spam! {i}")
            # Sleep to simulate some other work
            sleep(1)
            if i % 2:
                print(f"Stdout: Ham! {i}")
