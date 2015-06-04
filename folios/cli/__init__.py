#!/usr/bin/env python3
# encoding: utf-8
#
# Folios - Yet Another Static Site Generator
# Copyright (C) 2015 - Magnun Leno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

Folios - Yet another Static site generator.

Usage: folios init   [options] ...
       folios update [options] ...
       folios clean  [options] ...
       folios serve  [options] ...
       folios list   [options] ...

Descriptions:

    init    Creates a new site.
    update  Updates the HTML files, metadata or cache.
    clean   Cleans the HTML files, metadata or cache.
    serve   Serves the generates site.

        * For more info about each command, use 'folios <command> -h'

Options:
  -h --help             Show this screen.
  --version             Show version.
"""

__all__ = ['init', 'update', 'serve', 'clean', 'list']

import os
import importlib

from glob import glob
from docopt import docopt
from difflib import SequenceMatcher

import folios
from folios.core import utils
from folios.core import logger
from folios.core import settings


def main(argv, do_exit=True):
    from folios.cli import init
    from folios.cli import update
    from folios.cli import serve
    from folios.cli import clean
    from folios.cli import list as _list

    arg_map = {
        'init': init,
        'update': update,
        'serve': serve,
        'clean': clean,
        'list': _list,
        }

    args = docopt(__doc__, argv=argv[:1], version='Folios '+folios.__version__)
    for (arg, module) in arg_map.items():
        flag = args.__getitem__(arg)
        if flag:
            break

    inner_args = docopt(arg_map[arg].__doc__, argv=argv, version="Folios {}".format(folios.__version__))

    debug = inner_args['--debug']
    verbose = inner_args['--verbose']

    sett = settings.Settings(basepath=None)
    sett['file-log.enabled'] = False
    if debug:
        sett.set_tmp('cli-log.level', 'debug')
    if verbose:
        sett.set_tmp('core.verbose', verbose)

    try:
        site = arg_map[arg].run(inner_args, verbose, debug)
    except exceptions.FoliosAbortException as e:
        log = logger.get_logger('cli.main', sett)
        log.warning("Execution aborted! {}".format(e.message))
        if do_exit:
            exit(1)
    except exceptions.FoliosBaseException as e:
        log = logger.get_logger('cli.main', sett)
        if verbose:
            log.error("Folios exception", exc_info=e)
        else:
            log.error("Folios exception: {}".format(e.message))
        if do_exit:
            exit(1)
    except Exception as e:
        log = logger.get_logger('cli.main', sett)
        log.error("Unexpected exception", exc_info=e)
        if do_exit:
            exit(1)
    else:
        log = logger.get_logger('cli.main', site.settings)
        log.debug("Ended succesfully!")
        if do_exit:
            exit(0)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
