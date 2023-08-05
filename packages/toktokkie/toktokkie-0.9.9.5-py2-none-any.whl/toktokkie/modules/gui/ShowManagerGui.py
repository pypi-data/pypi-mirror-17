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
from toktokkie.modules.gui.framework import GlobalGuiFramework


class ShowManagerGui(GlobalGuiFramework.selected_grid_gui_framework):
    u"""
    GUI for the Show Manager plugin
    """

    def __init__(self, parent):
        u"""
        Constructor
        :param parent: the parent gui
        :return: void
        """
        # Initialization
        self.directory_browse_entry = None
        self.directory_browse_button = None
        self.directory_name_label = None
        self.directory_content_list_box = None

        self.selected_show_name = None
        self.selected_show_main_icon = None
        self.selected_show_season_icon = None
        self.selected_show_content_list_box = None

        super(ShowManagerGui, self).__init__(u"Show Manager", parent, True)

    def lay_out(self):
        u"""
        Sets up all interface elements of the GUI
        :return: void
        """
        self.directory_browse_entry = self.generate_text_entry(u"")
        self.directory_browse_button = self.generate_button(u"Browse")
        self.directory_name_label = self.generate_label(u"                                    ")
        self.directory_content_list_box = self.generate_primitive_multi_column_list_box(
            {u"Directory": (0, unicode), u"Show Name": (1, unicode)}, False)

        self.position_absolute(self.directory_browse_entry, 0, 0, 10, 5)
        self.position_absolute(self.directory_browse_button, 10, 0, 10, 5)
        self.position_absolute(self.directory_name_label, 20, 0, 10, 5)
        self.position_absolute(self.directory_content_list_box, 0, 5, 30, 50)

        self.selected_show_name = self.generate_label(u"")
        self.selected_show_main_icon = self.generate_label(u"Image goes Here")
        self.selected_show_season_icon = self.generate_label(u"Image goes Here")
        self.selected_show_content_list_box = self.generate_primitive_multi_column_list_box({u"Show Name": (0, unicode)})

        self.position_absolute(self.selected_show_name, 30, 0, 40, 10)
        self.position_absolute(self.selected_show_main_icon, 30, 10, 20, 20)
        self.position_absolute(self.selected_show_season_icon, 50, 10, 20, 20)
        self.position_absolute(self.selected_show_content_list_box, 30, 30, 40, 25)




