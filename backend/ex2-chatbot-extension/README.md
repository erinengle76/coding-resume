Note the requests library is used in both files and must be installed prior to running the files + serverMapping.json must exist in the same directory as the servers when they are being run on Flask.

jones_erin_a2_chatbotparser.py is the main server that functions in tandem with terminal_chatbot.py. This server contains several helper functions and two routes

"/message"
This endpoint accepts POST methods and expects a JSON input containing {"data":{"command": "insert command", "message": "appropriate message from chatbot"}}
If any of the data is missing, a 404 error will be thrown
If message and command exist, the server will parse the command (signified by /command in the chatbot) and the message
The command will be checked against local file "serverMapping.json"
If the command exists in the server mapping JSON, the associated server URL address will be pulled from the file; a request is then sent with the message and command in JSON format to the appropriate server address to handle the request and pass back required data
If the command does not exist in the server mapping JSON, the message and command are returned in JSON format, displaying only the message in the terminal
If no command exists, only a message, solely the message will be returned with command set to None (displaying only the message in the terminal)

"/register"
This enpoint accepts POST methods and expects JSON input containing {"data"{"command":"given command", "server_url":"given url"}}
If command or server are empty, a 404 error is returned
Otherwise the command is checked against the local file serverMapping.json
If the command exists, the URL is updated with the URL given in the request body and the file is saved
If the command does not exist, command/URL pair are added to the server map and the file is updated
jones_erin_a2_shrugserver.py is the server associated with handling messages sent with the /shrug command to the chatbot. This server contains a single route as follows

"/execute"
This route accepts a "POST" method and expects {"data":{"command": "insert command", "message": "appropriate message from chatbot"}}
If any data is missing from the request, a 404 error is thrown
If the command is not equal to shrug, a 400 error is thrown
If the message is not empty, the server concatenates existing message with "¯_(ツ)_/¯" and returns in JSON format
If the message is empty, a 404 error is thrown with error message