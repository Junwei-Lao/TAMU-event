from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow React frontend to talk to Flask

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = ""

    if data and ("messages" in data) and (len(data["messages"]) > 0):
        user_message = data["messages"][-1].get("text", "")
        if (user_message[0] == "/"):
            command = user_message[1:]
            match command:
                case "commands":
                    bot_reply = "Here are the valid commands: \n* **/commands**: List valid commands \n* **/list**: List all the events \n* **/about**: Do this if you want to know who built the website"
                case "list":
                    bot_reply = "Here is the list of all events: "
                case "about":
                    bot_reply = "This website is constructed by Jack Lao, a junior majors in CS. This website is open-source which you can find from his [GitHub](https://github.com/Junwei-Lao/TAMU-event.git). Feel free to check his GitHub and [LinkedIn](http://www.linkedin.com/in/junwei-lao-jack) profiles."
                case _:
                    bot_reply = "That's not a valid command."
        else:
            bot_reply = user_message
    else:
        bot_reply = "There is something wrong because the server didn't receive your message. Please try again later."
    

    print(bot_reply)
    return jsonify({"text": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6500, debug=True)
