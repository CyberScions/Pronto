#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: binary -*-

import os
import random
import datetime
import requests

# User-Agent for the info leak. Without it, we wouldn't be able to do these amazing things.
# Thanks twitter!
GLOBALUSERAGENT = {"User-Agent":'Windows / IE 6: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'}

class Utilities():

    # use only one print statement.
    def pi(self, pdata=''):
        print pdata

    # sys.argv bool checks for assurance.
    def sabc(self, argnum):
        try:
            if sys.argv[argnum]:
                return True
        except Exception:
            return False

    # String boolean checkself.
    def sbc(self, fn, s):
        #return a NoneType if the string is not in the file.

        if os.path.exists(fn) is False:
            MakeFile = open(fn, 'a').close()

        if os.path.exists(fn) is True:
            pass

        with open(fn, 'r') as f:
            for i in f:
                i = i.replace("\n", '')
                if s.encode('utf-8') in i:
                    return True

    # Get Requests HTTP style
    def GetHTTPRequest(self, url):
        GetRequestSession = requests.Session()
        response = GetRequestSession.get(url, headers=GLOBALUSERAGENT)
        return response # Just return the object, not the content.

utilities = Utilities()
