#!/usr/bin/env python3
# encoding: utf-8

import os
import tempfile
from folios import utils, exceptions, cmd, site
from nose.tools import raises


@raises(exceptions.FoliosAbortException)
def test_not_a_site():
    tmpdir = tempfile.mkdtemp()
    not_a_site = utils.joinPath(tmpdir, 'not-a-site')
    os.mkdir(not_a_site)
    os.chdir(not_a_site)
    site.Site()


def test_site_init():
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    cmd.main(['init', 'My Site', '-d', 'test-site'])
    os.chdir(utils.joinPath(tmpdir, 'test-site'))
    s = site.Site()
    assert s.settings['site.name'] == 'My Site'
