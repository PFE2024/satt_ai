
from flask import Flask, abort, jsonify, request

import  AI

import json

app1 = Flask(__name__)

@app1.errorhandler(400)
def handle_bad_request(error):
    # Get the custom error message from the error object
    message = str(error)
    
    response = jsonify({'error': message})
    response.status_code = 400
    return response
@app1.route('/checkfollowers', methods=[ 'POST'])
def checkfollowers():
    try:
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
             abort(400, "this model work only with  twitter")
    except Exception as e:
        return str(e)
@app1.route('/checkfriends', methods=[ 'POST'])
def checkfriends():
    try:
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
             abort(400, "this model work only with  twitter")
    except Exception as e:
        abort(400, str(e))
   
   

# def create_app():
#    return app

if __name__ == "__main__":
    app1.run(debug=False)