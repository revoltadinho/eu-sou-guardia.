from flask import Flask, render_template, request
import os

from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackContext
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mensagem', methods=['POST'])
def mensagem_web():
    user_input = request.form.get('mensagem')
    resposta = processar_mensagem(user_input)
    return render_template('index.html', resposta=resposta)

def processar_mensagem(texto):
    if "ESC" in texto:
        return "A ESCU é a moeda que vai mudar o mundo."
    elif "valor" in texto:
        return "Tu és o Guardião do Valor. ESCU reflete isso."
    else:
        return "Sou a Guardiã ESCU, pronta para te guiar no universo Eusou."

# ==== Funções do Telegram ====

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Olá! Sou a Guardiã ESCU. Envia-me a tua pergunta.")

def mensagem_telegram(update: Update, context: CallbackContext):
    texto = update.message.text
    resposta = processar_mensagem(texto)
    update.message.reply_text(resposta)

def iniciar_bot_telegram():
    token = os.environ.get("TELEGRAM_TOKEN")
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, mensagem_telegram))

    updater.start_polling()
    print("🤖 Bot Guardiã ESCU iniciado no Telegram.")

# ==== Início da aplicação ====

if __name__ == "__main__":
    iniciar_bot_telegram()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
