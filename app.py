from flask import Flask, request
import telebot
import os
from web3 import Web3
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! 👋 Eu sou a Guardiã EuSou. Como posso ajudar-te?")
app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Lógica de blockchain (opcional nesta fase)
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")

# Ligação à blockchain (opcional nesta fase)
w3 = Web3(Web3.HTTPProvider(RPC_URL)) if RPC_URL else None

@app.route('/' + BOT_TOKEN, methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    url = f"https://{request.host}/{BOT_TOKEN}"
    if bot.set_webhook(url=url):
        return "✅ Webhook configurado com sucesso!"
    else:
        return "❌ Erro ao configurar o webhook."

@app.route('/')
def home():
    return '🤖 Guardiã EuSou está ativa!'

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👁‍🗨 Eu Sou a Guardiã. Estou contigo.")

# Comando de teste
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "🏓 pong!")

# Fallback para outras mensagens
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, "Recebido. Estou a ouvir...")

if __name__ == '__main__':
    app.run(debug=True)
