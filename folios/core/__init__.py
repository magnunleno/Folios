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

"""
You can choose a ready guide
In some celestial voice
If you choose not to decide
You still have made a choice

You can choose from phantom fears
And kindness that can kill
I will choose a path that's clear
I will choose free will

        --- Freewill (Rush)
"""

__all__ = ['exceptions', 'logger', 'settings', 'site', 'utils']
__rootfolder__ = '.folios'

from folios.core import utils
from folios.core.site import Site
from folios.core.settings import Settings
