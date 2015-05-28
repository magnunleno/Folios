#!/usr/bin/env python3
# encoding: utf-8
#
# Folios - Yet Another Static Site Generator
# Copyright (C) 2015 - Magnun Leno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import logging
from logging import handlers
from colorama import Fore, Back, Style

INITIALIZED = False
RESET_ALL = Fore.RESET + Back.RESET + Style.RESET_ALL

LEVEL = {
    logging.DEBUG: (
        'DEBG',
        Fore.BLACK + Back.BLUE + Style.NORMAL,
        Fore.BLUE + Back.RESET + Style.NORMAL,
        ),
    logging.INFO: (
        'INFO',
        Fore.RESET + Back.RESET + Style.NORMAL,
        Fore.RESET + Back.RESET + Style.NORMAL,
        ),
    logging.WARNING: (
        'WARN',
        Fore.BLACK + Back.YELLOW + Style.NORMAL,
        Fore.YELLOW + Back.RESET + Style.NORMAL,
        ),
    logging.ERROR: (
        'ERRR',
        Fore.BLACK + Back.RED + Style.NORMAL,
        Fore.RED + Back.RESET + Style.NORMAL,
        ),
    logging.CRITICAL: (
        'CRIT',
        Fore.YELLOW + Back.RED + Style.NORMAL,
        Fore.RED + Back.RESET + Style.BRIGHT,
        ),
    }


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, verbose=False):
        self.verbose = verbose

        if self.verbose:
            fmt = Style.DIM + "[%(asctime)s] %(name)s:%(funcName)s@" + \
                "%(filename)s:%(lineno)s" + Style.NORMAL + \
                " %(level_color)s%(message)s"
        else:
            fmt = Style.DIM + "%(name)s@" + Style.NORMAL + \
                "%(level_color)s%(message)s"

        datefmt = "%Y-%m-%d %H:%M"
        super(ColorFormatter, self).__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):
        if (hasattr(record, 'colorized') and record.colorized):
            return super(ColorFormatter, self).format(record)

        lvl, lvl_cl, msg_cl = LEVEL[record.levelno]
        if record.levelno == logging.INFO:
            record.level_color = RESET_ALL
        else:
            record.level_color = "{0}{1}:{2} ".format(lvl_cl, lvl, RESET_ALL)
        record.msg = msg_cl + record.msg + RESET_ALL
        return super(ColorFormatter, self).format(record)


def resolve_level(name):
    name = name.upper()
    if hasattr(logging, name):
        return getattr(logging, name)
    else:
        print("Unknown logging level '{}'", name)
        print("Using fallback value: warning")
        return logging.INFO


def get_logger(name, settings, handler=None):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    # File logger
    file_level = resolve_level(settings['file-log.level'])
    if settings['file-log.enable']:
        logger.addHandler(
            get_file_handler(
                fname=settings['file-log.file_name'],
                size=int(settings['file-log.size'])*1024,
                backups=int(settings['file-log.backups']),
                level=file_level,
                )
            )

    # Cli logger
    cli_level = resolve_level(settings['cli-log.level'])
    logger.addHandler(
        get_cli_handler(
            handler=handler,
            level=cli_level,
            verbose=settings['core.verbose'],
            )
        )
    if cli_level <= file_level:
        logger.setLevel(cli_level)
    else:
        logger.setLevel(file_level)

    return logger


def get_cli_handler(handler=None, level=logging.WARNING, verbose=False):
    if handler is None:
        handler = logging.StreamHandler()

    handler.setLevel(level)
    handler.setFormatter(ColorFormatter(verbose=verbose))
    return handler


def get_file_handler(fname, size, backups, level=logging.INFO):
    handler = handlers.RotatingFileHandler(
        fname,
        maxBytes=size,
        backupCount=backups
        )
    handler.setLevel(level)
    handler.setFormatter(
        logging.Formatter(
            fmt="[%(asctime)s@%(name)s] :%(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M"
            )
        )
    return handler

if __name__ == '__main__':
    print("First test")
    log = get_logger('main',
                     {
                         'core.verbose': True,
                         'cli-log.level': 'debug',
                         'file-log.enable': True,
                         'file-log.file_name': '/tmp/folios.log',
                         'file-log.level': 'debug',
                         'file-log.backups': 5,
                         'file-log.size': 10,
                     }
                     )
    log.debug('This is a debug text')
    log.info('This is a info text')
    log.warning('This is a warning text')
    log.error('This is a error text')
    log.critical('This is a critical text')

    print("\nSecond test")
    log = get_logger('main2',
                     {
                         'core.verbose': False,
                         'cli-log.level': 'debug',
                         'file-log.enable': True,
                         'file-log.file_name': '/tmp/folios.log',
                         'file-log.level': 'debug',
                         'file-log.backups': 5,
                         'file-log.size': 10,
                         }
                     )
    log.debug('This is a debug text')
    log.info('This is a info text')
    log.warning('This is a warning text')
    log.error('This is a error text')
    log.critical('This is a critical text')
