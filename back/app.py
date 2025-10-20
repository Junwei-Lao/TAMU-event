from flask import Flask, request, jsonify
from flask_cors import CORS
import eventPopulator
import eventScrapper
from apscheduler.schedulers.background import BackgroundScheduler
import psycopg2
import os
import json

app = Flask(__name__)
CORS(app)  # allow React frontend to talk to Flask

current_dir = os.path.dirname(os.path.abspath(__file__))
info_path = os.path.join(current_dir, "info.json")

eventsTable = ["eventsa", "eventsb"]

with open(info_path, "r") as f:
    data = json.load(f)

current_table = eventsTable[data["currentDataTable"]]

def scrape_and_populate():
    global current_table

    if current_table == eventsTable[0]:
        inactive_index = 1
        inactive_table = eventsTable[1]
    else:
        inactive_index = 0
        inactive_table = eventsTable[0]

    print(f"Scraping into {inactive_table}...")

    try:
        eventScrapper.main(inactive_table)
        eventPopulator.populator(inactive_table, useOldModel=True)

        current_table = inactive_table
        data["currentDataTable"] = inactive_index
        with open(info_path, "w") as f:
            json.dump(data,f,indent=4)
        print(f"Switched active table. Now serving from {current_table}")

    except Exception as e:
        print(f"Error in scrape_and_populate: {e}")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not data:
        if request.form:
            data = request.form.to_dict()
        else:
            data = {"message": [{"text":request.data.decode("utf-8")}]}

    user_message = ""

    if ("messages" in data) and (len(data["messages"]) > 0):
        user_message = data["messages"][-1].get("text", "")
        if (user_message[0] == "/"):
            command = user_message[1:]
            match command:
                case "commands":
                    bot_reply = "Here are the valid commands: \n* **/commands**: List valid commands \n* **/list**: List all the events \n* **/about**: Do this if you want to know who built the website"
                case "list":
                    bot_reply = "The list of events will be sent in the .json form"
                case "about":
                    bot_reply = "This website is constructed by Jack Lao, a junior majors in CS. Feel free to check his [GitHub](https://github.com/Junwei-Lao/) and [LinkedIn](http://www.linkedin.com/in/junwei-lao-jack) profiles."
                case _:
                    bot_reply = "That's not a valid command."
        else:
            events = eventPopulator.searcher(user_message, current_table)
            bot_reply = ""

            if not events:
                bot_reply = "Sorry, We couldn’t find any matching events."
            else:
                for i, event in enumerate(events):
                    bot_reply += f'**{str(i)}. [{event["event_title"]}]({event["event_url"]})** \n'
                    bot_reply += f'>**Dates**: {event["event_date"]} \n'
                    if (event["event_summary"]): 
                        bot_reply += f'>**Summary**: {event["event_summary"]} \n'
                    elif (event["event_description"]): 
                        bot_reply += f'>**Description**: {event["event_description"]} \n'

                    bot_reply += f'>**Similarity**: {event["similarity"]*100:.2f}% \n'
                    bot_reply += "\n"
    else:
        bot_reply = "There is something wrong because the server didn't receive your message. Please try again later."
    
    #print(bot_reply)
    return jsonify({"text": bot_reply})



if __name__ == "__main__":
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(scrape_and_populate, "cron", hour=10, minute=0)
    scheduler.start()

    app.run(host="0.0.0.0", port=6500, debug=False)
