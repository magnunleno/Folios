#!/usr/bin/env python3
# encoding: utf-8

import os
import shutil
import tempfile
from nose.tools import raises

from folios import cli
from folios.core import Site
from folios.core import Settings
from folios.core import exceptions as ex


@raises(ex.AbortException)
def test_not_a_site():
    tmpdir = tempfile.mkdtemp()
    not_a_site = os.path.join(tmpdir, 'not-a-site')
    os.mkdir(not_a_site)
    os.chdir(not_a_site)
    settings = Settings(os.getcwd())
    Site(settings, os.getcwd())


class TestSite(object):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        os.chdir(self.tmpdir)
        cli.main(['init', 'My Site', '-d', 'test-site'], do_exit=False)
        os.chdir(os.path.join(self.tmpdir, 'test-site'))
        settings = Settings(os.getcwd())
        self.s = Site(settings, os.getcwd())

    def teardown(self):
        shutil.rmtree(self.tmpdir)

    def test_init_settings(self):
        assert self.s.settings['core.articles'] == './articles'
        assert self.s.settings['core.images'] == './images'
        assert self.s.settings['core.output'] == './output'
        assert self.s.settings['cache.enable'] is True
        assert self.s.settings['cache.folder'] == './.folios/cache'

    def test_sitename_attribution(self):
        assert self.s.settings['site.name'] == 'My Site'

    def test_default_fallback(self):
        assert self.s.settings['site.url'] == 'http://localhost:8000'

    @raises(ex.UnknownSettingException)
    def test_site_get_invalid_section(self):
        self.s.settings['unkown.section']

    @raises(ex.UnknownSettingException)
    def test_site_get_invalid_option(self):
        self.s.settings['core.unknown']

    @raises(ex.UnknownSettingException)
    def test_site_set_invalid_section(self):
        self.s.settings['unkown.section'] = 'wrong'

    @raises(ex.UnknownSettingException)
    def test_site_set_invalid_option(self):
        self.s.settings['core.unknown'] = 'wrong'
