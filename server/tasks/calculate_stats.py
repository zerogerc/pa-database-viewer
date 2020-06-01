import json
import logging
from collections import defaultdict, Counter
from typing import List, Dict, Tuple

import attr

from server.collection import CollectionData
from server.data.stats import RTypeCounts, EntityGroupCounts, EntityIdCount, CollectionStats
from server.entities import CHEMICAL, GENE, DISEASE
from server.tasks.task import PreprocessTask

G_LOG = logging.getLogger(__name__)


class CalculateStatsTask(PreprocessTask):
    def __init__(self, directory: CollectionData, *, override_previous: bool = False):
        super(CalculateStatsTask, self).__init__('calculate-stats', directory, override_previous=override_previous)

    def run_preprocessing(self):
        total_relations, r_type_counts = self._calculate_r_type_counts()
        all_entity_group_counts = self._calculate_entity_group_counts()
        stats = CollectionStats(
            total_relations=total_relations,
            r_type_counts=r_type_counts,
            total_entities=sum([c.total for _, c in all_entity_group_counts.items()]),
            chemicals=all_entity_group_counts[CHEMICAL],
            genes=all_entity_group_counts[GENE],
            diseases=all_entity_group_counts[DISEASE]
        )

        self.directory.path_stats.write_text(json.dumps(attr.asdict(stats, recurse=True), indent=4))

    def _calculate_entity_group_counts(self) -> Dict[str, EntityGroupCounts]:
        result: Dict[str, EntityGroupCounts] = defaultdict(EntityGroupCounts)

        group_eids: Dict[str, Counter] = defaultdict(Counter)
        for relation in self.directory.relations_db.get_extracted_relations():
            for group, eid in [(relation.group1, relation.id1), (relation.group2, relation.id2)]:
                assert ';' not in eid
                result[group].relations += 1
                group_eids[group].update({eid: 1})

        for group, eids in group_eids.items():
            result[group].total = len(eids)
            result[group].top = [EntityIdCount(eid, count) for eid, count in eids.most_common(n=10)]
        return result

    def _calculate_r_type_counts(self) -> Tuple[int, List[RTypeCounts]]:
        relations_db = self.directory.relations_db

        num_buckets = 20
        probs = [i / num_buckets for i in range(num_buckets + 1)]

        r_type_counts: Dict[str, List[int]] = {r: [] for r in list(relations_db.get_relation_types())}
        for min_prob, max_prob in zip(probs, probs[1:]):
            G_LOG.info(f'{self.name} | Getting stats for [{min_prob} .. {max_prob}]')
            for r in r_type_counts.keys():
                r_type_counts[r].append(0)
            for r_type, count in relations_db.get_relation_type_counts(min_prob=min_prob, max_prob=max_prob):
                r_type_counts[r_type][-1] = count

        total = sum(c for _, counts in r_type_counts.items() for c in counts)
        return total, [RTypeCounts(r_type=r_type, counts=counts) for r_type, counts in r_type_counts.items()]
