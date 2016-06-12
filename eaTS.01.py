'''

eaStreamTwitter
by Eyal Assaf
v0.2
Write CSV file

Stream tweets based on hashtags and compiles them into a CSV file, to be sent to UE4

'''
# -*- coding: cp1252 -*-
# _*_ coding:utf-8 _*_
import sys
import io
# Import the necessary methods from tweepy library
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import json
import csv

import os
import os.path
'''
PATH='./file.txt'

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    print "File exists and is readable"
else:
    print "Either file is missing or is not readable"
'''
# Variables that contains the user credentials to access Twitter API
access_token = "3741374896-nHOo1GxSDXzKOwrGf3zTXuIQ5azENs5RfKQxz2y"
access_token_secret = "RiuAq559cr4DDHbt2NxdZVr1AbI7J37wdMa9IQGus8BRJ"
consumer_key = "HNDGwz1zOHXKjWhUovAkfHzpd"
consumer_secret = "7D2XrKIyWt6uNMB8f2XZgRDMWb2IZlE0l37475nsNvMdQqy8ki"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# prevents unicode errors - I hope
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# sys.stderr = codecs.getwriter('utf8')(sys.stderr.buffer, 'strict')
# confirm login into Twitter api
print("Successfully logged in as " + api.me().name + ".")

# tell computer where to put CSV
outfile_path='D:/GITHUB/MDMthesis/test.csv'

# open it up, the w means we will write to it
writer = csv.writer(open(outfile_path, 'w'))



# This is a basic listener that just prints received tweets to stdout.
class eaTweetStreamer(StreamListener):
    '''
    def __init__(self):
        self.startStream()
        '''

    def twitterStart(self):
        # variable to get user input. Send to get_input() method
        self.get_input(["s", "p", "q"])

    def get_input(self,userChoice):
        choice=""
        while choice not in userChoice:
            print("Twitter client menu - press 's' to search and 'q' to quit.")
            choice=input("-->")
            if choice=="s":
                self.searchHt() #go to search tweet method

            elif choice=="q":
                print ("goodbye!")
        return choice

    def searchHt(self):
        numTweets= input("Number of tweets to iterate (minimum 1):")
        if len(numTweets)>=1 and numTweets.isdigit():
            search = input("Search for a hashtag:") # get user input

            getHt=api.search(q="#{0}".format(search), count=numTweets)
            #self.startStream(search)
            '''
            for index,tweet in enumerate(getHt):
                print(index,tweet.text)
            '''
            # Only iterate through the first 200 statuses
            with open(outfile_path,"w") as acsv:
                w=csv.writer(acsv)
                #w.writerow(("User","Text"))
                #create a list with headings for our columns
                headers = ['user','created_at', 'location','time_zone','coordinates','tweet_text']

                #write the row of headings to our CSV file
                w.writerow(headers)


                for index,tweet in enumerate(tweepy.Cursor(api.search,q=search).items(int(numTweets))):
                    coded=tweet.text.encode('utf-8')
                    cleanTweet=str(coded)
                    loc=tweet.user.location.encode('utf-8')
                    location=str(loc)
                    print(index,cleanTweet[2:-1])
                    print("location: {0}".format(tweet.user.location))
                    print()
                    print("created: ",tweet.created_at)
                    print("Time zone: ", tweet.user.time_zone)
                    print("Place: ", tweet.place)
                    #print("Place: ", tweet.coordinates)
                    #print("============================")
                    #print("RAW DATA:")
                    #tUser=tweet.user
                    #print(tUser)
                    #print("============================")
                    user_coordinates=tweet.coordinates

                    if user_coordinates is None:
                        final_coordinates=user_coordinates
                    else:
                        dictCoords=tweet.coordinates
                        listCoords=dictCoords['coordinates']
                        final_coordinates=[listCoords[0],listCoords[1]]
                        print("coordinates:" ,final_coordinates)


                    #once you have all the cells in there, write the row to your csv
                    w.writerow((tweet.user.screen_name,tweet.created_at,location[2:-1],tweet.user.time_zone,final_coordinates,cleanTweet[2:-1]))


                    self.on_status(tweet)
                    #self.on_data(tweet)

                    print("============================")

            self.twitterStart()
        else:
            print("Enter at least 1 for tweets to search!")
            self.searchHt()

if __name__ == '__main__':
    eaTweetStreamer().twitterStart()
