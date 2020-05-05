import json
from typing import Any

import tornado
from tornado import httputil
from tornado.web import RequestHandler

from server.database import PaperAnalyzerDatabase
from server.views.base import BaseRequestHandler


class RelationPmidsHandler(BaseRequestHandler):

    def __init__(self, application: tornado.web.Application,
                 request: httputil.HTTPServerRequest, *, db: PaperAnalyzerDatabase, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.db = db

    def post(self):
        params = json.loads(self.request.body)
        pmid_probs = self.db.get_relation_pmid_probs(
            id1=params['id1'], id2=params['id2'], label=params['label'],
            pmids=params['pmids'])
        self.send_response({
            "pmidProbs": list(pmid_probs)
        })
