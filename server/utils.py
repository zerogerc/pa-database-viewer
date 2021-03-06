import gzip
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, IO, Any

from server.data.relations import BioEntity, ExtractedRelationEntry


@contextmanager
def create_tempdir() -> Generator[Path, None, None]:
    tempdir = tempfile.mkdtemp()
    try:
        yield Path(tempdir)
    finally:
        if tempdir:
            shutil.rmtree(tempdir)


@contextmanager
def open_file(path: Path, mode: str = 'rt') -> Generator[IO[Any], None, None]:
    if path.name.endswith('.gz'):
        with gzip.open(str(path.resolve()), mode=mode) as f:
            yield f
    else:
        with path.open(mode=mode) as f:
            yield f


def relation_entry_from_entities(e1: BioEntity, e2: BioEntity,
                                 label: str, pmid: str, prob: float) -> ExtractedRelationEntry:
    return ExtractedRelationEntry(
        e1.name, e1.id, e1.group, e2.name, e2.id, e2.group,
        label=label, pmid=pmid, prob=prob, in_ctd=0
    )
