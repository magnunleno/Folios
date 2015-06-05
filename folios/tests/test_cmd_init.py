#!/usr/bin/env python3
# encoding: utf-8

import os
import tempfile
from docopt import DocoptExit
from nose.tools import raises

from folios import cli
from folios.core import utils
from folios.core import __rootfolder__


@raises(DocoptExit)
def test_init_error():
    cli.main(['init'])


@raises(DocoptExit)
def test_init_unknown_option():
    cli.main(['init', 'site-name', '-x'])


def test_init_site():
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    print("TMP", tmpdir)
    cli.main(['init', 'site-name'], do_exit=False)
    assert os.path.exists(os.path.join(tmpdir, 'site-name'))
    assert os.path.exists(os.path.join(tmpdir, 'site-name', 'articles'))
    assert os.path.exists(os.path.join(tmpdir, 'site-name', 'images'))
    assert os.path.exists(os.path.join(tmpdir, 'site-name', __rootfolder__))
    utils.delete_folder(tmpdir)


def test_init_site_folder():
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    cli.main(['init', 'site-name', '-d', 'folder-name'], do_exit=False)
    assert os.path.exists(os.path.join(tmpdir, 'folder-name'))
    assert os.path.exists(os.path.join(tmpdir, 'folder-name', 'articles'))
    assert os.path.exists(os.path.join(tmpdir, 'folder-name', 'images'))
    assert os.path.exists(os.path.join(tmpdir, 'folder-name', __rootfolder__))
    utils.delete_folder(tmpdir)
