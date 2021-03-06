import logging
from typing import Any, Dict

import attr
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
        self.relations_collections = relations_collections

    def get(self) -> None:
        collection = self.get_argument('collection', default='')
        stats = self.relations_collections[collection].stats
        self.send_response({
            'stats': attr.asdict(stats, recurse=True)
        })
