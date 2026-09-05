import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

ofertas_publicadas = set()


@app.route("/")
def home():
    return "Bot de promoções online!"


def calcular_desconto(preco_antigo, preco_atual):
    if preco_antigo <= 0:
        return 0

    desconto = ((preco_antigo - preco_atual) / preco_antigo) * 100
    return round(desconto)


def publicar_oferta(oferta):
    produto = oferta["produto"]
    preco_antigo = float(oferta["preco_antigo"])
    preco_atual = float(oferta["preco_atual"])
    categoria = oferta["categoria"]
    link = oferta["link"]

    desconto = calcular_desconto(
        preco_antigo,
        preco_atual
    )

    if desconto < 20:
        return {
            "publicada": False,
            "motivo": "Desconto menor que 20%",
            "desconto": desconto
        }

    identificador = f"{produto}|{link}"

    if identificador in ofertas_publicadas:
        return {
            "publicada": False,
            "motivo": "Oferta já publicada"
        }

    texto = (
        "🔥 OFERTA ENCONTRADA!\n\n"
        f"🛍️ {produto}\n"
        f"🏷️ Categoria: {categoria}\n\n"
        f"❌ De: R$ {preco_antigo:.2f}\n"
        f"✅ Por: R$ {preco_atual:.2f}\n"
        f"🔥 {desconto}% OFF\n\n"
        "🛒 COMPRAR AGORA 👇\n"
        f"{link}"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": texto
        },
        timeout=15
    )

    resultado = response.json()

    if resultado.get("ok"):
        ofertas_publicadas.add(identificador)

    return resultado


@app.route("/publicar-ofertas")
def publicar_ofertas():
    try:
        with open("ofertas.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        ofertas = dados.get("ofertas", [])
        resultados = []

        for oferta in ofertas:
            resultado = publicar_oferta(oferta)
            resultados.append(resultado)

        return {
            "ok": True,
            "quantidade": len(ofertas),
            "resultados": resultados
        }

    except Exception as erro:
        return {
            "ok": False,
            "erro": str(erro)
        }


@app.route("/oferta")
def oferta():
    produto = request.args.get("produto")
    preco = request.args.get("preco")
    link = request.args.get("link")

    if not produto or not preco or not link:
        return "Faltam informações."

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


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
