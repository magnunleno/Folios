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
This module implements a miscellaneous of functions used by the whole Folios
project.


Rock 'n' roll ain't noise pollution
Rock 'n' roll ain't gonna die
Rock 'n' roll ain't noise pollution
Rock 'n' roll it will survive 

        --- Rock 'n' Roll Ain't Noise Pollution (AC/DC)
"""

import re
import os
import shutil
import hashlib
import unicodedata

import folios
from folios.core import __rootfolder__
from folios.core import exceptions as ex

ROOT_FOLDER = None


def resolve_root_folder(folder=None):
    '''
    Searches recursively for the site's root folder, having the provided folder
    (or the current folder) as the starting point. This function will return the
    absolute path of the site's root folder or raise an AbortError exception.
    '''
    if not folder:
        folder = os.getcwd()

    global ROOT_FOLDER
    if ROOT_FOLDER:
        return ROOT_FOLDER

    if not os.path.basename(folder):
        errstr = "I'm sorry Dave. I'm afraid I can't do that. " +\
            "Are you sure you're inside a Folios site folder?"
        raise ex.AbortException(errstr)

    if is_folios_site(folder):
        ROOT_FOLDER = folder
        return folder

    # Go back one level and try again
    new_folder = os.path.abspath(os.path.join(folder, os.path.pardir))
    ROOT_FOLDER = resolve_root_folder(new_folder)
    return ROOT_FOLDER


def is_folios_site(path):
    '''
    Check's if the specified folder is a folios site (if there is a .folios
    folder).
    '''
    return os.path.exists(os.path.join(path, __rootfolder__))


def normpath(path, base=None):
    '''
    This function normalize a path taking as starting point the current working
    director, or the path informed on the base argument.
    '''
    if base is None:
        base = os.getcwd()
    path = os.path.abspath(path)
    return os.path.relpath(path, base)


def delete_folder(folder_path):
    '''
    This function deletes an specified folder and all it's contents, regardless
    of it's existence.
    '''
    try:
        shutil.rmtree(folder_path)
    except OSError:
        return False
    return True


def get_skel(skel_name):
    '''
    Inspect the skel folder searching for a skeleton folder/file. Raises and
    SkelException if the skeleton name doesn't exist.
    '''
    skel_path = os.path.abspath(
        os.path.sep.join([folios.__root__, 'data', 'skel', skel_name])
        )
    if not os.path.exists(skel_path):
        raise ex.SkelException("Couldn't file skel '{}'".format(skel_name))
    return skel_path


def copy_skel(skel_name, dest_path):
    '''
    Copy an skeleton folder/file for the specified destination. Uses the
    get_skel function in order to ensure the existence of the informed skeleton.
    '''
    skel_path = get_skel(skel_name)
    dest_path = os.path.abspath(dest_path)
    shutil.copytree(skel_path, dest_path)


def mkdir(path):
    '''
    Make a directory (and all it's non existent parent folders), weather it
    already exists or not. Just like "mkdir -p ./sub/parent".
    '''
    if os.path.exists(path):
        return

    head, tail = os.path.split(path)
    if head == tail:
        return

    if not os.path.exists(head):
        mkdir(head)
    os.mkdir(path)


def copy(src, dst):
    '''
    Copy a file/folder to a specified destination. If the destination doesn't
    exist, it will create the necessary folders. If the source doesn't exist, it
    raises and UnexistentSourceException.
    '''
    if not os.path.exists(src):
        raise ex.UnexistentSourceException("Couldn't fund '{}'".format(src))

    folder = os.path.dirname(dst)
    if not os.path.exists(folder):
        mkdir(folder)

    shutil.copy(src, dst)
    return True


def list_files(root, filters=set()):
    '''
    Recursively list all files from an specified root folder. If necessary, you
    can specify a set with the filenames to be ignored.
    '''
    for root, dirs, files in os.walk(root):
        for fname in files:
            if fname in filters:
                continue
            yield os.path.abspath(os.path.join(root, fname))


def list_empty_folders(root):
    '''
    Lists all empty directories from a specified root folder.
    '''
    for root, dirs, files in os.walk(root):
        if not dirs and not files:
            yield os.path.abspath(root)


def sha1(file_path):
    '''
    Returns an sha1 hexdigest for a file. If the file doesn't exists it raises
    an UnexistentSourceException.
    '''
    if not os.path.exists(file_path):
        raise ex.UnexistentSourceException("Couldn't fund '{}'".format(file_path))

    hash = hashlib.sha1()
    with open(file_path, 'rb') as f:
        read_chunk = iter(lambda: f.read(hash.block_size), b'')
        for chunk in read_chunk:
            hash.update(chunk)
    return hash.hexdigest()


def slugify(text):
    '''
    Creates a slug for a given string.

    Taken from DJango source code:
    https://github.com/django/django/blob/master/django/utils/text.py
    '''
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub('[^\w\s-]', '', text).strip().lower()
    return re.sub('[-\s]+', '-', text)
