#!/usr/bin/env python3
# encoding: utf-8

import re
import hashlib
from os import path
from os import mkdir
from shutil import rmtree
from datetime import datetime
from unicodedata import normalize


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
