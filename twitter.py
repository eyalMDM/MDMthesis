# Import Pythong/Twitter API using tweepy
import tweepy

# get twitter info from MDMryerson_bot
access_token = "2871921500-6ThFwpYuAMMjarFX3TbhkQR20bBIrX2iXH3RDhF"
access_token_secret = "zaKT9TPYvFAAuofKYEc5WpZIB1ZOYvmRo8AmeJoFHFOPl"
consumer_key = "oBVAq8cZPfdvf0QgTFyDenaye"
consumer_secret = "CMGBjcTZJ1XzWc75uiyufm9su5Q8e7E9cpmp2NY0CzggsItven"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# confirm login into Twitter api
print "Successfully logged in as " + api.me().name + "."

# start program
# create array with viable user options and call get_input method
def twitter():
    user_input=get_input(["p","s","q"])

# main method including error check if wrong keys pressed
def get_input(userChoice):
    choice=""
    while choice not in userChoice:
        print "Twitter client menu- press 'p' to post a tweet, 's' to search for a hashtag, or 'q' to quit"
        choice=raw_input("-->")
        if choice=="p":
          tweetmsg() #go to tweetmsg function

        elif choice=="s":
          searchht() #go to searchmsg function

        elif choice=="q":
            print "goodbye!" #exit the program

    return choice

# tweet function
def tweetmsg():
  tweet=raw_input("Enter tweet:") # get tweet msg
  if len(tweet)<=140:
    status=api.update_status(status=tweet)
    print "Thanks! Your tweet has been sent."
    twitter()
  else:
    print "You have more than 140 characters. Please edit your tweet!"
    tweetmsg()

# search hashtag funciton
def searchht():
  search=raw_input("Search for a hashtag:") # get user input
  getht=api.search(q="#{0}".format(search)) # start the search query and add an # to the query

  # this command is to print the first tweet in the search
  userName=(getht[0].user.screen_name)
  print "@{0}".format(userName) #print the user name
  print (getht[0].text) # print the first tweet

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

