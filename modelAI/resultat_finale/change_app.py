from flask import Flask, abort, jsonify, request
from flask_cors import CORS
import  twitter_model
import  tiktok_model
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
@app.errorhandler(400)
def handle_bad_request(error):
    # Get the custom error message from the error object
    message = str(error)
    
    response = jsonify({'error': message})
    response.status_code = 400
    return response

@app.route('/change', methods=['POST'])
def update():
    try:
        request_data=request.json
        username = request_data['username']
        type = request_data['type']
        if request_data['oracle']==6:
            return json.dumps(tiktok_model.changetiktokpredicte(username,type), indent = 4)  
        elif request_data['oracle']==4:
            return json.dumps(twitter_model.changetwitterpredicte(username,type), indent = 4) 
        else:
             abort(400, "this model work only with tiktok and twitter")
    except Exception as e:
        abort(400, str(e))
if __name__ == "__main__":
    app.run(debug=False)