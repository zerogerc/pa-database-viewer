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


class CollectionData:

    def __init__(self, root: Path):
        self.root = root

    @property
    def path_relations_db(self) -> Path:
        return self.root / 'relations.db'

    @property
    def path_suggest_db(self) -> Path:
        return self.root / 'suggest.db'
