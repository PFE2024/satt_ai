# %%
from flask import Flask, request
import joblib
import  AI
import numpy as np 
import pandas as pd 
app = Flask(__name__)

from waitress import serve
@app.route('/', methods=['GET', 'POST'])
def main():
    # If a form is submitted
    if request.method == "POST":
        # Unpickle classifier
        clf = joblib.load("clf.pkl")
        # Get values through input bars
        height = request.form.get("height")
        weight = request.form.get("weight") 
        # Put inputs to dataframe
        X = pd.DataFrame([[height, weight]], columns = ["Height", "Weight"])
        # Get prediction
        prediction = clf.predict(X)[0]
    else:
        prediction = ""
    return prediction

@app.route('/', methods=['GET', 'POST'])
def update():
    AI.fun()

if __name__ == "__main__":
    
    serve(app, host="0.0.0.0", port=8080)


