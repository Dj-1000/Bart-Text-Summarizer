from flask import Flask, render_template, url_for,redirect
import requests
from flask import request as req
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask('__name__')
app.debug = True


@app.route('/',methods = ["GET","POST"])
def home():
    return render_template('index.html',name='home')





@app.route('/summarize',methods = ["GET","POST"])
def summarize(name = 'Summarize'):
    if req.method=="POST":
        token = os.getenv('API_TOKEN')
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer {token}"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        data = req.form['data']
        maxL = int(req.form['maxL'])
        minL =  maxL 
        print("MINL :",minL)
        print("Input data :",data,maxL,minL)
        # sentence = clean_text(sentence)	
        print("HI")
        payload = {
            "inputs":data ,
            "parameters":{
                "max_length": maxL,
                "min_length": minL
            }
        }
        output = query(payload)[0].get('summary_text')
        print("OUTPUT :",output)
        return render_template('index.html', result = output)
    else:
        return redirect(url_for('home'))




if __name__=="__main__":
    app.run()
    