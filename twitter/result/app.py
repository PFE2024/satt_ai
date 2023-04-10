
from flask import Flask, request
import joblib
import  AI
import numpy as np 
import pandas as pd 
import json
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)

@app.route('/ai/predicte', methods=['GET', 'POST'])
def predicte():
    # If a form is submitted //  headers = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Credentials': 'true'}
    
    if request.method == "POST":
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8')) 
        nom = request_data['nom']
        access_key= request_data['access_key']
        access_secret= request_data['access_secret']
        prediction=AI.predicte(nom,access_key,access_secret)
        json_object = json.dumps(prediction, indent = 4) 
        return json_object
    else:
        prediction = ""
    return prediction
@app.route('/ai', methods=['GET'])
def main():
    return 'welcome'
@app.route('/ai/accounts', methods=['GET'])
def accounts():
    accounts=pd.read_csv('./accounts.csv')
    accounts = accounts.to_json(orient='records')
    return accounts
@app.route('/ai/run', methods=['GET'])
def run():
    json_object = json.dumps(AI.run(), indent = 4) 
    return json_object

@app.route('/ai/rerun', methods=['GET'])
def rerun():
    json_object = json.dumps(AI.rerun(), indent = 4) 
    return json_object
@app.route('/ai/change', methods=['POST'])
def update():
    request_data=request.json
    nom = request_data['nom']
    type = request_data['type']
    return json.dumps(AI.changepredicte(nom,type), indent = 4)  
def create_app():
   return app
