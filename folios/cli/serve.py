#!/usr/bin/env python3
# encoding: utf-8

"""
Folios - Yet another Static site generator.

Usage: folios serve [-b=<address:port>]

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  -b            Bind address and port. [default: 127.0.0.1:8000]
"""

import folios

from docopt import docopt


def run(argv):
    args = docopt(__doc__, argv=argv, version='Folios '+folios.__version__)
    print(args)
    return args
