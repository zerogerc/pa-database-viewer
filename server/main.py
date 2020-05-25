import logging
from pathlib import Path

import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

from server.config import SERVER_CONFIG
from server.db.relations import PaperAnalyzerDatabase
from server.utils import CollectionData
from server.views.main import MainHandler
from server.views.relation_pmids import RelationPmidsHandler
from server.views.relations import RelationsHandler
from server.views.stats import StatsHandler

define('port', type=int, default=8888, help='port to listen on')
define('debug', type=bool, default=False, help='run in debug mode')
define('collection', type=str, default='', help='path to a directory with relations and task outputs')
define('index_path', type=str, default='', help='path to index.html')
define('static_dir', type=str, default='', help='path to static files')

G_LOG = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    tornado.options.parse_command_line()
    SERVER_CONFIG.debug = options.debug

    collection_data = CollectionData(Path(options.collection))
    db = PaperAnalyzerDatabase(collection_data.path_relations_db)

    handlers = [
        (f'/api/relations', RelationsHandler, dict(db=db)),
        (f'/api/relation-pmids', RelationPmidsHandler, dict(db=db)),
        (f'/api/stats', StatsHandler, dict(db=db)),
    ]
    if not options.debug:
        handlers.append((r'/static/(.*)', tornado.web.StaticFileHandler, {'path': Path(options.static_dir)}))
        handlers.append((r'/', MainHandler, dict(index_path=Path(options.index_path))))

    app = Application(handlers)
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    G_LOG.info('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
