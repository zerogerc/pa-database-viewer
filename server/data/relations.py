from pathlib import Path
from typing import Any, Iterator, Optional, Tuple, Dict, List

import attr
from sqlalchemy import create_engine, Column, Float, String, select, func, Integer, desc
from sqlalchemy.orm import sessionmaker

from server.data.base import Base
from server.entities import SUPPORTED_ENTITY_GROUPS


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

    def __init__(self,
                 name1: str, id1: str, group1: str,
                 name2: str, id2: str, group2: str,
                 label: str, pmid: str, prob: float, in_ctd: int):
        self.name1, self.id1, self.group1 = name1, id1, group1
        self.name2, self.id2, self.group2 = name2, id2, group2
        self.label = label
        self.pmid = pmid
        self.prob = prob
        self.in_ctd = in_ctd

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@attr.s(auto_attribs=True, frozen=True)
class BioEntity:
    id: str
    name: str
    group: str = attr.ib(validator=lambda _, a, val: val in SUPPORTED_ENTITY_GROUPS)

    @staticmethod
    def extract_1_from_row(row: Dict[str, Any]) -> 'BioEntity':
        return BioEntity(id=row[ExtractedRelationEntry.id1.key],
                         name=row[ExtractedRelationEntry.name1.key],
                         group=row[ExtractedRelationEntry.group1.key])

    @staticmethod
    def extract_2_from_row(row: Dict[str, Any]) -> 'BioEntity':
        return BioEntity(id=row[ExtractedRelationEntry.id2.key],
                         name=row[ExtractedRelationEntry.name2.key],
                         group=row[ExtractedRelationEntry.group2.key])


@attr.s(auto_attribs=True, frozen=True)
class MergedRelation:
    entity1: BioEntity
    entity2: BioEntity
    label: str
    pmids: List[str]
    prob: float

    @staticmethod
    def from_row(row: Dict[str, Any]) -> 'MergedRelation':
        return MergedRelation(
            entity1=BioEntity.extract_1_from_row(row), entity2=BioEntity.extract_2_from_row(row),
            label=row['label'], pmids=row['pmids'].split(','), prob=row['prob']
        )


@attr.s(auto_attribs=True, frozen=True)
class RelationPmidProb:
    pmid: str
    prob: float

    @staticmethod
    def from_row(row: Dict[str, Any]) -> 'RelationPmidProb':
        return RelationPmidProb(row['pmid'], row['prob'])


COLUMNS_ENTITY_1 = [ExtractedRelationEntry.name1, ExtractedRelationEntry.id1, ExtractedRelationEntry.group1]
COLUMNS_ENTITY_2 = [ExtractedRelationEntry.name2, ExtractedRelationEntry.id2, ExtractedRelationEntry.group2]


class ExtractedRelationsDatabase:

    def __init__(self, db_path: Path):
        self.db_engine = create_engine('sqlite:///{}'.format(db_path))
        self.session_maker = sessionmaker(bind=self.db_engine)

    def insert_entries(self, entries: List[ExtractedRelationEntry]):
        session = self.session_maker()
        session.add_all(entries)
        session.commit()

    def delete_all(self):
        session = self.session_maker()
        session.query(ExtractedRelationEntry).delete()
        session.commit()

    def get_extracted_relations(self) -> Iterator[ExtractedRelationEntry]:
        session = self.session_maker()
        query = select([ExtractedRelationEntry])
        yield from (ExtractedRelationEntry(**dict(row)) for row in session.connection().execute(query))

    def get_entity_pairs(self) -> Iterator[Tuple[BioEntity, BioEntity]]:
        with self.db_engine.connect() as connection:
            query = select(COLUMNS_ENTITY_1 + COLUMNS_ENTITY_2).distinct()
            yield from (
                (BioEntity.extract_1_from_row(row), BioEntity.extract_2_from_row(row))
                for row in connection.execute(query)
            )

    def get_merged_relations(self, id1: Optional[str] = None, id2: Optional[str] = None, pmid: Optional[str] = None,
                             in_ctd: Optional[int] = None) -> Iterator[MergedRelation]:
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
                MergedRelation.from_row(row)
                for row in connection.execute(query)
            )

    def get_relation_pmid_probs(self, id1: str, id2: str, label: str, pmids: List[str]) -> Iterator[Any]:
        with self.db_engine.connect() as connection:
            query = select([ExtractedRelationEntry.pmid, ExtractedRelationEntry.prob]) \
                .where(ExtractedRelationEntry.id1 == id1) \
                .where(ExtractedRelationEntry.id2 == id2) \
                .where(ExtractedRelationEntry.label == label) \
                .where(ExtractedRelationEntry.pmid.in_(pmids))

            yield from (RelationPmidProb.from_row(row) for row in connection.execute(query))

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
