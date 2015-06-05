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

Usage: folios serve [-b <address:port>] [-D -V]

Options:
  -h --help                 Show this screen.
  -v --version              Show version.
  -V --verbose              Show verbose information.
  -D --debug                Show verbose information.

  -b --bind=<address:port>  Bind address and port.
"""

__description__ = "Serves the site in a easy way."

import os

from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler


def run(args, settings, verbose, debug):
    _bind = settings['core.serve']
    browser = settings['core.browser']
    path = settings.get_path('core.output')

    if args['--bind']:
        _bind = args['--bind']

    if ':' in _bind:
        address, port = _bind.split(':')
        if not address:
            address = 'localhost'
        port = int(port)
    else:
        address = _bind
        port = 8000

    bind = (address, port)

    os.chdir(path)
    try:
        server = HTTPServer(bind, SimpleHTTPRequestHandler)
    except OSError as e:
        print(e.args[1])
    else:
        os.system("(sleep 2 && {} http://{}:{}) &".format(browser, *bind))
        try:
            server.serve_forever()
        except KeyboardInterrupt as e:
            print("\nThanks for all the fish")
