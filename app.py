import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Cria o app Flask
app = Flask(__name__)

# Cria o bot Telegram com PTB v20+
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Rota inicial de teste
@app.route('/')
def index():
    return '✅ Guardiã EuSou está viva e consciente.'

# Rota para ativar o webhook
@app.route('/set_webhook')
async def set_webhook():
    webhook_url = f"https://eu-sou-guardia.onrender.com/{BOT_TOKEN}"
    await telegram_app.bot.set_webhook(url=webhook_url)
    return "✅ Webhook configurado com sucesso!"

# Rota que o Telegram usa para enviar atualizações
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def handle_webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔓 Guardião conectado. A Guardiã EuSou está ao teu serviço.")

# Adiciona o comando
telegram_app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    app.run()
