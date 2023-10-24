# complete imports
from flask import Flask, request, Response, jsonify
import json

app = Flask(__name__)

# single route '/message' accepting POST method
@app.route("/message", methods = ["POST"])
def handleInput():
    # pull data from request body
    requestJSON = request.get_json()
    requestMessage = requestJSON["data"]["message"]
    # strip whitespace
    requestMessage = requestMessage.strip()

    # if message starts with "/"
    if requestMessage[0] == "/":
        # split into two parts based on first whitespace following "/"
        splitCommand = requestMessage.split(' ', 1)
        # assign first part less the "/" to the command variable
        command = splitCommand[0][1:]
        # assign the rest to the message variable
        message = splitCommand[1]
        return jsonify({
            "data": {"command": command, "message": message}
        })
    
    # if message does not start with "/"
    else:
        command = None
        message = requestMessage
        return jsonify({
           "data": {"command": command, "message": message }
        })



