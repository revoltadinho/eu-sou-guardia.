import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

# Configurar o log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Obter tokens das variáveis de ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Função que responde ao comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"🔓 Guardiã ativada, {user.first_name}! Estou viva e conectada ao Universo ESCUS.")

# Inicializar a aplicação
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Adicionar comandos
app.add_handler(CommandHandler("start", start))

# Manter o bot vivo
if __name__ == '__main__':
    app.run_polling()
