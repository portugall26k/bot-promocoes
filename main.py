import os
import json
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

ofertas_publicadas = set()


PAGINA = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Central de Ofertas</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 30px auto;
            padding: 20px;
        }

        h1 {
            text-align: center;
        }

        input, select, button {
            width: 100%;
            padding: 14px;
            margin: 8px 0;
            box-sizing: border-box;
            font-size: 16px;
        }

        button {
            cursor: pointer;
            font-weight: bold;
        }

        .resultado {
            margin-top: 20px;
            padding: 15px;
            background: #f1f1f1;
            border-radius: 8px;
        }
    </style>
</head>

<body>

<h1>🔥 Central de Ofertas</h1>

<form method="POST" action="/publicar">

    <label>🛍️ Nome do produto</label>
    <input
        type="text"
        name="produto"
        placeholder="Ex: Teclado Logitech G515"
        required
    >

    <label>❌ Preço antigo</label>
    <input
        type="number"
        name="preco_antigo"
        step="0.01"
        placeholder="949.90"
        required
    >

    <label>✅ Preço atual</label>
    <input
        type="number"
        name="preco_atual"
        step="0.01"
        placeholder="633.37"
        required
    >

    <label>🏷️ Categoria</label>
    <select name="categoria" required>
        <option value="Eletrônicos">Eletrônicos</option>
        <option value="Games">Games</option>
        <option value="Celulares">Celulares</option>
        <option value="Informática">Informática</option>
        <option value="Tênis">Tênis</option>
        <option value="Roupas">Roupas</option>
        <option value="Casa">Casa</option>
        <option value="Gamer">Gamer</option>
        <option value="Outros">Outros</option>
    </select>

    <label>🔗 Link do SiteStripe</label>
    <input
        type="url"
        name="link"
        placeholder="Cole aqui seu link de afiliado"
        required
    >

    <button type="submit">
        🚀 PUBLICAR OFERTA
    </button>

</form>

{% if mensagem %}
<div class="resultado">
    {{ mensagem }}
</div>
{% endif %}

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGINA)


def calcular_desconto(preco_antigo, preco_atual):

    if preco_antigo <= 0:
        return 0

    desconto = (
        (preco_antigo - preco_atual)
        / preco_antigo
    ) * 100

    return round(desconto)


def enviar_telegram(
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


@app.route("/publicar", methods=["POST"])
def publicar():

    produto = request.form.get("produto", "").strip()
    preco_antigo = request.form.get("preco_antigo", "").strip()
    preco_atual = request.form.get("preco_atual", "").strip()
    categoria = request.form.get("categoria", "").strip()
    link = request.form.get("link", "").strip()

    if not produto or not preco_antigo or not preco_atual or not categoria or not link:

        return render_template_string(
            PAGINA,
            mensagem="❌ Preencha todos os campos."
        )

    try:

        preco_antigo = float(preco_antigo)
        preco_atual = float(preco_atual)

    except ValueError:

        return render_template_string(
            PAGINA,
            mensagem="❌ Os preços precisam ser números."
        )

    desconto = calcular_desconto(
        preco_antigo,
        preco_atual
    )

    if desconto < 20:

        return render_template_string(
            PAGINA,
            mensagem=f"❌ Oferta recusada: apenas {desconto}% de desconto. O mínimo é 20%."
        )

    identificador = f"{produto}|{link}"

    if identificador in ofertas_publicadas:

        return render_template_string(
            PAGINA,
            mensagem="⚠️ Essa oferta já foi publicada."
        )

    resultado = enviar_telegram(
        produto,
        preco_antigo,
        preco_atual,
        categoria,
        link
    )

    if resultado.get("ok"):

        ofertas_publicadas.add(identificador)

        return render_template_string(
            PAGINA,
            mensagem=f"✅ Oferta publicada com sucesso! 🔥 {desconto}% OFF"
        )

    return render_template_string(
        PAGINA,
        mensagem=f"❌ Erro ao publicar: {resultado}"
    )


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

    port = int(
        os.getenv("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
