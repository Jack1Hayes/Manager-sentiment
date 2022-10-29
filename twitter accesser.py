"""
Created on Tue Aug  9 21:21:45 2022

@author: Hayes
"""
import tweepy
import csv
import pandas as pd
from datetime import datetime, timedelta
from textblob import TextBlob



# Connecting to your Twitter Developer APIs
api_key= 'kkNqG6QlAJfAUwkaHANj0EGv4' 
api_secret= 'UXlRuPxuBI81iKB3oWU8lzj2g5d22eRm2rkK7klzYaQFHUFkd9'
access_token= '1436025732-uQbqEAxbG4MYFyCksAeK5EvYx6iJldguIvBzeoK'
access_token_secret= '96l7QHPdFgfYYI8l6y7PDQ1jNTeHjKCjUiAMKKhWIiZ4u'
bearer_token= 'AAAAAAAAAAAAAAAAAAAAALAcfwEAAAAAws5L8IRN6AdaSwFRJ1buXqVK1L4%3DiONfYZq9Uv95GaqyIjrki37dEwTKwD1UD1NBu6FoR4Fk5iKPTw'

client = tweepy.Client(bearer_token)
# Authenticating the APIs
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

Twitter_table = pd.read_csv(r'C:\Users\Hayes\OneDrive\Documents\Data_sets\data from web\TwitterHandle+Manager_names_Table.csv')


# Define the search term and the date_since date as variables


def get_tweets():

    for i in Twitter_table.index:
        headers = pd.DataFrame(columns=['created_at','text', 'source','verified', 'like_count', 'reply_count','retweet_count','quote_count'])
        headers.to_csv(r'C:\Users\Hayes\OneDrive\Documents\Data_sets\Tweet.0\test'+str(Twitter_table['Club'][i][:3])+str(Twitter_table['Club'][i][-1])+'.csv',mode='w+',  index = False)
        for j in range(6):
            try:
                query = "("+(str(Twitter_table['last name'][i])+ " OR " + str(Twitter_table['first name'][i]) + ") lang:en -is:retweet to:"+str(Twitter_table['Twiiter name'][i])+" @"+str(Twitter_table['Twiiter name'][i]))
                print(query)
                # your start and end time for fetching tweets
                start_time = (datetime.today()-timedelta(days=(6-j))).strftime('%Y-%m-%dT00:00:00Z')
                end_time = (datetime.today()-timedelta(days=(5-j))).strftime('%Y-%m-%dT00:00:00Z')
                # get tweets from the API
                tweets = client.search_recent_tweets(query=query,
                                                     start_time=start_time,
                                                     end_time=end_time,
                                                     tweet_fields = ["created_at", "text", "source","public_metrics"],
                                                     user_fields = ["verified"],
                                                     max_results = 100,
                                                     expansions='author_id'
                                                     )

                
                # create a list of records
                tweet_info_ls = []
                # iterate over each tweet and corresponding user details
                for tweet, user in zip(tweets.data, tweets.includes['users']):
                    tweet_info = {
                        'created_at': tweet.created_at,
                        'text': tweet.text,
                        'source': tweet.source,
                        'verified': user.verified,
                        'like count': tweet.public_metrics['like_count'],
                        'reply_count': tweet.public_metrics['reply_count'],
                        'retweet_count': tweet.public_metrics['retweet_count'],
                        'quote_count': tweet.public_metrics['quote_count'],
                    }
                    tweet_info_ls.append(tweet_info)
                # create dataframe from the extracted records
                tweets_df = pd.DataFrame(tweet_info_ls)
                # display the dataframe
                tweets_df.head()
                #saving to csvpd.DataFrame(columns=['A','B','C','D','E','F','G'])
                                
                tweets_df.to_csv(r'C:\Users\Hayes\OneDrive\Documents\Data_sets\Tweet.0\test'+str(Twitter_table['Club'][i][:3])+str(Twitter_table['Club'][i][-1])+'.csv' ,mode='a',header = False, index = False)
            except KeyError:
                pass
        
get_tweets()
