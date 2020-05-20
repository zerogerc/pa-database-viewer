import logging
from typing import Any, List, Dict

import tornado
from tornado import httputil
from tornado.web import RequestHandler

from server.database import PaperAnalyzerDatabase
from server.views.base import BaseRequestHandler

G_LOG = logging.getLogger(__name__)


class StatsHandler(BaseRequestHandler):

    def __init__(self, application: tornado.web.Application,
                 request: httputil.HTTPServerRequest, *, db: PaperAnalyzerDatabase, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.relations_per_page = 10
        self.db = db

    def get(self) -> None:
        relation_type_counts = self.relation_type_counts()

        self.send_response({
            'rTypeCounts': [
                {
                    'rType': r_type,
                    'counts': counts
                }
                for r_type, counts in relation_type_counts.items()
            ],
        })

    def relation_type_counts(self) -> Dict[str, List[int]]:
        G_LOG.info('relation_type_counts: Started')
        relation_types: List[str] = list(self.db.get_relation_types())
        G_LOG.info('relation_type_counts: Got relation types')
        result: Dict[str, List[int]] = {r: [] for r in relation_types}

        num_buckets = 20
        probs = [i / num_buckets for i in range(num_buckets + 1)]
        for min_prob, max_prob in zip(probs, probs[1:]):
            G_LOG.info(f'relation_type_counts: Getting stats for [{min_prob} .. {max_prob}]')
            for r in result.keys():
                result[r].append(0)
            for r_type, count in self.db.get_relation_type_counts(min_prob=min_prob, max_prob=max_prob):
                result[r_type][-1] = count
        return result
