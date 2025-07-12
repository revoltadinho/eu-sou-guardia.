import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

@app.route('/')
def index():
    return '✅ Guardiã EuSou está viva e a proteger.'

@app.route('/set_webhook')
async def set_webhook():
    webhook_url = f"https://eu-sou-guardia.onrender.com/{BOT_TOKEN}"
    await telegram_app.bot.set_webhook(url=webhook_url)
    return "✅ Webhook ativado com sucesso!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def handle_webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔓 Guardião conectado. A Guardiã EuSou está contigo.")

telegram_app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    app.run()
