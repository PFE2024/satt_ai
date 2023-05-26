
from flask import Flask, abort, jsonify, request
import  AI
import json

from clean_input_data import get_twitter_poste
from clean_input_data import get_tiktok_poste


app = Flask(__name__)



@app.errorhandler(400)
def handle_bad_request(error):
    # Get the custom error message from the error object
    message = str(error)
    
    response = jsonify({'error': message})
    response.status_code = 400
    return response

@app.route('/check_all', methods=[ 'POST'])
def checkuser():
    try:
        request_data = request.json
        if request_data['oracle']==6:
            try:
                id_Post = request_data['id_Post']
                missions =request_data['missions']
                refresh= request_data['refreshToken']
            except Exception as e:
                abort(400, "id poste or messions dosen't exist")
                
            prediction=AI.tiktokcheckuser(request_data)
            s1=prediction["score"]
            text=get_tiktok_poste(id_Post,refresh)
            prediction=AI.text_confirm(missions,text)
            s2=prediction["score"]
            x={"human_score":s1,"text_confirm_score":s2,"score_finale":(s1+s2)/2}
            json_object = json.dumps(prediction, indent = 4) 
            return json_object
        elif request_data['oracle']==4: 
            try:
                username = request_data['username']
                id_Post = request_data['id_Post']
                missions =request_data['missions']
                access_token_key= request_data['access_token_key']
                access_token_secret= request_data['access_token_secret']
            except Exception as e:
                abort(400,'username or tokens indisponible')
            prediction=AI.twittercheckuser(username,access_token_key,access_token_secret)
            s1=prediction["score"]
            chart=prediction["chart"]
            text=get_twitter_poste(id_Post, access_token_key, access_token_secret)
            prediction=AI.text_confirm(missions,text)
            s2=prediction["score"]
            x={"human_score":str(s1),"text_confirm_score":str(s2),"chart":chart,"score_finale":str((int(s1)+int(s2))/2)}
            json_object = json.dumps(x, indent = 4) 
            return json_object
        else:
             abort(400, "this model work only with tiktok and twitter")
    except Exception as e:
        abort(400, str(e))
    
if __name__ == "__main__":
    app.run(debug=False)