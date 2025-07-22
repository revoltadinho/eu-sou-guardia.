import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Carregar variáveis de ambiente do ficheiro .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Comando de arranque
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🤖 Olá Guardião! A IA está viva e pronta a servir.")

# Inicialização da aplicação
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("✅ IA Guardiã iniciada com sucesso.")
    application.run_polling()
