from pathlib import Path
from typing import Dict, Optional

from server.db.relations import PaperAnalyzerDatabase
from server.db.suggest import SuggestDatabase


class CollectionData:

    def __init__(self, root: Path):
        self.root = root
        self._relations_db: Optional[PaperAnalyzerDatabase] = None
        self._suggest_db: Optional[SuggestDatabase] = None

    @property
    def relations_db(self) -> PaperAnalyzerDatabase:
        if self._relations_db is None:
            self._relations_db = PaperAnalyzerDatabase(self.path_relations_db)
        return self._relations_db

    @property
    def suggest_db(self) -> SuggestDatabase:
        if self._suggest_db is None:
            self._suggest_db = SuggestDatabase(self.path_suggest_db)
        return self._suggest_db

    @property
    def path_relations_db(self) -> Path:
        return self.root / 'relations.db'

    @property
    def path_suggest_db(self) -> Path:
        return self.root / 'suggest.db'


def read_collections(directory: Path) -> Dict[str, CollectionData]:
    collections: Dict[str, CollectionData] = {}
    for collection_dir in directory.iterdir():
        if collection_dir.is_dir():
            collections[collection_dir.name] = CollectionData(collection_dir)
    return collections
