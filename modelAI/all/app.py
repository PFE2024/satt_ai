
from flask import Flask, request,jsonify
import joblib
import  AI
import numpy as np 
import pandas as pd 
import json

app = Flask(__name__)


@app.route('/checkuser', methods=[ 'POST'])
def checkuser():
    request_data = request.json
    
    # If a form is submitted
    if request_data['oracle']==1:
        prediction=AI.tiktokcheckuser(request_data)
        json_object = json.dumps(prediction, indent = 4) 
        return json_object
    elif request_data['oracle']==0:
        username = request_data['username']
        access_token_key= request_data['access_token_key']
        access_token_secret= request_data['access_token_secret']
        prediction=AI.twittercheckuser(username,access_token_key,access_token_secret)
        json_object = json.dumps(prediction, indent = 4) 
        return json_object
    

@app.route('/', methods=['GET'])
def main():
    return 'welcome'


@app.route('/rerun', methods=['POST'])
def rerun():

    request_data = request.json 
    # If a form is submitted
    if request_data['oracle']==1:
        json_object = json.dumps(AI.tiktokrerun(), indent = 4) 
    elif request_data['oracle']==0:
        json_object = json.dumps(AI.twitterrerun(), indent = 4) 
    return json_object
@app.route('/change', methods=['POST'])
def update():
    request_data=request.json
    username = request_data['username']
    type = request_data['type']
    if request_data['oracle']==1:
        return json.dumps(AI.changetiktokpredicte(username,type), indent = 4)  
    elif request_data['oracle']==0:
        return json.dumps(AI.changetwitterpredicte(username,type), indent = 4) 
# def create_app():
#    return app

if __name__ == "__main__":
    app.run(debug=False)