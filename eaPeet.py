# code for streaming twitter to a mysql db
# for Python 3 and will support emoji characters (utf8mb4)
# based on the Python 2 code
# supplied by http://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
# for further information on how to use python 3, twitter's api, and
# mysql together visit: http://miningthedetails.com/blog/python/TwitterStreamsPythonMySQL/

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
#import mysql.connector
#from mysql.connector import errorcode
import time
import json
import csv

#test




#Twitter consumer key, consumer secret, access token, access secret
ckey="HNDGwz1zOHXKjWhUovAkfHzpd"
csecret="7D2XrKIyWt6uNMB8f2XZgRDMWb2IZlE0l37475nsNvMdQqy8ki"
atoken="3741374896-nHOo1GxSDXzKOwrGf3zTXuIQ5azENs5RfKQxz2y"
asecret="RiuAq559cr4DDHbt2NxdZVr1AbI7J37wdMa9IQGus8BRJ"
auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

# tell computer where to put CSV
outfile_path='C:/Users/Eyal/Documents/GitHub/MDMthesis/test.csv'

# open it up, the w means we will write to it
writer = csv.writer(open(outfile_path, 'w'))

#create a list with headings for our columns
headers = ['user', 'tweet_text']

#write the row of headings to our CSV file
writer.writerow(headers)

# set up stream listener
class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
		# collect all desired data fields
        if 'text' in all_data:
          tweetRaw         = all_data["text"]
          codedTweet = tweetRaw.encode('utf-8')
          tweet = str(codedTweet)
          #print("results are: ",s[2:-1])

          created_at    = all_data["created_at"]
          retweeted     = all_data["retweeted"]
          username      = all_data["user"]["screen_name"]
          user_tz       = all_data["user"]["time_zone"]
          user_location = all_data["user"]["location"]
          user_coordinates   = all_data["coordinates"]

	  # if coordinates are not present store blank value
	  # otherwise get the coordinates.coordinates value
          if user_coordinates is None:
            final_coordinates = user_coordinates
          else:
            final_coordinates = str(all_data["coordinates"]["coordinates"])


          print((username,tweet))

          return True
        else:
          return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

# create stream and filter on a searchterm
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["zika"],
  languages = ["en"], stall_warnings = True)
