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

from urllib.parse import urljoin
from collections.abc import Iterable

from folios.core import utils
from folios.core import logger


class GenericContent(object):
    type = "Generic Content"
    __all__ = {}
    __extensions__ = []
    __slots__ = [
        'log',
        'slug',
        'fname',
        'out_hash',
        'src_hash',
        'src_path',
        'settings',
        ]

    def __init__(self, path, settings):
        super().__init__()
        self.settings = settings
        self.src_path = path

        self.fname = os.path.basename(self.src_path)
        self.src_hash = utils.sha1(self.src_path)
        self.out_hash = None

        name, extension = os.path.splitext(self.fname)
        self.slug = utils.slugify(name)

    @property
    def norm_src_path(self):
        return utils.normpath(self.src_path, utils.resolve_root_folder())

    @property
    def out_path(self):
        out_path = os.path.join(
            self.settings.get_path('core.output'),
            self.settings['{}.save_as'.format(self.type)],
            )
        return out_path.format(**self.as_dict())

    @property
    def norm_out_path(self):
        return utils.normpath(self.out_path, utils.resolve_root_folder())

    @property
    def url(self):
        # TODO: Review this
        fmt = self.settings['{}.url'.format(self.type)]
        return urljoin(
            self.settings['site.url'],
            '/'.join(fmt.format(**self.as_dict()).split(os.sep)),
            )
    @property
    def extension(self):
        name, extension = os.path.splitext(self.fname)
        if extension and extension.startswith("."):
            return extension[1:]
        return None

    def as_dict(self):
        out = {}
        for key in self.__slots__:
            if key != "__weakref__":
                out[key] = getattr(self, key)
        return out

    @property
    def compilable(self):
        raise NotImplemented("You must implement this!")

    @property
    def cache_obj(self):
        return {
            "src-hash": self.src_hash,
            "out-hash": self.out_hash,
            "type": self.type,
            }

    @classmethod
    def search(kls, settings):
        kls.__all__ = {}
        base_search_path = settings.get_path('{}.source'.format(kls.type))
        for path in utils.list_files(base_search_path,
                extensions=kls.__extensions__):
            obj = kls(path, settings)
            kls.__all__[path] = obj
        return [i for i in kls.__all__.values()]

from folios.core.content.theme import Theme
from folios.core.content.article import Article
