u"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
from typing import Tuple

from puffotter.calc import get_byte_size_from_string


class XDCCPack(object):
    u"""
    Class that models an XDCC Pack Object. It contains essential information about the
    pack and how to download it, as well as methods that can be called to access the information
    in a user-presentable way
    """

    filename = u""
    u"""
    The pack's file name
    """

    server = u""
    u"""
    The IRC server on which the bot that hosts this pack lives
    """

    channel = u""
    u"""
    The IRC channel on which the bot that hosts this pack lives
    """

    bot = u""
    u"""
    The bot that hosts the pack file
    """

    packnumber = -1
    u"""
    The pack number of the pack.
    """

    size = -1
    u"""
    The approximate file size of the pack in bytes
    """

    pretty_size = u""
    u"""
    The file size in a more human-readable format
    """

    def __init__(self, filename, server, bot, packnumber, size):
        u"""
        Constructor of the XDCCPack class. It gets information of the pack via the arguments
        and parses them accordingly

        :param filename: the pack's file name
        :param server: the server of the pack
        :param bot: the bot of the pack
        :param packnumber: the pack number
        :param size: the file size
        :return: None
        """
        self.filename = filename
        self.server = server
        self.bot = bot
        self.packnumber = packnumber
        self.size = get_byte_size_from_string(size)
        self.pretty_size = size

    def to_string(self):
        u"""
        Returns the bot information as a string
        :return: the bot information as a string
        """
        return self.filename + u"  -  " + self.bot + u"  -  Size:" + self.pretty_size

    def to_tuple(self):
        u"""
        Returns the bot information as a tuple
        :return: the bot information as a tuple
        """
        return self.bot, self.packnumber, self.pretty_size, self.filename
