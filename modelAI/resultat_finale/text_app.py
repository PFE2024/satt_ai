
from flask import Flask, abort, jsonify, request

import json

from flask_cors import CORS

from get_input_data import get_twitter_poste , get_tiktok_poste

from text_model import text_confirm

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.errorhandler(400)
def handle_bad_request(error):
    # Get the custom error message from the error object
    message = str(error)
    
    response = jsonify({'error': message})
    response.status_code = 400
    return response
@app.route('/checktext', methods=[ 'POST'])
def checktext():
    try:
        request_data = request.json
        # If a form is submitted
        if request_data['oracle']==4:
            try:
                id_Post = request_data['id_Post']
                missions =request_data['missions']
                access_token_key= request_data['access_token_key']
                access_token_secret= request_data['access_token_secret']
            except Exception as e:
                return {"message":'request data  indisponible'}
            text=get_twitter_poste(id_Post, access_token_key, access_token_secret)
            prediction=text_confirm(missions,text)
            json_object = json.dumps(prediction, indent = 4) 
            return json_object
        elif request_data['oracle']==6:
            try:
                id_Post = request_data['id_Post']
                missions =request_data['missions']
                refresh= request_data['refreshToken']
            except Exception as e:
                return {"message":'request data  indisponible'}
            text=get_tiktok_poste(id_Post,refresh)
            prediction=text_confirm(missions,text)
            json_object = json.dumps(prediction, indent = 4) 
            return json_object
        else:
             abort(400, "this model work only with tiktok and twitter")
    except Exception as e:
        abort(400, str(e))
    

@app.route('/', methods=['GET'])
def main():
    return 'welcome'


if __name__ == "__main__":
    app.run(debug=False)