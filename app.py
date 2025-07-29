import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)
import openai

# Ativar logging para ver erros
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Variáveis de ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_ID = os.getenv("ADMIN_ID")

openai.api_key = OPENAI_API_KEY

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou o teu bot com GPT-4 Turbo. Envia uma pergunta!")

# Mensagens de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = str(update.message.chat_id)

    # Permitir apenas o admin, se definido
    if ADMIN_ID and user_id != ADMIN_ID:
        await update.message.reply_text("Acesso restrito. Este bot é privado.")
        return

    try:
        # Enviar para GPT-4 Turbo
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=500
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Erro na OpenAI: {e}")
        await update.message.reply_text("Ocorreu um erro ao processar tua mensagem.")

# Inicialização do bot
def main():
    if not BOT_TOKEN or not OPENAI_API_KEY:
        logging.error("BOT_TOKEN ou OPENAI_API_KEY não estão definidos no ambiente.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot iniciado com sucesso.")
    app.run_polling()

if __name__ == "__main__":
    main()
