#!/usr/bin/python
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
import sys
from typing import List

from gfworks.templates.generators.GridTemplateGenerator import GridTemplateGenerator
from toktokkie.eastereggs.EasterEggManager import EasterEggManager
from toktokkie.modules.gui.framework import GlobalGuiFramework
from toktokkie.metadata import sentry


# noinspection PyTypeChecker
def main(ui_override = u"", easter_egg_override = None):
    u"""
    Main method that runs the program.

    It can be used without parameters, in which case it will start in interactive
    command line mode.

    Other options include using the --gtk or --tk flags to start either a GTK 3- or
    a Tkinter-based graphical user interface. This can also be accomplished by
    passing 'gtk' or 'tk' as the ui_override parameter of the main method.

    :param ui_override: Can override the program mode programmatically
    :param easter_egg_override: Can give a second kind of sys.argv for use in easter eggs
    :return: None
    """

    # noinspection PyBroadException
    try:

        # Activate Easter Eggs
        EasterEggManager.activate_easter_eggs(sys.argv, easter_egg_override)

        # First, the used mode of the program is determined using sys.argv
        cli_mode = False

        # Try to set a GUI framework, if it fails use the CLI instead
        try:
            selected_gui = ui_override
            if not selected_gui:
                selected_gui = sys.argv[1]
            GlobalGuiFramework.selected_grid_gui_framework = GridTemplateGenerator.get_grid_templates()[selected_gui]
        except (KeyError, IndexError):
            cli_mode = True

        # The program starts here, using the selected mode
        if cli_mode:
            from toktokkie.modules.cli.MainCli import MainCli
            MainCli().start()
        else:
            from toktokkie.modules.gui.MainGui import MainGui
            MainGui().start()

    except KeyboardInterrupt:
        print u"\nThanks for using the Tok Tokkie media manager!"
        sys.exit(0)
    except:
        sentry.captureException()


# This executes the main method
if __name__ == u'__main__':
    main()


