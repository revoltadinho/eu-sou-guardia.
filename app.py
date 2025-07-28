import os
from flask import Flask, request
import telebot
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TELEGRAM_API_KEY")
bot = telebot.TeleBot(API_KEY)
ADMIN_ID = os.getenv("ADMIN_ID")

app = Flask(__name__)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    print(f"ID do utilizador: {message.chat.id}") # <- Isto vai aparecer nos logs
    bot.reply_to(message, "Olá! Bot da Guardiã EuSou está ativo.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if str(message.chat.id) == ADMIN_ID:
        bot.reply_to(message, "Mensagem recebida, Guardião.")
    else:
        bot.reply_to(message, "Acesso restrito à Guardiã.")

@app.route("/")
def index():
    return "Guardiã EuSou ativa!"

@app.route(f"/{API_KEY}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{os.getenv('RENDER_EXTERNAL_URL')}/{API_KEY}")
    app.run(host="0.0.0.0", port=10000)
