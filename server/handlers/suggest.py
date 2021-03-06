import logging
from typing import Any, Dict

import tornado
from tornado import httputil
from tornado.web import RequestHandler

from server.collection import CollectionData
from server.handlers.base import BaseRequestHandler

G_LOG = logging.getLogger(__name__)


class SuggestHandler(BaseRequestHandler):

    def __init__(self, application: tornado.web.Application,
                 request: httputil.HTTPServerRequest, *, relations_collections: Dict[str, CollectionData],
                 **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.relations_collections = relations_collections

    def get(self) -> None:
        collection = self.get_argument('collection', default='LitCovid')
        query = self.get_argument('query', '')

        G_LOG.info(f'Suggest, collection = {collection}')
        items = self.relations_collections[collection].suggest_db.suggest(query=query)
        self.send_response({
            'suggest': [
                {
                    'id': item.id,
                    'name': item.name
                } for item in items
            ]
        })
