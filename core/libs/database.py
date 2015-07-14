import re
import os
import time
from paint import color
from twitter import operations
from functions import Utilities
from core.info import notifications

class store(Utilities):

    def __init__(self):
        # Variables
        self.__found   = []
        self.__unique  = {}

        #Instantiations
        self.__twitter = operations()
        self.__notify  = notifications()
        self.__color   = color()

    def VisualizeTweets (self, username):
        """Extracts tweets from it's respective html.
        """
        # Mass decision maker, when visualing tweets.
        self.pi("\n{}Visualizing {}'s collected tweets".format(self.__notify.INFO, username))

        self.idn = self.__twitter.GetTwitterIDFromHandle(username)

        # This path already exists.
        self.tweets_path = '{}/{}_{}.tweet.links'.format(username, self.idn, username)

        # This path will exist if it doesn't.
        self._visual_tweet_path = '{}/tweets/'.format(username)
        self._visual_tweet_path_bool = os.path.exists(self._visual_tweet_path)

        if self._visual_tweet_path_bool is True:
            pass

        if self._visual_tweet_path_bool is False:
            os.mkdir(self._visual_tweet_path)

        with open(self.tweets_path, 'r') as file:
            os.chdir(self._visual_tweet_path) # Change into your visual tweets directory and write the tweets to file.

            for line in file:
                self.line = line.replace('\n', '')
                self.line_identifcation  = self.line.split('/')[5]
                self.tweet_date = self.__twitter.GetTweetDate(self.line)
                self.tweet_time = self.tweet_date.split('-')

                if self.tweet_date is not None:
                    self.tweet_identification = self.tweet_date.replace(' ', '_') + '_' + self.line_identifcation + ".{}".format(username) + ".tweet.html"

                #Turn your tweets into html, for viewing.
                self.html = self.GetHTTPRequest(self.line).text.encode('utf-8')
                self.tweet_path = '{}/tweets/{}'.format(username, tweetid)

                #Bools for checks
                self.path_bool = os.path.exists(self.tweet_path) # Tweet pass bool. Trying to speed up the process of visualing tweets.
                self.tweet_path_bool = os.path.exists(self.tweet_identification)

                # Trying to speed up the process of visualing tweets with file checks.
                if self.path_bool is True:
                    pass

                elif self.path_bool is False:

                    if self.tweet_path_bool is False:
                        self.tweet_containter = re.findall(r'<div class="dir-ltr" dir="ltr">  .*', html)
                        lot = len(tweetextract)
                        self.pi("{}Visualizing a tweet from {}.".format(self.__notify.INFO, tweetdate))

                        #Validation check
                        for tweet in self.tweet_containter:
                            self.__found.append(tweet)

                        for item in self.__found:
                            self.__unique[item] = 1

                        for content in self.__unique:
                            with open(self.tweet_identification, 'a+') as file:
                                self.bool_check = self.string_bool_check(tweetid, content)

                                if self.tweet_path_bool is None:
                                    file.write("\n" + content)

            self.pi("{}Visualized all collected tweets.\n".format(self.__notify.INFO))

    def tweets2file(self, IDN, username, TweetLinks):
        self.pi(self.__notify.INFO + "Wrote {} of {}'s tweet links to disk.\n".format(len(TweetLinks), username))
        self.handle_directory = '{}'.format(username)
        self.handle_directory_path_bool = os.path.exists(self.handle_directory) # Handle Direcory path

        if self.handle_directory_path_bool is True:
            pass

        elif self.handle_directory_path_bool is False:
            os.mkdir(self.handle_directory)

        self.tweets_path =  '{}/{}_{}.tweet.links'.format(username, IDN, username)

        with open(self.tweets_path, 'a+') as file:
                self.bool_check = self.string_bool_check(self.tweets_path, line)

                if self.bool_check is None:
                    file.write(line + "\n")

                elif self.bool_check is True:
                    pass

    def followers2file(self, username, followers):
        self.pi(self.__notify.INFO + "Collected {} of {}'s followers".format(len(followers), username))
        self.pi(self.__notify.INFO + "Wrote {} of {}'s followers to disk\n".format(len(followers), username))
        self.followers_path = '{}/{}.followers'.format(username, username)

        if followers is None:
            self.pi(self.__notify.INFO + username + ' isn\'t following anyone at this time.')
            exit(0)

        elif followers is not None:
            # Create a usernames directory if it doesn't exist.
            self.handle_directory = '{}'.format(username)
            self.handle_path_bool = os.path.exists(self.handle_directory) # Handle Direcory path

            if self.handle_path_bool is True:
                pass

            elif self.handle_path_bool is False:
                os.mkdir(self.handle_directory)

            with open(self.followers_path, 'a+') as file:
                for line in followers:
                    self.string_check = self.string_bool_check(self.followers_path, line)

                    if self.string_check is None:
                        file.write(line + " - " + self.__notify.PL + line + "\n")

                    if self.string_check is True:
                        pass

    def following2file(self, username, following):
        self.pi(self.__notify.INFO + "Collected {} of the users {} is following".format(len(following), username))
        self.pi(self.__notify.INFO + "Wrote {} to disk\n".format(len(following), username))
        self.following_path = '{}/{}.following'.format(username, username)

        if following is None:
            self.pi(self.__notify.INFO + username + ' isn\'t following anyone at this time.')
            exit(0)

        # Create a usernames directory if it doesn't exist.
        self.handle_directory = '{}'.format(username)
        self.handle_path_bool = os.path.exists(self.handle_directory) # Handle Direcory path

        if self.handle_path_bool is True:
            pass

        elif self.handle_path_bool is False:
            os.mkdir(self.handle_directory)

        with open(self.following_path, 'a+') as file:
            for line in following:
                self.line = line
                self.name_check = self.string_bool_check(self.following_path, self.line)

                if self.name_check is None:
                    file.write(line + " - " + self.__notify.PL + self.line + "\n")

    def profile2file(self, ID, username, Followers, Following, Tweets, PFL):
        # Path to profile.
        self.profile_path = '{}/{}_{}.twitter.profile'.format(username, ID, username)

        # Profile Path Boolean
        self.profile_path_bool = os.path.exists(self.profile_path)

        # Create a usernames directory if it doesn't exist.
        self.handle_directory = '{}'.format(username)
        self.handle_directory_bool = os.path.exists(self.handle_directory) # Handle Direcory path

        if self.handle_directory_bool is True:
            pass

        elif self.handle_directory_bool is False:
            os.mkdir(self.handle_directory)

        if self.profile_path_bool is True:
            pass

        elif self.profile_path_bool is False:

            with open(self.profile_path, 'w+') as file: # w+, when a handles updates there profile.
                file.write(self.__notify.TID + ID + "\n")
                file.write(self.__notify.TWEETS + Tweets + "\n")
                file.write(self.__notify.USERNAME + username + "\n")
                file.write(self.__notify.FOLLOWERS + Followers + "\n")
                file.write(self.__notify.FOLLOWING + Following + "\n")
                file.write(self.__notify.PROFILELINK + PFL + "\n")

    def hoard_handles(self, handles):
        self.data_file = os.path.dirname(os.path.dirname(__file__)) + '/data/mass_collection.txt'
        with open(self.data_file, 'a+') as file:
            for handle in handles:
                self.handle = handle.lower()
                self.handle_bool = self.string_bool_check(self.data_file, self.handle)
                
                if self.handle_bool is None:
                    self.idn = self.__twitter.GetIDFromHandle(self.handle)
                    if self.idn is None:
                        pass
                    self.pi(self.__notify.INFO + "Adding {} - {} to your mass user database.".format(self.__color.W + self.handle + self.__color.N, self.idn))
                    file.write(self.handle + " - " + str(self.idn) + " - " + self.__notify.PL + self.handle + '\n')
                elif self.handle_bool is True:
                    pass
            #self.pi(self.__notify.INFO + "Added %d users to your mass user database." % len(self.__found))
