'''

eaStreamTwitter
by Eyal Assaf
v0.1

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
outfile_path='C:/Users/Eyal/Documents/GitHub/MDMthesis/test.csv'

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
            print("Twitter client menu - press 's' to search, 'p' to post and 'q' to quit.")
            choice=input("-->")
            if choice=="s":
                self.searchHt() #go to search tweet method
            elif choice=="p":
                self.tweetMsg() # go to tweet message method

            elif choice=="q":
                print ("goodbye!")
        return choice

    def tweetMsg(self):
        print("tweeting message")
        self.twitterStart()

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
                headers = ['user','created_at', 'tweet_text']

                #write the row of headings to our CSV file
                w.writerow(headers)


                for index,tweet in enumerate(tweepy.Cursor(api.search,q=search).items(int(numTweets),)):
                    print(index,tweet.text)
                    print("location: {0}".format(tweet.user.location))
                    print()
                    print("created: ",tweet.user.created_at)
                    print("Time zone: ", tweet.user.time_zone)
                    print("Place: ", tweet.place)
                    print("============================")
                    #print("RAW DATA:")
                    #tUser=tweet.user
                    #print(tUser)



                    #once you have all the cells in there, write the row to your csv
                    w.writerow((tweet.user.screen_name,tweet.user.created_at,tweet.text.encode('utf-8')))


                    self.on_status(tweet)
                    #self.on_data(tweet)

                    print("============================")

            self.twitterStart()
        else:
            print("Enter at least 1 for tweets to search!")
            self.searchHt()
'''
    def on_status(self, status):

        if status.coordinates:
            print('coords:', status.coordinates)
        if status.place:
            print('place:', status.place.full_name)

        return True

    on_event = on_status

    def on_error(self, status):
        print("ERROR:" ,status)

    def on_data(self, data):
        print(data)
        parsed_json=json.loads(data)
        return True

    def startStream(self,search):
        #This handles Twitter authetification and the connection to Twitter Streaming API
        l = eaTweetStreamer()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)

        #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
        stream.filter(track=[search])
        return True





IS THIS EVEN NEEDED?

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

    def startStream(self):
        #This handles Twitter authetification and the connection to Twitter Streaming API
        l = eaTweetStreamer()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)

        #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
        stream.filter(track=['zika'])

'''

if __name__ == '__main__':
    eaTweetStreamer().twitterStart()
