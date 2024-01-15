import os
import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Session(app)

@app.route("/", methods=["GET"])
def index_get():
    if session.get("username"):
        return render_template("home.html", username=session.get("username")), 200
    else:
        return redirect(os.environ.get("USER_APP"))

@app.route("/", methods=["POST"])
def index_post():    
    if session.get("username"):
        pokemon = request.form['pokemon'].lower()
        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
            data = response.json()
            poke = []
            for i in data['sprites']:
                if type(data['sprites'][i]) == str:
                    poke.append(data['sprites'][i])

            description  = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}").json()
            poke_description = description['flavor_text_entries'][0]['flavor_text'].replace('\n', " ")
            poke.append(poke_description)
        except:
            return render_template("home.html", username=session.get("username"), msg="There was an issue with the POKEMON API."), 400

        return render_template("home.html", username=session.get("username"), data=True, poke=poke), 200
    else:
        return redirect(os.environ.get("USER_APP"))

@app.route("/logout")
def redirect_logout():
    return redirect(os.environ.get("USER_APP") + "/logout")

@app.route("/home")
def redirect_home():
    return redirect(os.environ.get("USER_APP"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5052)