#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: binary -*-

import re
import time
import json
import storage
from functions import utilities
from core.info import notifications

class TwitterOperations():

    def GrabEntireProfile(self, TwitterHandle):
        utilities.pi("\n{}Attempting to Generate {}'s Twitter Profile information".format(notifications.INFO, TwitterHandle))
        url = utilities.GetHTTPRequest('https://mobile.twitter.com/{}?p=s'.format(TwitterHandle))

        if url.status_code == 404:
            utilities.pi("{} 404: User not found!\n".format(ERROR))
            exit(0)

        url = utilities.GetHTTPRequest('https://mobile.twitter.com/{}?p=s'.format(TwitterHandle)).content

        # For readable output.
        print ""

        # Location data.
        ProfileLocationContainer = re.search(r'<div class="location">.*?</div>', url)
        ProfileLocation = ProfileLocationContainer.group()
        Location = ProfileLocation.replace('<div class="location">', '').replace("</div>", '')

        # Name data.
        ProfileNameContainer = re.search(r'<span class="screen-name">.*?</span>', url)
        ProfileNameBlock = ProfileNameContainer.group()
        ProfileName = ProfileNameBlock.replace('<span class="screen-name">', '').replace('</span>', '')

        # Statnumbers data | Tweets | Following | Followers
        statnums = re.findall(r'<div class="statnum">.*?</div>', url)
        TotalTweets = statnums[0].replace('<div class="statnum">', '').replace('</div>', "")
        FollowingTotal = statnums[1].replace('<div class="statnum">', '').replace('</div>', "")
        FollowersTotal = statnums[2].replace('<div class="statnum">', '').replace('</div>', "")

        # Get AN ID Number from a twitter account.
        IDN = str(operations.GetTwitterIDFromHandle(TwitterHandle))
        PFL = notifications.PL + TwitterHandle

        # Output information to console
        utilities.pi("" + notifications.TID + IDN)
        utilities.pi("" + notifications.TWEETS + TotalTweets)
        utilities.pi("" + notifications.FOLLOWING + FollowingTotal)
        utilities.pi("" + notifications.FOLLOWERS + FollowersTotal)
        utilities.pi("" + notifications.USERNAME + TwitterHandle)

        if Location is not "":
            utilities.pi(notifications.LOCATION + Location)

        utilities.pi(notifications.PROFILELINK + PFL)

        # self, ID, Username, Followers, Following, Tweets, PFL
        # Auto-Write Info to storage.database
        storage.database.WriteHandleProfileToFile(IDN, TwitterHandle.lower(), FollowersTotal, FollowingTotal, TotalTweets, PFL)
        print ""

    def GrabFollowingStats(self, TwitterHandle):
        url = utilities.GetHTTPRequest("https://mobile.twitter.com/{}?p=s".format(TwitterHandle)).text
        statnums = re.findall(r'<div class="statnum">.*?</div>', url)
        FollowingTotal = statnums[1].replace('<div class="statnum">', '').replace('</div>', '')
        return FollowingTotal

    def GrabFollwerStats(self, TwitterHandle):
        url = utilities.GetHTTPRequest("https://mobile.twitter.com/{}?p=s".format(TwitterHandle)).text
        statnums = re.findall(r'<div class="statnum">.*?</div>', url)
        FollowersTotal = statnums[2].replace('<div class="statnum">', '').replace('</div>', '')
        return FollowersTotal

    def GrabStatusCursor(sel, url):
        try:
            d = utilities.GetHTTPRequest(url).content
            z = re.search(r'max_id=.*?">', d)
            x = z.group().replace("max_id=", '?max_id=').replace('">', "")
            return x
        except AttributeError:
            return None

    def GrabStatusLink(self, url):
        #UNAME = url.split('/')[3] # Extract Username

        d = utilities.GetHTTPRequest(url).content
        i = re.findall(r'href=".*?p=v', d)
        f = []
        for s in i:
            f.append(s)
        u = {}
        for z in f:
            u[z] = 1
        k = u.keys()
        cl = []
        for x in k:
            x = x.replace("href=\"/", 'https://mobile.twitter.com/').replace("?p=v", '')
            cl.append(x)
        return cl

    def CollectStatuses(self, TwitterHandle):
        # List object that collects all statuses of a user.
        #try:
        pages = [] # status pages
        sl = [] # Status links

        p = 'https://mobile.twitter.com/{}'.format(TwitterHandle)
        d = operations.GrabStatusCursor('https://mobile.twitter.com/{}'.format(TwitterHandle))
        pages.append(p)
        pages.append(p + d) # Get the first page !, Don't miss it !
        c = 0
        while True:
            if d is None:
                continue

            d = operations.GrabStatusCursor(p + d)
            if d is None:
                c = 1
                break # Prevents a NoneType Object from being added to the list
            print "{}Collecting {}'s Tweets from page {}".format(notifications.INFO, TwitterHandle, len(pages) - 1)
            pages.append(p + d)
        for i in pages:
            d = operations.GrabStatusLink(i)
            for s in d:
                if TwitterHandle in s: # Filter ONLY that users tweets, NO retweets.
                    sl.append(s)
        if len(pages) - 1 == 1:
            utilities.pi("{}Collected {} page of tweets from {}".format(notifications.INFO, len(pages) - 1, TwitterHandle))

        else:
            utilities.pi("{}Collected {} pages of tweets from {}".format(notifications.INFO, len(pages) - 1, TwitterHandle))

        # Get the ID of handle.
        IDN = operations.GetTwitterIDFromHandle(TwitterHandle)
        storage.database.WriteTweetLinksToFile(IDN, TwitterHandle, sl)
        return len(sl)
        #except TypeError:
        #    utilities.pi('{}404 User doesn\'t exist!\n'.format(notifications.INFO))

    def GrabTweetDate(self, StatusLink):
        d = utilities.GetHTTPRequest(StatusLink).content
        #return d
        i = re.findall(r'<a href="#" class="">.*?</a>', d)
        f = []

        for x in i:
            x = x.replace('<a href="#" class="">', '').replace('</a>', '')
            f.append(x)

        u = {}
        for item in f:
            u[item] = 1
        try:
            try:
                return u.keys()[0]
            except AttributeError:
                pass
        except IndexError:
            pass

    # Get Twitter ID from external site.
    def GetTwitterIDFromHandle(self, TwitterHandle):
        #TwitterHandle = "http://mytwitterid.com/api/?screen_name={0}".format(TwitterHandle)
        HandleIDRequest = json.loads(utilities.GetHTTPRequest("http://mytwitterid.com/api/?screen_name={}".format(TwitterHandle)).content)
        try:
            HandleIDResponse = HandleIDRequest[0]['id_str']
            return json.loads(HandleIDResponse)
        except KeyError:
            return None

    # Get Twitter Handle from external site, through TOR.
    def GetTwitterHandleFromID(self, TwitterID):
        """ Object to provide A Twitter users Handle from ID without the API. """
        IDRequest = utilities.GetHTTPRequest("http://twopcharts.com/idcheck?user={}&type=id".format(TwitterID)).content
        d = IDRequest.split()
        for i in d:
            if 'href="tweettimes/' in i.strip(): # Find it. The conditional way.
                x = i.strip() # make it a list ... again.
                p = x.replace('"><button', "").replace('href="tweettimes/', "") # Remove the bullshit.
                return p.split()[0]

    def GrabCursor(self, url): # Non-usable method.
          """ Stand Alone object """
          time.sleep(1)
          ppurl = utilities.GetHTTPRequest(url).text # Get the ascii version of the page
          Page = ppurl.split()
          for Data in Page:
              if 'href="/' and '?cursor=' and '">Show' in Data:
                  NextPage = Data.replace('href="/', "https://mobile.twitter.com/").replace('">Show', "").replace('value="/', "https://mobile.twitter.com/").replace('"/>', '')
                  return NextPage.split()

    def GrabFollows(self, url):
        time.sleep(1)
        # Non-usable method."""" This is NOT a Stand Alone object! """
        followers = [] # Keeps track of twitter followers.
        PPURL = utilities.GetHTTPRequest(url).text
        PageOfFollowers = PPURL.split()
        for TwitterFollower in PageOfFollowers:
            if 'class="username">' in TwitterFollower:
                # Find IT!
                TwitterFollower = TwitterFollower.replace('class="username"><span>@</span>', "").replace('</span></a>', "") # Remove the junk.
                followers.append(TwitterFollower)

        if 'class="username">@' and '</span>' in followers[0]:
            return followers[1:]

        else:
            return followers[0:]

    def CollectFollowers(self, TwitterHandle):
        try:
            print ""
            FollowersNumber = operations.GrabFollwerStats(TwitterHandle)
            utilities.pi(notifications.INFO + 'Attempting to collect {} of {}\'s followers'.format(FollowersNumber ,TwitterHandle))
            d = operations.GrabCursor("https://mobile.twitter.com/{}/followers".format(TwitterHandle))
            p = [] # pages visited
            p.append("https://mobile.twitter.com/{}/followers".format(TwitterHandle))
            f = []
            while True:
                for i in d:
                    d = operations.GrabCursor(i)
                    p.append(i)
                    if d is None: # Will surpress an NoneType error.
                        for o in p:
                            a = operations.GrabFollows(o)
                            for t in a:
                                f.append(t)
                        return f
        except TypeError:
            utilities.pi(notifications.INFO + 'User Doesn\'t exist.')
            exit(0)

    def CollectFollowing(self, TwitterHandle):
        try:
            print ""
            FollowingNumber = operations.GrabFollowingStats(TwitterHandle)
            utilities.pi(notifications.INFO + 'Attempting to collect the {} Users that {} is following'.format(FollowingNumber ,TwitterHandle))
            d = operations.GrabCursor("https://mobile.twitter.com/{}/following".format(TwitterHandle))
            p = [] # pages visited
            p.append("https://mobile.twitter.com/{}/following".format(TwitterHandle)) # So you don't miss any.
            f = []
            while True:
                for i in d:
                    d = operations.GrabCursor(i)
                    p.append(i)
                    if d is None: # Will surpress an NoneType error.
                        for o in p:
                            a = operations.GrabFollows(o)
                            for t in a:
                                f.append(t)
                        return f
        except TypeError:
            utilities.pi(notifications.INFO + 'User Doesn\'t exist.')
            exit(0)

    # Useful for interactive operations
    def select(self, message):
        while True:
            select = raw_input("\n{} ".format(message))
            return select

operations = TwitterOperations()
