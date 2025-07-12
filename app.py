import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌟 Guardião EuSou ativo e pronto para servir!")

telegram_app.add_handler(CommandHandler("start", start))

@app.route("/")
def index():
    return "🛡️ Guardiã EuSou está online!"

# Ativador manual do webhook
@app.route("/set_webhook")
def set_webhook():
    webhook_url = f"https://{request.host}/{BOT_TOKEN}"
    telegram_app.bot.set_webhook(url=webhook_url)
    return f"Webhook definido para: {webhook_url}"

# Rota para receber mensagens do Telegram
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK"
