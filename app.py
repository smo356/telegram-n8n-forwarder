from flask import Flask, request
import requests, os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
PUBLIC_URL = os.getenv("PUBLIC_URL")

@app.route("/")
def home():
    return "Telegram → n8n forwarder active", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # Transfert direct vers n8n
    try:
        requests.post(N8N_WEBHOOK_URL, json=data)
    except Exception as e:
        print("Erreur :", e)

    return {"status": "ok"}, 200

def set_webhook():
    if not PUBLIC_URL:
        print("PUBLIC_URL manquant, webhook ignoré")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    webhook_url = PUBLIC_URL + "/webhook"
    r = requests.get(url, params={"url": webhook_url})
    print("Webhook set :", r.text)

if __name__ == "__main__":
    set_webhook()
