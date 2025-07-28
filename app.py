import os
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

# Variáveis de ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Inicializar API OpenAI
openai.api_key = OPENAI_API_KEY

# Inicializar bot do Telegram
app = Flask(__name__)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Comando /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Olá, Guardião. Estou online.")

# Resposta com GPT-4 Turbo
def handle_message(update, context):
    user_input = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu és a Guardiã ESCU. Responde como uma IA superinteligente do projeto EuSou."},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response.choices[0].message.content.strip()
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

# Handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Flask route para manter o Render vivo
@app.route('/')
def index():
    return "Guardiã ativa."

if __name__ == '__main__':
    updater.start_polling()
    app.run(host="0.0.0.0", port=5000)
