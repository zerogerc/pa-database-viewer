import logging
from typing import Any, Dict

import tornado
from tornado import httputil
from tornado.web import RequestHandler

from server.collection import CollectionData
from server.handlers.base import BaseRequestHandler

G_LOG = logging.getLogger(__name__)


class StatsHandler(BaseRequestHandler):

    def __init__(self, application: tornado.web.Application,
                 request: httputil.HTTPServerRequest, *, relations_collections: Dict[str, CollectionData],
                 **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.relations_per_page = 10
        self.relations_collections = relations_collections

    def get(self) -> None:
        collection = self.get_argument('collection', default='')
        relation_type_stats = self.relations_collections[collection].stats

        self.send_response({
            'rTypeCounts': [
                {
                    'rType': rc.r_type,
                    'counts': rc.counts
                }
                for rc in relation_type_stats.counts
            ],
        })
