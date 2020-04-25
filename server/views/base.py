import json

from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin


class BaseRequestHandler(RequestHandler, SessionMixin):

    def set_default_headers(self):
        # if SERVER_CONFIG.debug:
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'access-control-allow-origin,authorization,content-type')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Content-Type', 'application/json; charset="utf-8"')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def send_response(self, data, status=200):
        self.set_status(status)
        self.write(json.dumps(data))
