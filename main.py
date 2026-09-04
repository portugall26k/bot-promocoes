import os
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/")
def home():
    return "Bot de promoções online!"

@app.route("/teste")
def teste():
    if not TOKEN:
        return "ERRO: TELEGRAM_TOKEN não foi encontrado no Render."

    # Mostra apenas informações do token, nunca o token inteiro
    print("Token carregado:", True)
    print("Tamanho:", len(TOKEN))
    print("Primeiro caractere:", TOKEN[0] if TOKEN else "N/A")
    print("Possui dois pontos:", ":" in TOKEN)

    url = f"https://api.telegram.org/bot{TOKEN}/getMe"

    response = requests.get(url)

    print("Resposta Telegram:", response.text)

    return response.text

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
