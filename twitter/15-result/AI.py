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
from imblearn.over_sampling import SMOTE
# # load data
def rerun():
    data = pd.read_csv('./dataFinal.csv')
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
    joblib.dump(clf, "clf.pkl")
    return {"message":"terminer","Training Accuracy score":metrics.accuracy_score(y_train, y_pred_train),
            "Testing Accuracy score":metrics.accuracy_score(y_test, y_pred_test)}


def checkuser(name,access_key,access_secret):
    
  
    account=get_inpute_data.get_details(name,access_key,access_secret)
    # print(account)
    if 'message' in account:
        return account
    dp=pd.DataFrame(account, index=[0])
    dp1=dp.drop('screen_name',axis=1)
    try:
        clf=joblib.load("clf.pkl")
        
    except:
        rerun()
    clf=joblib.load("clf.pkl")
    predicted=clf.predict(dp1)
    predict_proba=clf.predict_proba(dp1)[:,1]
    dp1['screen_name']=dp['screen_name']
    dp1['account_type']=predicted
   
    existing_data = pd.read_csv('./dataFinal.csv')
  
    merged_data = pd.concat([existing_data, dp1], ignore_index=True)
    # drop the duplicates based on the 'username' column
    merged_data.drop_duplicates(subset=['screen_name'], inplace=True,keep='last')
    # write the merged and de-duplicated data to a new CSV file
    merged_data.to_csv('./dataFinal.csv', index=False)
    return {"result":"bot" if str(predicted[0]) == "0" else "human","bot proba":str(1-predict_proba[0])}



def checkfollowers(name,access_key,access_secret):
    
    account=get_inpute_data.get_followers_details(name,access_key,access_secret)
    # print(account)
    if 'message' in account:
        return account
    
    dp1=pd.DataFrame(account)
   
   
    try:
        clf=joblib.load("clf.pkl")
    except:
        rerun()
    clf=joblib.load("clf.pkl")
    resultes=[]
    resulte=[]
    nb_bot=0
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
        if  (user['account_type'] == 0.0).any():
                nb_bot+=1
        
        u={"screen_name":dp['screen_name'].iloc[0],"result":"bot" if str(predicted[0]) == "0" else "human","bot proba":str(round(1-predict_proba[0],2))}
        resultes.append(u)
        resulte.append(user)
    existing_data = pd.read_csv('./dataFinal.csv')
    resultes_df = pd.concat(resulte, axis=0, ignore_index=True)
    
    # append the new data to the existing data
    merged_data = pd.concat([existing_data, resultes_df], ignore_index=True)
    # drop the duplicates based on the 'username' column
    merged_data.drop_duplicates(subset=['screen_name'], inplace=True,keep='last')
    # write the merged and de-duplicated data to a new CSV file
    merged_data.to_csv('./dataFinal.csv', index=False)
    prop = (nb_bot / nb) * 100
    # convert float to string
    prop_str = str(prop)
   
    return {'proportion':prop_str,'resultes':resultes}





def checkfriends(name,access_key,access_secret):
    
    account=get_inpute_data.get_friends_details(name,access_key,access_secret)
    # print(account)
    if 'message' in account:
        return account
    
    dp1=pd.DataFrame(account)
   
   
    try:
        clf=joblib.load("clf.pkl")
    except:
        rerun()
    clf=joblib.load("clf.pkl")
    resultes=[]
    resulte=[]
    nb_bot=0
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
        if  (user['account_type'] == 0.0).any():
                nb_bot+=1
        
        u={"screen_name":dp['screen_name'].iloc[0],"result":"bot" if str(predicted[0]) == "0" else "human","bot proba":str(round(1-predict_proba[0],2))}
        resultes.append(u)
        resulte.append(user)
    existing_data = pd.read_csv('./dataFinal.csv')
    resultes_df = pd.concat(resulte, axis=0, ignore_index=True)
    
    # append the new data to the existing data
    merged_data = pd.concat([existing_data, resultes_df], ignore_index=True)
    # drop the duplicates based on the 'username' column
    merged_data.drop_duplicates(subset=['screen_name'], inplace=True,keep='last')
    # write the merged and de-duplicated data to a new CSV file
    merged_data.to_csv('./dataFinal.csv', index=False)
    prop = (nb_bot / nb) * 100
    # convert float to string
    prop_str = str(prop)
   
    return {'proportion':prop_str,'resultes':resultes}


def changepredicte(name,type):
    # data = pd.read_csv('./featuresfloatvf.csv')
    # column_names = data.columns.tolist()
    try:
        accounts=pd.read_csv('./dataFinal.csv')
        
        accounts['screen_name'] = accounts['screen_name'].astype(str).str.lower()
        dp = accounts[accounts['screen_name']==str.lower(name)]
        
        if dp.shape[0] == 0:
            return {"message": "accounts with that name does not exist"}
        else :
            #  dp[0]['account_type']=type
            
            y=  "0" if type == "bot" else 1 if type == "human" else  Exception("erreur type must be bot or human")
            if isinstance(y, Exception):
                raise y
            accounts.loc[accounts['screen_name']==str.lower(name), 'account_type'] =y
            accounts.to_csv('./dataFinal.csv', index=False)
            return {"message":"done please rerun"}            
    except Exception as e:
        return {"message": "error","error":str(e)}

