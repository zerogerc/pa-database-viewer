import logging
from pathlib import Path

import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

from server.collection import read_collections
from server.config import SERVER_CONFIG
from server.handlers.collections import CollectionsHandler
from server.handlers.main import MainHandler
from server.handlers.relation_pmids import RelationPmidsHandler
from server.handlers.relations import RelationsHandler
from server.handlers.stats import StatsHandler
from server.handlers.suggest import SuggestHandler

define('port', type=int, default=8888, help='port to listen on')
define('debug', type=bool, default=False, help='run in debug mode')
define('collections_dir', type=str, default='', help='path to a directories with extracted relations collections')
define('index_path', type=str, default='', help='path to index.html')
define('static_dir', type=str, default='', help='path to static files')

G_LOG = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    tornado.options.parse_command_line()
    SERVER_CONFIG.debug = options.debug

    collections = read_collections(Path(options.collections_dir))

    handlers = [
        (f'/re-viewer/api/relations', RelationsHandler, dict(relations_collections=collections)),
        (f'/re-viewer/api/relation-pmids', RelationPmidsHandler, dict(relations_collections=collections)),
        (f'/re-viewer/api/stats', StatsHandler, dict(relations_collections=collections)),
        (f'/re-viewer/api/suggest', SuggestHandler, dict(relations_collections=collections)),
        (f'/re-viewer/api/collections', CollectionsHandler, dict(relations_collections=collections))
    ]
    if not options.debug:
        handlers.append((r'/re-viewer/static/(.*)', tornado.web.StaticFileHandler, {'path': Path(options.static_dir)}))
        handlers.append((r'/re-viewer/.*', MainHandler, dict(index_path=Path(options.index_path))))

    app = Application(handlers)
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    G_LOG.info('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
