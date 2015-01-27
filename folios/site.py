#!/usr/bin/env python3
# encoding: utf-8

import os

from folios import __rootfolder__
from folios.exceptions import FoliosAbortException
from folios.utils import joinPath


class Site(object):
    __slots__ = (
        'basepath',
        'settings',
        )

    def __init__(self):
        self.basepath = os.path.abspath(os.getcwd())
        if not self.__isFoliosSite(self.basepath):
            self.basepath = self.__resolveRootFolder(self.basepath)

    def __resolveRootFolder(self, folder):
        if not os.path.basename(folder):
            errstr = "I'm sorry Dave. I'm afraid I can't do that.\n" +\
                "Are you sure you're inside a Folios site folder?"
            raise FoliosAbortException(errstr)

        if self.__isFoliosSite(folder):
            return folder

        new_folder = os.path.abspath(joinPath(folder, os.path.pardir))
        self.__resolveRootFolder(new_folder)

    def __isFoliosSite(self, path):
        return os.path.exists(joinPath(path, __rootfolder__))
