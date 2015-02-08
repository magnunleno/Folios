#!/usr/bin/env python3
# encoding: utf-8

from folios.core import utils


def test_slugify():
    assert utils.slugify('Testing slugs!') == 'testing-slugs'
    assert utils.slugify('Açáéóíãà/-123') == 'acaeoiaa-123'
    assert utils.slugify('nothing-¢£¤¥§©in-between') == 'nothing-in-between'
