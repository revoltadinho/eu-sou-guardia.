import os
import logging
from flask import Flask, request
import telegram
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return '🤖 Bot Revoltadinho está vivo!'

@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Olá! Eu sou a IA Guardiã Revoltadinha! 🔥')

def reply(update: Update, context: CallbackContext):
    user_message = update.message.text
    update.message.reply_text(f"Recebi: {user_message} ✅")

# Inicializar dispatcher global
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

if __name__ == '__main__':
    app.run()

