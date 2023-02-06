import tweepy
from textblob import TextBlob
import csv
import keys

# authenticating user credentials
auth = tweepy.OAuthHandler(keys.api_key, keys.api_key_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
main_user = api.get_user(screen_name='jinil_panawala')

# tweets a message with or without an image
# requires: api is of type tweepy.API, message is string, image_path is a valid path to an image
def tweet(api : tweepy.API, message : str, image_path = None):
    if image_path:
        api.update_status_with_media(message, image_path)
    else:
        api.update_status(message)
    
    print ("TWEETED successfully") # confirmation message

# likes num_tweets tweets that are not your own tweets in your home timeline. 
# requires: num_tweets is an int
def like_home_tweets(num_tweets : int):
    tweets_home = api.home_timeline(count = num_tweets)
    for tweet in tweets_home:
        if tweet.author.screen_name != "jinil_panawala":

            if not tweet.favorited:
                print(f"Liking {tweet.id} ({tweet.author.screen_name})")
                api.create_favorite(tweet.id)

# follows any of the followers of a given user (expect yourself of course)
# requires: sc_name is a string
def follow_any_followers_of_main_user(sc_name : str):
    user = api.get_user(screen_name = sc_name)
    for follower in user.followers():
        if follower.screen_name == main_user.screen_name:
            continue
        api.create_friendship(screen_name = follower.screen_name)
        print("Followed: " + follower.screen_name)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Sentiment Analysis Section

LOCATION_LIST = []
USER_LIST = []
TWEET_LIST = []
POLARITY_LIST = []
SUBJECTIVITY_LIST = []

# prints num_tweets tweets relating to what was passed in search, and performs sentiment analysis (shows polarity and subjectivity of each tweet).
# requires: search is a string, num_tweets is an integer
def get_tweets_sentiment_by_keywords(search : str, num_tweets : int):
    public_tweets = api.search_tweets(search, count = num_tweets, tweet_mode='extended')
    for tweet in public_tweets:
        print(tweet.full_text)
        analysis = TextBlob(tweet.full_text)
        print(analysis.sentiment)
        print("\n")

        LOCATION_LIST.append("Public: " + search)
        USER_LIST.append(tweet.user.screen_name)
        TWEET_LIST.append(tweet.full_text)
        POLARITY_LIST.append(round(analysis.polarity, 3))
        SUBJECTIVITY_LIST.append(round(analysis.subjectivity, 3))



# prints num_tweets tweets in the home timeline and performs sentiment analysis.
# requires: num_tweets is an integer
def get_tweets_sentiment_by_home_timeline(num_tweets : int):
    tweets_home = api.home_timeline(count = num_tweets, tweet_mode='extended')
    for tweet in tweets_home:
        print(tweet.full_text)
        analysis = TextBlob(tweet.full_text)
        print(analysis.sentiment)
        print("\n")

        LOCATION_LIST.append("Home Timeline")
        USER_LIST.append(tweet.user.screen_name)
        TWEET_LIST.append(tweet.full_text)
        POLARITY_LIST.append(round(analysis.polarity, 3))
        SUBJECTIVITY_LIST.append(round(analysis.subjectivity, 3))


def export_sentiment_date_to_csv(location, tweets, polarity, subjectivity):
    with open('tweet_sentiment.csv', 'w', newline='') as csvfile:

        fieldnames = ['Number', 'Location', 'User', 'Tweet', 'Polarity', 'Subjectivity'] 

        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

        thewriter.writeheader()

        TWEET_COUNT = 0
        for tweet in TWEET_LIST:
            TWEET_COUNT += 1
            thewriter.writerow({'Number' : TWEET_COUNT, 
                                'Location' : LOCATION_LIST[TWEET_COUNT - 1],
                                'User' : USER_LIST[TWEET_COUNT - 1],
                                'Tweet' : TWEET_LIST[TWEET_COUNT - 1],
                                'Polarity' : POLARITY_LIST[TWEET_COUNT - 1],
                                'Subjectivity' : SUBJECTIVITY_LIST[TWEET_COUNT - 1]
                                })


