import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Ativar logs (útil para debugging)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔐 Guardiã EuSou online.\nTudo pronto para proteger o teu valor.")

# Comando /ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛰️ Pong — conexão ativa!")

# Função principal
def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise Exception("⚠️ TELEGRAM_TOKEN não está definido no ambiente Render!")

    app = ApplicationBuilder().token(token).build()

    # Handlers de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))

    # Inicia o bot
    app.run_polling()

if __name__ == "__main__":
    main()
