# coding=utf-8
# noinspection PyUnresolvedReferences
import chatcommunicate  # coverage
import chatcommands
from apigetpost import api_get_post
from parsing import to_protocol_relative
from classes._Post import Post
from globalvars import GlobalVars
from datahandling import _remove_pickle

import datetime
import os
import pytest
import regex
import types
import requests
if GlobalVars.on_windows:
    # noinspection PyPep8Naming
    from classes._Git_Windows import git
else:
    from sh.contrib import git

from fake import Fake
from unittest.mock import patch


def test_null():
    assert chatcommands.null() is None


def test_coffee():
    msg = Fake({"owner": {"name": "El'endia Starman"}})

    coffees = "\\*brews a cup of ({}) for ".format("|".join(chatcommands.COFFEES))
    assert regex.match(coffees + "@El'endiaStarman\\*", chatcommands.coffee(None, original_msg=msg))
    assert regex.match(coffees + "@angussidney\\*", chatcommands.coffee("angussidney"))


def test_tea():
    msg = Fake({"owner": {"name": "El'endia Starman"}})

    teas = "\\*brews a cup of ({}) tea for ".format("|".join(chatcommands.TEAS))
    assert regex.match(teas + "@El'endiaStarman\\*", chatcommands.tea(None, original_msg=msg))
    assert regex.match(teas + "@angussidney\\*", chatcommands.tea("angussidney"))


def test_lick():
    assert chatcommands.lick() == "*licks ice cream cone*"


def test_brownie():
    assert chatcommands.brownie() == "Brown!"


def test_wut():
    assert chatcommands.wut() == "Whaddya mean, 'wut'? Humans..."


def test_alive():
    assert chatcommands.alive() in chatcommands.ALIVE_MSG


def test_location():
    assert chatcommands.location() == GlobalVars.location


def test_version():
    assert chatcommands.version() == '{id} [{commit_name}]({repository}/commit/{commit_code})'.format(
        id=GlobalVars.location, commit_name=GlobalVars.commit_with_author_escaped,
        commit_code=GlobalVars.commit.id, repository=GlobalVars.bot_repository)


def test_bisect():
    chatcommunicate.parse_room_config("test/test_rooms.yml")
    msg = Fake({
        "owner": {
            "name": "ArtOfCode",
            "id": 121520,
            "is_moderator": True
        },
        "room": {
            "_client": {
                "host": "stackexchange.com"
            },
            "id": 11540
        },
        "content_source": None
    })

    # Testing to see if a watch/blacklist regex is performing poorly.
    # The post text in the next two tests is from actual posts which caused SD to hang.
    # This test resulted in finding the \\L<city> issue; Can be used to show which sub-group of watch/blacklist regexes causes the problem.
    # Doing so may take additional debugging, but the report from pytest should provide enough information.
    test_text = "<p>shiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!</p>\n"
    msg.content_source = "!!/bisect {}".format(test_text)
    msg.content = msg.content_source
    assert chatcommands.bisect(None, original_msg=msg) == r"{!r} is not caught by a blacklist or watchlist item.".format(test_text)

    # Text from a post which caused SD to hang when run through findspam. It's here to find new watch/blacklist regexes
    # which have problems with backtracking on very long text which doesn't have word breaks.
    test_text = "<p>burhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhanburhan</p>\n"
    msg.content_source = "!!/bisect {}".format(test_text)
    msg.content = msg.content_source
    assert chatcommands.bisect(None, original_msg=msg) == r"{!r} is not caught by a blacklist or watchlist item.".format(test_text)

    msg.content_source = "!!/bisect :::essayssos.com:::"
    msg.content = msg.content_source
    assert chatcommands.bisect(None, original_msg=msg) == r"Matched by `essayssos\.com` on [line 1 of watched_keywords.txt](https://github.com/{}/blob/{}/watched_keywords.txt#L1)".format(GlobalVars.bot_repo_slug, GlobalVars.commit.id)

    test_text = "OoOasdfghjklOoO"
    msg.content_source = "!!/bisect {}".format(test_text)
    msg.content = msg.content_source
    assert chatcommands.bisect(None, original_msg=msg) == r"{!r} is not caught by a blacklist or watchlist item.".format(test_text)


