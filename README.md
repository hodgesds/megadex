# Megadex
Megadex is a mega indexer that will index file (meta)data into Elasticsearch.
This allows for searching of data within a directory from a web interface. In
addition, it will also monitor the filesystem and attempt to reindex data upon
file changes. Megadex works by first attempting to index a file using the file
extension. If indexing by the file extension fails Megadex will faill back and
use **libmagic** to do a *best effort* attempt at indexing the file.

# Installation
Megadex requires a few python modules that rely on C extensions (libyaml,
libmagic, libxml2, libpng, and a few others). Most should be available via your
package manger for your OS. The other commands that get shelled out are postly
pdf utilities from poppler and mdbtools for interacting with access databases
(again consult your package manager on how to install).

Once you have all the correct C libraries install you can simply do:

```sh
pip install megadex
```

Verify the installation worked:

```sh
megadex -h

usage: megadex [-h] [--log-level {info,debug,error,warning,critical}]
               [--log-file LOG_FILE] [--es-host ES_HOSTS] [--port PORT]
               [--ssl] [--verify-certs] [--http-user HTTP_USER]
               [--http-password HTTP_PASSWORD] [--ca-certs CA_CERTS]
               [--es-cert ES_CERT] [--es-key ES_KEY]
               dir

MegaDex Indexer

positional arguments:
  dir                   Directory to watch

optional arguments:
  -h, --help            show this help message and exit
  --log-level {info,debug,error,warning,critical}
                        log level
  --log-file LOG_FILE   log file (- for STDOUT)
  --es-host ES_HOSTS    Elasticsearch host(s) ES_HOSTS
  --port PORT           Elasticsearch port ES_PORT
  --ssl                 Elasticsearch SSL
  --verify-certs        Elasticsearch verify certificates
  --http-user HTTP_USER
                        Elasticsearch HTTP user ES_USER
  --http-password HTTP_PASSWORD
                        Elasticsearch HTTP password ES_PASSWORD
  --ca-certs CA_CERTS   Elasticsearch HTTP password
  --es-cert ES_CERT     Elasticsearch client cert file
  --es-key ES_KEY       Elasticsearch client key file
```


# Usage
Using Megadex is rather simple, it will by default attempt to connect to a
local instance of Elasticsearch for indexing. The only required parameter is
the folder for indexing and monitoring for reindexing. For example the command
`megadex .` will recursively index and monitor everything in the current
directory.


# Performance Notes
Indexing large files can make things slow and can use up a lot of space. There
are several tools to break up large PDFs such as `pdfseparate`. In addition,
the configuration of the Elasticsearch cluster that the data is being indexed
to needs to be appropriately configured (consult the [Elasticsearch
documentation)(https://www.elastic.co/guide/index.html) for more info).
