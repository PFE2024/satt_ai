

# # import
import sys

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
import get_inpute_data 
import csv
import joblib
import os
# # load data
def run():
    data = pd.read_csv('./Data/featuresfloatvf.csv')
    # x=data.loc[:,['statuses' , 'date_joined' , 'most_recent_post' , 'following' , 'followers' , 'likes', 'retweet' , 'retweeted_count'  ,'avg_tweets_by_hour_of_day', 'avg_tweets_by_day_of_week']]
    x=data.iloc[:, :-2]
    y = data.account_type.values.tolist()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42,stratify=y)
    
    # # # scale features
    # # # Create an instance of StandardScaler
    # scaler = StandardScaler()
    # # Fit the scaler to your data
    # x_train = scaler.fit_transform(x_train)
    # x_test = scaler.transform(x_test)
    # sm = ADASYN(random_state=42)
    # x_train,y_train = sm.fit_resample(x_train,y_train)
    clf=RandomForestClassifier()
    clf.fit(x_train,y_train)
    y_pred_train = clf.predict(x_train)
    y_pred_test = clf.predict(x_test)
    joblib.dump(clf, "clf.pkl")
    return {"message":"done","Training Accuracy score":metrics.accuracy_score(y_train, y_pred_train),"Testing Accuracy score":metrics.accuracy_score(y_test, y_pred_test)}

def rerun():  
    try:
        accounts=pd.read_csv('./Data/accounts.csv')
    except :
        return {"message":"there is nothing to add"}
    data = pd.read_csv('./Data/featuresfloatvf.csv')
    accounts['screen_name'] = accounts['screen_name'].astype(str).str.lower()
    data['screen_name'] = data['screen_name'].astype(str).str.lower()
    ac=accounts[~accounts['screen_name'].isin(data['screen_name'])]
    ac=ac.drop(['predict_proba'],axis=1)
    ac.to_csv('./Data/featuresfloatvf.csv', mode='a', header=False, index=False)
    os.remove('./Data/accounts.csv')
    return run()

def predicte(name):
    
    # data = pd.read_csv('./Data/featuresfloatvf.csv')
    # column_names = data.columns.tolist()
    
    try:
        accounts=pd.read_csv('./Data/accounts.csv')
        accounts['screen_name'] = accounts['screen_name'].astype(str).str.lower()
        dp = accounts[accounts['screen_name']==str.lower(name)]
        
        if dp.shape[0] == 0:
            x=1
        else :
             print("data exist in accounts")
             return {"result":str(dp[0]['account_type']),"proba":str(dp[0]['predict_proba'][0])}            
    except Exception as e:
         x=-1
    account=get_inpute_data.get_details(name)
    dp=pd.DataFrame(account, index=[0])
    dp1=dp.drop('screen_name',axis=1)
    try:
        clf=joblib.load("clf.pkl")
    except:
        run()
    predicted=clf.predict(dp1)
    predict_proba=clf.predict_proba(dp1)[:,1]
    dp1['account_type']=predicted
    dp1['predict_proba']=predict_proba
    dp1['screen_name']=dp['screen_name']
    if x ==1:
        dp1.to_csv('./Data/accounts.csv', mode='a', header=False, index=False)
    else:
         dp1.to_csv('./Data/accounts.csv', index=False)
    return {"result":str(predicted[0]),"proba":str(predict_proba[0])}



def changepredicte(name,type):
    # data = pd.read_csv('./Data/featuresfloatvf.csv')
    # column_names = data.columns.tolist()
    try:
        accounts=pd.read_csv('./Data/accounts.csv')
        
        accounts['screen_name'] = accounts['screen_name'].astype(str).str.lower()
        dp = accounts[accounts['screen_name']==str.lower(name)]
        
        if dp.shape[0] == 0:
            return {"message": "accounts with that name does not exist"}
        else :
            #  dp[0]['account_type']=type
             accounts.loc[accounts['screen_name']==str.lower(name), 'account_type'] = type
            
             accounts.to_csv('./Data/accounts.csv', index=False)
             return {"message":"done please rerun"}            
    except Exception as e:
        return {"message": "accounts empty","error":str(e)}

