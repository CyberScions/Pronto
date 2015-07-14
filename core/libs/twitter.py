import re
import time
import json
import random
import database
from os.path import dirname
from functions import Utilities
from core.libs.paint import color
from core.info import notifications

class operations(Utilities):

    def __init__(self):
        #Variables
        self.__found         = [] # Items Found
        self.__newest_trends = [] # Accessed by GetNewestTrends() only.
        self.__latest_trends = [] # Accessed by PickLatestTrend() only.
        self.__stream_collection = [] # Accessed by GetUserNameFromStream() only.
        self.__collection_following_pages = [] # Accessed by CollectFollowing only.
        self.__collection_followers_pages = [] # Accessed by CollectFollowers only.
        self.__found_following = []
        self.__found_followers = []
        self.__page          = []
        self.__domain        = 'https://mobile.twitter.com'
        self.__status_link   = [] # Holds status links
        self.__unique        = {}
        self.__unique_stream_collection = {} # Accessed by GetUserNameFromStream only.

        #Instantiations
        self.color         = color()
        self.__notify      = notifications()

    def GetEntireProfile(self, handle):
        self.pi("\n{}Attempting to Generate {}'s Twitter Profile information.".format(self.__notify.INFO, handle))
        self.response = self.GetRequest('https://mobile.twitter.com/{}?p=s'.format(handle))

        if self.response.status_code == 404:
            self.pi("{} 404: User not found!\n".format(ERROR))
            exit(0)

        # Location data.
        self.profile_location_container = re.search(r'<div class="location">.*?</div>', self.response.content)
        self.profile_location = self.profile_location_container.group()
        self.location = self.profile_location.replace('<div class="location">', '').replace("</div>", '')

        # Name data.
        self.profile_name_container = re.search(r'<span class="screen-name">.*?</span>', self.response.content)
        self.profile_name_block = self.profile_name_container.group()
        self.profile_name = self.profile_name_block.replace('<span class="screen-name">', '').replace('</span>', '')

        # Stat numbers data | Tweets | Following | Followers
        self.stat_numbers    = re.findall(r'<div class="statnum">.*?</div>', self.response.content)
        self.total_tweets    = self.stat_numbers[0].replace('<div class="statnum">', '').replace('</div>', "")
        self.following_total = self.stat_numbers[1].replace('<div class="statnum">', '').replace('</div>', "")
        self.followers_total = self.stat_numbers[2].replace('<div class="statnum">', '').replace('</div>', "")

        # Get an identification number from a twitter handle.
        self.id_number    = str(self.GetIDFromHandle(handle))
        self.profile_link = self.__notify.PL + handle

        # Output information to console.
        self.pi("" + self.__notify.TID + self.id_number)
        self.pi("" + self.__notify.TWEETS + self.total_tweets)
        self.pi("" + self.__notify.FOLLOWING + self.following_total)
        self.pi("" + self.__notify.FOLLOWERS + self.followers_total)
        self.pi("" + self.__notify.USERNAME + handle)

        if self.location is not "":
            self.pi(self.__notify.LOCATION + self.location)

        self.pi(self.__notify.PROFILELINK + self.profile_link)

        # self, ID, Username, Followers, Following, Tweets, PFL
        database.store().profile2file(self.id_number, handle, self.followers_total, self.following_total, self.total_tweets, self.profile_link)

    def GetFollowingStats(self, TwitterHandle):
        self.request = self.GetRequest("https://mobile.twitter.com/{}?p=s".format(TwitterHandle)).text
        self.status_numbers = re.findall(r'<div class="statnum">.*?</div>', self.request)
        self.total_following = self.status_numbers[1].replace('<div class="statnum">', '').replace('</div>', '')
        return self.total_following

    def GetFollowerStats(self, TwitterHandle):
        self.request = self.GetRequest("https://mobile.twitter.com/{}?p=s".format(TwitterHandle)).text
        self.status_numbers = re.findall(r'<div class="statnum">.*?</div>', self.request)
        self.total_followers = self.status_numbers[2].replace('<div class="statnum">', '').replace('</div>', '')
        return self.total_followers

    def GetStatusCursor(sel, url):
        try:
            self.regex = re.search(r'max_id=.*?">', self.GetRequest(url).content)
            self.container = self.regex.group().replace("max_id=", '?max_id=').replace('">', "")
            return self.container
        except AttributeError:
            return None

    def GetStatusLink(self, url):
        self.request = self.GetRequest(url).content
        self.links = re.findall(r'href=".*?p=v', self.request)

        for link in self.links:
            self.__found.append(link)

        for item in self.__found:
            self.__unique[item] = 1

        for key in self.__unique.keys():
            key = key.replace("href=\"/", 'https://mobile.twitter.com/').replace("?p=v", '')
            self.__status_link.append(key)
        return self.__status_link

    def CollectStatuses(self, TwitterHandle):
        self.main_page = 'https://mobile.twitter.com/{}'.format(TwitterHandle)
        self.first_page = self.GetStatusCursor('https://mobile.twitter.com/{}'.format(TwitterHandle))
        self.__page.append(self.main_page)
        self.__page.append(self.main_page + self.first_page) # Get the first page !, Don't miss it !

        self.count = 0
        while True:
            if self.first_page is None:
                continue

            self.first_page = self.GetStatusCursor(self.main_page + self.first_page)
            if self.first_page is None:
                self.count = 1
                break # Prevents a NoneType Object from being added to the list.
            print "{}Collecting {}'s Tweets from page {}".format(self.__notify.INFO, TwitterHandle, len(pages) - 1)
            self.__page.append(self.main_page + self.first_page)

        for i in pages:
            self.first_page = operations.GetStatusLink(i)
            for page in self.first_page:
                if TwitterHandle in page: # Do not collect a users retweets.
                    self.__status_link.append(s)

        if len(pages) - 1 == 1:
            self.pi("{}Collected {} page of tweets from {}".format(self.__notify.INFO, len(pages) - 1, TwitterHandle))

        else:
            self.pi("{}Collected {} pages of tweets from {}".format(self.__notify.INFO, len(pages) - 1, TwitterHandle))

        # Get the ID of handle.
        self.id = self.GetIDFromHandle(TwitterHandle)
        storage().store.WriteTweetLinksToFile(self.id, TwitterHandle, self.__status_link)
        return len(self.__status_link) # Number of collected tweets

    def GetTweetDate(self, StatusLink):
        self.page = self.GetRequest(StatusLink).content
        self.date_container = re.findall(r'<a href="#" class="">.*?</a>', self.page)

        for date in self.date_container:
            date = date.replace('<a href="#" class="">', '').replace('</a>', '')
            self.__found.append(date)

        for item in self.__found:
            self.__unique[item] = 1
        try:
            try:
                return self.__unique.keys()[0]
            except AttributeError:
                pass
        except IndexError:
            pass

    def GetIDFromHandle(self, handle):
        """Get a Twitter identification number from http://mytwitterid.com/.
        """
        # Add random.choice conditional to pick between a few different sites, so we don't get banned later.
        self.random_pick = random.randrange(0, 2)

        if self.random_pick == 0:
            self.request = json.loads(self.GetRequest("http://mytwitterid.com/api/?screen_name={}".format(handle)).content)
            try:
                self.response = self.request[0]['id_str']
                return json.loads(self.response)
            except KeyError:
                return None

        elif self.random_pick == 1:
            self.request = self.GetRequest("http://www.idfromuser.com/getID.php?service=twitter&username={}".format(handle)).text
        return self.request

    def GetTwitterHandleFromID(self, idn):
        """Provide A Twitter handles identification number.
        """
        # Add random.choice conditional to pick between a few different sites, so we don't get banned later.
        self.request = self.GetRequest("http://twopcharts.com/idcheck?user={}&type=id".format(idn)).content
        self.reponse_list = self.request.split()

        for item in self.reponse_list:
            if 'href="tweettimes/' in item.strip():
                item = item.strip()
                self.next_item = x.replace('"><button', "").replace('href="tweettimes/', "")
                return self.next_item.split()[0]

    def GetCursor(self, url): # Non-usable method.
          self.request = self.GetRequest(url).text
          self.reponse = self.request.split()

          for data in self.reponse:
              if 'href="/' and '?cursor=' and '">Show' in data:
                  self.next_page = data.replace('href="/', "https://mobile.twitter.com/").replace('">Show', "").replace('value="/', "https://mobile.twitter.com/").replace('"/>', '')
                  return self.next_page.split()

    def GetFollows(self, url):
        self.page_of_followers = self.GetRequest(url).text.split()
        f = []
        for follower in self.page_of_followers:
            if 'class="username">' in follower:
                follower = follower.replace('class="username"><span>@</span>', "").replace('</span></a>', "") # Remove the junk.
                f.append(follower)

        if 'class="username">@' and '</span>' in f[0]:
            return f[1:]

        else:
            return f[0:]

    def CollectFollowers(self, handle):
        try:
            self.followers_stat = self.GetFollowerStats(handle)
            self.pi("\n" + self.__notify.INFO + 'Attempting to collect {} of {}\'s followers'.format(self.followers_stat ,handle))
            self.main = self.GetCursor("https://mobile.twitter.com/{}/followers".format(handle))
            self.__collection_followers_pages.append("https://mobile.twitter.com/{}/followers".format(handle))

            while True:
                if self.main is None and self.following_stat > 1:
                    return self.GetFollows(self.__collection_followers_pages[0])

                elif self.main is not None:
                    for item in self.main:
                        self.main = self.GetCursor(item)
                        self.__collection_followers_pages.append(item)
                        if self.main is None: # Will /dev/null a NoneType error message.
                            for obvious in self.__collection_followers_pages:
                                self.appendage = self.GetFollows(obvious)
                                for trace in self.appendage:
                                    self.__found_followers.append(trace)
                            database.store().hoard_handles(self.__found_followers)
                            return self.__found_followers
                else:
                    return None
        except TypeError:
            self.pi(self.__notify.INFO + 'User Doesn\'t exist yet.')
            exit(0)

    def CollectFollowing(self, handle):
        try:
            self.following_stat = self.GetFollowingStats(handle)
            self.pi("\n" + self.__notify.INFO + 'Attempting to collect the {} Users that {} is following'.format(self.following_stat, handle))
            self.main = self.GetCursor("https://mobile.twitter.com/{}/following".format(handle))
            self.__collection_following_pages.append("https://mobile.twitter.com/{}/following".format(handle))

            while True:
                if self.main is None and self.following_stat > 1:
                    return self.GetFollows(self.__collection_following_pages[0])
                    #self.__found_following
                elif self.main is not None:
                    for item in self.main:
                        self.main = self.GetCursor(item)
                        self.__collection_following_pages.append(item)
                        if self.main is None: # Will surpress an NoneType error.
                            for obvious in self.__collection_following_pages:
                                self.appendage = self.GetFollows(obvious)
                                for trace in self.appendage:
                                    self.__found_following.append(trace)
                            database.store().hoard_handles(self.__found_following)
                            return self.__found_following
                else:
                    return None
        except TypeError, e:
            print e
            exit(1)
            self.pi(self.__notify.INFO + 'User Doesn\'t exist yet.')
            exit(0)

    def GetRefreshStreamCursor(self, content):
        self.refresh_response = re.findall(r'<a href="(/.*)"> Refresh </a>', content)
        if self.refresh_response != []:
            return self.refresh_response[0].replace('&amp;', '&')

        if self.refresh_response == []:
            return None

    def GetUserNameFromStream(self, content):
        self.name_container = re.findall(r'<a href="/(.*)\?p=s">', content)

        for name in self.name_container:
            self.__stream_collection.append(name)

        for item in self.__stream_collection:
            self.__unique_stream_collection[item] = 1
        return self.__unique_stream_collection.keys()

    def GetNewestTrends(self):
        self.woe_trend = re.findall(r'<a href="/search\?\?s=tren&amp;p=c&amp;q=(.*)">', self.GetRequest('https://mobile.twitter.com/trends').content)
        for tag in self.woe_trend:
            tag = tag.replace('%23', '').replace('%22', '"').replace('%20', ' ')
            self.__newest_trends.append(tag)
        return self.__newest_trends

    def PickLatestTrend(self):
        self.pick = random.randrange(0, 2)
        self.woe_trends = dirname(dirname(__file__)) + '/data/woetrends.txt'

        if self.pick == 1:
            with open(self.woe_trends, 'r') as file:
                for place in file:
                    place = place.replace('\n', '')
                    self.__latest_trends.append(place)

            self.found_length = len(self.__latest_trends)
            self.tin = random.randrange(0, self.found_length)
            return self.__latest_trends[self.tin]

        elif self.pick == 0:
            self.tags = self.GetNewestTrends()

            for tag in self.tags:
                self.__latest_trends.append(tag)

            self.found_length = len(self.__latest_trends)
            self.tin = random.randrange(0, self.found_length)
            return self.__latest_trends[self.tin]

    def CollectHandlesFromTrendStream(self):
        trend = self.PickLatestTrend()
        self.stream_location = 'https://mobile.twitter.com/search?q=%23{}'.format(trend)
        self.stream_content = self.GetRequest(self.stream_location).content
        self.pi(self.__notify.INFO + "Collecting users from the {} trend.".format(self.color.W + trend + self.color.N))
        while True:
            self.main_content = self.GetRefreshStreamCursor(self.stream_content)

            if self.main_content != None:
                self.refresh = self.__domain + self.main_content
                self.stream_content = self.GetRequest(self.refresh).content
                self.handles = self.GetUserNameFromStream(self.stream_content)

                if self.handles != []:
                    database.store().hoard_handles(self.handles)
                    time.sleep(7) # Wait for more people to tweet about the current hashtag.

            elif self.main_content == None:
                self.pi(self.__notify.INFO + 'restarting the collection process ...')
                self.CollectHandlesFromTrendStream() # Creates a vicious continuous loop.