"""
@patch("chatcommands.datetime")
def test_hats(date):
    date.side_effect = datetime.datetime

    date.utcnow.return_value = datetime.datetime(2018, 12, 11, hour=23)
    assert chatcommands.hats() == "WE LOVE HATS! Winter Bash will begin in 0 days, 1 hour, 0 minutes, and 0 seconds."

    date.utcnow.return_value = datetime.datetime(2019, 1, 1, hour=23)
    assert chatcommands.hats() == "Winter Bash won't end for 0 days, 1 hour, 0 minutes, and 0 seconds. GO EARN SOME HATS!"
"""


def test_info():
    assert chatcommands.info() == "I'm " + GlobalVars.chatmessage_prefix +\
        " a bot that detects spam and offensive posts on the network and"\
        " posts alerts to chat."\
        " [A command list is available here](https://charcoal-se.org/smokey/Commands)."


def test_blame():
    msg1 = Fake({
        "_client": {
            "host": "stackexchange.com",
            "get_user": lambda id: Fake({"name": "J F", "id": id})
        },

        "room": {
            "get_current_user_ids": lambda: [161943]
        }
    })

    assert chatcommands.blame(original_msg=msg1) == "It's [J F](https://chat.stackexchange.com/users/161943)'s fault."

    msg2 = Fake({
        "_client": {
            "host": "stackexchange.com",
            "get_user": lambda id: Fake({"name": "J F", "id": id})
        }
    })

    assert chatcommands.blame2("\u200B\u200C\u2060\u200D\u180E\uFEFF\u2063", original_msg=msg2) == "It's [J F](https://chat.stackexchange.com/users/161943)'s fault."


def test_privileged():
    chatcommunicate.parse_room_config("test/test_rooms.yml")

    msg = Fake({
        "owner": {
            "name": "ArtOfCode",
            "id": 121520,
            "is_moderator": False
        },
        "room": {
            "_client": {
                "host": "stackexchange.com"
            },
            "id": 11540
        }
    })

    assert chatcommands.amiprivileged(original_msg=msg) == "\u2713 You are a privileged user."

    msg.owner.id = 2
    assert chatcommands.amiprivileged(original_msg=msg) == "\u2573 " + GlobalVars.not_privileged_warning

    msg.owner.is_moderator = True
    assert chatcommands.amiprivileged(original_msg=msg) == "\u2713 You are a privileged user."


def test_deprecated_blacklist():
    assert chatcommands.blacklist("").startswith("The `!!/blacklist` command has been deprecated.")


