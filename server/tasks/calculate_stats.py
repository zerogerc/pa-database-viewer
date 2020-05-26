import json
import logging
from typing import List, Dict

from server.collection import CollectionData
from server.data.stats import RTypesStats, RTypeCounts
from server.tasks.task import PreprocessTask

G_LOG = logging.getLogger(__name__)


class CalculateStatsTask(PreprocessTask):
    def __init__(self, directory: CollectionData, *, override_previous: bool = False):
        super(CalculateStatsTask, self).__init__('calculate-stats', directory, override_previous=override_previous)

    def run_preprocessing(self):
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

        stats = RTypesStats(
            counts=[RTypeCounts(r_type=r_type, counts=counts) for r_type, counts in r_type_counts.items()]
        )

        self.directory.path_stats.write_text(json.dumps(stats.to_json(), indent=4))
