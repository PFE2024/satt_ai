
from flask import Flask, request,jsonify
import joblib
import  AI
import numpy as np 
import pandas as pd 
import json

app = Flask(__name__)


@app.route('/checkuser', methods=['GET', 'POST'])
def checkuser():
    # If a form is submitted
    if request.method == "POST":
        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8')) 
        prediction=AI.checkuser(request_data)
        json_object = json.dumps(prediction, indent = 4) 
        return json_object
    else:
        prediction = ""
    return prediction




@app.route('/', methods=['GET'])
def main():
    return 'welcome'


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

