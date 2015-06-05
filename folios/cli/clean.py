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

Usage: folios clean [-c][-o][-l][<filename>] [-D -V]

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  -V --verbose      Show verbose information.
  -D --debug        Show verbose information.

  -c --cache    Cleans all cache contents.
  -o --output   Cleans all HTML output.
  -l --log      Cleans all site logging files.
  <filename>    Cleans all cache and HTML from a specific filename
"""
__description__ = "Cleans the HTML files, metadata or cache."

import os
import glob

from folios.core import utils


def delete_folder(path, basepath):
    print("Cleaning cache at '{}'".format(
        utils.normpath(path, basepath)
        ))
    utils.delete_folder(path)


def run(args, settings, verbose, debug):
    basepath = utils.resolve_root_folder()

    if args["--cache"]:
        delete_folder(settings.get_path("cache.folder"), basepath)

    if args["--output"]:
        delete_folder(settings.get_path("core.output"), basepath)

    if args["--log"] and settings['file-log.enabled']:
        file_pattr = settings.get_path('file-log.file_name') + "*"
        files = glob.glob(file_pattr)
        files.sort()
        for fname in files:
            print("Cleaning log at '{}'".format(
                utils.normpath(fname, basepath)
                ))
            os.remove(fname)
