#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: binary -*-

from libs.paint import colors

class COLOREDOUTPUT():

    INFO = colors.W+"[INFO]"+colors.N + ": "
    FAIL = colors.R+"[FAILED]"+colors.N + ": "
    ERROR = colors.R+"[ERROR]"+colors.N + ": "

    # Display link
    PL = "https://twitter.com/"

    # Operational link
    SL = "https://mobile.twitter.com/{}/status/{}"

    # Proile Varibles:
    TID = "ID: "
    TWEETS = "Tweets: "
    FOLLOWING = "Following: "
    FOLLOWERS = "Followers: "
    USERNAME = "Username: "
    LOCATION = "Location: "
    PROFILELINK = "Profile Link: "

notifications = COLOREDOUTPUT()

def Help():
    print """
    """+colors.W+"""[GWF-CERTIFIED]"""+colors.N+""" - """+colors.Y+"""https://twitter.com/GuerrillaWF"""+colors.N+"""

    ./pronto.py -i [ID-NUMBER]| Turn an ID into a Username.

    ./pronto.py -n [USERNAME] | Turn a Username into an ID.

    ./pronto.py -e [USERNAME] | Output basic profile information on a twitter handle.

    ./pronto.py -v [USERNAME] | Visualize a users tweets that you've collected.

    ./pronto.py --tweets [USERNAME] | Collect all of a Users tweets.

    ./pronto.py --followers [USERAME]| Download all of the followers a twitter handle has.

    ./pronto.py --following [USERAME]| Download all of the twitter handles that a user is following.
        """
