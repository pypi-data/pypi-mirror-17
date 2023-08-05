"""
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
import os
import re
import sys
import time

from typing import Dict, List

from toktokkie.modules.objects.ProgressStruct import ProgressStruct
from toktokkie.modules.objects.XDCCPack import XDCCPack
from toktokkie.modules.objects.Episode import Episode
from toktokkie.metadata import sentry
from toktokkie.modules.utils.downloaders.IrcLibDownloader import IrcLibDownloader
from toktokkie.modules.utils.searchengines.SearchEngineManager import SearchEngineManager


def update(config: List[Dict[str, str]], search_engines: List[str]) -> None:
    """
    Updates all shows defined in the config.

    :param config: List of dictionaries with the following attributes:
                        (target directory, season, quality, horriblesubs-name, bot)
    :param search_engines: List of search engines to be used
    :return: None
    """
    logfile = open("anime_updater.log", 'a')

    for show in config:

        horriblesubs_name = show["horriblesubs_name"]
        quality = show["quality"]
        season = int(show["season"])
        bot = show["bot"]

        show_directory = show["target_directory"]
        target_directory = os.path.join(show_directory, "Season " + str(season))
        meta_directory = os.path.join(show_directory, ".icons")
        showname = os.path.basename(os.path.dirname(meta_directory))

        print("Processing " + showname)

        if not os.path.isdir(meta_directory):
            os.makedirs(meta_directory)
        if not os.path.isdir(target_directory):
            os.makedirs(target_directory)

        episode_count = 1
        previous_eps = os.listdir(target_directory)
        for previous_ep in sorted(previous_eps):
            episode = Episode(os.path.join(target_directory, previous_ep), episode_count, season, showname)
            episode.rename()
            episode_count += 1

        while True:  # == Do While Loop
            current_episode = len(os.listdir(target_directory)) + 1
            next_pack = get_next(horriblesubs_name, bot, quality, current_episode, search_engines)
            if next_pack:
                prog = ProgressStruct()
                downloader = IrcLibDownloader([next_pack],
                                              prog,
                                              target_directory,
                                              showname,
                                              current_episode,
                                              season,
                                              verbosity_level=1)
                downloader.download_loop()
                logfile.write(showname + " episode " + str(current_episode) + "\n")
            else:
                break
    logfile.close()


def get_next(horriblesubs_name: str, bot: str, quality: str, episode: int, search_engines: List[str]) -> XDCCPack:
    """
    Gets the next XDCC Pack of a show, if there is one

    :param horriblesubs_name: the horriblesubs name of the show
    :param bot: the bot from which the show should be downloaded
    :param quality: the quality the show is supposed to be in
    :param episode: the episode to download
    :param search_engines: The search engines to use
    :return: The XDCC Pack to download or None if no pack was found
    """

    for searcher in search_engines:

        search_engine = SearchEngineManager.get_search_engine_from_string(searcher)

        episode_string = str(episode) if episode >= 10 else "0" + str(episode)

        episode_patterns = [horriblesubs_name + " - " + episode_string + " \[" + quality + "\].mkv",
                            horriblesubs_name + "_-_" + episode_string]

        results = search_engine(horriblesubs_name + " " + episode_string).search()

        for result in results:
            for pattern in episode_patterns:
                if result.bot == bot and re.search(re.compile(pattern), result.filename):
                    return result
    return None


def generate_rss_file(config: List[Dict[str, str]]) -> None:
    """
    Generates a Nyaa RSS OPML file as updater-rss.opml

    :param config: the config to turn into an RSS file
    :return: None
    """
    with open("updater-rss.opml", 'w') as opml_file:
        opml_file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        opml_file.write("<opml version=\"1.1\">\n")
        opml_file.write("\t<head>\n")
        opml_file.write("\t\t<text>Anime Updater Releases</text>\n")
        opml_file.write("\t</head>\n")
        opml_file.write("\t<body>\n")
        opml_file.write("\t\t<outline text=\"Seasonal Anime\" title=\"Seasonal Anime\">\n")

        for show in config:
            showname = show["horriblesubs_name"]
            show_rss_outline = "\t\t\t<outline text=\"" + showname + "\" title=\"" + showname + "\" type=\"rss\" "
            show_rss_outline += "xmlUrl=\"https://www.nyaa.se/?page=rss&amp;cats=1_0&amp;term=horriblesubs+"
            show_rss_outline += showname.replace(" ", "+") + "+" + show["quality"] + "\" />\n"
            opml_file.write(show_rss_outline)

        opml_file.write("\t\t</outline>\n")
        opml_file.write("\t</body>\n")
        opml_file.write("</opml>")


def start(config: List[Dict[str, str]], search_engines: List[str], continuous: bool = False, looptime: int = 3600)\
        -> None:
    """
    Starts the updater either once or in a continuous mode

    :param config: the config to be used to determine which shows to update
    :param search_engines: The search engines to be used
    :param continuous: flag to set continuous mode
    :param looptime: Can be set to determine the intervals between updates
    :return: None
    """
    # noinspection PyBroadException
    try:
        if "rss" in sys.argv:
            generate_rss_file(config)

        else:

            if continuous:
                while True:
                    update(config, search_engines)
                    time.sleep(looptime)
            else:
                update(config, search_engines)
    except KeyboardInterrupt:
        print("\nThanks for using the Tok Tokkie media manager!")
        sys.exit(0)
    except:
        sentry.captureException()
