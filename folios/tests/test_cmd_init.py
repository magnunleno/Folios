#!/usr/bin/env python3
# encoding: utf-8

import os
import tempfile
from folios import __rootfolder__
from folios import cmd
from folios import utils
from nose.tools import raises
from docopt import DocoptExit


@raises(DocoptExit)
def test_init_error():
    cmd.main(['init'])


@raises(DocoptExit)
def test_init_unknown_option():
    cmd.main(['init', 'site-name', '-x'])


def test_init_site():
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    args = cmd.main(['init', 'site-name'])
    assert args['init'] is True
    assert args['<site-name>'] == 'site-name'
    assert args['-d'] is None
    assert os.path.exists(utils.joinPath(tmpdir, 'site-name'))
    assert os.path.exists(utils.joinPath(tmpdir, 'site-name', 'articles'))
    assert os.path.exists(utils.joinPath(tmpdir, 'site-name', 'images'))
    assert os.path.exists(utils.joinPath(tmpdir, 'site-name', __rootfolder__))
    utils.deleteFolder(tmpdir)


def test_init_site_folder():
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    args = cmd.main(['init', 'site-name', '-d', 'folder-name'])
    assert args['init'] is True
    assert args['<site-name>'] == 'site-name'
    assert args['-d'] == 'folder-name'
    assert os.path.exists(utils.joinPath(tmpdir, 'folder-name'))
    assert os.path.exists(utils.joinPath(tmpdir, 'folder-name', 'articles'))
    assert os.path.exists(utils.joinPath(tmpdir, 'folder-name', 'images'))
    assert os.path.exists(utils.joinPath(tmpdir, 'folder-name', __rootfolder__))
    utils.deleteFolder(tmpdir)
