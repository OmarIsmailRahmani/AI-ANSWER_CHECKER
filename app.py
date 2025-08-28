from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# MongoDb connection 

client = MongoClient("mongodb://localhost:27017/")
db = client["EvaluatorDB"]

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/dashboard')
def dashbaord():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
    