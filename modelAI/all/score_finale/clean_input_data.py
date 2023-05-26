
import pandas as pd
from Twitterpreprocessor import TwitterPreprocessor
import matplotlib.pyplot as plt
import tweepy
from decouple import config
import json
import requests
import joblib
import spacy
nlp = spacy.load('en_core_web_sm')
consumer_key = config('TWITTER_CONSUMER_KEY')
consumer_secret = config('TWITTER_CONSUMER_SECRET')
tiktok_key=config('TIKTOK_KEY')

def get_twitter_poste(id_poste,access_token,access_token_secret) -> str:
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        tweet = api.get_status(id_poste)
        tweet = tweet._json
        return tweet['text']

def get_tiktok_poste(id_poste,refrech_token) -> str:
        getUrl = f"https://open-api.tiktok.com/oauth/refresh_token?client_key={tiktok_key}&grant_type=refresh_token&refresh_token={refrech_token}"
        resMedia = requests.get(getUrl)
        accessToken = json.loads(resMedia.text)['data']['access_token']
        api_endpoint = "https://open-api.tiktok.com/video/query/"
        # Set your payload (data)
        payload = {
            "access_token":accessToken,       
            "filters": {
                "video_ids": [
                   id_poste
                ]
            },
        'fields': ["duration","title","video_description"],
        }

        response = requests.post(api_endpoint, json=payload)
        v = response.json()['data']['videos'][0]
        return v["video_description"]+" "+v["title"]
