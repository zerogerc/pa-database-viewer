import json
from typing import Any, Dict

import tornado
from tornado import httputil
from tornado.web import RequestHandler

from server.collection import CollectionData
from server.handlers.base import BaseRequestHandler


class RelationPmidsHandler(BaseRequestHandler):

    def __init__(self, application: tornado.web.Application,
                 request: httputil.HTTPServerRequest, *, relations_collections: Dict[str, CollectionData],
                 **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.relations_collections = relations_collections

    def post(self):
        params = json.loads(self.request.body)
        pmid_probs = self.relations_collections['LitCovid'].relations_db.get_relation_pmid_probs(
            id1=params['id1'], id2=params['id2'], label=params['label'],
            pmids=params['pmids'])
        self.send_response({
            "pmidProbs": list(pmid_probs)
        })
