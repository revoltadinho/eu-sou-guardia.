mport logging
import asyncio
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Ativar logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Variáveis do ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0)) # Valor padrão caso não exista

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Olá {user.first_name}, eu sou a Guardiã EuSou.")
    logger.info(f"Novo utilizador: {user.id} - {user.full_name}")

# Handler para todas as mensagens
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message.text
    logger.info(f"Mensagem recebida de {user.id}: {msg}")

    # Apenas responde se o admin enviar algo
    if user.id == ADMIN_ID:
        await update.message.reply_text(f"Recebido, Guardião.")
    else:
        await update.message.reply_text("Mensagem recebida. Em breve entraremos em contacto.")

# Função principal
async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN não definido.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    logger.info("Bot iniciado com sucesso.")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())

