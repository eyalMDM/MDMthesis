'''

eaStreamTwitter
by Eyal Assaf

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
        getNum= input("Number of tweets to iterate (minimum 1):")
        if len(getNum)>=1 and getNum.isdigit():
            search = input("Search for a hashtag:") # get user input
            getHt=tweepy.Cursor(api.search,q="#{0}".format(search), count=getNum)
            for index,tweet in enumerate(getHt):
                print(index,tweet.text)
            self.twitterStart()
        else:
            print("Enter at least 1 for tweets to search!")
            self.searchHt()






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



if __name__ == '__main__':
    eaTweetStreamer().twitterStart()
