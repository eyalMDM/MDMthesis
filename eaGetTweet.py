#Import the necessary methods from tweepy library
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


#Variables that contains the user credentials to access Twitter API 
access_token =  "3741374896-nHOo1GxSDXzKOwrGf3zTXuIQ5azENs5RfKQxz2y"
access_token_secret = "RiuAq559cr4DDHbt2NxdZVr1AbI7J37wdMa9IQGus8BRJ"
consumer_key = "HNDGwz1zOHXKjWhUovAkfHzpd"
consumer_secret =  "7D2XrKIyWt6uNMB8f2XZgRDMWb2IZlE0l37475nsNvMdQqy8ki"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# confirm login into Twitter api
print("Successfully logged in as " + api.me().name + ".")
'''
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['zika'])
'''	
	
# start program
# create array with viable user options and call get_input method
def twitter():
    user_input=get_input(["p","s","q"])

# main method including error check if wrong keys pressed
def get_input(userChoice):
    choice=""
    while choice not in userChoice:
        print("Twitter client menu- press 'p' to post a tweet, 's' to search for a hashtag, or 'q' to quit")
        choice=input("-->")
        if choice=="p":
          tweetmsg() #go to tweetmsg function

        elif choice=="s":
          searchht() #go to searchmsg function

        elif choice=="q":
            print("goodbye!") #exit the program

    return choice

# tweet function
def tweetmsg():
  tweet=input("Enter tweet:") # get tweet msg
  if len(tweet)<=140:
    status=api.update_status(status=tweet)
    print("Thanks! Your tweet has been sent.")
    twitter()
  else:
    print("You have more than 140 characters. Please edit your tweet!")
    tweetmsg()

# search hashtag funciton
def searchht():
  search=input("Search for a hashtag:") # get user input
  getht=api.search(q="#{0}".format(search)) # start the search query and add an # to the query

  # this command is to print the first tweet in the search
  userName=(getht[0].user.screen_name)
  print("@{0}".format(userName))
  print((getht[0].text))

  twitter()
  '''

  # iterate through the latest tweets and print them one after the other
  print "Latest tweets:"
  for tweet in getht:
    print (tweet.text)
  twitter()
  '''


# run from cmd line
if __name__== '__main__':
    twitter()	
	