@pytest.mark.skipif(GlobalVars.on_branch != "master", reason="avoid branch checkout")
def test_watch(monkeypatch):
    # XXX TODO: expand
    def wrap_watch(pattern, force=False):
        cmd = 'watch{0}'.format('-force' if force else '')
        msg = Fake({
            "_client": {
                "host": "stackexchange.com",
                "get_user": lambda id: Fake({"name": "J F", "id": id})
            },
            "owner": {"name": "ArtOfCode", "id": 121520},
            "room": {"id": 11540, "get_current_user_ids": lambda: [161943]},
            # Ouch, this is iffy
            # Prevent an error from deep inside do_blacklist
            "content_source": '!!/{0} {1}'.format(cmd, pattern)
        })
        msg.content = msg.content_source
        msg.room._client = msg._client

        return chatcommands.watch(pattern, alias_used=cmd, original_msg=msg)

    # Prevent from attempting to check privileges with Metasmoke
    monkeypatch.setattr(GlobalVars, "code_privileged_users", [1, 161943])

    try:
        # Invalid regex
        resp = wrap_watch(r'?')
        assert "An invalid pattern was provided" in resp

        # This is one of the perpetually condemned spam domains, blacklisted forever
        resp = wrap_watch(r'israelbigmarket')
        assert "That pattern looks like it's already caught" in resp

        # The phone number here is the first one in this format in bad_keywords.txt
        resp = wrap_watch(r'[a-z_]*(?:1_*)?913[\W_]*608[\W_]*4584[a-z_]*')
        assert "Mostly non-latin" not in resp
        assert "Bad keyword in answer" in resp
        assert "Bad keyword in body" in resp

        # XXX TODO: figure out how to trigger duplicate entry separately
        monkeypatch.setattr("chatcommunicate.is_privileged", lambda *args: True)
        monkeypatch.setattr("gitmanager.GitManager.prepare_git_for_operation", lambda *args: (True, None))

        assert wrap_watch("trimfire", True).startswith("Already watched")

        monkeypatch.setattr("gitmanager.GitManager.add_to_blacklist", lambda *args, **kwargs: (True, "Hahaha"))
        assert wrap_watch("male enhancement", True) == "Hahaha"
    finally:
        git.checkout("master")


def test_approve(monkeypatch):
    msg = Fake({
        "_client": {
            "host": "stackexchange.com",
        },
        "id": 88888888,
        "owner": {"name": "ArtOfCode", "id": 121520},
        "room": {"id": 11540, "name": "Continuous Integration", "_client": None},
        "content_source": '!!/approve 8888',
    })
    msg.room._client = msg._client

    # Prevent from attempting to check privileges with Metasmoke
    monkeypatch.setattr(GlobalVars, "code_privileged_users", [])
    assert chatcommands.approve(8888, original_msg=msg).startswith("You need blacklist manager privileges")

    monkeypatch.setattr(GlobalVars, "code_privileged_users", [('stackexchange.com', 121520)])
    with monkeypatch.context() as m:
        # Oh no GitHub is down
        original_get = requests.get
        m.setattr("requests.get", lambda *args, **kwargs: None)
        assert chatcommands.approve(8888, original_msg=msg) == "Cannot connect to GitHub API"
        m.setattr("requests.get", original_get)
    assert chatcommands.approve(2518, original_msg=msg)[:8] in {"PR #2518", "Cannot c"}


