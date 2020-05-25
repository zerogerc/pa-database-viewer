from pathlib import Path

from server.utils import CollectionData


class PreprocessTask:
    def __init__(self, name: str, directory: CollectionData):
        self.directory = directory
        self.name = name

    @property
    def is_complete(self) -> bool:
        return self.path_is_complete.exists()

    def set_is_complete(self):
        assert not self.is_complete
        self.path_is_complete.write_text('OK')

    @property
    def path_is_complete(self) -> Path:
        return self.directory.root / f'.{self.name}.complete'
