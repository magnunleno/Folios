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

Usage: folios serve [-b=<address:port>] [-D -V]

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  -V --verbose      Show verbose information.
  -D --debug        Show verbose information.

  -b            Bind address and port. [default: 127.0.0.1:8000]
"""


import os

from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

from folios.core import utils
from folios.core import Settings


def run(args, verbose, debug):
    print(args)
    return args
