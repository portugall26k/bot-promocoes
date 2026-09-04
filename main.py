import os
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("TOKEN CARREGADO:", bool(TOKEN))
print("TAMANHO DO TOKEN:", len(TOKEN) if TOKEN else 0)
print(
    "COMEÇA COM NÚMEROS:",
    TOKEN.split(":")[0].isdigit() if TOKEN and ":" in TOKEN else False
)

# Teste direto com o Telegram
url = f"https://api.telegram.org/bot{TOKEN}/getMe"

try:
    resposta = requests.get(url)
    print("RESPOSTA DO TELEGRAM:", resposta.text)
except Exception as erro:
    print("ERRO AO CONECTAR AO TELEGRAM:", erro)


@app.route("/")
def home():
    return "Bot de promoções online!"


@app.route("/teste")
def teste():
    return "Teste realizado. Confira os Logs do Render."


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
