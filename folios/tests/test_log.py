#!/usr/bin/env python3
# encoding: utf-8

from folios.core import logger
from io import StringIO
import re
import logging


LEVELS = {
    logging.DEBUG: 'This is a debug text',
    logging.INFO: 'This is an info text',
    logging.WARNING: 'This is a warning text',
    logging.ERROR: 'This is a error text',
    logging.CRITICAL: 'This is a critical text',
    }


def build_match(level, string, name):
    lvl, lvl_color, msg_color = logger.LEVEL[level]
    name_match = '[a-zA-Z._]*'
    if level == logging.INFO:
        return re.compile("{}@{}".format(name_match, string))
    return re.compile('{}@{}: {}'.format(name_match, lvl, string))


def build_debug_match(level, string, name):
    date_match = '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}'
    fname_match = '[a-zA-Z._]*'
    funcname_match = '[a-zA-Z._]*'
    lineno_match = '[0-9]*'
    lvl, lvl_color, msg_color = logger.LEVEL[level]
    if level == logging.INFO:
        text = string
    else:
        text = '{}: {}'.format(lvl, string)
    match = '\[{0}@{1}:{2}:{3}\] {4}'.format(
            date_match, fname_match,
            funcname_match, lineno_match,
            text
        )
    return re.compile(match)


def test_levels():
    sett = {
        'core.verbose': False,
        'cli-log.level': 'debug',
        'file-log.enable': False,
        'file-log.level': 'debug',
        }
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    name = 'test.default'
    log = logger.get_logger(name, sett, handler=handler)
    for lvl, string in LEVELS.items():
        yield check_level, lvl, string, stream, name, log


def test_verbose_levels():
    sett = {
        'core.verbose': True,
        'cli-log.level': 'debug',
        'file-log.enable': False,
        'file-log.level': 'debug',
        }
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    name = 'test.verbose'
    log = logger.get_logger(name, sett, handler=handler)
    for lvl, string in LEVELS.items():
        yield check_debug_level, lvl, string, stream, name, log


def check_level(lvl, string, stream, name, log):
    log.log(lvl, string)
    stream.flush()
    received = re.sub('\x1b.*?m', '', stream.getvalue())
    received = [item for item in received.split('\n') if item][-1]
    match = build_match(lvl, string, name)
    assert bool(match.match(received)) is True


def check_debug_level(lvl, string, stream, name, log):
    log.log(lvl, string)
    stream.flush()
    received = re.sub('\x1b.*?m', '', stream.getvalue())
    received = [item for item in received.split('\n') if item][-1]
    match = build_debug_match(lvl, string, name)
    assert bool(match.match(received)) is True
