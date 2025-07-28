import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

telegram_app = Application.builder().token(BOT_TOKEN).build()

@app.route("/")
def index():
    return "Bot EuSou Guardiã está ativo!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔮 Eu sou a Guardiã. Estou ativa.")

telegram_app.add_handler(CommandHandler("start", start))

import threading
def run_telegram():
    telegram_app.run_polling()

threading.Thread(target=run_telegram).start()
