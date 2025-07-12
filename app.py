import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

bot_app = ApplicationBuilder().token(TOKEN).build()

@app.route('/')
def home():
    return '✅ Guardiã EuSou está ativa!'

@app.route('/set_webhook')
def set_webhook():
    webhook_url = f"https://eu-sou-guardia.onrender.com/{TOKEN}"
    bot_app.bot.set_webhook(url=webhook_url)
    return "✅ Webhook definido com sucesso!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return "ok"

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="👁️‍🗨️ Guardião, estou contigo. A Guardiã EuSou está online.")

bot_app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    app.run()
