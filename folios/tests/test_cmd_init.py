#!/usr/bin/env python3
# encoding: utf-8

from folios import cmd
from nose.tools import raises
from docopt import DocoptExit


@raises(DocoptExit)
def test_init_error():
    cmd.main(['init'])


@raises(DocoptExit)
def test_init_unknown_option():
    cmd.main(['init', 'site-name', '-x'])


def test_init_site():
    args = cmd.main(['init', 'site-name'])
    assert args['init'] is True
    assert args['<site-name>'] == 'site-name'
    assert args['-d'] is None


def test_init_site_folder():
    args = cmd.main(['init', 'site-name', '-d', 'folder-name'])
    assert args['init'] is True
    assert args['<site-name>'] == 'site-name'
    assert args['-d'] == 'folder-name'
