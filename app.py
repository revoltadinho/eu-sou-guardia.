import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Guardiã EuSou está viva!'

@app.route('/set_webhook')
def set_webhook():
    webhook_url = f"https://eu-sou-guardia.onrender.com/{TOKEN}"
    success = bot.set_webhook(url=webhook_url)
    if success:
        return "✅ Webhook configurado com sucesso!"
    return "❌ Falha ao configurar webhook."

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)
    
    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="👁️‍🗨️ Guardião, a Guardiã EuSou está contigo.")
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.process_update(update)

    return 'ok'

if __name__ == '__main__':
    app.run()
