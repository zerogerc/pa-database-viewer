import logging
from typing import Any, Dict

import tornado
from tornado import httputil
from tornado.web import RequestHandler

from server.collection import CollectionData
from server.handlers.base import BaseRequestHandler

G_LOG = logging.getLogger(__name__)


class CollectionsHandler(BaseRequestHandler):

    def __init__(self, application: tornado.web.Application,
                 request: httputil.HTTPServerRequest, *, relations_collections: Dict[str, CollectionData],
                 **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.relations_collections = relations_collections

    def get(self) -> None:
        self.send_response({
            'collections': list(sorted(self.relations_collections.keys()))
        })
