#!/usr/bin/env python3
# encoding: utf-8

"""
Folios - Yet another Static site generator.

Usage: folios clean [cache|output|log|<filename>] [-D -V]

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  -V --verbose      Show verbose information.
  -D --debug        Show verbose information.

  cache         Cleans all cache contents.
  output        Cleans all HTML output.
  log           Cleans all site logging files.
  <filename>    Cleans all cache and HTML from a specific filename
"""

import os
import glob
from docopt import docopt
from folios.core import utils
from folios.core.settings import Settings
from folios.core.site import Site


def run(args, verbose, debug):
    basepath = utils.resolveRootFolder(os.getcwd())

    settings = Settings(basepath)
    if debug:
        settings.set_tmp('cli-log.level', 'debug')
    if verbose:
        settings.set_tmp('core.verbose', verbose)

    site = Site(settings, basepath)

    if args["cache"]:
        print("Cleaning cache at '{}'".format(utils.normalizePath(site.cache.base, site.basepath)))
        utils.deleteFolder(site.cache.base)

    if args["output"]:
        print("Cleaning output at '{}'".format(utils.normalizePath(site.outpath, site.basepath)))
        utils.deleteFolder(site.outpath)

    if args["log"] and settings['file-log.enabled']:
        file_pattr = settings.getPath('file-log.file_name') + "*"
        files = glob.glob(file_pattr)
        files.sort()
        for fname in files:
            print("Cleaning log at '{}'".format(utils.normalizePath(fname, site.basepath)))
            os.remove(fname)
    return site
