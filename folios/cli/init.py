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
Folios - Yet another Static site generator.

Usage: folios init <site-name> [-d=<path>] [-D -V]

Options:
  -h --help         Show this screen.
  -v --version      Show version.
  -V --verbose      Show verbose information.
  -D --debug        Show verbose information.

  -d=<path>         Destiny path.
"""

__description__ = "Creates new sites."

import os

from folios.cli import dialogs
from folios.core import utils
from folios.core import Site
from folios.core import exceptions as ex


def run(args, settings, verbose, debug):
    sitename = args['<site-name>']
    path = args['-d'] if args['-d'] else utils.slugify(sitename)

    if os.path.exists(path):
        answer = dialogs.proceed_yes_no(
            "The path '{}' already exists, should I delete it".format(
                path
                )
            )
        if not answer:
            raise ex.AbortException("Folder already in use.")

    Site.new_site(sitename, path, debug, verbose)
