import os
import numpy as np
import requests
import random
import string
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Session(app)

db = SQLAlchemy(app)

class Users(db.Model):
    username = db.Column(db.String(200), primary_key=True)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    verified = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return {
            'username': self.username,
            'password_hash': self.password,
            'email': self.email,
            'verified': self.verified
        }
    
    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

def getUser(username):
    try:
        user = Users.query.filter_by(username=username).first()
        return user
    except: 
        return "error"

def readUsers():
    try:
        allRows = Users.query.all()
        quoteMap = dict()
        for row in allRows:
            quoteMap[row.username] = row
        return quoteMap    
    except:
        return "error"

def writeUser(username, password, email, code):
    newRow = Users(username=username, email=email, verified=code)
    newRow.hash_password(password)
    db.session.add(newRow)
    try:
        db.session.commit()
        return True
    except IntegrityError as e:
        db.session.rollback()
        return False

@app.route("/", methods=["GET"])
def index():
    if not session.get("username"):
        return render_template("home.html"), 200
    return render_template("home.html", username=session.get("username")), 200

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

@app.route("/finance")
def redirect_finance():
    return redirect(os.environ.get("FINANCE_APP"))

@app.route("/pokemon")
def redirect_pokemon():
    return redirect(os.environ.get("POKEMON_APP"))

@app.route("/news")
def redirect_news():
    return redirect(os.environ.get("NEWS_APP"))

@app.route("/streetview")
def redirect_streetview():
    return redirect(os.environ.get("STREETVIEW_APP"))

@app.route("/weather")
def redirect_weather():
    return redirect(os.environ.get("WEATHER_APP"))

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html"), 200

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form['username']
    password = request.form['password']

    user = getUser(username)
    if user == "error":
        return render_template("login.html", msg="(400) There was an internal problem with our database. Please try again later."), 400
    elif not user:
        return render_template("login.html", msg="(401) No account with that username exists."), 401
    elif user.verified:
        return render_template("login.html", msg="(401) You need to verify this account before proceeding. Click the link in your email."), 401
    else:
        if not user.verify_password(password):
            return render_template("login.html", msg="(401) Invalid username and/or password."), 401
        else:
            session['username'] = username
            return redirect(url_for('index'))

@app.route("/register", methods=["GET"])
def register_get():
    return render_template("register.html"), 200

@app.route("/register", methods=["POST"])
def register_post():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    user = getUser(username)
    if user == "error":
        return render_template("register.html", msg="(400) There was an internal problem with our database. Please try again later."), 400
    elif user:
        return render_template("register.html", msg="(400) The provided username is already in use."), 400 
    else:
        code = np.random.randint(low=100000, high=1000000)
        
        success = writeUser(username, password, email, code)
        if not success:
            return render_template("register.html", msg="(400) There was an internal problem with our database. Please try again later."), 400
        else:        
            url = request.base_url + f"/accountVerify/{code}"
            
            try:
                message = Mail(
                    from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
                    to_emails=email,
                    subject="Verify Account",
                    html_content=f"Click the following link to verify your account: {url}"
                )
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
            except Exception as e:
                return render_template("register.html", msg="(400) There was a problem with sending the account verification email."), 400
            
            return render_template("register.html", successSent=True), 201

def verifyAccount(code):
    try:
        allRows = Users.query.all()
        for row in allRows:
            print(row.verified)
            if int(code) == int(row.verified):
                row.verified = 0
                try:
                    db.session.commit()
                    return True
                except IntegrityError as e:
                    db.session.rollback()
                    return "error"
        return False  
    except:
        return "error"

@app.route("/register/accountVerify/<code>", methods=["GET"])
def accountVerify(code):
    resp = verifyAccount(code)
    if resp == "error":
        return render_template("register.html", msg="(400) There was an internal problem with our database. Please try again later."), 400
    else:
        if resp:
            return render_template("register.html", successVerified=True), 200
        else:
            return render_template("register.html", msg="(400) Invalid verification code."), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)