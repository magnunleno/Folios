#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
from folios import utils
from folios import cmd
from folios import exceptions

__ROOT__ = os.path.abspath(os.path.dirname(__file__))

__all__ = ['utils', 'cmd', 'exceptions']
__version__ = '0.1.0'


def main():
    try:
        cmd.main(sys.argv[1:])
    except exceptions.FoliosBaseException as e:
        print(e.message)
        exit(1)
    else:
        exit(0)
