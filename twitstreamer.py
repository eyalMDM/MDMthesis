#!/usr/bin/python3

# Copyright (C) 2012 Niall McCarroll
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the
# following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# twitstreamer.py
# a very simple tool for streaming tweets from the twitter streaming API
# run python3 twitstreamer.py -h for help

from urllib.parse import quote
import time
import json
import select
import datetime
import time
import os
from os.path import exists
import sys
import argparse
import logging
import random
import hashlib
import hmac
from hashlib import sha1
import base64
import csv

from http.client import HTTPSConnection

# you must fill in the following values before you can run this script!
#consumer_key = ""
#consumer_secret = ""

# access_token = ""
# access_secret = ""
access_token = "3741374896-nHOo1GxSDXzKOwrGf3zTXuIQ5azENs5RfKQxz2y"
access_secret = "RiuAq559cr4DDHbt2NxdZVr1AbI7J37wdMa9IQGus8BRJ"
consumer_key = "HNDGwz1zOHXKjWhUovAkfHzpd"
consumer_secret = "7D2XrKIyWt6uNMB8f2XZgRDMWb2IZlE0l37475nsNvMdQqy8ki"
# formatter class for storing tweets as CSV rows
class csvformatter(object):

    csv.register_dialect('quotedcsv', delimiter=',', quoting=csv.QUOTE_ALL)

    def __init__(self,columns,write_header):
        self.columns = columns
        self.writer = None
        self.writer = csv.writer(sys.stdout,dialect="quotedcsv")
        if write_header:
            self.writer.writerow([col[0] for col in self.columns])

    def write(self,raw,obj):
        row = []
        for (col,decoder) in self.columns:
            if col in obj:
                row.append(obj[col])
            else:
                row.append("")
        self.writer.writerow(row)


# formatter class for storing tweets as JSON objects
class jsonformatter(object):

    def __init__(self):
        self.file = sys.stdout

    def write(self,raw,obj):
        s = json.dumps(obj)
        self.file.write(s+"\n")

# formatter class for storing tweets as raw JSON objects
class rawformatter(object):

    def __init__(self):
        self.file = sys.stdout

    def write(self,raw,obj):
        s = json.dumps(raw)
        self.file.write(s+"\n")


