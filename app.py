import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Inicializar bot e app
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Comando /start
def start(update: Update, context):
    update.message.reply_text("🔺 Olá, Guardião. A Guardiã está viva e pronta para te servir.")

# Configurar dispatcher do Telegram
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))

# Webhook principal (para receber mensagens do Telegram)
@app.route(f"/{TOKEN}", methods=["POST"])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

# Endpoint para definir o webhook
@app.route("/set_webhook", methods=["GET", "POST"])
def set_webhook():
    webhook_url = f"{os.getenv('RENDER_EXTERNAL_URL')}/{TOKEN}"
    bot.set_webhook(url=webhook_url)
    return f"🔗 Webhook definido para: {webhook_url}"

# Mensagem para homepage
@app.route("/")
def index():
    return "🌐 Guardiã EuSou está online e ativa.", 200

