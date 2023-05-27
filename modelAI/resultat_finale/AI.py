
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
nlp = spacy.load('en_core_web_sm')
from nltk.stem import PorterStemmer
ps = PorterStemmer()

def porterstemmer(text):
  text = ' '.join(ps.stem(word) for word in text.split() if word in text)
  return text  

def lemmatization (text):
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)
def encode_text(text):
        # clean text from stop wods and punctuation
        text=TwitterPreprocessor(str(text)).fully_preprocess().text
        text=porterstemmer(text)
        text=lemmatization(text)
        text =[text]
        vectorizer = joblib.load('vectorizer.pkl')
        text = vectorizer.transform(text)
        text = torch.tensor(text.toarray())
        return text
def text_confirm(missions,response):
    if response.strip() == "":
        return {"score":0}
    # Expression régulière pour extraire les tags et les mentions
    pattern = r"([@#]\w+)"
    lien_pattern= re.compile(
            r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))'
            r'[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})')
    # Extraire les tags et les mentions de la réponse
    response_tags_mentions = set(re.findall(pattern, response))
    response_lien = set(re.findall(lien_pattern, response))
    # Extraire le texte de la réponse
    response_text = re.sub(pattern, "", response).strip()
    response_text = re.sub(lien_pattern, "", response_text).strip()
    # Initialiser le score de validation à 0
    validation_score = 0
    total=0
    # Vérifier chaque mission
    for mission in missions:
        # Extraire les tags et les mentions de la mission
        mission_tags_mentions = set(re.findall(pattern, mission))
        total+=len(mission_tags_mentions)
    
        mission_lien = set(re.findall(lien_pattern, mission))
        total+=len(mission_lien)
    
        # Vérifier si tous les tags et mentions de la mission sont présents dans la réponse
        validation_score +=len(mission_tags_mentions.intersection(response_tags_mentions))
        validation_score +=len(mission_lien.intersection(response_lien))
        mission_text = re.sub(pattern,"", mission).strip()
        mission_text = re.sub(lien_pattern,"", mission).strip()
        mission_vector = encode_text(mission_text)
        response_vector = encode_text(response_text)
        # Print the shapes
        
        mission_vector = mission_vector.float()
        response_vector = response_vector.float()
  
        # Calcul de la similarité cosinus
        similarity = np.dot(mission_vector, response_vector.T) / (np.linalg.norm(mission_vector) * np.linalg.norm( response_vector.T))
        total+=2
        if similarity > 0.7:
            # Ajouter un point si la similarité est suffisante
            validation_score += 1
    clf = joblib.load('postclf.pkl')
    predicted=clf.predict(response_vector)
    
    validation_score += 1 if predicted[0] == 1 else 0
    # Afficher le score de validation
    return {"score":round(validation_score *5 / total)}


# # load data
def tiktokrerun():
    data = pd.read_csv('./tiktokdataFinal.csv')
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
    existing_data = pd.read_csv('./tiktokdataFinal.csv')
    # append the new data to the existing data
    merged_data = pd.concat([existing_data, dp1], ignore_index=True)
    # drop the duplicates based on the 'username' column
    merged_data = merged_data[~merged_data['username'].duplicated(keep='last') | merged_data['username'].isnull()]
    # write the merged and de-duplicated data to a new CSV file
    merged_data.to_csv('./tiktokdataFinal.csv', index=False)
    return {"result":"bot" if predicted[0] == 1 else "human","score":str(round((1-predict_proba[0])*5))}

def twitterrerun():
    data = pd.read_csv('./twitterdataFinal.csv')
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
   
    existing_data = pd.read_csv('./twitterdataFinal.csv')
  
    merged_data = pd.concat([existing_data, dp1], ignore_index=True)
    # drop the duplicates based on the 'username' column
    merged_data.drop_duplicates(subset=['screen_name'], inplace=True,keep='last')
    # write the merged and de-duplicated data to a new CSV file
    merged_data.to_csv('./twitterdataFinal.csv', index=False)
    return {"result":"bot" if predicted[0] == 0 else "human","score":str(round(predict_proba[0]*5)),"chart":ac['chart']}

def changetwitterpredicte(name,type):
    # data = pd.read_csv('./featuresfloatvf.csv')
    # column_names = data.columns.tolist()
    try:
        accounts=pd.read_csv('./twitterdataFinal.csv')
        
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
            accounts.to_csv('./twitterdataFinal.csv', index=False)
            return {"message":"done please rerun"}            
    except Exception as e:
        abort(400, str(e))
        


def changetiktokpredicte(name,type):
    try:
        accounts=pd.read_csv('./tiktokdataFinal.csv')
        
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
            accounts.to_csv('./tiktokdataFinal.csv', index=False)
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


