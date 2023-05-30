
from flask import Flask, request

import  AI

import json

app1 = Flask(__name__)

@app1.route('/checkfollowers', methods=[ 'POST'])
def checkfollowers():
    request_data = request.data
    request_data = json.loads(request_data.decode('utf-8')) 

    # If a form is submitted
    if request.method == "POST" and  request_data['oracle']==4:
       
        username = request_data['username']
        access_token_key= request_data['access_token_key']
        access_token_secret= request_data['access_token_secret']
        prediction=AI.checkfollowers(username,access_token_key,access_token_secret)
        response = json.dumps(prediction, indent = 4)
        return response
    else:
        prediction = "not yet created"
    return prediction
@app1.route('/checkfriends', methods=[ 'POST'])
def checkfriends():
    # If a form is submitted
    request_data = request.data
    request_data = json.loads(request_data.decode('utf-8')) 
    if request.method == "POST" and  request_data['oracle']==4:
        
        username = request_data['username']
        access_token_key= request_data['access_token_key']
        access_token_secret= request_data['access_token_secret']
        prediction=AI.checkfriends(username,access_token_key,access_token_secret)
        response = json.dumps(prediction, indent = 4)
        return response
    else:
        prediction = "not yet created"
    return prediction
   
   

# def create_app():
#    return app

if __name__ == "__main__":
    app1.run(debug=False)