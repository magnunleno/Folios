#!/usr/bin/env python3
# encoding: utf-8

from folios import cmd
from nose.tools import raises
from docopt import DocoptExit


@raises(DocoptExit)
def test_main_error():
    cmd.main([])


@raises(DocoptExit)
def test_main_not_implemented():
    cmd.main(['NotImplemented'])


@raises(DocoptExit)
def test_main_init_error():
    cmd.main(['-v'])
