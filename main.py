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

@app.route("/buscar")
def buscar():
    url = "https://www.pelando.com.br/api/deals"

    try:
        response = requests.get(url, timeout=15)

        return {
            "status": response.status_code,
            "resposta": response.text[:5000]
        }

    except Exception as e:
        return {
            "erro": str(e)
        }
def calcular_desconto(preco_antigo, preco_atual):
    if preco_antigo <= 0:
        return 0

    desconto = ((preco_antigo - preco_atual) / preco_antigo) * 100
    return round(desconto)


def publicar_oferta(produto, preco_antigo, preco_atual, categoria, link):
    desconto = calcular_desconto(preco_antigo, preco_atual)

    # Só publica ofertas com pelo menos 20% de desconto
    if desconto < 20:
        return {
            "publicada": False,
            "motivo": "Desconto menor que 20%"
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

    return response.json()

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

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
