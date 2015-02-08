#!/usr/bin/env python3
# encoding: utf-8

import os
import tempfile
from folios.core import exceptions, site
from folios.core.settings import Settings
from folios import cli
from nose.tools import raises
import shutil


@raises(exceptions.FoliosAbortException)
def test_not_a_site():
    tmpdir = tempfile.mkdtemp()
    not_a_site = os.path.join(tmpdir, 'not-a-site')
    os.mkdir(not_a_site)
    os.chdir(not_a_site)
    settings = Settings(os.getcwd())
    site.Site(os.getcwd(), settings)


class TestSite(object):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        os.chdir(self.tmpdir)
        cli.main(['init', 'My Site', '-d', 'test-site'], do_exit=False)
        os.chdir(os.path.join(self.tmpdir, 'test-site'))
        settings = Settings(os.getcwd())
        self.s = site.Site(os.getcwd(), settings)

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

    @raises(exceptions.UnknownSettingException)
    def test_site_get_invalid_section(self):
        self.s.settings['unkown.section']

    @raises(exceptions.UnknownSettingException)
    def test_site_get_invalid_option(self):
        self.s.settings['core.unknown']

    @raises(exceptions.UnknownSettingException)
    def test_site_set_invalid_section(self):
        self.s.settings['unkown.section'] = 'wrong'

    @raises(exceptions.UnknownSettingException)
    def test_site_set_invalid_option(self):
        self.s.settings['core.unknown'] = 'wrong'
