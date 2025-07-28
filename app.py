import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá, Guardião. Estou pronto.")

# Comando /gpt
async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = ' '.join(context.args)
    if not user_message:
        await update.message.reply_text("Escreve algo depois de /gpt")
        return
    await update.message.reply_text(f"Recebi: {user_message} (GPT será integrado em breve...)")

# Rota web padrão para manter o Render acordado
@app.route('/')
def index():
    return 'Bot Guardião ativo.'

# Inicializar o bot corretamente com async
async def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gpt", gpt))
    await application.run_polling()

# Executar o bot no background (async)
import asyncio
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

   
