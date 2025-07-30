from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN") or "8420252346:AAEVHa54--Yw6tgr_ok6WGJ6am_ccFqnadM"

app = Flask(__name__)

application = ApplicationBuilder().token(TOKEN).build()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Eu sou a Guardiã Revoltadinha 😈💥")

# Adicionar handler
application.add_handler(CommandHandler("start", start))

# Webhook do Telegram
@app.route(f'/{TOKEN}', methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

# Página inicial
@app.route("/")
def home():
    return "Bot da Guardiã Revoltadinha está ativo 💥"

if __name__ == "__main__":
    app.run()
