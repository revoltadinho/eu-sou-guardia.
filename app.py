from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN") or "8420252346:AAEVHa54--Yw6tgr_ok6WGJ6am_ccFqnadM"

app = Flask(__name__)

# Criação da aplicação do Telegram
application = ApplicationBuilder().token(TOKEN).build()

# Comando de teste
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá, eu sou a Guardiã!")

application.add_handler(CommandHandler("start", start))

# Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.run(application.process_update(update))
    return "ok"

# Rota principal
@app.route("/")
def home():
    return "Bot da Guardiã EuSou está ativo."

if __name__ == "__main__":
    app.run(port=5000)
