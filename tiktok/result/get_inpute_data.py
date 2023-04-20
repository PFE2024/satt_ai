import requests
import datetime
import time
import tweepy
import pandas as pd
import numpy as np
import requests
from decouple import config
import json


def creation_year(year):
    try:
        dt = datetime.datetime.strptime(str(year), '%Y-%m-%d %H:%M:%S')
        return dt.year
    except Exception as e:

        return 0


def convert_string_to_datetime(date):
    # print(datetime.datetime.fromtimestamp(date))
    return datetime.datetime.fromtimestamp(date)


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


def tiktok(tiktokProfile):
    try:
        allvideos = []

        if not tiktokProfile:
            return 'indisponible'
        getUrl = f"https://open-api.tiktok.com/oauth/refresh_token?client_key={config('TIKTOK_KEY')}&grant_type=refresh_token&refresh_token={tiktokProfile['refreshToken']}"
        resMedia = requests.get(getUrl)

        accessToken = json.loads(resMedia.text)['data']['access_token']
        u = requests.get('https://open.tiktokapis.com/v2/user/info/?fields=is_verified,created_at,is_private,follower_count,following_count,likes_count,bio_description,display_name,username,video_count', headers={
            "Authorization": "Bearer " + accessToken,
        })

        u = u.json()['data']['user']
        cursor = 0
        nbr_videos = 0

        while True:
            payload = "{\"max_count\":20" + \
                "}" if cursor == 0 else "{\"max_count\":10,\"cursor\":" + \
                str(cursor)+"}"
            videos = requests.post('https://open.tiktokapis.com/v2/video/list/?fields=create_time,like_count,comment_count,share_count,view_count', headers={
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }, data=payload)

            has_more = videos.json()['data']['has_more']
            cursor = videos.json()['data']['cursor']
            v = videos.json()['data']['videos']

            nbr_videos += len(v)
            # print("nbr_videos",len(v))
            allvideos.extend(v)
            if nbr_videos >= 200 or has_more == False:
                break
        # print(allvideos)
        end_date = datetime.datetime.now()
        start_date = datetime.datetime.now() - datetime.timedelta(days=7)
        num_of_videos_this_week = 0
        monday_to_sunday = [0] * 7
        twelve_am_to_eleven_pm = [0] * 24
        retweeted = 0
        most_recent_post = 0
        if len(allvideos) >= 1:
            most_recent_post = convert_string_to_datetime(
                allvideos[0]["create_time"])
            for tweet in allvideos:
                retweeted += tweet["share_count"]
                tweet_time = convert_string_to_datetime(tweet["create_time"])
                if (tweet_time < end_date and tweet_time > start_date):
                    num_of_videos_this_week += 1
                monday_to_sunday[datetime.datetime.weekday(tweet_time)] += 1
                twelve_am_to_eleven_pm[tweet_time.hour] += 1
        else:
            pass

        u["is_verified"] = int(u["is_verified"])
        #uNameScore = 1 - (levenshtein_distance(u["username"], u["display_name"]) / max(
          #  len(u["username"]), len(u["display_name"])))

        most_recent_post = creation_year(most_recent_post)
       # avg_videos_by_hour_of_day = round(
         #   sum(twelve_am_to_eleven_pm)/len(twelve_am_to_eleven_pm), 3)
       # avg_videos_by_day_of_week = round(
          #  sum(monday_to_sunday)/len(monday_to_sunday), 3)
        u_data = {
            "hasProfilePicture": u["hasProfilePicture"],
            "following": u["following_count"],
            "follower": u["follower_count"],
            "HasAccountDescription":u["has_account_description"],
            "likes":u["likes_count"],
            "posts": most_recent_post,
            "AverageNumberOfHashtags":u["average_number_of_hashtags"], 
            "AverageNumberOfComments":u["AverageNumberOfComments"],
            "AverageNumberOfShare":u["AverageNumberOfShare"], 
            "AverageNumberOfLikes":u["AverageNumberOfLikes"],
            "AverageNumberOfLinkedProfiles":u["AverageNumberOfLinkedProfiles"], 
            "AverageNumberOfViews":u["AverageNumberOfViews"],
        }
        return u_data
    except Exception as error:
        print('tiktok fetch stats', error)