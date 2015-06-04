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

import os

from time import time

from folios.core import utils
from folios.core import logger
from folios.core.cache import Cache
from folios.core.content import Theme
from folios.core.content import ContentTypes
from folios.core.settings import Settings


class Site(object):
    __slots__ = (
        'basepath',
        'settings',
        'log',
        )

    def __init__(self, basepath, settings):
        # Saves basepath
        self.basepath = os.path.abspath(basepath)
        if not self.__isFoliosSite(self.basepath):
            errstr = "I'm sorry Dave. I'm afraid I can't do that.\n" +\
                "Are you sure you're inside a Folios site folder?"
            raise FoliosAbortException(errstr)

        # Initialize settings and log
        self.settings = settings
        self.log = logger.get_logger('site', self.settings)
        self.log.debug("Basepath: '{}'".format(self.basepath))

    @classmethod
    def resolveRootFolder(kls, folder):
        if not os.path.basename(folder):
            errstr = "I'm sorry Dave. I'm afraid I can't do that.\n" +\
                "Are you sure you're inside a Folios site folder?"
            raise FoliosAbortException(errstr)

        if kls.__isFoliosSite(folder):
            return folder

        # Go back one level and try again
        new_folder = os.path.abspath(os.path.join(folder, os.path.pardir))
        kls.resolveRootFolder(new_folder)

    @classmethod
    def __isFoliosSite(kls, path):
        return os.path.exists(os.path.join(path, __rootfolder__))
