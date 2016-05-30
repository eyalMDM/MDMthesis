"""

eaStreamTwitter
by Eyal Assaf

Stream tweets based on hashtags and compiles them into a CSV file,
to be sent to UE4

"""

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
# confirm login into Twitter api
print("Successfully logged in as " + api.me().name + ".")




# This is a basic listener that just prints received tweets to stdout.

class StdOutListener(StreamListener):
    '''
    def __init__(self):
        self.startStream()
        '''

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

    def startStream(self):
        # This handles Twitter authentification and the connection to Twitter
        # Streaming API
        l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)

        # This line filter Twitter Streams to capture data by the keywords:
        # 'python', 'javascript', 'ruby'
        stream.filter(track=['zika'])



if __name__ == '__main__':
    StdOutListener().startStream()
