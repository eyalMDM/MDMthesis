from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import csv
from time import sleep

# Variables that contains the user credentials to access Twitter API

access_token = "3741374896-nHOo1GxSDXzKOwrGf3zTXuIQ5azENs5RfKQxz2y"
access_token_secret = "RiuAq559cr4DDHbt2NxdZVr1AbI7J37wdMa9IQGus8BRJ"
consumer_key = "HNDGwz1zOHXKjWhUovAkfHzpd"
consumer_secret = "7D2XrKIyWt6uNMB8f2XZgRDMWb2IZlE0l37475nsNvMdQqy8ki"

# tell computer where to put CSV
outfile_path='C:/Users/Eyal/Documents/GitHub/MDMthesis/test.csv'

# open it up, the w means we will write to it
writer = csv.writer(open(outfile_path, 'w'))

#create a list with headings for our columns
headers = ['user', 'tweet_text']

#write the row of headings to our CSV file
writer.writerow(headers)

# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        json_load = json.loads(data)

        texts = json_load['text']
        print("texts: ",texts)
        coded = texts.encode('utf-8')
        print("coded: ",coded)
        s = str(coded)
        print("results are: ",s[2:-1])
        i=1
        while i<13:
            print(i)

            for tweet in s['results']:
                row=[]
                # add every 'cell' to the row list, identifying the item just like an index in a list
                row.append(str(tweet['from_user'].encode('utf-8')))
                row.append(str(tweet['created_at'].encode('utf-8')))
                row.append(str(tweet['text'].encode('utf-8')))
                #once you have all the cells in there, write the row to your csv
                writer.writerow(row)
            i=i+1



        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, StdOutListener())

# This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
stream.filter(track=['euro', 'dollar', 'loonie', ], languages=['en'])
