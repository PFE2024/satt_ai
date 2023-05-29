
from flask import Flask, abort, jsonify, request
import  twitter_model
import tiktok_model
import json

app = Flask(__name__)

@app.errorhandler(400)
def handle_bad_request(error):
    # Get the custom error message from the error object
    message = str(error)
    
    response = jsonify({'error': message})
    response.status_code = 400
    return response

@app.route('/checkuser', methods=[ 'POST'])
def checkuser():
    try:
        request_data = request.json
        
        # If a form is submitted
        if request_data['oracle']==6:
            try:
                username= request_data['username']
                refresh= request_data['refreshToken']
            except Exception as e:
                abort(400, "username or tokens indisponible")
            prediction=tiktok_model.tiktokcheckuser(request_data)
            json_object = json.dumps(prediction, indent = 4) 
            return json_object
        elif request_data['oracle']==4:
            try:
                username = request_data['username']
                access_token_key= request_data['access_token_key']
                access_token_secret= request_data['access_token_secret']
            except Exception as e:
                abort(400, "username or tokens indisponible")
                
            prediction=twitter_model.twittercheckuser(username,access_token_key,access_token_secret)
            json_object = json.dumps(prediction, indent = 4) 
            return json_object
        else:
             abort(400, "this model work only with tiktok and twitter")

    except Exception as e:
        abort(400, str(e))
    

@app.route('/', methods=['GET'])
def main():
    return 'welcome'


@app.route('/rerun', methods=['POST'])
def rerun():
    request_data = request.json 
    # If a form is submitted
    if request_data['oracle']==6:
        json_object = json.dumps(tiktok_model.tiktokrerun(), indent = 4) 
    elif request_data['oracle']==4:
        json_object = json.dumps(twitter_model.twitterrerun(), indent = 4) 
    else:
             abort(400, "this model work only with tiktok and twitter")
    return json_object

# def create_app():
#    return app

if __name__ == "__main__":
    app.run(debug=False)