from pathlib import Path
from typing import Any

import tornado
from tornado import httputil
from tornado.web import RequestHandler

from server.database import PaperAnalyzerDatabase
from server.views.base import BaseRequestHandler


class RelationsHandler(BaseRequestHandler):

    def __init__(self, application: tornado.web.Application,
                 request: httputil.HTTPServerRequest, *, pa_db_path: Path, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.pa_db_path = pa_db_path
        self._db = None

    def get(self) -> None:
        only_novel_arg = self.get_argument('only_novel', '')
        only_novel = int(only_novel_arg) if only_novel_arg.isnumeric() else 0

        data = list(self.db.get_raw_relations(
            id1=self.get_argument('id1', None),
            id2=self.get_argument('id2', None),
            pmid=self.get_argument('pmid', None),
            in_ctd=0 if only_novel else None
        ))
        self.send_response(data)

    @property
    def db(self) -> PaperAnalyzerDatabase:
        if self._db is not None:
            return self._db
        self._db = PaperAnalyzerDatabase(self.pa_db_path)
        return self._db
