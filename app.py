from flask import Flask, render_template, url_for,redirect
import requests
from flask import request as req
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
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
        error_message =''
        output = ''
        
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        
        data = req.form['data']
        if len(data.split(' ')) < 50:
            error_message ="Sorry! We accept at least 50 words for the summarization."
        else:
            maxL = int(req.form['maxL'])
            minL =  maxL 
            payload = {
                "inputs":data ,
                "parameters":{
                    "max_length": maxL,
                    "min_length": minL
                }
            }
            output = query(payload)[0].get('summary_text')

        return render_template('index.html', result = output,error = error_message)
    else:
        return redirect(url_for('home'))




if __name__=="__main__":
    app.run()
    