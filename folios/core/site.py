#!/usr/bin/env python3
# encoding: utf-8

import os
import logging

from folios.core import logger
from folios.core import __rootfolder__
from folios.core.exceptions import FoliosAbortException
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
