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
from imblearn.over_sampling import SMOTE
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
def rerun():
    data = pd.read_csv('./dataFinal.csv')
    x=data.iloc[:, :-2]
    y = data.IsABot.values.tolist()
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


def checkuser(tiktokProfile):
    
    account=get_inpute_data.get_details(tiktokProfile)
    if 'message' in account:
        return account
    dp=pd.DataFrame(account, index=[0])
    dp1=dp.drop('username',axis=1)
    try:
        clf=joblib.load("clf.pkl") 
    except:
        rerun()
    clf=joblib.load("clf.pkl")
    predicted=clf.predict(dp1)
    predict_proba=clf.predict_proba(dp1)[:,1]
    dp1['IsABot']=predicted
    dp1['username']=dp['username']
    existing_data = pd.read_csv('./dataFinal.csv')
    # append the new data to the existing data
    merged_data = pd.concat([existing_data, dp1], ignore_index=True)
    # drop the duplicates based on the 'username' column
    merged_data = merged_data[~merged_data['username'].duplicated(keep='last') | merged_data['username'].isnull()]
    
    # write the merged and de-duplicated data to a new CSV file
    merged_data.to_csv('./dataFinal.csv', index=False)
    return {"result":"bot" if str(predicted[0]) == "1" else "human","bot proba":str(predict_proba[0])}


def changepredicte(name,type):
    try:
        accounts=pd.read_csv('./dataFinal.csv')
        
        accounts['username'] = accounts['username'].astype(str).str.lower()
        dp = accounts[accounts['username']==str.lower(name)]
        
        if dp.shape[0] == 0:
            return {"message": "accounts with that name does not exist"}
        else :
            #  dp[0]['account_type']=type
            
            y=  "1" if type == "bot" else 0 if type == "human" else  Exception("erreur type must be bot or human")
            if isinstance(y, Exception):
                raise y
            accounts.loc[accounts['username']==str.lower(name), 'IsABot'] =y
            accounts.to_csv('./dataFinal.csv', index=False)
            return {"message":"done please rerun"}            
    except Exception as e:
        return {"message": "error","error":str(e)}
