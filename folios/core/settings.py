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
import configparser

import folios
from folios.core import utils
from folios.core import FoliosObject
from folios.core import __rootfolder__
from folios.core import exceptions as ex


class Settings(object):
    __slots__ = (
        'basepath',
        'fname',
        '__config',
        '__default',
        '__temporary',
        )

    def __init__(self, basepath=None):
        self.basepath = basepath

        # Custom user settings
        if self.basepath:
            self.__load_from(self.basepath)
        else:
            self.__config = configparser.ConfigParser()
            self.fname = None

        # Default settings shipped with Folios
        self.__default = configparser.ConfigParser()
        self.__default.read(
            os.path.join(folios.__ROOT__, 'data', 'default_config.ini')
            )

        # Temporary settings for one time execution only
        self.__temporary = configparser.ConfigParser()

    def __load_from(self, basepath):
        self.fname = os.path.join(
            self.basepath,
            __rootfolder__,
            'config'
            )
        self.__config = configparser.ConfigParser()
        self.__config.read(self.fname)
        self.basepath = basepath

    def __search_in(self, section, attr, config):
        if not config:
            return None
        try:
            val = config.get(section, attr)
        except (configparser.NoSectionError,
                configparser.NoOptionError):
            val = None
        return val

    def __convert(self, val):
        if val.lower() == 'yes':
            return True
        elif val.lower() == 'no':
            return False
        else:
            return val

    def __getitem__(self, key):
        section, attr = key.split('.')

        for base in (self.__temporary, self.__config, self.__default):
            val = self.__search_in(section, attr, base)
            if val:
                return self.__convert(val)

        raise exceptions.UnknownSettingException(key)

    def __set_at_base(self, base, key, value):
        if value is True:
            value = 'yes'
        elif value is False:
            value = 'no'
        else:
            value = str(value)

        section, attr = key.split('.')
        if self.__search_in(section, attr, self.__default) is None:
            raise exceptions.UnknownSettingException(key)

        if not base.has_section('section'):
            base[section] = {}
        base[section][attr] = str(value)

    def __setitem__(self, key, value):
        self.__set_at_base(self.__config, key, value)

    def set_tmp(self, key, value):
        self.__set_at_base(self.__temporary, key, value)

    def save(self):
        if self.fname is None:
            raise Exception("Setting using only fallback values")

        with open(self.fname, 'w') as fd:
            self.__config.write(fd, space_around_delimiters=True)
