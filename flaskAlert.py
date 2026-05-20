import telegram
import asyncio
import logging
import json
import os
import pprint
import traceback
from flask import Flask, request
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.secret_key = 'aYT>.L$kk2h>!'

app.config['BASIC_AUTH_USERNAME'] = os.environ['BASIC_AUTH_USERNAME']
app.config['BASIC_AUTH_PASSWORD'] = os.environ['BASIC_AUTH_PASSWORD']
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

bot = telegram.Bot(token=os.environ['TELEGRAM_BOTTOKEN'])
chatID = os.environ['TELEGRAM_CHATID']


@app.route('/alert', methods=['POST'])
def postAlertmanager():

    content = request.get_json()

    pprint.pprint(content)

    try:
        with open("/tmp/Output.txt", "w") as text_file:
            text_file.write(str(content))
    except Exception as e:
        print(f"File write error: {e}")

    try:
        for alert in content['alerts']:
            message = "Status: %s\n" % alert['status']
            message += "Alertname: %s\n" % (alert.get('labels', {}).get('alertname', 'N/A'))
            if alert['status'] == "firing":
                message += "Detected: %s\n" % alert.get('startsAt')
            if alert['status'] == "resolved":
                message += "Resolved: %s\n" % alert.get('endsAt')
            if "labels" in alert:
                message += "Labels:\n"
                for label in alert['labels']:
                    message += "\t%s : %s\n" % (
                        label,
                        alert['labels'][label])

            if "generatorURL" in alert: message += "%s\n" % alert['generatorURL']

            annotations = alert.get("annotations", {})

            summary = (
                annotations.get("message")
                or annotations.get("summary")
                or annotations.get("description")
                or "No details")

            message += "\n%s\n" % summary

            print(message)

            asyncio.run(
                bot.send_message(
                    chat_id=chatID,
                    text=message))

        return "Alert OK", 200

    except Exception as e:

        print("ERROR!")
        print(str(e))

        traceback.print_exc()

        return str(e), 500


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    app.run(host='0.0.0.0', port=9119)