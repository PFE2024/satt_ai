
import datetime
import time
import tweepy
import pandas as pd
import numpy as np
import requests
from decouple import config
# import pymongo
import json
consumer_key = config('consumer_key')
consumer_secret = config('consumer_secret')
access_key = config('access_key')
access_secret = config('access_secret')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def convert_twitter_datetime_to_string(date):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date, '%a %b %d %H:%M:%S +0000 %Y'))


def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    if m < n:
        return levenshtein_distance(s2, s1)
    if n == 0:
        return m

    previous_row = range(n+1)
    for i, c1 in enumerate(s1):
        current_row = [i+1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j+1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[n]




def creation_year(year):
    try:
        dt = datetime.datetime.strptime(str(year), '%Y-%m-%d %H:%M:%S')
        return dt.year
    except  Exception as e:
        
        return 0


def test_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=30)
      
       
        if response.status_code == 200:
            
            return 1
        else:
           
            return -1
    except Exception as e:
       
        return 0






def convert_string_to_datetime(date):
	return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

def get_details(username):

    try:
        userdata = api.get_user(screen_name=username)

    except Exception as e:
        
        return
        # 200 is the max

    end_date = datetime.datetime.now()
    start_date = datetime.datetime.now() - datetime.timedelta(days=7)
    user = userdata._json
    num_of_retweets_by_user = 0
    num_of_tweets_this_week = 0
    monday_to_sunday = [0] * 7
    twelve_am_to_eleven_pm = [0] * 24
    retweeted = 0
    most_recent_post = 0
    tweet_language = ''
    
    try:
        timeline = api.user_timeline(
            screen_name=username, count=200, include_rts=True, tweet_mode="extended")
        if len(timeline) >= 1:
            most_recent_post = convert_twitter_datetime_to_string(timeline[0]._json["created_at"])
            tweet_language = timeline[0]._json["lang"]
            for tweet in timeline:
                tweet = tweet._json
                retweeted += tweet["retweet_count"]
                if ("retweeted_status" in tweet):
                    num_of_retweets_by_user += 1
                tweet_time = convert_string_to_datetime(convert_twitter_datetime_to_string(tweet["created_at"]))
                if (tweet_time < end_date and tweet_time > start_date):
                    num_of_tweets_this_week += 1
                monday_to_sunday[datetime.datetime.weekday(tweet_time)] += 1
                twelve_am_to_eleven_pm[tweet_time.hour] += 1
        else:
            pass
    except Exception as e:
        return {"message":"can't get user_timeline"}
    user["url"] = test_url(user["url"])
    lang_dict = pd.read_csv("lang_dict1.csv", index_col=0).squeeze("columns")
    
    lang_dict = dict(lang_dict.items())
    
    lang_dict.setdefault(tweet_language, len(lang_dict)+1)
   
    tweet_language = lang_dict[tweet_language]
    lang_dict = pd.Series(lang_dict)
    lang_dict.to_csv('./lang_dict1.csv')
    user["location"] = int(user["location"] is not None)
    user["verified"] = int(user["verified"])
    userNameScore = 1 - (levenshtein_distance(user["screen_name"], user["name"]) / max(
        len(user["screen_name"]), len(user["name"])))
    dateofjoin =creation_year(convert_twitter_datetime_to_string(user["created_at"]))
    most_recent_post =creation_year(most_recent_post)
    avg_tweets_by_hour_of_day = round(
        sum(twelve_am_to_eleven_pm)/len(twelve_am_to_eleven_pm), 3)
    avg_tweets_by_day_of_week = round(
        sum(monday_to_sunday)/len(monday_to_sunday), 3)
    user_data = {
        "verified": user["verified"],
        "statuses": user["statuses_count"],
         "location": user["location"],
          "date_joined": dateofjoin,
           "most_recent_post": most_recent_post,
            "following": user["friends_count"],
        "followers": user["followers_count"],
"favourites": user["favourites_count"],
        "lists": user["listed_count"],
        "tweet_language": tweet_language,
           "tweets_this_week": num_of_tweets_this_week,
        "retweet": int(num_of_retweets_by_user),
        "retweeted_count": int(retweeted),
 "URL works": user["url"],
        "userNameScore": userNameScore,
        "avg_tweets_by_hour_of_day": avg_tweets_by_hour_of_day,
        "avg_tweets_by_day_of_week": avg_tweets_by_day_of_week,
        "screen_name":user["screen_name"],
    }
    return (user_data)
