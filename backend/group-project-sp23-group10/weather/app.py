import os
import random
import requests
from flask import Flask, render_template, request, session, redirect
from dotenv import load_dotenv
from flask_session import Session

load_dotenv()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Session(app)

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(zipcode, countrycode):
    # use zipcode, countrycode and api key in api call to get latitude and longitude coordinates
    url = "http://api.openweathermap.org/geo/1.0/zip?zip=" + zipcode + "," + countrycode + "&appid=" + API_KEY
    lat_lon_response = requests.get(url)
    lat_lon_response = lat_lon_response.json()
    lat = str(lat_lon_response["lat"])
    lon = str(lat_lon_response["lon"])

    # user lat and lon coordinates in api call to get weather data
    final_url = "https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lon + "&appid=" + API_KEY + "&units=imperial"
    weather_data = requests.get(final_url)
    weather_data = weather_data.json()
    current_temp = weather_data["main"]["temp"] # get current temp
    city = weather_data["name"] # get city of zipcode

    return current_temp

@app.route("/", methods=["GET"])
def index_get():
    if session.get("username"):
        return render_template("home.html", username=session.get("username")), 200
    else:
        return redirect(os.environ.get("USER_APP"))

@app.route("/", methods=["POST"])
def index_post():
    if session.get("username"):
        zipcode = request.form["zipcode"]
        countrycode = request.form["countrycode"].upper()
        try:
            current_temp = get_weather(zipcode, countrycode)
            output = "Current temperature for " + str(zipcode) + ": " + str(current_temp) + " °F"
            resp_code = 200
        except:
            output = "Please make sure you have entered a valid zipcode and countrycode"
            resp_code = 400
        return render_template("home.html", username=session.get("username"), output=output), resp_code
    else:
        return redirect(os.environ.get("USER_APP"))

@app.route("/logout")
def redirect_logout():
    return redirect(os.environ.get("USER_APP") + "/logout")

@app.route("/home")
def redirect_home():
    return redirect(os.environ.get("USER_APP"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055, debug=True)
