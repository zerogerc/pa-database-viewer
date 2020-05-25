import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator


@contextmanager
def create_tempdir() -> Generator[Path, None, None]:
    tempdir = tempfile.mkdtemp()
    try:
        yield Path(tempdir)
    finally:
        if tempdir:
            shutil.rmtree(tempdir)
