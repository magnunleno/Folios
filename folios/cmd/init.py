#!/usr/bin/env python3
# encoding: utf-8

"""
Folios - Yet another Static site generator.

Usage: folios init <site-name> [-d=<folder>]

Options:
  -h --help         Show this screen.
  -v --version      Show version.
  -d=<folder>       Destiny folder.
"""

import folios

from docopt import docopt


def run(argv):
    print("INIT!")
    args = docopt(__doc__, argv=argv, version='Folios '+folios.__version__)
    print(args)
    return args
