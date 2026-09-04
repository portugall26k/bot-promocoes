import os
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/")
def home():
    return "Bot de promoções online!"

@app.route("/teste")
def teste():
    if not TOKEN:
        return "ERRO: TELEGRAM_TOKEN não foi encontrado no Render"

    url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    response = requests.get(url)

    data = response.json()

    if data.get("ok"):
        return "TOKEN OK! Bot reconhecido pelo Telegram."

    return f"ERRO DO TELEGRAM: {data}"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
