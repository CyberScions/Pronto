#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: binary -*-

import re
import os
from twitter import operations
from functions import utilities
from core.info import notifications

class DatabaseOperations():

    def VisualizeTweetLinks (self, Username):
        # Mass decision maker, when visualing tweets.
        utilities.pi("\n{}Visualizing {}'s collected tweets".format(notifications.INFO, Username))
        Username = Username.lower() # Override any UPPERCASE strings

        IDN = operations.GetTwitterIDFromHandle(Username)

        # This path already exists.
        tweetspath = '{}/{}_{}.tweet.links'.format(Username, IDN, Username)
        # This path will exist if it doesn't.
        visualtweetpath = '{}/tweets/'.format(Username)
        vtpb = os.path.exists(visualtweetpath)

        if vtpb is True:
            pass

        if vtpb is False:
            os.mkdir(visualtweetpath)

        with open(tweetspath, 'r') as file:
            os.chdir(visualtweetpath) # Change into your visual tweets directory and write the tweets to file.
            for line in file:
                line = line.replace('\n', '')
                lineid  = line.split('/')[5]
                tweetdate = operations.GrabTweetDate(line)
                tweetime = tweetdate.split('-')

                if tweetdate is not None:
                    tweetid = tweetdate.replace(' ', '_') + '_' + lineid + ".{}".format(Username) + ".tweet.html" #| for debugging rounds.

                    #Turn your tweets into html, for viewing.
                html = utilities.GetHTTPRequest(line).text.encode('utf-8')
                tweetpath = '{}/tweets/{}'.format(Username, tweetid)
                pb = os.path.exists(tweetpath) # Tweet pass bool. Trying to speed up the process of visualing tweets.
                tpb = os.path.exists(tweetid)

                # Trying to speed up the process of visualing tweets with file checks.
                if pb is True:
                    pass

                elif pb is False:

                    if tpb is False:
                        foundtweet = []
                        tweetextract = re.findall(r'<div class="dir-ltr" dir="ltr">  .*', html)
                        lot = len(tweetextract)
                        utilities.pi("{}Visualizing a tweet from {}.".format(notifications.INFO, tweetdate))
                        #Validation check
                        for tweet in tweetextract:
                            foundtweet.append(tweet)

                        u = {}
                        for item in foundtweet:
                            u[item] = 1
                        keys = u.keys()

                        for content in keys:

                            with open(tweetid, 'a+') as file:
                                bc = utilities.sbc(tweetid, content)

                                if bc is None:
                                    file.write("\n" + content)

            utilities.pi("{}Visualized all collected tweets.\n".format(notifications.INFO))

    def WriteTweetLinksToFile(self, IDN, Username, TweetLinks):
        utilities.pi(notifications.INFO + "Wrote {} of {}'s tweet links to disk.\n".format(len(TweetLinks), Username))
        Username = Username.lower() # Override any UPPERCASE strings

        handledirectory = '{}'.format(Username)
        hdb = os.path.exists(handledirectory) # Handle Direcory path
        if hdb is True:
            pass

        elif hdb is False:
            os.mkdir(handledirectory)

        tweetspath =  '{}/{}_{}.tweet.links'.format(Username, IDN, Username)

        with open(tweetspath, 'a+') as file:
            for line in TweetLinks:

                bc = utilities.sbc(tweetspath, line)
                if bc is None:
                    file.write(line + "\n")

                if bc is True:
                    pass

    def WriteHandleFollowersToFile(self, Username, Followers):
        utilities.pi(notifications.INFO + "Collected {} of {}'s followers".format(len(Followers), Username))

        utilities.pi(notifications.INFO + "Wrote {} of {}'s followers to disk\n".format(len(Followers), Username))
        Username = Username.lower() # Override any UPPERCASE strings
        followerspath = '{}/{}.followers'.format(Username, Username)

        # Create a usernames directory if it doesn't exist.
        handledirectory = '{}'.format(Username)
        hdb = os.path.exists(handledirectory) # Handle Direcory path

        if hdb is True:
            pass

        elif hdb is False:
            os.mkdir(handledirectory)

        with open(followerspath, 'a+') as file:
            for line in Followers:
                bc = utilities.sbc(followerspath, line)

                if bc is None:
                    file.write(line + " - " + notifications.PL + line + "\n")

                if bc is True:
                    pass

    def WriteHandleFollowingToFile(self, Username, Following):
        utilities.pi(notifications.INFO + "Collected {} of the users {} is following".format(len(Following), Username))

        utilities.pi(notifications.INFO + "Wrote {} to disk\n".format(len(Following), Username))
        Username = Username.lower() # Override any UPPERCASE strings
        followingpath = '{}/{}.following'.format(Username, Username)

        # Create a usernames directory if it doesn't exist.
        handledirectory = '{}'.format(Username)
        hdb = os.path.exists(handledirectory) # Handle Direcory path

        if hdb is True:
            pass

        elif hdb is False:
            os.mkdir(handledirectory)

        with open(followingpath, 'a+') as file:

            for line in Following:
                line = line.lower()
                bc = utilities.sbc(followingpath, line)

                if bc is None:
                    file.write(line + " - " + notifications.PL + line + "\n")

    def WriteHandleProfileToFile(self, ID, Username, Followers, Following, Tweets, PFL):
        # Path to profile.
        profilepath = '{}/{}_{}.twitter.profile'.format(Username, ID, Username)

        # Profile Path Boolean
        ppb = os.path.exists(profilepath)

        # Create a usernames directory if it doesn't exist.
        handledirectory = '{}'.format(Username)
        hdb = os.path.exists(handledirectory) # Handle Direcory path
        if hdb is True:
            pass

        elif hdb is False:
            os.mkdir(handledirectory)

        if ppb is True:
            pass

        elif ppb is False:

            with open(profilepath, 'w+') as file:
                file.write(notifications.TID + ID + "\n")
                file.write(notifications.TWEETS + Tweets + "\n")
                file.write(notifications.USERNAME + Username + "\n")
                file.write(notifications.FOLLOWERS + Followers + "\n")
                file.write(notifications.FOLLOWING + Following + "\n")
                file.write(notifications.PROFILELINK + PFL + "\n")

database = DatabaseOperations()
