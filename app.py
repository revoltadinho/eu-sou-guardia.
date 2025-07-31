import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler

# Carrega as variáveis do .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def start(update, context):
    update.message.reply_text("👋 Olá! Eu sou o RevoltadinhoBot. Estou online e pronto para te ajudar!")

if __name__ == '__main__':
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    print("🤖 RevoltadinhoBot está online...")
    updater.start_polling()
    updater.idle()
