from flask import Flask, request, jsonify
from flask_cors import CORS
import eventPopulator
import eventScrapper
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import psycopg2

app = Flask(__name__)
CORS(app)  # allow React frontend to talk to Flask



eventsTable = ["eventsA", "eventsB"]
current_table = eventsTable[0]



# -------------------- Scheduled Job --------------------
def scrape_and_populate():
    global current_table

    inactive_table = eventsTable[1] if current_table == eventsTable[0] else eventsTable[0]

    print(f"Scraping into {inactive_table}...")

    try:
        eventScrapper.main()
        #idealy I will run the test code first, and that will download the model, so that I can use the saved model
        eventPopulator.populator(inactive_table, useOldModel=True)

    except Exception as e:
        print(f"❌ Error in scrape_and_populate: {e}")




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
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(scrape_and_populate, "cron", hour=2, minute=0)
    scheduler.start()
    app.run(host="0.0.0.0", port=6500, debug=True)
