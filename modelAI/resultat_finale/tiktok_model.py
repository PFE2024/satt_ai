
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



# # load data
def tiktokrerun():
    data = pd.read_csv('./TiktokAccount.csv')
    x=data.iloc[:, :-2]
    y = data.IsABot.values.tolist()
    smote = SMOTE(random_state=10)
    x, y =smote.fit_resample(x, y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42,stratify=y)
    clf=RandomForestClassifier()
    clf.fit(x_train,y_train)
    y_pred_train = clf.predict(x_train)
    y_pred_test = clf.predict(x_test)
    joblib.dump(clf, "tiktokclf.pkl")
    return {"message":"terminer","Training Accuracy score":metrics.accuracy_score(y_train, y_pred_train),
            "Testing Accuracy score":metrics.accuracy_score(y_test, y_pred_test)}


def tiktokcheckuser(tiktokProfile):
    account=tiktokget_inpute_data.get_details(tiktokProfile)
    if 'message' in account:
        abort(400, "can't get account details")
    dp=pd.DataFrame(account, index=[0])
    dp1=dp.drop('username',axis=1)
    try:
        clf=joblib.load("tiktokclf.pkl") 
    except:
        tiktokrerun()
    clf=joblib.load("tiktokclf.pkl")
    predicted=clf.predict(dp1)
    predict_proba=clf.predict_proba(dp1)[:,1]
    dp1['IsABot']=predicted
    dp1['username']=dp['username']
    existing_data = pd.read_csv('./TiktokAccount.csv')
    # append the new data to the existing data
    merged_data = pd.concat([existing_data, dp1], ignore_index=True)
    # drop the duplicates based on the 'username' column
    merged_data = merged_data[~merged_data['username'].duplicated(keep='last') | merged_data['username'].isnull()]
    # write the merged and de-duplicated data to a new CSV file
    merged_data.to_csv('./TiktokAccount.csv', index=False)
    return {"result":"bot" if predicted[0] == 1 else "human","score":str(round((1-predict_proba[0])*5))}


def changetiktokpredicte(name,type):
    try:
        accounts=pd.read_csv('./TiktokAccount.csv')
        
        accounts['username'] = accounts['username'].astype(str).str.lower()
        dp = accounts[accounts['username']==str.lower(name)]
        
        if dp.shape[0] == 0:
            abort(400, "accounts with that name does not exist")
      
        else :
            #  dp[0]['account_type']=type
            
            y=  "1.0" if type == "bot" else "0.0" if type == "human" else  Exception("erreur type must be bot or human")
            if isinstance(y, Exception):
                abort(400, "type must be bot or human")
            accounts.loc[accounts['username']==str.lower(name), 'IsABot'] =y
            accounts.to_csv('./TiktokAccount.csv', index=False)
            return {"message":"done please rerun"}            
    except Exception as e:
        abort(400, str(e))
        
    