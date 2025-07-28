import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Inicializar OpenAI
openai.api_key = OPENAI_API_KEY

# Inicializar bot
app = Flask(__name__)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Comando /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Olá, sou a Guardiã EuSou. Envia-me uma pergunta!")

# Mensagens de texto
def handle_message(update: Update, context: CallbackContext):
    pergunta = update.message.text
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Responde como a Guardiã do projeto EuSou, com sabedoria e clareza."},
            {"role": "user", "content": pergunta}
        ]
    )
    texto = resposta['choices'][0]['message']['content']
    update.message.reply_text(texto)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route("/", methods=["GET"])
def index():
    return "Guardiã EuSou ativa!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, updater.bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == "__main__":
    updater.start_polling()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

  
