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


'''
Nas grandes cidades do pequeno dia-a-dia.
O medo nos leva a tudo, sobretudo a fantasia.
Então erguemos muros que nos dão a garantia.
De que morreremos cheios de uma vida tão vazia.

Nas grandes cidades de um país tão violento.
Os muros e as grades nos protegem de quase tudo.
Mas o quase tudo quase sempre é quase nada.
E nada nos protege de uma vida sem sentido.

(...)

Um dia super... Uma noite super...  Uma vida superficial.
Entre sombras. Entre escombros. Da nossa solidez.

        --- Muros e Grades (Engenheiros do Hawaii)
'''

import os
import weakref

from math import ceil

from folios.core import utils
from folios.core import logger


class BaseIndex(object):
    '''
    Base class for all indexes. Should not be instantiated!
    '''
    __contents__ = []
    __name__ = ""
    __slots__ = [
        'settings',
        'log',
        ]

    def __init__(self, settings):
        '''
        Initialize the Index object, storing a reference to the settings and
        sorting the contents.
        '''
        self.settings = settings
        self.sort()

    @property
    def name(self):
        return self.__name__

    def deploy(self, site):
        raise NotImplemented

    @classmethod
    def sort(kls):
        raise NotImplemented

    @classmethod
    def add(kls, content):
        '''
        Stores the informed content in a list shared by all instances of this
        Index.
        '''
        kls.__contents__.append(content)


class IndexPage(object):
    '''
    A Index Page. This is the object that will be deployed in a paginated index.
    '''
    __slots__ = [
        "url",
        "slug",
        "index",
        "out_path",
        "contents",
        "settings",
        "page_number"
        ]
    def __init__(self, contents, page_number, index):
        '''
        Initialize the page, storing references to it's contents, it's page
        number, the master index object and retrieving patterns and paths from
        the settings object.
        '''
        self.contents = contents
        self.page_number = page_number
        self.index = index
        self.settings = index.settings
        self.slug = index.slug

        sufix = "first" if page_number == 1 else "others"
        out_path = self.settings['indexes.{}.save_as.{}'.format(
            index.__name__, sufix
            )]
        self.out_path = os.path.join(
            self.settings.get_path('core.output'),
            out_path
            )
        self.url = self.settings['indexes.{}.url.{}'.format(
            index.__name__, sufix
            )]

    def deploy(self, site):
        '''
        This method is responsible for writing the current page to the output.
        It will format the URL, out_path (save_as) and title using the page meta
        data.
        '''
        parameters = self.as_dict()
        self.out_path = self.out_path.format(**parameters)
        self.url = self.url.format(**parameters)

        title = "{slug} index" if self.page_number == 1 \
                else "{slug} index page {page_number}"
        title = title.format(**parameters)
        site.theme.write(
            self,
            "index.html",
            env={
                'settings': site.settings,
                'site': site,
                'content': self,
                'title': title
                }
            )

    @property
    def previews(self):
        '''
        Returns the previews page or None, if this is the first page.
        '''
        if self.page_number == 1:
            return None
        return self.index.pages[self.page_number - 2]

    @property
    def next(self):
        '''
        Returns the next page or None, if this is the last page.
        '''
        if self.page_number == len(self.index.pages):
            return None
        return self.index.pages[self.page_number]

    @property
    def norm_out_path(self):
        return utils.normpath(self.out_path)

    def as_dict(self, extras=None):
        out = {}
        for key in self.__slots__:
            if key != "__weakref__":
                out[key] = getattr(self, key)
        if extras:
            out.update(extras)
        return out


class BasePaginatedIndex(BaseIndex):
    __slots__ = BaseIndex.__slots__ + [
        'pages',
        ]

    def __init__(self, settings):
        '''
        Base paginated index. This is similar to a proxy class, since object
        will only generate it's pages and invoke they're writing methods.
        '''
        super().__init__(settings)
        self.pages = []

        page_size = self.settings['indexes.{}.page_size'.format(self.__name__)]
        pages_count = ceil(len(self.__contents__)/page_size)

        for page_n, idx in enumerate(range(0, len(self.__contents__), page_size)):
            contents = self.__contents__[idx:idx+page_size]
            self.pages.append(IndexPage(contents, page_n+1, self))

    def deploy(self, site):
        '''
        Invoke the deploy method for each page.
        '''
        for page in self.pages:
            self.log.debug("Writing {} index page {}".format(
                self.__name__,
                page.page_number
                ))
            page.deploy(site)


class ArticlesIndex(BasePaginatedIndex):
    __name__ = 'articles'

    def __init__(self, settings):
        '''
        Implements a paginated article for all articles.
        '''
        super().__init__(settings)
        self.log = logger.get_logger("ArticlesIndex", settings)

    @property
    def slug(self):
        return "article"

    @classmethod
    def sort(kls):
        '''
        Sort all articles based in it's date in reverse order (newest first).
        '''
        kls.__contents__.sort(key=lambda x: x.metadata['date'], reverse=True)
