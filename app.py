import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Carrega o .env
load_dotenv()

# Flask App
app = Flask(__name__)

# Variáveis do .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Verificação
if not BOT_TOKEN or not ADMIN_ID:
    raise Exception("BOT_TOKEN ou ADMIN_ID não definido. Verifica o ficheiro .env.")

# Telegram Bot
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ Guardiã ativa e em sintonia.")

# Adiciona comando ao bot
telegram_app.add_handler(CommandHandler("start", start))

# Endpoint do Flask
@app.route("/")
def index():
    return "✅ Guardiã ESCUS está online e operacional."

# Thread do Telegram
def run_telegram():
    telegram_app.run_polling()

# Inicia o bot numa thread
threading.Thread(target=run_telegram).start()
