from pathlib import Path


class PreprocessTask:
    def __init__(self, name: str, directory: Path):
        self.directory = directory
        self.name = name

    @property
    def is_complete(self) -> bool:
        return self.path_is_complete.exists()

    def set_is_complete(self):
        assert not self.is_complete
        self.path_is_complete.write_text('OK')

    @property
    def path_relations_db(self) -> Path:
        return self.directory / 'relations.db'

    @property
    def path_suggest_db(self) -> Path:
        return self.directory / 'suggest.db'

    @property
    def path_is_complete(self) -> Path:
        return self.directory / f'.{self.name}.complete'
