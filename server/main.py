from pathlib import Path

import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

from server.config import SERVER_CONFIG
from server.views.main import MainHandler
from server.views.relations import RelationsHandler

define('port', default=8888, help='port to listen on')
define('debug', default=True, help='run in debug mode')


def main():
    index_path = Path('/Users/Uladzislau.Sazanovich/dev/pa-database-viewer/client/build/index.html')
    static_dir = Path('/Users/Uladzislau.Sazanovich/dev/pa-database-viewer/client/build/static')
    pa_db_path = Path('/Users/Uladzislau.Sazanovich/dev/data/pa/paper-analyzer.db')

    SERVER_CONFIG.debug = options.debug

    handlers = [
        (f'/relations', RelationsHandler, dict(pa_db_path=pa_db_path)),
    ]
    if not options.debug:
        handlers.append(('/', MainHandler, dict(index_path=index_path)))
        handlers.append((r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_dir}))

    app = Application(handlers)
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
