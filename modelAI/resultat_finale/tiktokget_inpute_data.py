import requests
import datetime

import requests
from decouple import config
import json
import re

def creation_year(year):
    try:
        dt = datetime.datetime.strptime(str(year), '%Y-%m-%d %H:%M:%S')
        return dt.year
    except Exception as e:

        return 0


def convert_string_to_datetime(date):
    # print(datetime.datetime.fromtimestamp(date))
    return datetime.datetime.fromtimestamp(date)


def extract_hashtags_mentions_emojis(text):
    # Extract hashtags
    hashtags = len(re.findall(r"#(\w+)", text)) 
    
    # Extract mentions
    mentions = len(re.findall(r"@(\w+)", text))
    
    return hashtags, mentions

def get_details(tiktokProfile):
    try:
       
        share = 0
        like = 0
        views = 0
        comments = 0
        all_videos=0
        Hashtag=[]
        LinkedProfiles=[]
        hashtags= linked_profiles =0
        if not tiktokProfile or not tiktokProfile['refreshToken']:
            return {"message":'refreshToken indisponible'}
        getUrl = f"https://open-api.tiktok.com/oauth/refresh_token?client_key={config('TIKTOK_KEY')}&grant_type=refresh_token&refresh_token={tiktokProfile['refreshToken']}"
        resMedia = requests.get(getUrl)

        accessToken = json.loads(resMedia.text)['data']['access_token']
        u = requests.get('https://open.tiktokapis.com/v2/user/info/?fields=is_verified,avatar_url,follower_count,following_count,likes_count,bio_description,display_name,username,video_count', headers={
            "Authorization": "Bearer " + accessToken,
        })

        payload = "{\"max_count\":20}"
        u = u.json()['data']['user']
        HasAccountDescription=1 if u['bio_description'] else 0
        videos = requests.post('https://open.tiktokapis.com/v2/video/list/?fields=create_time,duration,like_count,comment_count,share_count,view_count,video_description', headers={
            "Authorization": "Bearer " + accessToken,
            "Content-Type": "application/json"
        }, data=payload)
        videos = videos.json()['data']['videos']
        if len(videos) >= 1:
            for video in videos:
                share += video["share_count"]
                like += video["like_count"]
                views += video["view_count"]
                comments += video["comment_count"]
               
                if video['video_description']:
                    hashtags, linked_profiles = extract_hashtags_mentions_emojis(video['video_description'])
                    Hashtag.append(hashtags)
                    LinkedProfiles.append(linked_profiles)
            all_videos=len(videos)
           
            share =share/all_videos
            like = like/all_videos
            views = views/all_videos
            comments = comments/all_videos
            hashtags =sum(Hashtag)/all_videos
            linked_profiles=sum(LinkedProfiles)/all_videos
        else:
            pass
       
  
        u_data = {
            
              'HasProfilePicture':1.0 if u["avatar_url"] else 0.0,
                'following':round(u['following_count'], 2) , 
                'follower':round(u['follower_count'], 2) ,
            'HasAccountDescription':round(HasAccountDescription, 2),
              'likes':round(u['likes_count'], 2) ,
                'posts':round(u['video_count'], 2),
               
            'AverageNumberOfHashtags':round(hashtags, 2) ,
              'AverageNumberOfComments':round(comments, 2) ,
            'AverageNumberOfShare':round(share, 2) ,
              'AverageNumberOfLikes':round( like, 2),
            'AverageNumberOfLinkedProfiles':round(linked_profiles, 2) ,
            'AverageNumberOfViews':round(views, 2) , 
             "username":u['username']
        }
        return u_data
    except Exception as error:
        return  {"message":error}