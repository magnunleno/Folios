#!/usr/bin/env python3
# encoding: utf-8

"""
Folios - Yet another Static site generator.

Usage: folios clean [cache|html|<filename>]

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  cache         Cleans all cache contents.
  html          Cleans all HTML output.
  <filename>    Cleans all cache and HTML from a specific filename
"""

import folios

from docopt import docopt


def run(argv):
    args = docopt(__doc__, argv=argv, version='Folios '+folios.__version__)
    print(args)
