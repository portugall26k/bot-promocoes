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
        return "Faltam informações."

    return enviar_oferta(produto, preco, link)


@app.route("/ofertas")
def ofertas():
    lista = [
        {
            "produto": "Tênis esportivo de teste",
            "preco": "R$ 99,90",
            "link": "https://exemplo.com/tenis"
        },
        {
            "produto": "Fone Bluetooth de teste",
            "preco": "R$ 79,90",
            "link": "https://exemplo.com/fone"
        },
        {
            "produto": "Produto eletrônico de teste",
            "preco": "R$ 149,90",
            "link": "https://exemplo.com/eletronico"
        }
    ]

    resultados = []

    for item in lista:
        resultado = enviar_oferta(
            item["produto"],
            item["preco"],
            item["link"]
        )
        resultados.append(resultado)

    return {
        "ok": True,
        "ofertas_enviadas": len(resultados),
        "resultados": resultados
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
