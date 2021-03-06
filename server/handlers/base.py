import json

from tornado.web import RequestHandler

from server.config import SERVER_CONFIG


class BaseRequestHandler(RequestHandler):

    def set_default_headers(self):
        if SERVER_CONFIG.debug:
            self.set_header('Access-Control-Allow-Origin', '*')
            self.set_header('Access-Control-Allow-Headers', 'access-control-allow-origin,authorization,content-type')
            self.set_header('Access-Control-Allow-Methods', 'GET,POST')

        self.set_header('Content-Type', 'application/json; charset="utf-8"')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def send_response(self, data, status=200):
        self.set_status(status)
        self.write(json.dumps(data))

    def get_numeric_argument(self, key: str, *, default: int = 0) -> int:
        arg = self.get_argument(key, '')
        return int(arg) if arg.isnumeric() else default
