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
This module is composed by:
 - the Settings class;
 - and by three functions:
     - _dict_walk: provides and easy way to walk throught a dict
     - _flat_dict: converts nested dicts in a flat dict
     - _load_sett: Loads a settings dict from a YAML file


Bad boy rock, bad boy roll
Gabba Gabba Hey! See then go
C.J. now, hit the gas
Hear Marky kick some ass
Go Johnny. Go, go, go
Go Tommy. Oh Way Oh
Misfits, twilight zone
R.A.M.O.N.E.S.
R.A.M.O.N.E.S.
RAMONES!
        --- R.A.M.O.N.E.S. (Motorhead)
"""

import os
import copy
import yaml

import folios
from folios.core import utils
from folios.core import __rootfolder__
from folios.core import exceptions as ex


class Settings(object):
    '''
    This class is responsible for loading, managing and saving the settings for
    the folios sites.
    '''
    type = "settings"
    __slots__ = [
        'src_hash',
        'src_path',
        '__config',
        '__orig_dict',
        'site_basepath',
        'norm_src_path',
        '__weakref__',
        ]

    def __init__(self, from_dict=None):
        '''
        Basic settings bootstrap:
            @from_dict: If a dict is informed the Settings instance won't
            search for the site settings file and will only base itself in
            the default settings and the informed dict. (dummy mode)
        '''
        default_dict = _load_sett(
                os.path.join(folios.__root__, 'data', 'config-default.yaml')
                )
        default_config = _flat_dict(default_dict)

        if from_dict is not None:
            self.src_path = None
            self.norm_src_path = None
            self.src_hash = None
            user_config = _flat_dict(from_dict)
            self.__orig_dict = copy.deepcopy(from_dict)
        else:
            self.site_basepath = utils.resolve_root_folder()
            self.src_path = os.path.join(
                self.site_basepath,
                __rootfolder__,
                'config.yaml'
                )
            self.norm_src_path = utils.normpath(self.src_path, self.site_basepath)
            self.src_hash = utils.sha1(self.src_path)
            self.__orig_dict = _load_sett(self.src_path)
            user_config = _flat_dict(self.__orig_dict)

        # Enforce only knwon settings keys
        diff_keys = set(user_config.keys()) - set(default_config.keys())
        if diff_keys:
            raise ex.UnknownSettingException(diff_keys)

        self.__config = default_config
        self.__config.update(user_config)

    def __getitem__(self, key):
        '''
        Implements the "dict lookup" in order to make the settings more
        Pythonic.
        Ex:
            settings['site.name']
        '''
        if key not in self.__config:
            raise ex.UnknownSettingException(key)
        return self.__config[key]

    def __setitem__(self, key, value):
        '''
        Implements the "dict attribution" in order to make the settings more
        Pythonic.
        Ex:
            settings['site.name'] = "My site"
        '''
        self.set_tmp(key, value)

        leaf_dict = self.__orig_dict
        for key_part in key.split('.')[:-1]:
            if key_part not in leaf_dict:
                leaf_dict[key_part] = {}
            leaf_dict = leaf_dict[key_part]
        else:
            leaf_dict[key.split('.')[-1]] = value

    def set_tmp(self, key, value):
        '''
        Implements a temporary settings attribution. In other words, the
        settings will only be stored in the __config dict, not in the
        __orig_dict.
        '''
        if key not in self.__config:
            raise ex.UnknownSettingException(key)
        self.__config[key] = value

    def get_path(self, key, fake_root=None):
        '''
        Inspect the requested path. If is an aboslute path (starting with /) it
        will return it as it is. If is a relative path, it will join with the
        site path. For dummy settings, inform a fake root.
        '''
        path = self[key]
        if path.startswith("/"):
            return path

        if fake_root:
            path = os.path.join(fake_root, path)
        else:
            path = os.path.join(self.site_basepath, path)

        return os.path.abspath(path)

    def save(self, fd=None):
        '''
        Stores the __orig_dict as a YAML file. If a fd is informed, it will
        write to it.
        '''
        if fd is None and not self.src_path:
            raise ex.DummySettingsException("Is this the real life? Is this just fantasy?")

        if fd:
            return yaml.safe_dump(self.__orig_dict, fd, default_flow_style=False)

        with open(self.src_path, 'w') as fd:
            yaml.safe_dump(self.__orig_dict, fd, default_flow_style=False, indent=8)

    @property
    def cache_obj(self):
        '''
        Return a dict with the items to be cached.
        '''
        return {
            'src-hash': self.src_hash,
            'type': self.type,
            }


def _dict_walk(data, parent_key=None):
    '''
    An easy to understand (and use) recursive implementatin of a walk function
    for nested dicts.
    '''
    for key, value in data.items():
        if isinstance(value, dict):
            if parent_key:
                key = "{}.{}".format(parent_key, key)
            yield from _dict_walk(value, key)
        else:
            if parent_key:
                key = "{}.{}".format(parent_key, key)
            yield (key, value)

def _flat_dict(data):
    '''
    Uses the _dict_walk to flatten a nested dict.
    '''
    new_dict = {}
    for key, value in _dict_walk(data):
        new_dict[key] = value
    return new_dict

def _load_sett(path):
    '''
    Load settings in the form of nested dicts from the YAML file.
    '''
    if not os.path.exists(path):
        return {}

    with open(path, 'r') as fd:
        data = yaml.safe_load(fd)
    return data
