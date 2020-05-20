from pathlib import Path
from typing import Any, Iterator, Optional, Tuple, Dict, List

from sqlalchemy import create_engine, MetaData, Table, Column, Float, String, select, func, Integer, desc

metadata = MetaData()

RELATIONS_TABLE = Table(
    'extracted_relations', metadata,
    Column('name1', String),
    Column('id1', String),
    Column('group1', String),
    Column('name2', String),
    Column('id2', String),
    Column('group2', String),
    Column('label', String),
    Column('pmid', String),
    Column('prob', Float),
    Column('in_ctd', Integer)
)

NAME_1 = RELATIONS_TABLE.columns.name1
ID_1 = RELATIONS_TABLE.columns.id1
GROUP_1 = RELATIONS_TABLE.columns.group1
NAME_2 = RELATIONS_TABLE.columns.name2
ID_2 = RELATIONS_TABLE.columns.id2
GROUP_2 = RELATIONS_TABLE.columns.group2
LABEL = RELATIONS_TABLE.columns.label
PMID = RELATIONS_TABLE.columns.pmid
PROB = RELATIONS_TABLE.columns.prob
IN_CTD = RELATIONS_TABLE.columns.in_ctd


class PaperAnalyzerDatabase:

    def __init__(self, db_path: Path):
        self.db_engine = create_engine('sqlite:///{}'.format(db_path))

    def get_relation_type_probabilities(self, r_type: str) -> List[float]:
        with self.db_engine.connect() as connection:
            query = select([PROB]).where(LABEL == r_type)
            yield from (row['prob'] for row in connection.execute(query))

    def get_merged_relations(self, id1: str, id2: str, pmid: str, in_ctd: Optional[int] = None) -> Iterator[Any]:
        with self.db_engine.connect() as connection:
            query = select([
                NAME_1, ID_1, GROUP_1, NAME_2, ID_2, GROUP_2, LABEL,
                func.group_concat(PMID.distinct()).label('pmids'),
                func.max(PROB).label('prob'),
            ])

            if id1:
                query = query.where(ID_1 == id1)
            if id2:
                query = query.where(ID_2 == id2)
            if pmid:
                query = query.where(PMID == pmid)
            if in_ctd is not None:
                query = query.where(IN_CTD == in_ctd)

            query = query.group_by(ID_1, GROUP_1, ID_2, GROUP_2, LABEL)
            query = query.order_by(desc('prob')).limit(100)
            yield from (self._relation_row_to_dict(row) for row in connection.execute(query))

    def _relation_row_to_dict(self, row: Tuple) -> Dict[str, Any]:
        result = dict(row)
        result['pmids'] = result['pmids'].split(',')
        return result

    def get_relation_pmid_probs(self, id1: str, id2: str, label: str, pmids: List[str]) -> Iterator[Any]:
        with self.db_engine.connect() as connection:
            query = select([PMID, PROB]) \
                .where(ID_1 == id1) \
                .where(ID_2 == id2) \
                .where(label == label) \
                .where(PMID.in_(pmids))

            yield from (dict(row) for row in connection.execute(query))


def main():
    db_path = Path('/Users/Uladzislau.Sazanovich/dev/data/pa/paper-analyzer.db')
    engine = create_engine('sqlite:///{}'.format(db_path))

    with engine.connect() as connection:
        query = select([
            RELATIONS_TABLE.columns.name1,
            RELATIONS_TABLE.columns.id1,
            RELATIONS_TABLE.columns.group1,
            RELATIONS_TABLE.columns.name2,
            RELATIONS_TABLE.columns.id2,
            RELATIONS_TABLE.columns.group2,
            RELATIONS_TABLE.columns.label,
            func.max(RELATIONS_TABLE.columns.prob).label('prob'),
            func.group_concat(RELATIONS_TABLE.columns.pmid).label('pmids')
        ]) \
            .where(RELATIONS_TABLE.columns.id1 == "MESH:D003042") \
            .where(RELATIONS_TABLE.columns.id2 == "MESH:D012640") \
            .group_by(RELATIONS_TABLE.columns.id1, RELATIONS_TABLE.columns.id2, RELATIONS_TABLE.columns.label)
        result = connection.execute(query)
        result = [dict(row) for row in result]
        for r in result:
            print(r)


if __name__ == '__main__':
    main()
