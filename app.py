import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ativa logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Olá! Eu sou o SouRevoltadinhoBot. Estou online!")

# Comando /ajuda
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Escreve algo e eu tentarei ajudar.")

# Início da aplicação
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))

    app.run_polling()

if __name__ == '__main__':
    main()
