import pytest

from server.data.relations import ExtractedRelationsDatabase, ExtractedRelationEntry, MergedRelation, RelationPmidProb, \
    BioEntity
from server.entities import GENE, CHEMICAL, DISEASE
from server.utils import create_tempdir, relation_entry_from_entities


@pytest.fixture(scope='session')
def relations_db_session() -> ExtractedRelationsDatabase:
    with create_tempdir() as tempdir:
        db = ExtractedRelationsDatabase(tempdir / 'relations.db')
        ExtractedRelationEntry.metadata.create_all(db.db_engine)
        yield db


@pytest.fixture()
def relations_db(relations_db_session: ExtractedRelationsDatabase):
    relations_db_session.delete_all()
    yield relations_db_session


def test_get_entity_pairs(relations_db: ExtractedRelationsDatabase):
    c1 = BioEntity('c1', 'cn1', CHEMICAL)
    g1, g2 = BioEntity('g1', 'gn1', GENE), BioEntity('g2', 'gn2', GENE)
    relations_db.insert_entries([
        relation_entry_from_entities(c1, g1, 'expression', pmid='1', prob=0.9),
        relation_entry_from_entities(c1, g1, 'expression', pmid='2', prob=0.5),
        relation_entry_from_entities(c1, g2, 'transport', pmid='3', prob=0.1)
    ])

    pairs = list(relations_db.get_entity_pairs())
    assert len(pairs) == 2
    assert pairs[0] == (c1, g1)
    assert pairs[1] == (c1, g2)


def test_merged_relations_eid1_filter(relations_db: ExtractedRelationsDatabase):
    c1 = BioEntity('c1', 'cn1', CHEMICAL)
    g1, g2 = BioEntity('g1', 'gn1', GENE), BioEntity('g2', 'gn2', GENE)
    d1 = BioEntity('d1', 'dn1', DISEASE)

    relations_db.insert_entries([
        relation_entry_from_entities(c1, g1, 'expression', pmid='1', prob=0.9),
        relation_entry_from_entities(c1, g1, 'expression', pmid='2', prob=0.5),
        relation_entry_from_entities(c1, g2, 'transport', pmid='3', prob=1.0),
        relation_entry_from_entities(g1, d1, 'marker', pmid='4', prob=0.1)
    ])

    merged = list(relations_db.get_merged_relations(id1='c1'))
    assert len(merged) == 2
    assert merged[0] == MergedRelation(c1, g2, 'transport', prob=1.0, pmids=['3'])
    assert merged[1] == MergedRelation(c1, g1, 'expression', prob=0.9, pmids=['1', '2'])


def test_merged_relations_eid2_filter(relations_db: ExtractedRelationsDatabase):
    c1 = BioEntity('c1', 'cn1', CHEMICAL)
    g1, g2 = BioEntity('g1', 'gn1', GENE), BioEntity('g2', 'gn2', GENE)
    d1 = BioEntity('d1', 'dn1', DISEASE)

    relations_db.insert_entries([
        relation_entry_from_entities(c1, g1, 'expression', pmid='1', prob=0.9),
        relation_entry_from_entities(c1, g1, 'expression', pmid='2', prob=0.5),
        relation_entry_from_entities(c1, g2, 'transport', pmid='3', prob=1.0),
        relation_entry_from_entities(g1, d1, 'marker', pmid='4', prob=0.1)
    ])

    merged = list(relations_db.get_merged_relations(id2='g2'))
    assert len(merged) == 1
    assert merged[0] == MergedRelation(c1, g2, 'transport', prob=1.0, pmids=['3'])


def test_merged_relations_pmid_filter(relations_db: ExtractedRelationsDatabase):
    c1 = BioEntity('c1', 'cn1', CHEMICAL)
    g1, g2 = BioEntity('g1', 'gn1', GENE), BioEntity('g2', 'gn2', GENE)
    d1 = BioEntity('d1', 'dn1', DISEASE)

    relations_db.insert_entries([
        relation_entry_from_entities(c1, g1, 'expression', pmid='1', prob=0.9),
        relation_entry_from_entities(c1, g1, 'expression', pmid='2', prob=0.5),
        relation_entry_from_entities(g1, d1, 'marker', pmid='1', prob=0.1)
    ])

    merged = list(relations_db.get_merged_relations(pmid='1'))
    assert len(merged) == 2
    assert merged[0] == MergedRelation(c1, g1, 'expression', prob=0.9, pmids=['1'])
    assert merged[1] == MergedRelation(g1, d1, 'marker', prob=0.1, pmids=['1'])


def test_get_relation_pmid_probs_all_pmids(relations_db: ExtractedRelationsDatabase):
    c1 = BioEntity('c1', 'cn1', CHEMICAL)
    g1, g2 = BioEntity('g1', 'gn1', GENE), BioEntity('g2', 'gn2', GENE)

    relations_db.insert_entries([
        relation_entry_from_entities(c1, g1, 'expression', pmid='1', prob=0.9),
        relation_entry_from_entities(c1, g1, 'expression', pmid='2', prob=0.5),
        relation_entry_from_entities(c1, g2, 'transport', pmid='3', prob=1.0),
    ])

    probs = list(relations_db.get_relation_pmid_probs(id1='c1', id2='g1', label='expression', pmids=['1', '2', '3']))
    assert set(probs) == {RelationPmidProb('1', 0.9), RelationPmidProb('2', 0.5)}


def test_get_relation_pmid_probs_pmids_subset(relations_db: ExtractedRelationsDatabase):
    c1 = BioEntity('c1', 'cn1', CHEMICAL)
    g1, g2 = BioEntity('g1', 'gn1', GENE), BioEntity('g2', 'gn2', GENE)

    relations_db.insert_entries([
        relation_entry_from_entities(c1, g1, 'expression', pmid='1', prob=0.9),
        relation_entry_from_entities(c1, g1, 'expression', pmid='2', prob=0.5),
        relation_entry_from_entities(c1, g2, 'transport', pmid='3', prob=1.0),
    ])

    probs = list(relations_db.get_relation_pmid_probs(id1='c1', id2='g1', label='expression', pmids=['2']))
    assert set(probs) == {RelationPmidProb('2', 0.5)}


def test_get_extracted_relations(relations_db: ExtractedRelationsDatabase):
    c1 = BioEntity('c1', 'cn1', CHEMICAL)
    g1, g2 = BioEntity('g1', 'gn1', GENE), BioEntity('g2', 'gn2', GENE)

    relations_db.insert_entries([
        relation_entry_from_entities(c1, g1, 'expression', pmid='1', prob=0.9),
        relation_entry_from_entities(c1, g1, 'expression', pmid='2', prob=0.5),
        relation_entry_from_entities(c1, g2, 'transport', pmid='3', prob=1.0),
    ])

    extracted = list(relations_db.get_extracted_relations())
    assert len(extracted) == 3
    assert extracted[0].as_dict() == relation_entry_from_entities(c1, g1, 'expression', pmid='1', prob=0.9).as_dict()
    assert extracted[1].as_dict() == relation_entry_from_entities(c1, g1, 'expression', pmid='2', prob=0.5).as_dict()
    assert extracted[2].as_dict() == relation_entry_from_entities(c1, g2, 'transport', pmid='3', prob=1.0).as_dict()
