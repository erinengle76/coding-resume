import os
import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Session(app)

def makeAPICall(country, key):
    url = ('https://newsapi.org/v2/top-headlines?'
        f'country={country}&'
        f'apiKey={key}')
    response = requests.get(url)
    jformat = response.json()
    del jformat['status']
    del jformat['totalResults']
    new_dict = jformat['articles']
    data = ""
    for i in range(0,len(new_dict)):
        data += "<td>" + f" Article {str(i+1)}" + "</td>"
        data += "<td>" + new_dict[i]['title'] + "</td>"
        data += "<td><a href=\""+ new_dict[i]['url'] + "\" target=\"_blank\"> CLICK HERE TO READ</a></td>"
        data += "<tr>"
    data = "<tr><th>Article Number</th><th>Article Title</th><th>Article URL</th><tr>" + data
    data = "<table border=1>" + data + "</tr></table>"
    return data

@app.route("/", methods=["GET"])
def index_get():
    if session.get("username"):
        return render_template("home.html", username=session.get("username")), 200
    else:
        return redirect(os.environ.get("USER_APP"))

@app.route("/", methods=["POST"])
def index_post():    
    if session.get("username"):
        country = request.form['country'].lower()
        key = os.environ.get("NEWS_API_KEY")
        try:
            newpath = r'./static'
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            data = makeAPICall(country,key)
            with open("./static/file.html", "w") as file:
                file.write(data)
            return render_template("home.html", username=session.get("username"), data=True, country=country), 200  
        except:
            return render_template("home.html", username=session.get("username"), msg="There was an issue with the NEWS API. Either the API failed to respond or the country you entered does not exist"), 400
    else:
        return redirect(os.environ.get("USER_APP"))

@app.route("/logout")
def redirect_logout():
    return redirect(os.environ.get("USER_APP") + "/logout")
    
@app.route("/home")
def redirect_home():
    return redirect(os.environ.get("USER_APP"))
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5053)