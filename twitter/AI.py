

# # import
import sys
print(sys.executable)
import numpy as np 
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import gender_guesser.detector as gender
import matplotlib.pyplot as plt 
from datetime import datetime
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report

# # load data
def fun():
    data = pd.read_csv('./Data/featuresfloatv2.csv')
    data=data.loc[:,['verified','statuses','location','date_joined','most_recent_post','following','followers','likes','lists','tweet_language','tweets_this_week','retweet_ratio','retweeted_count','URL works','userNameScore','avg_tweets_by_hour_of_day','avg_tweets_by_day_of_week','account_type']]

    x=data.loc[:,['verified','statuses','location','date_joined','most_recent_post','following','followers','likes','lists','tweet_language','tweets_this_week','retweet_ratio','retweeted_count','URL works','userNameScore','avg_tweets_by_hour_of_day','avg_tweets_by_day_of_week']]

    # scale features

    from sklearn.preprocessing import StandardScaler

    # Create an instance of StandardScaler
    scaler = StandardScaler()

    # Fit the scaler to your data
    scaler.fit(x)

    # Transform your data using the scaler
    X_scaled = scaler.transform(x)


    clf=RandomForestClassifier()
    y = data.account_type.values.tolist()
    x_train, x_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42,stratify=y)
    clf.fit(x_train,y_train)

    

    import joblib

    joblib.dump(clf, "clf.pkl")

