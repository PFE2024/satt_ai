
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
