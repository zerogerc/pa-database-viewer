from pathlib import Path
from typing import List

from sqlalchemy import Column, String, create_engine, select
from sqlalchemy.orm import sessionmaker

from server.data.base import Base


class SuggestEntry(Base):
    __tablename__ = 'suggest'

    id = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    cname = Column(String)

    def __init__(self, id: str, name: str, cname: str):
        self.id = id
        self.name = name
        self.cname = cname

    def __repr__(self):
        return f'{self.name} ({self.id}) Most common name = {self.cname}'


class SuggestDatabase:
    def __init__(self, path: Path):
        self.path = path
        self.engine = create_engine(f'sqlite:///{str(path)}')
        self.engine.execute(
            """
            CREATE TABLE IF NOT EXISTS suggest (
                id TEXT,
                name TEXT,
                cname TEXT,
                PRIMARY KEY (id, name) ON CONFLICT REPLACE
            );
            """
        )
        self.session_maker = sessionmaker(bind=self.engine)

    def insert_entries(self, entries: List[SuggestEntry]):
        session = self.session_maker()
        session.add_all(entries)
        session.commit()

    def delete_all(self):
        session = self.session_maker()
        session.query(SuggestEntry).delete()
        session.commit()

    def suggest(self, query: str) -> List[SuggestEntry]:
        session = self.session_maker()
        return session.query(SuggestEntry).filter(SuggestEntry.name.like(query + '%'))[0:10]


def main():
    db = SuggestDatabase(Path('/Users/Uladzislau.Sazanovich/dev/pa-database-viewer/data/suggest-temp.db'))
    db.insert_entries([
        SuggestEntry('123', 'chemical', 'chemical'),
        SuggestEntry('123', 'chemical', 'chemical'),
        SuggestEntry('123', 'chemical', 'chemical'),
        SuggestEntry('124', 'chemicalX', 'chemical'),
    ])

    query = select([SuggestEntry.name])
    with db.engine.connect() as connection:
        print([row[SuggestEntry.name.key] for row in connection.execute(query)])

    result = db.suggest('n')
    print(result)

    result = db.suggest('c')
    print(result)


if __name__ == '__main__':
    main()
