import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()


@app.route("/")
def home():
    return "Bot de promoções online!"


def enviar_oferta(produto, preco, link):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    texto = (
        "🔥 OFERTA ENCONTRADA!\n\n"
        f"🛍️ {produto}\n\n"
        f"💰 Por apenas {preco}\n\n"
        "🛒 COMPRAR AGORA 👇\n"
        f"{link}"
    )

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": texto
        },
        timeout=15
    )

    return response.json()


@app.route("/oferta")
def oferta():
    produto = request.args.get("produto")
    preco = request.args.get("preco")
    link = request.args.get("link")

    if not produto or not preco or not link:
        return "Faltam informações. Use: /oferta?produto=...&preco=...&link=..."

    resultado = enviar_oferta(produto, preco, link)

    return resultado


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