@patch("chatcommands.handle_spam")
def test_report(handle_spam):
    # Documentation: The process before scanning the post is identical regardless of alias_used.
    #   No need to supply alias_used to test that part.
    #   If no alias_used is supplied, it acts as if it's "scan"
    try:
        msg = Fake({
            "owner": {
                "name": "ArtOfCode",
                "id": 121520,
                "is_moderator": False
            },
            "room": {
                "id": 11540,
                "name": "Charcoal HQ",
                "_client": {
                    "host": "stackexchange.com"
                }
            },
            "_client": {
                "host": "stackexchange.com"
            },
            "id": 1337
        })

        assert chatcommands.report("test", original_msg=msg, alias_used="report") == "[Post](test): Invalid url."

        assert chatcommands.report("one two three four five plus-an-extra", original_msg=msg, alias_used="report") == (
            "To avoid SmokeDetector reporting posts too slowly, you can report at most 5 posts at a time. This is to avoid "
            "SmokeDetector's chat messages getting rate-limited too much, which would slow down reports."
        )

        # assert chatcommands.report('a a a a a "invalid"""', original_msg=msg) \
        #     .startswith("You cannot provide multiple custom report reasons.")

        assert chatcommands.report('https://stackoverflow.com/q/1', original_msg=msg) == \
            "[Post](https://stackoverflow.com/q/1): No data fetched from API. It may have been deleted."

        # Valid post
        assert chatcommands.report('https://stackoverflow.com/a/1732454', original_msg=msg, alias_used="scan") == \
            "[Post](https://stackoverflow.com/a/1732454): Does not look like spam."
        assert chatcommands.report('https://stackoverflow.com/a/1732454 "~o.O~"', original_msg=msg, alias_used="report") is None

        _, call = handle_spam.call_args_list[-1]
        assert isinstance(call["post"], Post)
        assert call["reasons"] == ["Manually reported answer"]
        assert call["why"] == (
            "Post manually reported by user *ArtOfCode* in room *Charcoal HQ* with reason: *~o.O~*."
            "\n\nThis post would not have been caught otherwise."
        )

        # Bad post
        # This post is found in Sandbox Archive, so it will remain intact and is a reliable test post
        # backup: https://meta.stackexchange.com/a/228635
        test_post_url = "https://meta.stackexchange.com/a/209772"
        assert chatcommands.report(test_post_url, original_msg=msg, alias_used="scan") is None

        _, call = handle_spam.call_args_list[-1]
        assert isinstance(call["post"], Post)
        assert call["why"].startswith("Post manually scanned by user *ArtOfCode* in room *Charcoal HQ*.")

        # Now with report-direct
        GlobalVars.blacklisted_users.clear()
        GlobalVars.latest_questions.clear()
        assert chatcommands.report(test_post_url, original_msg=msg, alias_used="report-direct") is None
        _, call = handle_spam.call_args_list[-1]
        assert isinstance(call["post"], Post)
        assert call["why"].startswith(
            "Post manually reported by user *ArtOfCode* in room *Charcoal HQ*."
            "\n\nThis post would have also been caught for:"
        )

        # Don't re-report
        GlobalVars.latest_questions = [('stackoverflow.com', '1732454', 'RegEx match open tags except XHTML self-contained tags')]
        assert chatcommands.report('https://stackoverflow.com/a/1732454', original_msg=msg).startswith("[Post](https://stackoverflow.com/a/1732454): Already recently reported")

        # Can use report command multiple times in 30s if only one URL was used
        assert chatcommands.report('https://stackoverflow.com/q/1732348', original_msg=msg, alias_used="report") is None
    finally:
        GlobalVars.blacklisted_users.clear()
        GlobalVars.latest_questions.clear()


@patch("chatcommands.handle_spam")
def test_allspam(handle_spam):
    try:
        msg = Fake({
            "owner": {
                "name": "ArtOfCode",
                "id": 121520,
                "is_moderator": False
            },
            "room": {
                "id": 11540,
                "name": "Charcoal HQ",
                "_client": {
                    "host": "stackexchange.com"
                }
            },
            "_client": {
                "host": "stackexchange.com"
            },
            "id": 1337
        })

        assert chatcommands.allspam("test", original_msg=msg) == "[User](test): Invalid url."

        # If this code lasts long enough to fail, I'll be happy
        assert chatcommands.allspam("https://stackexchange.com/users/10000000000", original_msg=msg) == \
            "The specified user does not appear to exist."

        assert chatcommands.allspam("https://stackexchange.com/users/5869449", original_msg=msg) == (
            "The specified user has an abnormally high number of accounts. Please consider flagging for moderator "
            "attention, otherwise use !!/report on the user's posts individually."
        )

        assert chatcommands.allspam("https://stackexchange.com/users/11683", original_msg=msg) == (
            "The specified user's reputation is abnormally high. Please consider flagging for moderator attention, "
            "otherwise use !!/report on the posts individually."
        )

        assert chatcommands.allspam("https://stackoverflow.com/users/22656", original_msg=msg) == (
            "The specified user's reputation is abnormally high. Please consider flagging for moderator attention, "
            "otherwise use !!/report on the posts individually."
        )

        assert chatcommands.allspam("https://stackexchange.com/users/12108751", original_msg=msg) == \
            "The user has no post yet."

        assert chatcommands.allspam("https://stackoverflow.com/users/8846458", original_msg=msg) == \
            "The user has no post yet."

        # This test is for users with <100rep but >15 posts
        # If this breaks in the future because the below user eventually gets 100 rep (highly unlikely), use the following
        # data.SE query to find a new target. Alternatively, get a sock to post 16 answers in the sandbox.
        # https://stackoverflow.com/users/7052649/vibin (look for low rep but >1rep users, 1rep users are usually suspended)
        assert chatcommands.allspam("https://stackoverflow.com/users/7052649", original_msg=msg) == (
            "The specified user has an abnormally high number of spam posts. Please consider flagging for moderator "
            "attention, otherwise use !!/report on the posts individually."
        )

        # Valid user for allspam command
        assert chatcommands.allspam("https://stackexchange.com/users/12108974", original_msg=msg) is None

        assert handle_spam.call_count == 1
        _, call = handle_spam.call_args_list[0]
        assert isinstance(call["post"], Post)
        assert call["reasons"] == ["Manually reported answer"]
        assert call["why"].startswith(
            "Post manually reported by user *ArtOfCode* in room *Charcoal HQ*."
            "\n\nThis post would not have been caught otherwise."
        )

        handle_spam.reset_mock()

        assert chatcommands.allspam("https://meta.stackexchange.com/users/373807", original_msg=msg) is None

        assert handle_spam.call_count == 1
        _, call = handle_spam.call_args_list[0]
        assert isinstance(call["post"], Post)
        # We expect "blacklisted user" here, as the blacklist is dumped to a pickle
        # Hence when the pickle is loaded again, the user is blacklisted again
        assert call["reasons"] == ["blacklisted user"]
        # There is no "This post would have also been caught for:" as the reported post
        # is not manually ignored or marked as fp
        assert call["why"].startswith(
            "Post manually reported by user *ArtOfCode* in room *Charcoal HQ*."
        )

    finally:
        GlobalVars.blacklisted_users.clear()


