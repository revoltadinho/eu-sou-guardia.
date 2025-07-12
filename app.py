from flask import Flask, request
import telebot
import os
from web3 import Web3

# Inicialização
app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Blockchain (opcional nesta fase)
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
w3 = Web3(Web3.HTTPProvider(RPC_URL)) if RPC_URL else None

# Mensagem de boas-vindas
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Olá! Eu sou a Guardiã EuSou. Como posso ajudar-te hoje?")

# Webhook para receber atualizações do Telegram
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# Endpoint para configurar o webhook
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    url = f"https://{request.host}/{BOT_TOKEN}"
    if bot.set_webhook(url=url):
        return "✅ Webhook configurado com sucesso!"
    else:
        return "❌ Falha ao configurar webhook."

# Para manter o serviço ativo
@app.route('/', methods=['GET'])
def home():
    return '👁️ Guardiã EuSou ativa.'

if __name__ == '__main__':
    app.run(debug=True)
