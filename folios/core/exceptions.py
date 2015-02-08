#!/usr/bin/env python3
# encoding: utf-8


class FoliosBaseException(Exception):
    def __init__(self, message):
        self.message = message


class FoliosAbortException(FoliosBaseException):
    pass


class FoliosSkelException(FoliosBaseException):
    pass
