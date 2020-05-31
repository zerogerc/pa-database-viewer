from pathlib import Path
from typing import Any

import tornado
from tornado import httputil
from tornado.web import RequestHandler


class MainHandler(RequestHandler):

    def __init__(self, application: tornado.web.Application,
                 request: httputil.HTTPServerRequest, *, index_path: Path, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.index_path = index_path

    def get(self):
        self.render(str(self.index_path.resolve()))
