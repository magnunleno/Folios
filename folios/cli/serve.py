#!/usr/bin/env python3
# encoding: utf-8

"""
Folios - Yet another Static site generator.

Usage: folios serve [-b=<address:port>] [-D -V]

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  -V --verbose      Show verbose information.
  -D --debug        Show verbose information.

  -b            Bind address and port. [default: 127.0.0.1:8000]
"""

import folios

from docopt import docopt


def run(argv):
    args = docopt(__doc__, argv=argv, version='Folios '+folios.__version__)
    print(args)
    return args