@pytest.mark.skipif(os.path.isfile("blacklistedUsers.p"), reason="shouldn't overwrite file")
def test_blacklisted_users():
    try:
        msg = Fake({
            "owner": {
                "name": "ArtOfCode",
                "id": 121520,
                "is_moderator": False
            },
            "room": {
                "id": 11540,
                "_client": {
                    "host": "stackexchange.com"
                }
            },
            "_client": {
                "host": "stackexchange.com"
            },
            "id": 1337
        })

        # Format: !!/*blu profileurl
        assert chatcommands.isblu("https://stackoverflow.com/users/4622463/angussidney", original_msg=msg) == \
            "User is not blacklisted (`4622463` on `stackoverflow.com`)."
        assert chatcommands.addblu("https://stackoverflow.com/users/4622463/angussidney", original_msg=msg) == \
            "User blacklisted (`4622463` on `stackoverflow.com`)."
        # TODO: Edit command to check and not blacklist again, add test
        assert chatcommands.isblu("https://stackoverflow.com/users/4622463/angussidney", original_msg=msg) == \
            "User is blacklisted (`4622463` on `stackoverflow.com`)."
        assert chatcommands.rmblu("https://stackoverflow.com/users/4622463/angussidney", original_msg=msg) == \
            "User removed from blacklist (`4622463` on `stackoverflow.com`)."
        assert chatcommands.isblu("https://stackoverflow.com/users/4622463/angussidney", original_msg=msg) == \
            "User is not blacklisted (`4622463` on `stackoverflow.com`)."
        assert chatcommands.rmblu("https://stackoverflow.com/users/4622463/angussidney", original_msg=msg) == \
            "User is not blacklisted."

        # Format: !!/*blu userid sitename
        assert chatcommands.isblu("4622463 stackoverflow", original_msg=msg) == \
            "User is not blacklisted (`4622463` on `stackoverflow.com`)."
        assert chatcommands.addblu("4622463 stackoverflow", original_msg=msg) == \
            "User blacklisted (`4622463` on `stackoverflow.com`)."
        # TODO: Add test here as well
        assert chatcommands.isblu("4622463 stackoverflow", original_msg=msg) == \
            "User is blacklisted (`4622463` on `stackoverflow.com`)."
        assert chatcommands.rmblu("4622463 stackoverflow", original_msg=msg) == \
            "User removed from blacklist (`4622463` on `stackoverflow.com`)."
        assert chatcommands.isblu("4622463 stackoverflow", original_msg=msg) == \
            "User is not blacklisted (`4622463` on `stackoverflow.com`)."
        assert chatcommands.rmblu("4622463 stackoverflow", original_msg=msg) == \
            "User is not blacklisted."

        # Invalid input
        assert chatcommands.addblu("https://meta.stackexchange.com/users", original_msg=msg) == \
            "Invalid format. Valid format: `!!/addblu profileurl` *or* `!!/addblu userid sitename`."
        assert chatcommands.rmblu("https://meta.stackexchange.com/", original_msg=msg) == \
            "Invalid format. Valid format: `!!/rmblu profileurl` *or* `!!/rmblu userid sitename`."
        assert chatcommands.isblu("msklkldsklaskd", original_msg=msg) == \
            "Invalid format. Valid format: `!!/isblu profileurl` *or* `!!/isblu userid sitename`."

        # Invalid sitename
        assert chatcommands.addblu("1 completelyfakesite", original_msg=msg) == \
            "Error: Could not find the given site."
        assert chatcommands.isblu("1 completelyfakesite", original_msg=msg) == \
            "Error: Could not find the given site."
        assert chatcommands.rmblu("1 completelyfakesite", original_msg=msg) == \
            "Error: Could not find the given site."
    finally:
        # Cleanup
        _remove_pickle("blacklistedUsers.p")


