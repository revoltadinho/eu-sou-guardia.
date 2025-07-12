import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Telegram & Blockchain configs
TOKEN = os.getenv("TELEGRAM_TOKEN")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS") # opcional

bot = Bot(token=TOKEN)
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Wallet derivada da private key
account = web3.eth.account.from_key(PRIVATE_KEY)
wallet_address = account.address

# Comando /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"👋 Olá, Guardião!\nWallet ligada:\n{wallet_address}")

# Comando /saldo
def saldo(update: Update, context: CallbackContext) -> None:
    try:
        saldo_wei = web3.eth.get_balance(wallet_address)
        saldo_eth = web3.from_wei(saldo_wei, 'ether')
        update.message.reply_text(f"💰 Saldo atual: {saldo_eth:.6f} BNB")
    except Exception as e:
        update.message.reply_text(f"Erro ao obter saldo: {str(e)}")

# Inicialização do bot
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("saldo", saldo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

