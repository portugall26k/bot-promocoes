import os
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Verificação do token
print("TOKEN CARREGADO:", bool(TOKEN))
print("TAMANHO DO TOKEN:", len(TOKEN) if TOKEN else 0)
print(
    "COMEÇA COM NÚMEROS:",
    TOKEN.split(":")[0].isdigit() if TOKEN and ":" in TOKEN else False
)

@app.route("/")
def home():
    return "Bot de promoções online!"

@app.route("/teste")
def teste():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": "🤖 Bot de promoções conectado com sucesso!"
        }
    )

    return response.text


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