@pytest.mark.skipif(os.path.isfile("whitelistedUsers.p"), reason="shouldn't overwrite file")
def test_whitelisted_users():
    try:
        msg = Fake({
            "owner": {
                "name": "El'endia Starman",
                "id": 1,
                "is_moderator": False
            },
            "room": {
                "id": 11540,
                "_client": {
                    "host": "stackexchange.com"
                }
            },
            "_client": {
                "host": "stackexchange.com"
            }
        })

        # Format: !!/*wlu profileurl
        assert chatcommands.iswlu("https://stackoverflow.com/users/4622463/angussidney", original_msg=msg) == \
            "User is not whitelisted (`4622463` on `stackoverflow.com`)."
        assert chatcommands.addwlu("https://stackoverflow.com/users/4622463/angussidney", original_msg=msg) == \
            "User whitelisted (`4622463` on `stackoverflow.com`)."
        # TODO: Add test here as well
        assert chatcommands.iswlu("https://stackoverflow.com/users/4622463/angussidney", original_msg=msg) == \
            "User is whitelisted (`4622463` on `stackoverflow.com`)."
        assert chatcommands.rmwlu("https://stackoverflow.com/users/4622463/angussidney", original_msg=msg) == \
            "User removed from whitelist (`4622463` on `stackoverflow.com`)."
        assert chatcommands.iswlu("https://stackoverflow.com/users/4622463/angussidney", original_msg=msg) == \
            "User is not whitelisted (`4622463` on `stackoverflow.com`)."
        assert chatcommands.rmwlu("https://stackoverflow.com/users/4622463/angussidney", original_msg=msg) == \
            "User is not whitelisted."

        # Format: !!/*wlu userid sitename
        assert chatcommands.iswlu("4622463 stackoverflow", original_msg=msg) == \
            "User is not whitelisted (`4622463` on `stackoverflow.com`)."
        assert chatcommands.addwlu("4622463 stackoverflow", original_msg=msg) == \
            "User whitelisted (`4622463` on `stackoverflow.com`)."
        # TODO: Add test here as well
        assert chatcommands.iswlu("4622463 stackoverflow", original_msg=msg) == \
            "User is whitelisted (`4622463` on `stackoverflow.com`)."
        assert chatcommands.rmwlu("4622463 stackoverflow", original_msg=msg) == \
            "User removed from whitelist (`4622463` on `stackoverflow.com`)."
        assert chatcommands.iswlu("4622463 stackoverflow", original_msg=msg) == \
            "User is not whitelisted (`4622463` on `stackoverflow.com`)."
        assert chatcommands.rmwlu("4622463 stackoverflow", original_msg=msg) == \
            "User is not whitelisted."

        # Invalid input
        assert chatcommands.addwlu("https://meta.stackexchange.com/users", original_msg=msg) == \
            "Invalid format. Valid format: `!!/addwlu profileurl` *or* `!!/addwlu userid sitename`."
        assert chatcommands.rmwlu("https://meta.stackexchange.com/", original_msg=msg) == \
            "Invalid format. Valid format: `!!/rmwlu profileurl` *or* `!!/rmwlu userid sitename`."
        assert chatcommands.iswlu("msklkldsklaskd", original_msg=msg) == \
            "Invalid format. Valid format: `!!/iswlu profileurl` *or* `!!/iswlu userid sitename`."

        # Invalid sitename
        assert chatcommands.addwlu("1 completelyfakesite", original_msg=msg) == \
            "Error: Could not find the given site."
        assert chatcommands.iswlu("1 completelyfakesite", original_msg=msg) == \
            "Error: Could not find the given site."
    except:
        # Cleanup
        _remove_pickle("whitelistedUsers.p")


