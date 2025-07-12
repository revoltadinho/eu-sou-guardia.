import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Função de resposta ao /start
def start(update: Update, context):
    update.message.reply_text("👁️‍🗨️ Olá, Guardião. A Guardiã está viva e pronta para te servir.")

# Configuração do dispatcher
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))

# Rota principal do webhook
@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

# Rota para definir o webhook (executada uma vez)
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    webhook_url = f"{os.environ.get('RENDER_EXTERNAL_URL')}{TOKEN}"
    bot.set_webhook(url=webhook_url)
    return f"Webhook definido para: {webhook_url}", 200

# Confirmação simples de que a app está online
@app.route('/')
def index():
    return "🔮 Guardiã EuSou está online e ativa.", 200

  
