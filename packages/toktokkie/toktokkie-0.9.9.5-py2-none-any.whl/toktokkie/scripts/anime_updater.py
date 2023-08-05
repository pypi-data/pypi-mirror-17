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
from __future__ import with_statement
from __future__ import absolute_import
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
from io import open


def update(config, search_engines):
    u"""
    Updates all shows defined in the config.

    :param config: List of dictionaries with the following attributes:
                        (target directory, season, quality, horriblesubs-name, bot)
    :param search_engines: List of search engines to be used
    :return: None
    """
    logfile = open(u"anime_updater.log", u'a')

    for show in config:

        horriblesubs_name = show[u"horriblesubs_name"]
        quality = show[u"quality"]
        season = int(show[u"season"])
        bot = show[u"bot"]

        show_directory = show[u"target_directory"]
        target_directory = os.path.join(show_directory, u"Season " + unicode(season))
        meta_directory = os.path.join(show_directory, u".icons")
        showname = os.path.basename(os.path.dirname(meta_directory))

        print u"Processing " + showname

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
                logfile.write(showname + u" episode " + unicode(current_episode) + u"\n")
            else:
                break
    logfile.close()


def get_next(horriblesubs_name, bot, quality, episode, search_engines):
    u"""
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

        episode_string = unicode(episode) if episode >= 10 else u"0" + unicode(episode)

        episode_patterns = [horriblesubs_name + u" - " + episode_string + u" \[" + quality + u"\].mkv",
                            horriblesubs_name + u"_-_" + episode_string]

        results = search_engine(horriblesubs_name + u" " + episode_string).search()

        for result in results:
            for pattern in episode_patterns:
                if result.bot == bot and re.search(re.compile(pattern), result.filename):
                    return result
    return None


def generate_rss_file(config):
    u"""
    Generates a Nyaa RSS OPML file as updater-rss.opml

    :param config: the config to turn into an RSS file
    :return: None
    """
    with open(u"updater-rss.opml", u'w') as opml_file:
        opml_file.write(u"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        opml_file.write(u"<opml version=\"1.1\">\n")
        opml_file.write(u"\t<head>\n")
        opml_file.write(u"\t\t<text>Anime Updater Releases</text>\n")
        opml_file.write(u"\t</head>\n")
        opml_file.write(u"\t<body>\n")
        opml_file.write(u"\t\t<outline text=\"Seasonal Anime\" title=\"Seasonal Anime\">\n")

        for show in config:
            showname = show[u"horriblesubs_name"]
            show_rss_outline = u"\t\t\t<outline text=\"" + showname + u"\" title=\"" + showname + u"\" type=\"rss\" "
            show_rss_outline += u"xmlUrl=\"https://www.nyaa.se/?page=rss&amp;cats=1_0&amp;term=horriblesubs+"
            show_rss_outline += showname.replace(u" ", u"+") + u"+" + show[u"quality"] + u"\" />\n"
            opml_file.write(show_rss_outline)

        opml_file.write(u"\t\t</outline>\n")
        opml_file.write(u"\t</body>\n")
        opml_file.write(u"</opml>")


def start(config, search_engines, continuous = False, looptime = 3600):
    u"""
    Starts the updater either once or in a continuous mode

    :param config: the config to be used to determine which shows to update
    :param search_engines: The search engines to be used
    :param continuous: flag to set continuous mode
    :param looptime: Can be set to determine the intervals between updates
    :return: None
    """
    # noinspection PyBroadException
    try:
        if u"rss" in sys.argv:
            generate_rss_file(config)

        else:

            if continuous:
                while True:
                    update(config, search_engines)
                    time.sleep(looptime)
            else:
                update(config, search_engines)
    except KeyboardInterrupt:
        print u"\nThanks for using the Tok Tokkie media manager!"
        sys.exit(0)
    except:
        sentry.captureException()
