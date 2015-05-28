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

import re
import hashlib
from os import path
from os import mkdir
from shutil import rmtree, copytree
from datetime import datetime
from unicodedata import normalize

import folios
from folios.core.exceptions import FoliosSkelException


def createFolder(folder_path):
    try:
        mkdir(folder_path)
    except OSError:
        return False
    return True


def deleteFolder(folder_path):
    try:
        rmtree(folder_path)
    except OSError:
        return False
    return True


def getSkel(skel_name):
    skel_path = path.abspath(
        path.sep.join([folios.__ROOT__, 'data', 'skel', skel_name])
        )
    if not path.exists(skel_path):
        raise FoliosSkelException("Couldn't file skel '{}'".format(skel_name))
    return skel_path


def copySkel(skel_name, dest_path):
    skel_path = getSkel(skel_name)
    dest_path = path.abspath(dest_path)
    copytree(skel_path, dest_path)


def getFileCTime(file_path):
    if not path.exists(file_path):
        return None
    mtime = datetime.fromtimestamp(path.getctime(file_path))
    return str(mtime)


def getFileMTime(file_path):
    if not path.exists(file_path):
        return None
    mtime = datetime.fromtimestamp(path.getmtime(file_path))
    return str(mtime)


def sha1(file_path):
    if not path.exists(file_path):
        return None
    hash = hashlib.sha1()
    with open(file_path, 'rb') as f:
        read_chunk = iter(lambda: f.read(hash.block_size), b'')
        for chunk in read_chunk:
            hash.update(chunk)
    return hash.hexdigest()


def slugify(text):
    '''
    Taken from DJango source code:
    https://github.com/django/django/blob/master/django/utils/text.py
    '''
    text = normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub('[^\w\s-]', '', text).strip().lower()
    return re.sub('[-\s]+', '-', text)
