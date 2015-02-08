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

import os
import logging

from folios.cli import dialogs
from folios.cli import init_cli
from folios.core import utils
from folios.core import logger
from folios.core.site import Site
from folios.core.settings import Settings
from folios.core.exceptions import FoliosAbortException

DEBUG = False
VERBOSE = False

DBG_NAME, DBG_NAME_COLOR, DBG_TEXT_COLOR = logger.LEVEL[logging.DEBUG]
DBG_HEADER = DBG_NAME_COLOR + DBG_NAME + ":" + logger.RESET_ALL


def log_debug(msg, *args):
    if DEBUG:
        msg = DBG_TEXT_COLOR + msg.format(*args) + logger.RESET_ALL
        print("{} {}".format(DBG_HEADER, msg))


@init_cli
def run(argv):
    if 'debug' in globals():
        global DEBUG
        DEBUG = debug
        logger.set_force_debug(debug)

    if 'verbose' in globals():
        global VERBOSE
        VERBOSE = verbose
        logger.set_force_verbose(verbose)

    if args['-d']:
        folder = args['-d']
        log_debug("Folder specified '{}'", folder)
    else:
        folder = utils.slugify(args['<site-name>'])
        log_debug("Folder name generated based in site name: '{}'", folder)

    if os.path.exists(folder):
        log_debug("Folder already exists")
        answer = dialogs.proceed_yes_no(
            "The folder '{}' already exists, should I delete it".format(
                folder
                )
            )
        if not answer:
            raise FoliosAbortException("Folder already in use.")
        log_debug("Deleting folder...")
        utils.deleteFolder(folder)

    log_debug("Copying skel...")
    utils.copySkel('demo-site', folder)

    folder = os.path.abspath(folder)
    os.chdir(folder)

    log_debug("Loading settings")
    settings = Settings(folder)

    log_debug("Settings temporary values")
    if VERBOSE:
        settings.set_tmp('core.verbose', VERBOSE)
    if DEBUG:
        settings.set_tmp('cli-log.level', 'debug')

    log_debug("Initializing new site...")
    site = Site(folder, settings)
    log = logger.get_logger('cli.init', settings)

    log.debug("Setting site name in settings")
    settings['site.name'] = args['<site-name>']
    settings.save()

    log.info("New site available at '{}'".format(folder))
    return site
