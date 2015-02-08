#!/usr/bin/env python3
# encoding: utf-8

from folios import cli
from nose.tools import raises
from docopt import DocoptExit


@raises(DocoptExit)
def test_main_error():
    cli.main([])


@raises(DocoptExit)
def test_main_not_implemented():
    cli.main(['NotImplemented'])


@raises(DocoptExit)
def test_main_init_error():
    cli.main(['-v'])
