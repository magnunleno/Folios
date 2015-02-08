#!/usr/bin/env python3
# encoding: utf-8

"""
Folios - Yet another Static site generator.

Usage: folios clean [cache|html|<filename>] [-D -V]

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  -V --verbose      Show verbose information.
  -D --debug        Show verbose information.

  cache         Cleans all cache contents.
  html          Cleans all HTML output.
  <filename>    Cleans all cache and HTML from a specific filename
"""

from docopt import docopt


from folios.cli import init_cli

@init_cli
def run(argv):
    print(args)
