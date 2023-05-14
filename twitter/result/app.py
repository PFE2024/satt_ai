
from flask import Flask, request
import joblib
import  AI
import numpy as np 
import pandas as pd 
import json

app = Flask(__name__)


@app.route('/predicte', methods=['GET', 'POST'])
def predicte():
    # If a form is submitted
    if request.method == "POST":
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8')) 
        username = request_data['username']
        access_token_key= request_data['access_token_key']
        access_token_secret= request_data['access_token_secret']
        prediction=AI.predicte(username,access_token_key,access_token_secret)
        json_object = json.dumps(prediction, indent = 4) 
        return json_object
    else:
        prediction = ""
    return prediction
@app.route('/', methods=['GET'])
def main():
    return 'welcome'
@app.route('/accounts', methods=['GET'])
def accounts():
    accounts=pd.read_csv('./accounts.csv')
    accounts = accounts.to_json(orient='records')
    return accounts
@app.route('/run', methods=['GET'])
def run():
    json_object = json.dumps(AI.rerun(), indent = 4) 
    return json_object

@app.route('/rerun', methods=['GET'])
def rerun():
    json_object = json.dumps(AI.rerun(), indent = 4) 
    return json_object
@app.route('/change', methods=['POST'])
def update():
    request_data=request.json
    username = request_data['username']
    type = request_data['type']
    return json.dumps(AI.changepredicte(username,type), indent = 4)  
def create_app():
   return app

