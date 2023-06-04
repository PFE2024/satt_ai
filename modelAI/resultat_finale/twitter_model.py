
from flask import abort
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from imblearn.over_sampling import SMOTE
import tiktokget_inpute_data 
import twitterget_inpute_data 
import joblib



import joblib


import re
import numpy as np

import spacy
import torch

from Twitterpreprocessor import TwitterPreprocessor

def twitterrerun():
    data = pd.read_csv('./TwitterAccount.csv')
    # x=data.loc[:,['statuses' , 'date_joined' , 'most_recent_post' , 'following' , 'followers' , 'likes', 'retweet' , 'retweeted_count'  ,'avg_tweets_by_hour_of_day', 'avg_tweets_by_day_of_week']]
    x=data.iloc[:, :-2]
    y = data.account_type.values.tolist()
    smote = SMOTE(random_state=10)
    x, y =smote.fit_resample(x, y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42,stratify=y)
    clf=RandomForestClassifier()
    clf.fit(x_train,y_train)
    y_pred_train = clf.predict(x_train)
    y_pred_test = clf.predict(x_test)
    joblib.dump(clf, "twitterclf.pkl")
    return {"message":"terminer","Training Accuracy score":metrics.accuracy_score(y_train, y_pred_train),
            "Testing Accuracy score":metrics.accuracy_score(y_test, y_pred_test)}

def twittercheckuser(name,access_key,access_secret):  
    ac=twitterget_inpute_data.get_details(name,access_key,access_secret)
    account=ac['user_data']
    # print(account)
    if 'message' in account:
        abort(400, "can't get account details")
    dp=pd.DataFrame(account, index=[0])
    dp1=dp.drop('screen_name',axis=1)
    try:
        clf=joblib.load("twitterclf.pkl")
    except:
        twitterrerun()
    clf=joblib.load("twitterclf.pkl")
    predicted=clf.predict(dp1)
    predict_proba=clf.predict_proba(dp1)[:,1]
    dp1['screen_name']=dp['screen_name']
    dp1['account_type']=predicted
   
    existing_data = pd.read_csv('./TwitterAccount.csv')
  
    merged_data = pd.concat([existing_data, dp1], ignore_index=True)
    # drop the duplicates based on the 'username' column
    merged_data.drop_duplicates(subset=['screen_name'], inplace=True,keep='last')
    # write the merged and de-duplicated data to a new CSV file
    merged_data.to_csv('./TwitterAccount.csv', index=False)
    return {"result":"bot" if predicted[0] == 0 else "human","score":str(round(predict_proba[0]*5)),"chart":ac['chart']}

def changetwitterpredicte(name,type):
    try:
        accounts=pd.read_csv('./TwitterAccount.csv')
        
        accounts['screen_name'] = accounts['screen_name'].astype(str).str.lower()
        dp = accounts[accounts['screen_name']==str.lower(name)]
        
        if dp.shape[0] == 0:
            abort(400, "accounts with that name does not exist")
            
        else :
            #  dp[0]['account_type']=type
            
            y=  "0.0" if type == "bot" else "1.0" if type == "human" else  Exception("erreur type must be bot or human")
            if isinstance(y, Exception):
                abort(400, "type must be bot or human")
            accounts.loc[accounts['screen_name']==str.lower(name), 'account_type'] =y
            accounts.to_csv('./TwitterAccount.csv', index=False)
            return {"message":"done please rerun"}            
    except Exception as e:
        abort(400, str(e))
        
def checkfollowers(name,access_key,access_secret):
    
    account=twitterget_inpute_data.get_followers_details(name,access_key,access_secret)
    # print(account)
    if 'message' in account:
        abort(400, "can't get account followers")
    dp1=pd.DataFrame(account)
    try:
        clf=joblib.load("twitterclf.pkl")
    except:
        twitterrerun()
    clf=joblib.load("twitterclf.pkl")
    resultes=[]
    resulte=[]
    nb_humain=0
    nb=0
    for i,user in dp1.iterrows():
        user= user.to_frame().T
        dp=user
        user=user.iloc[:, :-1]
        predicted=clf.predict(user)
        predict_proba=clf.predict_proba(user)[:,1]
        user['screen_name']=dp['screen_name'].iloc[0]
        user['account_type']=predicted
        nb+=1
        if  (user['account_type'] == 1).any():
                nb_humain+=1
        u={"screen_name":dp['screen_name'].iloc[0],"score":str(round(predict_proba[0]*5))}
        resultes.append(u)
        resulte.append(user)

    # existing_data = pd.read_csv('./dataFinal.csv')
    # resultes_df = pd.concat(resulte, axis=0, ignore_index=True)
    # # append the new data to the existing data
    # merged_data = pd.concat([existing_data, resultes_df], ignore_index=True)
    # # drop the duplicates based on the 'username' column
    # merged_data.drop_duplicates(subset=['screen_name'], inplace=True,keep='last')
    # # write the merged and de-duplicated data to a new CSV file
    # merged_data.to_csv('./dataFinal.csv', index=False)
    prop = (nb_humain / nb) * 5
    # convert float to string
    prop_str = str(round(prop))
    return {'score':prop_str,'resultes':resultes}


def checkfriends(name,access_key,access_secret):
    
    account=twitterget_inpute_data.get_friends_details(name,access_key,access_secret)
    # print(account)
    if 'message' in account:
        abort(400, "can't get account friends")
    
    dp1=pd.DataFrame(account)
   
   
    try:
        clf=joblib.load("twitterclf.pkl")
    except:
        twitterrerun()
    clf=joblib.load("twitterclf.pkl")
    resultes=[]
    resulte=[]
    nb_humain=0
    nb=0
    for i,user in dp1.iterrows():
        user= user.to_frame().T
        dp=user
        user=user.iloc[:, :-1]
       
        predicted=clf.predict(user)
        predict_proba=clf.predict_proba(user)[:,1]
        
        user['screen_name']=dp['screen_name'].iloc[0]
        user['account_type']=predicted
        nb+=1
        if  (user['account_type'] == 1).any():
                nb_humain+=1
        
        u={"screen_name":dp['screen_name'].iloc[0],"score":str(round(predict_proba[0]*5))}
        resultes.append(u)
        resulte.append(user)
    # existing_data = pd.read_csv('./dataFinal.csv')
    # resultes_df = pd.concat(resulte, axis=0, ignore_index=True)
    
    # # append the new data to the existing data
    # merged_data = pd.concat([existing_data, resultes_df], ignore_index=True)
    # # drop the duplicates based on the 'username' column
    # merged_data.drop_duplicates(subset=['screen_name'], inplace=True,keep='last')
    # # write the merged and de-duplicated data to a new CSV file
    # merged_data.to_csv('./dataFinal.csv', index=False)
    prop = (nb_humain / nb) * 5
    # convert float to string
    prop_str = str(round(prop))
   
    return {'score':prop_str,'resultes':resultes}


