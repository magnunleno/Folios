#!/usr/bin/env python3
# encoding: utf-8

"""
Folios - Yet another Static site generator.

Usage: folios init   [options] ...
       folios update [options] ...
       folios clean  [options] ...
       folios serve  [options] ...

Descriptions:

    init    Creates a new site.
    update  Updates the HTML files, metadata or cache.
    clean   Cleans the HTML files, metadata or cache.
    serve   Serves the generates site.

        * For more info about each command, use 'folios <command> -h'

Options:
  -h --help             Show this screen.
  --version             Show version.
"""

import folios
from folios.cmd import init, update, serve, clean

from docopt import docopt

ARG_MAP = {
    'init': init,
    'update': update,
    'serve': serve,
    'clean': clean,
    }


def main(argv):
    args = docopt(__doc__, argv=argv[:1], version='Folios '+folios.__version__)

    for arg in ARG_MAP:
        if args.__getitem__(arg):
            return ARG_MAP[arg].run(argv)
