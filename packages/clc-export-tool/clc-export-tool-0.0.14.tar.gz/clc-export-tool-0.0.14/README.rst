

Usage
=============

Type `estool --help` to see general help.

The tool supports two commands: export and types. The former to export data into text files and
the later to find the exact spelling/version document type identifiers.


estool export
--------------

`export` allows to query for data from Elasticsearch and pipe it into a file.

Without the --fields argument you get the json messages, one per line.
When you specify --fields the tool create tab separated lines, one line per message.
::

    usage: estool export [-h] [-f FIELDS [FIELDS ...]] [-s START] [-e END]
                         [-t TOP]
                         index doc_type [query]

    positional arguments:
      index                 index pattern (without the appended date)
      doc_type              full document type (including version)
      query                 query in lucence syntax https://goo.gl/n9zJSx

    optional arguments:
      -h, --help            show this help message and exit
      -f FIELDS [FIELDS ...], --fields FIELDS [FIELDS ...]
                            list of fields
      -s START, --start START
                            start time for query
      -e END, --end END     end time for query
      -t TOP, --top TOP     only return the first TOP items


estool types
-------------

``types`` allows to identivy the available document types. in the export command one need to specify the
document type as the second parameter and this command helps to identifiy what is available.


::

    usage: estool types [-h] index

    positional arguments:
      index       index pattern (without the appended date)

    optional arguments:
      -h, --help  show this help message and exit


Query syntax
=============


[query string syntax on Elasticsearch.co](https://goo.gl/n9zJSx)

