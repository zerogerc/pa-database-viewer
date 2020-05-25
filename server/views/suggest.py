import logging
from typing import Any, Dict

import tornado
from tornado import httputil
from tornado.web import RequestHandler

from server.collection import CollectionData
from server.views.base import BaseRequestHandler

G_LOG = logging.getLogger(__name__)


class SuggestHandler(BaseRequestHandler):

    def __init__(self, application: tornado.web.Application,
                 request: httputil.HTTPServerRequest, *, relations_collections: Dict[str, CollectionData],
                 **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.relations_collections = relations_collections

    def get(self) -> None:
        query = self.get_argument('query', '')
        items = self.relations_collections['LitCoivid'].suggest_db.suggest(query=query)
        self.send_response({
            'suggest': [
                {
                    'id': item.id,
                    'name': item.cname
                } for item in items
            ]
        })
