from pathlib import Path

import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

from server.config import SERVER_CONFIG
from server.views.main import MainHandler
from server.views.relations import RelationsHandler

define('port', type=int, default=8888, help='port to listen on')
define('debug', type=bool, default=False, help='run in debug mode')
define('pa_db_path', type=str, default='', help='path to paper-analyzer database')
define('index_path', type=str, default='', help='path to index.html')
define('static_dir', type=str, default='', help='path to static files')


def main():
    tornado.options.parse_command_line()
    SERVER_CONFIG.debug = options.debug

    handlers = [
        (f'/api/relations', RelationsHandler, dict(pa_db_path=Path(options.pa_db_path))),
    ]
    if not options.debug:
        handlers.append((r'/static/(.*)', tornado.web.StaticFileHandler, {'path': Path(options.static_dir)}))
        handlers.append((r'/(.*)', MainHandler, dict(index_path=Path(options.index_path))))

    app = Application(handlers)
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
