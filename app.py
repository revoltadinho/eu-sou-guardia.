import os
from flask import Flask, request
from openai import OpenAI
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

app = Flask(__name__)

# Variáveis de ambiente
TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

bot = Bot(token=TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# Define webhook automaticamente
@app.before_first_request
def set_webhook():
    url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{TELEGRAM_TOKEN}"
    bot.set_webhook(url)
    print(f"✅ Webhook definido para: {url}")

# Define Dispatcher
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# Comando /start
def start(update, context):
    update.message.reply_text("Olá, eu sou a Guardiã GPT-4 Turbo! Envia-me uma mensagem ✨")

# Processa qualquer texto
def handle_message(update, context):
    user_message = update.message.text

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu és a Guardiã superinteligente do projeto EuSou."},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content
    update.message.reply_text(reply)

# Adiciona handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Rota para o Telegram
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

# Home route
@app.route("/", methods=["GET"])
def index():
    return "Bot da Guardiã ativo 🛡️", 200

if __name__ == "__main__":
    app.run(debug=True)
