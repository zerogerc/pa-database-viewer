import json
from pathlib import Path
from typing import Dict, Optional

from server.data.relations import ExtractedRelationsDatabase
from server.data.stats import CollectionStats
from server.data.suggest import SuggestDatabase


class CollectionData:

    def __init__(self, root: Path):
        self.root = root
        self._relations_db: Optional[ExtractedRelationsDatabase] = None
        self._suggest_db: Optional[SuggestDatabase] = None

    @property
    def relations_db(self) -> ExtractedRelationsDatabase:
        if self._relations_db is None:
            self._relations_db = ExtractedRelationsDatabase(self.path_relations_db)
        return self._relations_db

    @property
    def suggest_db(self) -> SuggestDatabase:
        if self._suggest_db is None:
            self._suggest_db = SuggestDatabase(self.path_suggest_db)
        return self._suggest_db

    @property
    def stats(self) -> CollectionStats:
        return CollectionStats.from_dict(json.loads(self.path_stats.read_text()))

    @property
    def path_relations_tsv(self) -> Path:
        return self.root / 'relations.tsv.gz'

    @property
    def path_relations_db(self) -> Path:
        return self.root / 'relations.db'

    @property
    def path_suggest_db(self) -> Path:
        return self.root / 'suggest.db'

    @property
    def path_stats(self) -> Path:
        return self.root / 'stats.json'


def read_collections(directory: Path) -> Dict[str, CollectionData]:
    collections: Dict[str, CollectionData] = {}
    for collection_dir in directory.iterdir():
        if collection_dir.is_dir():
            collections[collection_dir.name] = CollectionData(collection_dir)
    return collections