def test_metasmoke():
    msg = Fake({
        "owner": {
            "name": "ArtOfCode",
            "id": 121520,
            "is_moderator": False
        },
        "room": {
            "id": 11540,
            "_client": {
                "host": "stackexchange.com"
            }
        },
        "_client": {
            "host": "stackexchange.com"
        }
    })
    msg_source = "metasmoke is {}. Current failure count: {} " + "({id})".format(id=GlobalVars.location)

    assert chatcommands.metasmoke(original_msg=msg, alias_used="ms-up") == "metasmoke is now considered up."
    assert chatcommands.metasmoke(original_msg=msg, alias_used="ms-status") == msg_source.format("up", 0)
    assert chatcommands.metasmoke(original_msg=msg, alias_used="ms-down") == "metasmoke is now considered down."
    assert chatcommands.metasmoke(original_msg=msg, alias_used="ms-status") == msg_source.format("down", 999)
    assert chatcommands.metasmoke(original_msg=msg, alias_used="ms-up") == "metasmoke is now considered up."
    assert chatcommands.metasmoke(original_msg=msg, alias_used="ms-status") == msg_source.format("up", 0)


@pytest.mark.skipif(os.path.isfile("notifications.p"), reason="shouldn't overwrite file")
def test_notifications():
    try:
        msg1 = Fake({
            "owner": {
                "name": "El'endia Starman",
                "id": 1,
                "is_moderator": False
            },
            "room": {
                "id": 11540,
                "_client": {
                    "host": "stackexchange.com"
                }
            },
            "_client": {
                "host": "stackexchange.com"
            }
        })

        msg2 = Fake({
            "owner": {
                "name": "angussidney",
                "id": 145827,
                "is_moderator": False
            },
            "room": {
                "id": 11540,
                "_client": {
                    "host": "stackexchange.com"
                }
            },
            "_client": {
                "host": "stackexchange.com"
            }
        })

        # User 1
        assert chatcommands.allnotificationsites("11540", original_msg=msg1) == \
            "You won't get notified for any sites in that room."
        assert chatcommands.willbenotified("11540", "gaming", original_msg=msg1) == \
            "No, you won't be notified for that site in that room."
        assert chatcommands.notify("11540", "gaming", None, original_msg=msg1) == \
            "You'll now get pings from me if I report a post on `gaming`, in room `11540` on `chat.stackexchange.com`"
        assert chatcommands.notify("11540", "codegolf.stackexchange.com", None, original_msg=msg1) == \
            "You'll now get pings from me if I report a post on `codegolf.stackexchange.com`, in room `11540` on " \
            "`chat.stackexchange.com`"
        assert chatcommands.willbenotified("11540", "gaming.stackexchange.com", original_msg=msg1) == \
            "Yes, you will be notified for that site in that room."
        assert chatcommands.willbenotified("11540", "codegolf", original_msg=msg1) == \
            "Yes, you will be notified for that site in that room."

        # User 2
        assert chatcommands.allnotificationsites("11540", original_msg=msg2) == \
            "You won't get notified for any sites in that room."
        assert chatcommands.willbenotified("11540", "raspberrypi", original_msg=msg2) == \
            "No, you won't be notified for that site in that room."
        assert chatcommands.notify("11540", "raspberrypi", None, original_msg=msg2) == \
            "You'll now get pings from me if I report a post on `raspberrypi`, in room `11540` on `chat.stackexchange.com`"
        assert chatcommands.notify("11540", "raspberrypi", None, original_msg=msg2) == \
            "That notification configuration is already registered."
        assert chatcommands.willbenotified("11540", "raspberrypi.stackexchange.com", original_msg=msg2) == \
            "Yes, you will be notified for that site in that room."

        # Check for no interaction
        assert chatcommands.allnotificationsites("11540", original_msg=msg1) == \
            "You will get notified for these sites:\r\ncodegolf.stackexchange.com, gaming.stackexchange.com"
        assert chatcommands.allnotificationsites("11540", original_msg=msg2) == \
            "You will get notified for these sites:\r\nraspberrypi.stackexchange.com"

        # Remove all notifications and check
        assert chatcommands.unnotify("11540", "gaming.stackexchange.com", original_msg=msg1) == \
            "I will no longer ping you if I report a post on `gaming.stackexchange.com`, in room `11540` on " \
            "`chat.stackexchange.com`"
        assert chatcommands.unnotify("11540", "codegolf", original_msg=msg1) == \
            "I will no longer ping you if I report a post on `codegolf`, in room `11540` on `chat.stackexchange.com`"
        assert chatcommands.unnotify("11540", "raspberrypi", original_msg=msg2) == \
            "I will no longer ping you if I report a post on `raspberrypi`, in room `11540` on `chat.stackexchange.com`"
        assert chatcommands.unnotify("11540", "raspberrypi", original_msg=msg2) == \
            "That configuration doesn't exist."
        assert chatcommands.allnotificationsites("11540", original_msg=msg1) == \
            "You won't get notified for any sites in that room."
        assert chatcommands.willbenotified("11540", "raspberrypi", original_msg=msg2) == \
            "No, you won't be notified for that site in that room."

        assert chatcommands.allnotificationsites("asdf", original_msg=msg1) == "Invalid input type given for an argument"
        assert chatcommands.notify("11540", "charcoalspam.stackexchange.com", None, original_msg=msg1) == \
            "The given SE site does not exist."

        assert chatcommands.notify("11540", "codegolf", "True", original_msg=msg1) == \
            "You'll now get pings from me if I report a post on `codegolf`, in room `11540` on `chat.stackexchange.com`"
        assert chatcommands.notify("11540", "codegolf", "False", original_msg=msg1) == \
            "That notification configuration is already registered."
    finally:
        # Cleanup
        _remove_pickle("notifications.p")


def test_inqueue():
    site = Fake({"keys": (lambda: ['1'])})

    class FakeQueue:
        def __getitem__(self, _):
            return site

        def __contains__(self, name):
            return name == "codegolf.stackexchange.com"

    chatcommands.GlobalVars.bodyfetcher = Fake({"queue": FakeQueue()})

    assert chatcommands.inqueue("https://codegolf.stackexchange.com/a/1") == "Can't check for answers."
    assert chatcommands.inqueue("https://stackoverflow.com/q/1") == "Not in queue."
    assert chatcommands.inqueue("https://codegolf.stackexchange.com/q/1") == "#1 in queue."
