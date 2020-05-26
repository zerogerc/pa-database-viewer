from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterator, Optional, Tuple, Dict, List

from sqlalchemy import create_engine, Column, Float, String, select, func, Integer, desc

from server.data.base import Base


class ExtractedRelationEntry(Base):
    __tablename__ = 'extracted_relations'

    name1 = Column(String)
    id1 = Column(String, primary_key=True)
    group1 = Column(String)
    name2 = Column(String)
    id2 = Column(String, primary_key=True)
    group2 = Column(String)
    label = Column(String, primary_key=True)
    pmid = Column(String, primary_key=True)
    prob = Column(Float)
    in_ctd = Column(Integer)


COLUMNS_ENTITY_1 = [ExtractedRelationEntry.name1, ExtractedRelationEntry.id1, ExtractedRelationEntry.group1]
COLUMNS_ENTITY_2 = [ExtractedRelationEntry.name2, ExtractedRelationEntry.id2, ExtractedRelationEntry.group2]


class BioEntity(SimpleNamespace):
    id: str
    name: str
    group: str

    @staticmethod
    def extract_1_from_row(row) -> 'BioEntity':
        return BioEntity(id=row[ExtractedRelationEntry.id1.key],
                         name=row[ExtractedRelationEntry.name1.key],
                         group=row[ExtractedRelationEntry.group1.key])

    @staticmethod
    def extract_2_from_row(row) -> 'BioEntity':
        return BioEntity(id=row[ExtractedRelationEntry.id2.key],
                         name=row[ExtractedRelationEntry.name2.key],
                         group=row[ExtractedRelationEntry.group2.key])


class PaperAnalyzerDatabase:

    def __init__(self, db_path: Path):
        self.db_engine = create_engine('sqlite:///{}'.format(db_path))

    def get_entity_pairs(self) -> Iterator[Tuple[BioEntity, BioEntity]]:
        with self.db_engine.connect() as connection:
            query = select(COLUMNS_ENTITY_1 + COLUMNS_ENTITY_2).distinct()
            yield from (
                (BioEntity.extract_1_from_row(row), BioEntity.extract_2_from_row(row))
                for row in connection.execute(query)
            )

    def get_relation_types(self) -> Iterator[str]:
        with self.db_engine.connect() as connection:
            query = select([ExtractedRelationEntry.label]).distinct(ExtractedRelationEntry.label)
            yield from (
                row[ExtractedRelationEntry.label.key]
                for row in connection.execute(query)
            )

    def get_relation_type_counts(self, min_prob: float, max_prob: float) -> Iterator[Tuple[str, int]]:
        with self.db_engine.connect() as connection:
            query = select([
                ExtractedRelationEntry.label,
                func.count().label('count')
            ]) \
                .where(min_prob < ExtractedRelationEntry.prob) \
                .where(ExtractedRelationEntry.prob <= max_prob) \
                .group_by(ExtractedRelationEntry.label)
            yield from (
                (row[ExtractedRelationEntry.label.key], row['count'])
                for row in connection.execute(query)
            )

    def get_relation_pmid_probs(self, id1: str, id2: str, label: str, pmids: List[str]) -> Iterator[Any]:
        with self.db_engine.connect() as connection:
            query = select([ExtractedRelationEntry.pmid, ExtractedRelationEntry.prob]) \
                .where(ExtractedRelationEntry.id1 == id1) \
                .where(ExtractedRelationEntry.id2 == id2) \
                .where(ExtractedRelationEntry.label == label) \
                .where(ExtractedRelationEntry.pmid.in_(pmids))

            yield from (dict(row) for row in connection.execute(query))

    def get_merged_relations(self, id1: Optional[str], id2: Optional[str], pmid: Optional[str],
                             in_ctd: Optional[int] = None) -> Iterator[Any]:
        if id1 is None and id2 is None and pmid is None:
            return []

        with self.db_engine.connect() as connection:
            query = select([
                ExtractedRelationEntry.name1, ExtractedRelationEntry.id1, ExtractedRelationEntry.group1,
                ExtractedRelationEntry.name2, ExtractedRelationEntry.id2, ExtractedRelationEntry.group2,
                ExtractedRelationEntry.label,
                func.group_concat(ExtractedRelationEntry.pmid.distinct()).label('pmids'),
                func.max(ExtractedRelationEntry.prob).label('prob'),
            ])

            if id1:
                query = query.where(ExtractedRelationEntry.id1 == id1)
            if id2:
                query = query.where(ExtractedRelationEntry.id2 == id2)
            if pmid:
                query = query.where(ExtractedRelationEntry.pmid == pmid)
            if in_ctd is not None:
                query = query.where(ExtractedRelationEntry.in_ctd == in_ctd)

            query = query.group_by(ExtractedRelationEntry.id1, ExtractedRelationEntry.group1,
                                   ExtractedRelationEntry.id2, ExtractedRelationEntry.group2,
                                   ExtractedRelationEntry.label)
            query = query.order_by(desc('prob')).limit(100)
            yield from (
                self._relation_row_to_dict(row)
                for row in connection.execute(query)
            )

    def _relation_row_to_dict(self, row: Tuple) -> Dict[str, Any]:
        result = dict(row)
        result['pmids'] = result['pmids'].split(',')
        return result


def main():
    db_path = Path('/Users/Uladzislau.Sazanovich/dev/pa-database-viewer/data/pa-covid.db')
    db = PaperAnalyzerDatabase(db_path)

    for e1, e2 in db.get_entity_pairs():
        print(e1, e2)


if __name__ == '__main__':
    main()
