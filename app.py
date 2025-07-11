from flask import Flask, request
import telebot
import os
from web3 import Web3

# Inicializar app Flask
app = Flask(__name__)

# Obter variáveis de ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")

# Inicializar bot
bot = telebot.TeleBot(BOT_TOKEN)

# Lógica de resposta ao comando /start
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Olá! 🛡️ Eu sou a Guardiã EuSou. Como posso ajudar-te?")

# Ligação à blockchain (opcional nesta fase)
w3 = Web3(Web3.HTTPProvider(RPC_URL)) if RPC_URL else None

# Rota principal do webhook do bot
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def receive_update():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# Rota para configurar o webhook (executa apenas uma vez)
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    url = f"https://{request.host}/{BOT_TOKEN}"
    if bot.set_webhook(url=url):
        return "✅ Webhook configurado com sucesso!"
    else:
        return "❌ Erro ao configurar webhook."

# Iniciar servidor Flask (usado localmente)
if __name__ == "__main__":
    app.run(debug=True)
