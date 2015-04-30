#!/usr/bin/env python3
# encoding: utf-8

"""
Folios - Yet another Static site generator.

Usage: folios init   [options] ...
       folios update [options] ...
       folios clean  [options] ...
       folios serve  [options] ...

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

__all__ = ['init', 'update', 'serve', 'clean', 'dialogs']

from docopt import docopt

import folios
from folios.core import exceptions
from folios.core import logger
from folios.core import settings

def main(argv, do_exit=True):
    from folios.cli import init
    from folios.cli import update
    from folios.cli import serve
    from folios.cli import clean

    arg_map = {
        'init': init,
        'update': update,
        'serve': serve,
        'clean': clean,
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
