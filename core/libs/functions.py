import os
import requests

class Utilities(object):

    def __init__(self):
        pass

    def pi(self, pdata=''):
        print pdata

    def select(self, message):
        while True:
            select = raw_input("\n{} ".format(message))
            return select

    def string_bool_check(self, file_name, string): # Check if string is in a file.
        #return a NoneType if the string is not in the file.
        #.readlines() May be a problem is database files get too large.

        if os.path.exists(file_name) is False:
            open(file_name, 'a').close()

        if os.path.exists(file_name) is True:
            pass

        with open(file_name, 'r') as file:
            for item in file:
                item = item.replace("\n", '')
                if string.decode('utf-8').encode('utf-8') in item:
                    return True

    # Get Requests HTTP style
    def GetRequest(self, url):
        self.session = requests.Session()
        self.response = self.session.get(url, headers=self.agent())
        return self.response

    def PostRequest(self, url, data):
        self.session = requests.Session()
        self.response = self.session.get(url, params=data,headers=self.agent())
        return self.response

    def agent(self):
        return {"User-Agent":'Windows / IE 6: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'}
