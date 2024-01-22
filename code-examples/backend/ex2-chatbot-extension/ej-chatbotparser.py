# complete imports
from flask import Flask, request, Response, jsonify
import json
import argparse
from urllib.parse import urljoin
import requests

app = Flask(__name__)

# Helper function to pull the file map from "serverMapping.json"
def getDataFromFile():
    file = open("serverMapping.json")
    commandDict = json.load(file)
    file.close()
    return commandDict
    

# Helper function to update serverMapping.json when a new server/route pair is added
def updateFile(updatedCommandMap):
    with open("serverMapping.json", "w") as f:
        json.dump(updatedCommandMap, f)
        f.close()
    return True

# Helper function that pings separate server, returns request data
def pingOtherServer(full_url,raw_data):
    try:
        r = requests.post(full_url, json=raw_data)
        r.raise_for_status()
        data = r.json()
        return data["data"]
    except requests.exceptions.ConnectionError as err:
        # eg, no internet
        raise SystemExit(err)
    except requests.exceptions.HTTPError as err:
        # eg, url, server and other errors
        raise SystemExit(err)

# Helper function to return data in json format    
def returnMessage(command,message):
    return jsonify({
        "data": {"command": command, "message": message}
    })

# '/message' route - accepts POST call with message and command from terminal chatbot in json format
@app.route("/message", methods = ["POST"])
def handleInput():
    try:
        # pull data from request body
        requestJSON = request.get_json()
        # parse message
        requestMessage = requestJSON["data"]["message"]
        requestMessage = requestMessage.strip()
        # ensure message is not empty
        if len(requestMessage) != 0:
        # collect command after '/'
            if requestMessage[0] == "/":
                splitCommand = requestMessage.split(' ', 1)
                command = splitCommand[0][1:]
                try:
                    message = splitCommand[1]
                    try:
                        commandMap = getDataFromFile()
                        # test to see if command exists in command map file
                        try:
                            # create route for command
                            server_url = commandMap[command]
                            full_url = urljoin(server_url, "/execute")
                            # create request body
                            raw_data = {}
                            raw_data["data"] = {"command": command, "message": message}
                            # send command to appropriate server if available
                            serverData = pingOtherServer(full_url,raw_data)
                            return returnMessage(serverData["command"], serverData["message"])
                        # if doesn't exist, return message as is (original a1 functionality)
                        except KeyError:
                            return returnMessage(command, message)
                    except FileNotFoundError:
                        return returnMessage(command, message)
                except IndexError:
                    return returnMessage(command,"Message cannot be blank"), 404
            # if message does not start with "/"
            else:
                command = None
                message = requestMessage
                return returnMessage(command,message)
        # response if message is empty
        else:
            return returnMessage(None, "Message cannot be empty"), 404
    # if improper input is sent by the client
    except KeyError:
        return returnMessage(None,"Request is missing a valid message or command"), 404

# 'register' route - accepts POST call with json 
@app.route("/register", methods = ["POST"])
def registerInput():
    try:
        # pulls data from request
        requestJSON = request.get_json()
        command = requestJSON["data"]["command"]
        associatedServer = requestJSON["data"]["server_url"]
        # ensure command is not empty
        if len(command) != 0:
            # ensure route is not empty
            if len(associatedServer) != 0:
                existingRoutes = getDataFromFile()
                try:
                    # See if file contains command already
                    originalServer = existingRoutes[command]
                    # Update route with data if command exists
                    existingRoutes[command] = associatedServer
                    updateFile(existingRoutes)
                    return returnMessage(command, f"The command sent already exists in the dictionary. The associated server address has been updated from {originalServer} to {associatedServer}"), 200
                # If command does not exist, add to file as new command/route pair
                except KeyError:
                    existingRoutes[command] = associatedServer
                    updateFile(existingRoutes)
                    return returnMessage(command, "saved"), 201
            else:
                return "Associated server cannot be empty", 404
        else:
            return "Command cannot be empty", 404
    except KeyError:
        return "The input provided was missing valid input for the data, command, or server_url fields. Please update your input and try again.", 404


