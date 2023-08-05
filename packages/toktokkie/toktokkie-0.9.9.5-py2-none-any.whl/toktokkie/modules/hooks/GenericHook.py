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
from gfworks.interfaces.GenericWindow import GenericWindow
from puffotter.interactive_cli.PuffOtterCli import PuffOtterCli


class GenericHook(object):
    u"""
    Generic Plugin that serves as a unified interface for the media manager modules.

    It defines multiple methods that give information about the plugin, as well
    as methods to start the GUI, interactive CLI or argument-driven CLI
    """

    def get_name(self):
        u"""
        This method returns the name of the Plugin for display purposes

        :return: the name of this plugin
        """
        raise NotImplementedError()

    def get_command_name(self):
        u"""
        This method return the command name used by the argument parser
        when using the argument-driven CLI

        :return: the command that starts this plugin
        """
        raise NotImplementedError()

    def get_config_tag(self):
        u"""
        This method returns the tag used to enable or disable this plugin
        in the config file of media-manager.

        :return: the config tag of this plugin
        """
        raise NotImplementedError()

    def start_cli(self, parent_cli):
        u"""
        Starts the CLI of the plugin in interactive mode

        :param parent_cli: the parent cli to which the plugin can return to
        :return: None
        """
        raise NotImplementedError()

    def start_gui(self, parent_gui):
        u"""
        Starts the GUI of the plugin

        :param parent_gui: the gui's parent to which the plugin can return to
        :return: None
        """
        raise NotImplementedError()
