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

from os import getcwd

from docopt import docopt

from folios import __version__
from folios.core import utils
from folios.core.site import Site
from folios.core.settings import Settings


def run(argv):
    args = docopt(__doc__, argv=argv, version='Folios '+__version__)

    debug = args['--debug']
    verbose = args['--verbose']

    basepath = utils.resolveRootFolder(getcwd())

    settings = Settings(basepath)
    if debug:
        settings.set_tmp('cli-log.level', 'debug')
    if verbose:
        settings.set_tmp('core.verbose', verbose)

    site = Site(basepath, settings)
    site.update()
    return site
