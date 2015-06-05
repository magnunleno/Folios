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

__description__ = "Updates the site (and/or it's meta informations) or parts " + \
                  "of it."

from folios.core import Site


def run(args, settings, verbose, debug):
    if debug:
        settings.set_tmp('cli-log.level', 'debug')
    if verbose:
        settings.set_tmp('core.verbose', verbose)

    site = Site(settings)
    site.update()
