#!/usr/bin/env python3
# encoding: utf-8

import io
from nose.tools import raises

from folios.core import Settings
from folios.core import exceptions as ex

user_sett = {
    "site": {
        "name": "Testing site"
        }
    }

@raises(ex.AbortException)
def test_settings_bootstrap_exception():
    '''
    Tests the base settings bootstrap, which will raise and error when
    called outside a folios site.
    '''
    sett = Settings()

def test_settings_success_bootstrap():
    '''
    Tests the base settings bootstrap called in dummy mode.
    '''
    sett = Settings(from_dict=user_sett)

def test_retrieving_values():
    '''
    Test the data retrieval from settings for 2 values:
     - site.name: Set by the user settings (from_dict argument).
     - site.url: From the default settings.
    '''
    sett = Settings(from_dict=user_sett)
    assert sett['site.name'] == "Testing site"
    assert sett['site.url'] == "http://localhost:8000"

def test_path_retrieval():
    '''
    Tests the path retrieval, which should insert the site basepath before the
    stored path, unless it starts with a non relative path, ex: /tmp/output
    '''
    sett = Settings(from_dict=user_sett)
    sett['core.output'] = "/tmp/my-site-html"
    sett['images.source'] = "resources/images"

    assert sett.get_path("core.output") == "/tmp/my-site-html"
    assert sett.get_path("images.source", fake_root="/ROOT") == "/ROOT/resources/images"
    assert sett.get_path("articles.source", fake_root="/ROOT") == "/ROOT/articles"


def test_value_attribution():
    '''
    Tests a simple value attribution, assuring the previews and after values.
    Also, it checks if the value is ready to be saved.
    '''
    sett = Settings(from_dict=user_sett)
    assert sett['site.default_author'] == "John Doe"
    sett['site.default_author'] = "Jane Doe"
    assert sett['site.default_author'] == "Jane Doe"
    assert sett._Settings__orig_dict['site']['default_author'] == "Jane Doe"

def test_settings_save():
    '''
    Test settings save feature using StrinIO instead of a file.
    '''
    sett = Settings(from_dict=user_sett)
    sett['site.default_author'] = "Jane Doe"
    str_io = io.StringIO()
    sett.save(fd=str_io)
    saved = str_io.getvalue()
    assert saved == "site:\n  default_author: Jane Doe\n  name: Testing site\n"


def test_temp_value_attribution():
    '''
    Tests the temporary value attribution (won't be saved). A temporary value
    will not be saved, since it's stored only in Settings.__config.
    '''
    sett = Settings(from_dict=user_sett)

    assert sett['site.default_author'] == "John Doe"
    sett['site.default_author'] = "Another Doe"
    assert sett['site.default_author'] == "Another Doe"

    sett.set_tmp('site.default_author', "Jane Doe")
    assert sett['site.default_author'] == "Jane Doe"
    assert sett._Settings__config['site.default_author'] == "Jane Doe"
    assert sett._Settings__orig_dict['site']['default_author'] == "Another Doe"

    str_io = io.StringIO()
    sett.save(fd=str_io)
    saved = str_io.getvalue()
    assert saved == "site:\n  default_author: Another Doe\n  name: Testing site\n"

@raises(ex.UnknownSettingException)
def test_icorrect_value_attribution():
    '''
    Simple test to ensure the settings keys enforcement
    '''
    sett = Settings(from_dict=user_sett)
    sett['incorrect.key'] = "Value"

@raises(ex.DummySettingsException)
def test_settings_save():
    '''
    Ensure that Folios won't allow the user to save dummy settings.
    '''
    sett = Settings(from_dict=user_sett)
    sett.save()
