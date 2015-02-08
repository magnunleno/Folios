#!/usr/bin/env python3
# encoding: utf-8

"""
Folios - Yet another Static site generator.

Usage: folios update [cache|html|<filename>...] [-D -V]

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  -V --verbose      Show verbose information.
  -D --debug        Show verbose information.

  all           Updates everything.
  cache         Rescans the source files and updates cache but don't write any
                HTML.
  html          Updates all HTML output and it's cache contents.
  <filename>    Updates the HTML output and cache contents of a specific
                file(s).
"""

from docopt import docopt

from folios.cli import init_cli

@init_cli
def run(argv):
    print(args)
    return args
