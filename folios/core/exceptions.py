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
I'd rather hate you for everything you are
Than ever love you for something you are not
I'd rather you hate me for everything i am
Than have you love me for something that i can't
            --- Never Enough (Five Finger Death Punch)
"""

class BaseException(Exception):
    def __init__(self, message):
        self.message = message


class AbortException(BaseException):
    pass


class SkelException(BaseException):
    pass


class UnexistentSourceException(BaseException):
    pass



class UnknownSettingException(BaseException):
    def __init__(self, key):
        if isinstance(key, str):
            self.message = "Unknown setting '{}'".format(key)
        elif isinstance(key, set):
            key = ", ".join(key)
            self.message = "Unknown setting '{}'".format(key)


class DummySettingsException(BaseException):
    pass


class ContentCompilingException(BaseException):
    pass
