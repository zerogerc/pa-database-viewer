import pytest

from server.data.suggest import SuggestDatabase, SuggestEntry
from server.utils import create_tempdir


@pytest.fixture(scope='session')
def suggest_db_session() -> SuggestDatabase:
    with create_tempdir() as tempdir:
        yield SuggestDatabase(tempdir / 'suggest.db')


@pytest.fixture()
def suggest_db(suggest_db_session: SuggestDatabase):
    suggest_db_session.delete_all()
    yield suggest_db_session


def test_suggest_empty(suggest_db: SuggestDatabase):
    assert suggest_db.suggest('') == []


def test_suggest_single_query_is_not_a_substring(suggest_db: SuggestDatabase):
    suggest_db.insert_entries([
        SuggestEntry('123', 'chemical', 'chemical')
    ])

    suggest = suggest_db.suggest('gene')
    assert len(suggest) == 0


def test_suggest_single_query_is_substring(suggest_db: SuggestDatabase):
    suggest_db.insert_entries([
        SuggestEntry('123', 'chemical', 'chemical')
    ])

    suggest = suggest_db.suggest('chem')
    assert len(suggest) == 1
    assert suggest[0].id == '123'
    assert suggest[0].name == 'chemical'
    assert suggest[0].cname == 'chemical'


def test_suggest_multiple(suggest_db: SuggestDatabase):
    suggest_db.insert_entries([
        SuggestEntry('100', 'gene', 'gene'),
        SuggestEntry('125', 'chemical_1', 'chemical'),
        SuggestEntry('126', 'chemical_2', 'chemical')
    ])

    suggest = suggest_db.suggest('chem')
    assert {s.id for s in suggest} == {'125', '126'}
