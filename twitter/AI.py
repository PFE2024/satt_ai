

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
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib
# # load data
def fun():
    data = pd.read_csv('./Data/featuresfloatv3.csv')
    x=x.loc[:,['statuses' , 'date_joined' , 'most_recent_post' , 'following' , 'followers' , 'likes', 'retweet' , 'retweeted_count'  ,'avg_tweets_by_hour_of_day', 'avg_tweets_by_day_of_week'   ]]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42,stratify=y)
    # scale features
    # Create an instance of StandardScaler
    scaler = StandardScaler()

    # Fit the scaler to your data
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    # Transform the data using PCA
    pca = PCA(n_components=10)
    x_train = pca.fit_transform(x_train)
    x_test = pca.transform(x_test)
    clf=RandomForestClassifier(n_estimators=100, random_state=42)
    y = data.account_type.values.tolist()
    clf.fit(x_train,y_train)

    joblib.dump(clf, "clf.pkl")

