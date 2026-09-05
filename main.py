import os
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()


@app.route("/")
def home():
    return "Bot de promoções online!"


def enviar_oferta(produto, preco, link):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": (
                f"🔥 OFERTA!\n\n"
                f"🛍️ {produto}\n"
                f"💰 Preço: {preco}\n\n"
                f"🔗 Comprar: {link}"
            )
        },
        timeout=15
    )

    return response.json()


@app.route("/teste")
def teste():
    resultado = enviar_oferta(
        "Produto de teste",
        "R$ 99,90",
        "https://exemplo.com"
    )

    return resultado


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
