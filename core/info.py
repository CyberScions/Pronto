#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: binary -*-

from libs.paint import color

class notifications(object):

    INFO = color.W  + "[INFO]"   + color.N + ": "
    FAIL = color.R  + "[FAILED]" + color.N + ": "
    ERROR = color.R + "[ERROR]"  + color.N + ": "

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
