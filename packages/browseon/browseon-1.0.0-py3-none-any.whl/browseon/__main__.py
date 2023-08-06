from __future__ import annotations
import sys
import argparse
from srutil import util

from . import browse, __version__, __package__


def get_argument():
    parser = argparse.ArgumentParser(prog=__package__, usage=util.stringbuilder(__package__, " [options]"))
    parser.add_argument('-v', '--version', action='version', help='show version number and exit', version=__version__)
    group = parser.add_argument_group("to browse web")
    group.add_argument("-q", "--query", dest='query', metavar='', default=None, type=str, help="query to search")
    group.add_argument("-u", "--url", dest="url", default=None, metavar='', type=str, help="url to open")
    group.add_argument("-e", "--engine", dest="engine", metavar='', default="google", required=False,
                       choices=["google", "duckduckgo", "yahoo", "bing", "yandex", "qwant", "wikipedia", "youtube"],
                       help="search engine to search (Optional)")
    parser.add_argument_group(group)
    options = parser.parse_args()
    if not options.query and not options.url:
        parser.error("one of the following arguments are required: -q/--query or -u/--url")
    if options.query and options.url:
        parser.error("any one of the following arguments should be given: -q/--query or -u/--url")
    return options


def main():
    options = get_argument()
    if options.query:
        browse.search(query=options.query, engine=options.engine)
    elif options.url:
        browse.open(url=options.url)


if __name__ == "__main__":
    sys.exit(main())
