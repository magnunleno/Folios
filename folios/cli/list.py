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

Usage: folios list [cache|articles|pages|images] [-D -V]

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  -V --verbose      Show verbose information.
  -D --debug        Show verbose information.

  cache         Cleans all cache contents.
  html          Cleans all HTML output.
  <filename>    Cleans all cache and HTML from a specific filename
"""

import os
from colorama import Fore

from folios.core import utils
from folios.core.settings import Settings
from folios.core.site import Site


def print_dict(_dict, indent="    "):
    items = [(attr, val) for attr, val in _dict.items()]
    items.sort()
    last = []
    for attr, val in items:
        if not val:
            continue
        if isinstance(val, dict):
            last.append((attr, val))
            continue
        elif isinstance(val, list):
            val = map(str, val)
            val = ', '.join(val)
        print("{}{}{}{} {}{}{}".format(
            Fore.BLUE, indent, attr.ljust(12), Fore.RESET,
            Fore.GREEN, val, Fore.RESET,
            ))
    for attr, val in last:
        print("{}{}[{}]{}".format(Fore.YELLOW, indent, attr, Fore.RESET))
        print_dict(val, indent=indent*2)


def list_cache(site):
    if not site.cache.enabled:
        print("The caching system is currently disabled")
        return

    keys = [key for key in site.cache]
    keys.sort()
    for key in keys:
        print("{}[{}]{}".format(Fore.RED, key, Fore.RESET))
        print_dict(site.cache[key])
        print("")


def run(args, verbose, debug):
    basepath = utils.resolveRootFolder(os.getcwd())

    settings = Settings(basepath)
    if debug:
        settings.set_tmp('cli-log.level', 'debug')
    if verbose:
        settings.set_tmp('core.verbose', verbose)

    site = Site(settings, basepath)

    if "cache" in args:
        list_cache(site)
    return site
