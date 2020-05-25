from typing import Any

import tornado
from tornado import httputil
from tornado.web import RequestHandler

from server.db.relations import PaperAnalyzerDatabase
from server.views.base import BaseRequestHandler


class RelationsHandler(BaseRequestHandler):

    def __init__(self, application: tornado.web.Application,
                 request: httputil.HTTPServerRequest, *, db: PaperAnalyzerDatabase, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.relations_per_page = 10
        self.db = db

    def get(self) -> None:
        only_novel = self.get_numeric_argument('only_novel', default=0)
        page = self.get_numeric_argument('page', default=0)

        relations = list(self.db.get_merged_relations(
            id1=self.get_argument('id1', None),
            id2=self.get_argument('id2', None),
            pmid=self.get_argument('pmid', None),
            in_ctd=0 if only_novel else None
        ))

        total_relations = len(relations)
        total_pages = total_relations // self.relations_per_page + int(total_relations % self.relations_per_page != 0)
        page = min(page, total_pages)

        self.send_response({
            'relations': relations[self.relations_per_page * page: self.relations_per_page * (page + 1)],
            'page': page,
            'totalPages': total_pages,
        })
