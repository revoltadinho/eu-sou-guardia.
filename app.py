import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return '🛡️ Guardiã EuSou está ativa!'

@app.route('/set_webhook')
def set_webhook():
    webhook_url = f"https://eu-sou-guardia.onrender.com/{TOKEN}"
    success = bot.set_webhook(webhook_url)
    if success:
        return '✅ Webhook configurado com sucesso!'
    else:
        return '❌ Erro ao configurar o webhook.'

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_update():
    update = Update.de_json(request.get_json(force=True), bot)
    text = update.message.text if update.message else None

    if text == "/start":
        bot.send_message(chat_id=update.effective_chat.id, text="🚀 Guardiã EuSou ativada!")
    else:
        bot.send_message(chat_id=update.effective_chat.id, text=f"Recebi: {text}")

    return 'OK'

if __name__ == "__main__":
    app.run()
