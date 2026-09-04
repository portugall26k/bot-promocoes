import os
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

@app.route("/")
def home():
    return "Bot de promoções online!"

@app.route("/teste")
def teste():
    if not TOKEN:
        return "TOKEN NAO ENCONTRADO"

    response = requests.get(
        "https://api.telegram.org/bot" + TOKEN + "/getMe",
        timeout=15
    )

    return f"""
    Status HTTP: {response.status_code}<br>
    Resposta Telegram: {response.text}
    """

    url = f"https://api.telegram.org/bot{TOKEN}/getMe"

    response = requests.get(url, timeout=15)

    return response.text

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
