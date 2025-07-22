from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Comando de arranque
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🤖 Olá Guardião! A IA está viva e pronta a servir.")

# Inicialização da aplicação
if __name__ == '__main__':
    application = ApplicationBuilder().token("7830732466:AAEl5DWOS1Amwp-rtX1YPpyOQvuiziEi3BU").build()

    application.add_handler(CommandHandler("start", start))

    print("✅ IA Guardiã iniciada com sucesso.")
    application.run_polling()

