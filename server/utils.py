import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from server.data.relations import BioEntity, ExtractedRelationEntry


@contextmanager
def create_tempdir() -> Generator[Path, None, None]:
    tempdir = tempfile.mkdtemp()
    try:
        yield Path(tempdir)
    finally:
        if tempdir:
            shutil.rmtree(tempdir)


def relation_entry_from_entities(e1: BioEntity, e2: BioEntity,
                                 label: str, pmid: str, prob: float) -> ExtractedRelationEntry:
    return ExtractedRelationEntry(
        e1.name, e1.id, e1.group, e2.name, e2.id, e2.group,
        label=label, pmid=pmid, prob=prob, in_ctd=0
    )
