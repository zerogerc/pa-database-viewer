import pytest

from server.collection import CollectionData
from server.data.relations import ExtractedRelationEntry, BioEntity
from server.data.stats import RTypeCounts, EntityGroupCounts, EntityIdCount
from server.entities import CHEMICAL, GENE, DISEASE
from server.tasks.calculate_stats import CalculateStatsTask
from server.utils import create_tempdir, relation_entry_from_entities


@pytest.fixture()
def collection_data() -> CollectionData:
    with create_tempdir() as tempdir:
        data = CollectionData(tempdir)
        ExtractedRelationEntry.metadata.create_all(data.relations_db.db_engine)
        yield data


def test_stats_empty(collection_data: CollectionData):
    task = CalculateStatsTask(collection_data)
    task.execute()
    stats = collection_data.stats

    assert stats.total_relations == 0
    assert stats.total_entities == 0


def test_stats_total(collection_data: CollectionData):
    c1 = BioEntity('c1', 'cn1', CHEMICAL)
    g1, g2 = BioEntity('g1', 'gn1', GENE), BioEntity('g2', 'gn2', GENE)
    collection_data.relations_db.insert_entries([
        relation_entry_from_entities(c1, g1, 'expression', pmid='1', prob=0.9),
        relation_entry_from_entities(c1, g2, 'transport', pmid='2', prob=0.1)
    ])

    task = CalculateStatsTask(collection_data)
    task.execute()
    stats = collection_data.stats

    assert stats.total_relations == 2
    assert stats.total_entities == 3


def test_stats_r_type_counts(collection_data: CollectionData):
    c1 = BioEntity('c1', 'cn1', CHEMICAL)
    g1, g2 = BioEntity('g1', 'gn1', GENE), BioEntity('g2', 'gn2', GENE)
    collection_data.relations_db.insert_entries([
        relation_entry_from_entities(c1, g1, 'expression', pmid='1', prob=0.99),
        relation_entry_from_entities(c1, g2, 'transport', pmid='2', prob=0.01),
        relation_entry_from_entities(c1, g2, 'transport', pmid='3', prob=0.02),
        relation_entry_from_entities(c1, g2, 'transport', pmid='4', prob=0.09)
    ])

    task = CalculateStatsTask(collection_data)
    task.execute()
    stats = collection_data.stats

    assert stats.r_type_counts == [
        RTypeCounts('expression', [0] * 19 + [1]),
        RTypeCounts('transport', [2, 1] + [0] * 18)
    ]


def test_stats_entities(collection_data: CollectionData):
    c1 = BioEntity('c1', 'cn1', CHEMICAL)
    g1, g2 = BioEntity('g1', 'gn1', GENE), BioEntity('g2', 'gn2', GENE)
    d1 = BioEntity('d1', 'dn1', DISEASE)
    collection_data.relations_db.insert_entries([
        relation_entry_from_entities(c1, g1, 'expression', pmid='1', prob=0.99),
        relation_entry_from_entities(c1, g2, 'transport', pmid='2', prob=0.01),
        relation_entry_from_entities(c1, g2, 'transport', pmid='3', prob=0.02),
        relation_entry_from_entities(g2, d1, 'marker', pmid='4', prob=0.09)
    ])

    task = CalculateStatsTask(collection_data)
    task.execute()
    stats = collection_data.stats

    assert stats.chemicals == EntityGroupCounts(total=1, relations=3, top=[EntityIdCount('c1', 3)])
    assert stats.genes == EntityGroupCounts(total=2, relations=4, top=[EntityIdCount('g2', 3), EntityIdCount('g1', 1)])
    assert stats.diseases == EntityGroupCounts(total=1, relations=1, top=[EntityIdCount('d1', 1)])
