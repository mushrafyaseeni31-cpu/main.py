# -*- coding: utf-8 -*-
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAAfMBZAIWDYcBSgURtW4dhlvoAOtembfS2vgVDOryfgB26o47JNVT2XqvlgaNRWRO887Fyz0ZBDWvXeMM8cpSQmebOEVekNX4jUZBNOWrqZCZCHy9g0IMEZAn7Glm78KbibgEtsd1oJIaENpu1qxmRuFkxQO3JRKTUnENF9h2ybnbvb8TnBRuPzMddpZCfWy2GsjWYQTNQ1Yo67xYFyYzZADjEj8NEoukUwlvNhRRIR0JXoHfZBZA4O8rmCsI9Pk2NSsDxzfvh3mfDgqplIkTZCSHqjOSkfQ9olChj0ZBQEV0UaJnRrOVoIhkCvM2LUFZCb4AlSqlbEDdICm3IBTQsYwovnbQmQZDZD"
VERIFY_TOKEN = "chattrigger_secure_verify_token"

@app.route("/", methods=["GET"])
def home():
    return "ChatTrigger Instagram Bot is Running!", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403
    return "Webhook Endpoint Active", 200

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.json
    print("Incoming Webhook data:", data)

    try:
        if data.get("object") == "instagram":
            for entry in data.get("entry", []):
                changes = entry.get("changes", [])
                for change in changes:
                    if change.get("field") == "comments":
                        comment_data = change.get("value", {})
                        comment_id = comment_data.get("id")
                        text = comment_data.get("text")
                        
                        send_comment_reply(comment_id, "வணக்கம்! எங்கள் பதிவிற்கு நன்றி. மேலதிக விவரங்களுக்கு DM-ஐ பார்க்கவும்.")
                        
    except Exception as e:
        print(f"Error processing webhook: {e}")

    return jsonify({"status": "received"}), 200

def send_comment_reply(comment_id, message_text):
    url = f"https://graph.facebook.com/v20.0/{comment_id}/replies"
    payload = {
        "message": message_text,
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    print("Reply response:", response.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
