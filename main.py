import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

# Guarda as ofertas que já foram publicadas
ofertas_publicadas = set()


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


def calcular_desconto(preco_antigo, preco_atual):
    if preco_antigo <= 0:
        return 0

    desconto = ((preco_antigo - preco_atual) / preco_antigo) * 100
    return round(desconto)


def publicar_oferta(
    produto,
    preco_antigo,
    preco_atual,
    categoria,
    link
):
    desconto = calcular_desconto(
        preco_antigo,
        preco_atual
    )

    # Só publica ofertas com pelo menos 20% de desconto
    if desconto < 20:
        return {
            "publicada": False,
            "motivo": "Desconto menor que 20%"
        }

    # Cria um identificador único para a oferta
    identificador = f"{produto}|{link}"

    # Impede publicação duplicada
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

    # Só marca como publicada se o Telegram aceitou a mensagem
    if resultado.get("ok"):
        ofertas_publicadas.add(identificador)

    return resultado


@app.route("/oferta-teste")
def oferta_teste():
    resultado = publicar_oferta(
        produto="Tênis Nike de teste",
        preco_antigo=399.90,
        preco_atual=249.90,
        categoria="Tênis",
        link="https://exemplo.com/tenis"
    )

    return resultado


@app.route("/ofertas-teste")
def ofertas_teste():
    ofertas = [
        {
            "produto": "Tênis esportivo",
            "preco_antigo": 299.90,
            "preco_atual": 179.90,
            "categoria": "Tênis",
            "link": "https://exemplo.com/tenis"
        },
        {
            "produto": "Fone Bluetooth",
            "preco_antigo": 199.90,
            "preco_atual": 169.90,
            "categoria": "Eletrônicos",
            "link": "https://exemplo.com/fone"
        },
        {
            "produto": "Jogo de videogame",
            "preco_antigo": 299.90,
            "preco_atual": 199.90,
            "categoria": "Games",
            "link": "https://exemplo.com/jogo"
        }
    ]

    resultados = []

    for oferta in ofertas:
        resultado = publicar_oferta(
            oferta["produto"],
            oferta["preco_antigo"],
            oferta["preco_atual"],
            oferta["categoria"],
            oferta["link"]
        )

        resultados.append(resultado)

    return {
        "ok": True,
        "resultados": resultados
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port
    )
