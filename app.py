import os
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("telegram_TOKEN")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
RPC_URL = os.getenv("RPC_URL")

bot = Bot(token=TOKEN)

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Guardião Ativado! Bem-vindo ao sistema.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
