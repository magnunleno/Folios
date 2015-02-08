#!/usr/bin/env python3
# encoding: utf-8

"""
Folios - Yet another Static site generator.

Usage: folios init <site-name> [-d=<folder>] [-D -V]

Options:
  -h --help         Show this screen.
  -v --version      Show version.
  -V --verbose      Show verbose information.
  -D --debug        Show verbose information.

  -d=<folder>       Destiny folder.
"""

import folios
from folios import utils
from folios.cmd import dialogs
from folios.site import Site
from folios.exceptions import FoliosAbortException

from docopt import docopt
from os.path import exists
from os import chdir


def run(argv):
    args = docopt(__doc__, argv=argv, version='Folios '+folios.__version__)
    if args['-d']:
        folder = args['-d']
    else:
        folder = utils.slugify(args['<site-name>'])

    if exists(folder):
        answer = dialogs.proceed_yes_no(
            "The folder '{}' already exists, should I delete it".format(
                folder
                )
            )
        if not answer:
            raise FoliosAbortException("Aborting execution...")
        utils.deleteFolder(folder)

    utils.copySkel('demo-site', folder)

    chdir(utils.joinPath(folder))
    site = Site()

    print("New site available at '{}'".format(folder))
    return args
