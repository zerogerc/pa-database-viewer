from pathlib import Path
from typing import Any, Iterator

from sqlalchemy import create_engine, MetaData, Table, Column, Float, String, select, func

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
)


class PaperAnalyzerDatabase:

    def __init__(self, db_path: Path):
        self.db_engine = create_engine('sqlite:///{}'.format(db_path))

    def get_raw_relations_by_ids(self, id1: str, id2: str) -> Iterator[Any]:
        with self.db_engine.connect() as connection:
            query = select([RELATIONS_TABLE]) \
                .where(RELATIONS_TABLE.columns.id1 == id1) \
                .where(RELATIONS_TABLE.columns.id2 == id2)
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