# utility class for streaming tweets from the twitter API
class twitstream(object):

    def __init__(self,options):
        self.options = options
        self.track = options.track
        self.locations = options.locations
        self.count = 0
        self.checkpoint_count = 0
        self.start_time = 0
        self.checkpoint_time = 0

        def date_decoder(s):
            return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(s,'%a %b %d %H:%M:%S +0000 %Y'))

        def geo_decoder(g,index):
            try:
                return str(g["geo"]["coordinates"][index])
            except:
                return ""

        # define which columns to create from each tweet object
        # as a list of column name, extractor-function pairs
        # an extractor function extracts the value of the column from
        # the tweet object
        # if extractor-function is set to None, the column name
        # is used as the lookup key in the tweet object
        self.columns = [("id",None),
                ("created_at",lambda x: date_decoder(x["created_at"])),
                ("geo_lat",lambda x: geo_decoder(x,0)),
                ("geo_lon",lambda x: geo_decoder(x,1)),
                ("from_user_name",lambda x:x["user"]["name"]),
                ("from_user_screen_name",lambda x:x["user"]["screen_name"]),
                ("iso_language_code",lambda x: x["user"]["lang"]),
                ("text",None)]

        self.formatter = self.createFormatter(self.columns)

    # create and return a formatter object
    def createFormatter(self,columns):
        if self.options.format == "json":
            return jsonformatter()
        elif self.options.format == "raw":
            return rawformatter()
        elif self.options.format == "csv":
            return csvformatter(columns,True)
        else:
            return csvformatter(columns,False)

    # generate a nonce used in the OAuth process
    def generate_nonce(self):
        random_number = ''.join(str(random.randint(0, 9)) for i in range(40))
        m = hashlib.md5((str(time.time()) + str(random_number)).encode())
        return m.hexdigest()

    # generate an OAuth Authorization header to add to each request
    # see https://dev.twitter.com/docs/auth/authorizing-request
    def generate_authorization_header(self,method,url,query_parameters):
        nonce = self.generate_nonce()
        s = ""
        params = {}
        for key in query_parameters.keys():
            params[key] = query_parameters[key]

        params["oauth_nonce"] = nonce
        params["oauth_consumer_key"] = consumer_key
        params["oauth_token"] = access_token
        params["oauth_signature_method"] = "HMAC-SHA1"
        params["oauth_version"] = "1.0"
        params["oauth_timestamp"] = str(int(time.time()))

        sortkeys = [k for k in params.keys()]
        sortkeys.sort()
        for k in sortkeys:
            if s != "":
                s += "&"
            s += quote(k,'')
            s += '='
            s += quote(params[k],'')

        base_string = quote(method,'')+"&"+quote(url,'')+"&"+quote(s,'')

        signing_key = consumer_secret+"&"+access_secret

        tok = base64.standard_b64encode(hmac.new(signing_key.encode(),base_string.encode(),sha1).digest()).decode('ascii')

        params["oauth_signature"] = tok

        auth_header = "OAuth "
        auth_keys = [k for k in params.keys()]
        auth_keys.sort()
        first = True
        for k in auth_keys:
            if k.startswith("oauth"):
                if not first:
                    auth_header += ", "
                auth_header += k
                auth_header += '="'
                auth_header += quote(params[k])
                auth_header += '"'
                first = False
        return auth_header

    def sample(self):
        url = "https://stream.twitter.com/1.1/statuses/sample.json"
        query = {}
        self.start_time = int(time.time())
        while True:
            try:
                auth_header = self.generate_authorization_header("GET",url,query)
                conn = HTTPSConnection("stream.twitter.com")
                logging.getLogger("twitstream").debug("calling: https://stream.twitter.com/1.1/statuses/sample.json")
                conn.request("GET","/1.1/statuses/sample.json",None,{'User-agent':'Mozilla/5.0','Authorization':auth_header})
                self.stream(conn)
            except Exception as ex:
                logging.getLogger("twitstream").error(str(ex))

    def filter(self):
        url = "https://stream.twitter.com/1.1/statuses/filter.json"
        query = {}
        querystring =""
        if self.track:
            query["track"] = self.track
            querystring += "track="+quote(self.track)

        if self.locations:
            query["locations"] = self.locations
            if querystring:
                querystring += "&"
            querystring += "locations="+quote(self.locations)

        self.start_time = int(time.time())
        running = True
        while running:
            try:
                auth_header = self.generate_authorization_header("POST",url,query)
                logging.getLogger("twitstream").debug("calling: https://stream.twitter.com/1.1/statuses/filter.json?"+querystring)
                conn = HTTPSConnection("stream.twitter.com")
                conn.request("POST","/1.1/statuses/filter.json?"+querystring,"",{'User-agent':'Mozilla/5.0','Authorization':auth_header})
                running = self.stream(conn)
            except Exception as ex:
                logging.getLogger("twitstream").error(str(ex))

    def stream(self,conn):
        resp = conn.getresponse()
        data = bytes()

        while True:
            ready = select.select([resp],[],[],90.0)[0]
            if not ready:
                # twitter api is designed to send a dummy message every 30 seconds
                # but we have not recieved anything in 90 seconds, timeout reading and restart the connection
                logging.getLogger("twitstream").error("timeout - retrying connection")
                return True
            newdata = resp.read(65536)
            data += newdata
            pos = data.find(b'\r\n')
            while pos > -1:
                line = data[:pos]
                data = data[pos+2:]
                if line:
                    try:
                        j = line.decode("utf-8")
                        status = json.loads(j)
                        if "text" not in status:
                            if "delete" not in status:
                                logging.getLogger("twitstream").info("not a status?:"+json.dumps(status))
                        else:
                            self.write(status)
                        if options.maxtweets and self.count > options.maxtweets:
                            logging.getLogger("twitstream").info("collected "+str(options.maxtweets)+",terminating")
                            return False
                    except Exception as ex:
                        logging.getLogger("twitstream").error(str(ex))
                pos = data.find(b'\r\n')


    # call the twitter search API to fetch tweets matching search term
    def start(self):
        if self.track or self.locations:
            self.filter()
        else:
            self.sample()


    def write(self,r):
        obj = {}
        for (col,decoder) in self.columns:
            try:
                if decoder:
                    obj[col] = decoder(r)
                elif col in r:
                    obj[col] = str(r[col])
            except:
                obj[col] = None
        self.formatter.write(r,obj)
        self.count += 1

        if self.options.interval:
            t = int(time.time())
            if self.checkpoint_time == 0:
                self.checkpoint_time = t

            lastinterval = (t - self.checkpoint_time)
            interval = (t - self.start_time)
            if lastinterval > self.options.interval:
                rate = self.count / interval
                recentcount = self.count - self.checkpoint_count
                lastrate = recentcount / lastinterval
                self.checkpoint_time =  t
                self.checkpoint_count = self.count
                logging.getLogger("twitstream").info("recent: %d records in %d secs (%.2f records per second).  overall: %d records in %d secs (%.2f records per second)."%(recentcount,lastinterval,lastrate,self.count,interval,rate))

if __name__ == '__main__':

    if consumer_key == "" or consumer_secret == "" or access_token == "" or access_secret == "":
        print("Error - please define the variables consumer_key,consumer_secret,access_token and access_secret at the start of this program")
        sys.exit(-1)

    parser = argparse.ArgumentParser(description="stream tweets from the twitter streaming APIs", usage="python3 twitstreamer.py")

    parser.add_argument('-t', "--track", dest='track', type=str, help='track option to filter tweets, for example to recieve whiskey related treets, -t=whiskey for more information see https://dev.twitter.com/docs/streaming-apis/parameters#track')
    parser.add_argument("-v","--verbose",dest="verbose",action="store_true",help="display verbose messages")
    parser.add_argument("-i","--interval",dest="interval",type=int,default=300,help="define number of seconds interval for reporting statistics")
    parser.add_argument("-l","--locations",dest="locations",type=str,help="supply location filter in form of a bounding box lon_sw,lat_sw,lon_ne,lat_ne (example for London: -l=-0.563000,51.280430,0.278970,51.683979 for more information see https://dev.twitter.com/docs/streaming-apis/parameters#locations",default="")
    parser.add_argument("-f","--format",dest="format",type=str,help="supply format as json or csv",choices=["csv","csv_noheader", "json", "raw"], default="csv")
    parser.add_argument("-m","--max",dest="maxtweets",type=int,help="limit the number of tweets retrieved to the specified number")


    options = parser.parse_args()

    if options.verbose:
        logging.getLogger("twitstream").setLevel(level=logging.DEBUG)
    else:
        logging.getLogger("twitstream").setLevel(level=logging.INFO)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logging.getLogger("twitstream").addHandler(handler)
    tw = twitstream(options)
    tw.start()
