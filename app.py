import os
from flask import Flask, request
from telegram import Bot, Update

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return '🛡️ Guardiã EuSou ativa'

@app.route('/set_webhook')
def set_webhook():
    webhook_url = f"https://eu-sou-guardia.onrender.com/{TOKEN}"
    s = bot.set_webhook(webhook_url)
    if s:
        return "✅ Webhook configurado com sucesso!"
    else:
        return "❌ Falha ao configurar o webhook."

@app.route(f"/{TOKEN}", methods=['POST'])
def receive_update():
    update = Update.de_json(request.get_json(force=True), bot)
    if update.message and update.message.text == "/start":
        bot.send_message(chat_id=update.message.chat_id, text="🔮 Guardiã EuSou conectada.")
    return "OK"
