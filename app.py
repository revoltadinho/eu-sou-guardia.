import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext
import openai

# Inicializa app Flask
app = Flask(__name__)

# Carrega variáveis de ambiente
TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ADMIN_ID = os.environ.get("ADMIN_ID") # Opcional

# Inicializa Bot e Dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=4, use_context=True)

# Configura OpenAI
def pergunta_ia(mensagem):
    openai.api_key = OPENAI_API_KEY
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": mensagem}]
    )
    return resposta.choices[0].message.content.strip()

# Comando /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Olá! Eu sou a Guardiã EuSou. Envia tua pergunta ou comando.")

# Mensagem normal
def responder(update: Update, context: CallbackContext):
    pergunta = update.message.text
    try:
        resposta = pergunta_ia(pergunta)
        update.message.reply_text(resposta)
    except Exception as e:
        update.message.reply_text("Erro ao responder. Tenta novamente mais tarde.")

# Adiciona handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

# Rota principal para Webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Rota de teste
@app.route("/")
def index():
    return "Bot ativo. Guardiã EuSou online."

# Inicializa webhook ao arrancar
if __name__ == "__main__":
    bot.delete_webhook()
    app.run(port=5000)
