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

"""
What you own is your own kingdom
What you do is your own glory
What you love is your own power
What you live is your own story
In your head is the answer
Let it guide you along
Let your heart be the anchor
And the beat of your own song

You don't get something for nothing
You can't have freedom for free
You won't get wise
With the sleep still in your eyes
No matter what your dreams might be 
                --- Something for Nothing (Rush)
"""

__doc__ = """
Folios - Yet another Static site generator.

Usage:
    folios <command> [options] ...

Descriptions:
{descriptions}
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
from folios.core import Settings
from folios.core import exceptions as ex

_path = os.path.split(__file__)[0]
commands = [os.path.basename(fname).split(".py")[0]
            for fname in glob(os.path.join(_path, "*.py"))]

if "__init__" in commands:
    commands.remove("__init__")
commands.sort()

MODULES = {}
descriptions = []
for command in commands:
    module = importlib.import_module("folios.cli.{}".format(command))
    MODULES[command] = module
    if not hasattr(module, "__description__"):
        continue
    description = module.__description__

    descriptions.append("    {} {}.".format(command.ljust(10), description))

__doc__ = __doc__.format(descriptions='\n'.join(descriptions))


def get_command(name):
    if name in commands:
        return name

    matches = []
    for command in commands:
        m = SequenceMatcher(None, command, name)
        matches.append((command, m.ratio()))
    matches.sort(key=lambda x: x[1], reverse=True)
    best = [match for match in matches if match[1] >= 0.88]
    if best:
        print("I'll pretend you typed '{}'...".format(best[0][0]))
        return best[0][0]

    best = [match for match in matches if match[1] >= 0.6]
    if not best:
        print(__doc__)
        exit(1)

    if len(best) == 1:
        print("Did you meant '{}'? I'm {}% sure...".format(
            best[0][0], round(best[0][1]*100, 2))
            )
        exit(1)

    print("Did you mean:")
    for match in best:
        print("    {}".format(match[0]))
    exit(1)


def main(argv, do_exit=True):
    args = docopt(__doc__, argv=argv[:1], version='Folios '+folios.__version__)

    name = get_command(args['<command>'])
    argv[0] = name
    mod = MODULES[name]
    inner_args = docopt(mod.__doc__, argv=argv,
                        version="Folios {}".format(folios.__version__))

    debug = inner_args['--debug']
    verbose = inner_args['--verbose']

    if name == "init":
        sett = Settings(from_dict={})
        sett['log.file.enabled'] = False
    else:
        sett = Settings()

    log = logger.get_logger('cli.main', sett)

    if debug:
        sett.set_tmp('log.cli.level', 'debug')

    if verbose:
        sett.set_tmp('core.verbose', verbose)

    try:
        mod.run(inner_args, sett, verbose, debug)
    except ex.AbortException as e:
        log.warning("Execution aborted! {}".format(e.message))
        if do_exit:
            exit(1)
    except ex.BaseException as e:
        if verbose:
            log.error("Folios exception", exc_info=e)
        else:
            log.error("Folios exception: {}".format(e.message))
        if do_exit:
            exit(1)
    except Exception as e:
        log.error("Unexpected exception", exc_info=e)
        if do_exit:
            exit(1)
    else:
        log.debug("Ended succesfully!")
        if do_exit:
            exit(0)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
