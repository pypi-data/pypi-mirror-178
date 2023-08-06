#!/usr/bin/python3
# -*- coding:Utf-8 -*-

# +--------------------------------------------------------------------------+
# | Layrageu                                                                 |
# | Copyright (C) 2022 Étienne Nadji                                         |
# |                                                                          |
# | This program is free software: you can redistribute it and/or modify     |
# | it under the terms of the GNU Affero General Public License as           |
# | published by the Free Software Foundation, either version 3 of the       |
# | License, or (at your option) any later version.                          |
# |                                                                          |
# | This program is distributed in the hope that it will be useful,          |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of           |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |
# | GNU Affero General Public License for more details.                      |
# |                                                                          |
# | You should have received a copy of the GNU Affero General Public License |
# | along with this program.  If not, see <https://www.gnu.org/licenses/>.   |
# +--------------------------------------------------------------------------+

"""
Layrageu : send Mastodon toots from a Flat OpenDocuments file.
"""

import os

__version__ = "0.2.1"
__author__ = "Etienne Nadji <etnadji@eml.cc>"

TOOT_VISIBILITIES = ["private", "unlisted", "public"]


def debug_mode() -> True:
    debug = os.environ.get("DEBUG_LAYRAGEU")

    if debug is None:
        return False

    return debug == "1"


# vim:set shiftwidth=4 softtabstop=4:
