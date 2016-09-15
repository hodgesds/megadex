import argparse
import os
import time
from megadex.handlers import ChangeHandler
from megadex.indexer import Indexer
from watchdog.observers import Observer


def setup_logger(args):
    import logging
    from logging.handlers import RotatingFileHandler

    logger = logging.getLogger('megadex')
    logger.setLevel(getattr(logging, args.log_level.upper()))

    if args.log_file == '-':
	logger.addHandler(logging.StreamHandler())
    else:
	rfh = RotatingFileHandler(args.log_file)
	logger.addHandler(rfh)

def mk_parser():
    parser = argparse.ArgumentParser(
	description = 'MegaDex Indexer',
    )

    parser.add_argument(
	'dir',
	help    = 'Directory to watch'
    )

    parser.add_argument(
	'--log-level',
	default = os.environ.get('MEGADEX_LOG_LEVEL', 'info'),
        choices = ('info', 'debug', 'error', 'warning', 'critical'),
	dest    = 'log_level',
	help    = 'log level'
    )

    parser.add_argument(
	'--log-file',
	default = os.environ.get('MEGADEX_LOG_FILE', '-'),
	dest    = 'log_file',
	help    = 'log file (- for STDOUT)'
    )

    hosts = os.environ.get('ES_HOSTS', ['http://127.0.0.1:9200'])
    if len(hosts) > 0 and isinstance(hosts, basestring):
    	hosts = filter(None, hosts.split(','))

    parser.add_argument(
	'--es-host',
	action  = 'append',
	default = hosts,
	dest    = 'es_hosts',
	help    = 'Elasticsearch host(s) ES_HOSTS'
    )

    parser.add_argument(
	'--paged-pdf',
	action  = 'store_true',
	default = False,
	dest    = 'paged_pdf',
	help    = 'Paged PDF files (format is pdf_foo-{page}.pdf)'
    )

    parser.add_argument(
	'--port',
	default = os.environ.get('ES_PORT', 9200),
	help    = 'Elasticsearch port ES_PORT'
    )

    parser.add_argument(
	'--ssl',
	action  = 'store_true',
	default = False,
	help    = 'Elasticsearch SSL'
    )

    parser.add_argument(
	'--verify-certs',
	action  = 'store_true',
	default = False,
	dest    = 'verify_certs',
	help    = 'Elasticsearch verify certificates'
    )

    parser.add_argument(
	'--http-user',
	default = os.environ.get('ES_USER', ''),
	dest    = 'http_user',
	help    = 'Elasticsearch HTTP user ES_USER'
    )

    parser.add_argument(
	'--http-password',
	default = os.environ.get('ES_PASSWORD', ''),
	dest    = 'http_password',
	help    = 'Elasticsearch HTTP password ES_PASSWORD'
    )

    parser.add_argument(
	'--ca-certs',
	default = '',
	dest    = 'ca_certs',
	help    = 'Elasticsearch HTTP password'
    )

    parser.add_argument(
	'--es-cert',
	default = '',
	dest    = 'es_cert',
	help    = 'Elasticsearch client cert file'
    )

    parser.add_argument(
	'--es-key',
	default = '',
	dest    = 'es_key',
	help    = 'Elasticsearch client key file'
    )

    return parser


def main():
    parser = mk_parser()

    args = parser.parse_args()

    setup_logger(args)

    indexer = Indexer(
	args.es_hosts,
	ca_certs     = args.ca_certs,
	client_cert  = args.es_cert,
	client_key   = args.es_key,
	http_auth    = (args.http_user, args.http_password),
        paged_pdf    =args.paged_pdf,
	port         = args.port,
	use_ssl      = args.ssl,
	verify_certs = args.verify_certs,
    )

    # Steps:
    # 1) Create all indexes
    # 2) Index all existing files in watch dir
    # 3) Watch directory and index any changes

    # 1)
    indexer.indices.create(index='csv', ignore=400)
    indexer.indices.create(index='doc', ignore=400)
    indexer.indices.create(index='docx', ignore=400)
    indexer.indices.create(index='jpg', ignore=400)
    indexer.indices.create(index='kml', ignore=400)
    indexer.indices.create(index='kmz', ignore=400)
    indexer.indices.create(index='mdb', ignore=400)
    indexer.indices.create(index='pdf', ignore=400)
    indexer.indices.create(index='ppt', ignore=400)
    indexer.indices.create(index='pptx', ignore=400)
    indexer.indices.create(index='scn', ignore=400)
    indexer.indices.create(index='tiff', ignore=400)
    indexer.indices.create(index='xml', ignore=400)
    indexer.indices.create(index='xyz', ignore=400)
    indexer.indices.create(index='zip', ignore=400)

    # 2)
    for root, dirs, files in os.walk(args.dir, topdown=False):
	for name in files:
            indexer.index_file(os.path.join(root, name))

    event_handler = ChangeHandler(**{'indexer':indexer})

    # 3)
    observer = Observer()
    observer.schedule(event_handler, args.dir, recursive=True)
    observer.start()

    try:
        while observer.isAlive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
