import os
from flask import Flask, render_template, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'super secret key'
Session(app)

@app.route("/")
def index():
    session.clear()
    session["Admin"] = 1
    session["user_id"] = 1
    return render_template("index.html")

@app.route("/billGen")
def billGen():
    return render_template("billGen.html")