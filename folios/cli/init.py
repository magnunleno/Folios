#!/usr/bin/env python3
# encoding: utf-8

"""
Folios - Yet another Static site generator.

Usage: folios init <site-name> [-d=<path>] [-D -V]

Options:
  -h --help         Show this screen.
  -v --version      Show version.
  -V --verbose      Show verbose information.
  -D --debug        Show verbose information.

  -d=<path>         Destiny path.
"""

import os
from docopt import docopt

from folios import __version__
from folios.cli import dialogs
from folios.core import utils
from folios.core.site import Site
from folios.core.exceptions import FoliosAbortException


def run(argv):
    args = docopt(__doc__, argv=argv, version='Folios '+__version__)

    sitename = args['<site-name>']
    path = args['-d'] if args['-d'] else utils.slugify(sitename)
    debug = args['--debug']
    verbose = args['--verbose']

    if os.path.exists(path):
        answer = dialogs.proceed_yes_no(
            "The path '{}' already exists, should I delete it".format(
                path
                )
            )
        if not answer:
            raise FoliosAbortException("Folder already in use.")

    return Site.new_site(sitename, path, debug, verbose)
