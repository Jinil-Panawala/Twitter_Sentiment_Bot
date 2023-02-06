import functions

# Available Functions For Twitter Interactions:
#   tweet(tweepy.API, message : str, image_path = None)
#   like_home_tweets(num_tweets : int)
#   follow_any_followers_of_main_user(sc_name : str)
#  
# Available Functions For Sentiment Analysis:
#   follow_any_followers_of_main_user(sc_name : str)
#   get_tweets_sentiment_by_home_timeline(num_tweets : int)
#
# Export To CSV:
#   export_sentiment_date_to_csv(location, tweets, polarity, subjectivity)

# NOTE: include functions. before calling each function or using a global variable

# Call all functions here
def main():

    # Examples:
    functions.get_tweets_sentiment_by_keywords("SpaceX", 5)
    functions.get_tweets_sentiment_by_keywords("Elon Musk", 5)
    functions.get_tweets_sentiment_by_home_timeline(5)

    functions.export_sentiment_date_to_csv(functions.LOCATION_LIST, functions.TWEET_LIST, functions.POLARITY_LIST, functions.SUBJECTIVITY_LIST)




main()