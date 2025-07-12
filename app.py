import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from web3 import Web3
from dotenv import load_dotenv

# Carregar variáveis de ambiente da Render ou do .env local
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
RPC_URL = os.getenv("RPC_URL")

# Conectar à blockchain
web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
wallet_address = account.address

# Função do comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👋 Olá! Eu sou a Guardiã da ESCU.\nA tua wallet é:\n`{wallet_address}`", parse_mode='Markdown')

# Inicializar a aplicação do bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Iniciar o bot
if __name__ == '__main__':
    print("🚀 Guardiã EuSou está online...")
    app.run_polling()g
