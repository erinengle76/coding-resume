import os
import random
import requests
from flask import Flask, render_template, request, session, redirect, make_response
from dotenv import load_dotenv
from flask_session import Session

load_dotenv()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Session(app)

API_KEY = os.getenv("STREETVIEW_API_KEY")

def geocode_location(location):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": location, "key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            return data["results"][0]["geometry"]["location"]
    return None

def download_images(location):
    url = "https://maps.googleapis.com/maps/api/streetview"
    images = []
    geocoded_location = geocode_location(location)
    if geocoded_location:
        lat, lng = geocoded_location["lat"], geocoded_location["lng"]
        for _ in range(20):  # Download 20 random images
            random_lat = lat + random.uniform(-0.005, 0.005)
            random_lng = lng + random.uniform(-0.005, 0.005)
            params = {
                "size": "600x300",
                "location": f"{random_lat},{random_lng}",
                "key": API_KEY,
                "fov": 120,
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                images.append(response.url)
    return images

@app.route("/", methods=["GET"])
def index_get():
    if session.get("username"):
        return render_template("home.html", username=session.get("username")), 200
    else:
        return redirect(os.environ.get("USER_APP"))

@app.route("/", methods=["POST"])
def index_post():
    if session.get("username"):
        location = request.form["location"]
        if not location:  # Check if the location input is empty
            return render_template("home.html", username=session.get("username"), error="Please enter a valid location."), 400

        images = download_images(location)
        if not images:  # Check if no images were downloaded
            return render_template("home.html", username=session.get("username"), error="Unable to download images for the specified location."), 400
        else:
            return render_template("home.html", username=session.get("username"), images=images), 200
    else:
        return redirect(os.environ.get("USER_APP"))

@app.route("/logout")
def redirect_logout():
    return redirect(os.environ.get("USER_APP") + "/logout")

@app.route("/home")
def redirect_home():
    return redirect(os.environ.get("USER_APP"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5054, debug=True)
