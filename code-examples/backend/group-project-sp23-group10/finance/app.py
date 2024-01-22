import os
import numpy as np
import requests
import random
import string
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import nasdaqdatalink
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Session(app)

db = SQLAlchemy(app)

class FinanceRelations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    symbol = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return {
            'id': self.id,
            'username': self.username,
            'symbol': self.symbol,
        }
    
def getUserRelations(username):
    try:
        allRows = FinanceRelations.query.filter_by(username=username).order_by(FinanceRelations.id.desc())
        return [row.symbol for row in allRows]
    except:
        return False

def addUserRelation(username, symbol):
    newRow = FinanceRelations(username=username, symbol=symbol)
    db.session.add(newRow)
    try:
        db.session.commit()
        return True
    except IntegrityError as e:
        db.session.rollback()
        return False

@app.route("/", methods=["GET"])
def index_get():
    if session.get("username"):
        symbols = getUserRelations(session.get("username"))
        if symbols == False:
            return render_template("home.html", username=session.get("username"), msg="(400) There was an issue with our database. Please try again later."), 400

        return render_template("home.html", username=session.get("username"), symbols=symbols), 200
    else:
        return redirect(os.environ.get("USER_APP"))

@app.route("/", methods=["POST"])
def index_post():    
    if session.get("username"):
        symbols = getUserRelations(session.get("username"))
        if symbols == False:
            return render_template("home.html", username=session.get("username"), msg="(400) There was an issue with our database. Please try again later."), 400
        
        symbol = request.form['symbol']
        try:
            newpath = r'./static'
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                
            data = nasdaqdatalink.get(symbol)

            data.plot()
            plt.title(symbol)
            plt.ylabel("price")
            plt.xlabel("date")
            plt.savefig('./static/my_plot.png')
        except:
            return render_template("home.html", username=session.get("username"), symbols=symbols, msg="(400) There was an issue with the NASDAQ API, or the symbol you inputted was invalid."), 400

        resp_code = 200
        if symbol not in symbols:    
            success = addUserRelation(session.get("username"), symbol)
            if not success:
                return render_template("home.html", username=session.get("username"), symbols=symbols, msg="(400) There was an issue with our database. Please try again later."), 400
            symbols = [symbol] + symbols
            resp_code = 201

        return render_template("home.html", username=session.get("username"), data=True, symbols=symbols), resp_code
    else:
        return redirect(os.environ.get("USER_APP"))

@app.route("/logout")
def redirect_logout():
    return redirect(os.environ.get("USER_APP") + "/logout")

@app.route("/home")
def redirect_home():
    return redirect(os.environ.get("USER_APP"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5051)