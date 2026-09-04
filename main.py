import os
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/")
def home():
    return "Bot de promoções online!"

@app.route("/teste")
def teste():
    if not TOKEN:
        return "TOKEN NAO ENCONTRADO"

    ultimos = TOKEN[-6:]

    return f"""
    TOKEN ENCONTRADO<br>
    Tamanho: {len(TOKEN)}<br>
    Últimos 6 caracteres: {ultimos}
    """
    url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    response = requests.get(url)

    return response.text
    

    return f"""
    TOKEN ENCONTRADO<br>
    Tamanho: {len(TOKEN)}<br>
    Começa com número: {TOKEN[0].isdigit()}<br>
    Tem dois pontos: {":" in TOKEN}
    """
    url = f"https://api.telegram.org/bot{TOKEN}/getMe"

    response = requests.get(url)

    print("Resposta Telegram:", response.text)

    return response.text

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
