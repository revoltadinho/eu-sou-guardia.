import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask

# Flask app para manter a instância ativa
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return 'Bot EuSou Guardiã ativo!'

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👁️ Olá, eu sou a Guardiã EuSou. Estou pronta para te acompanhar.")

# Resposta automática
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    resposta = f"Recebi a tua mensagem: '{texto}'\n🌐 (A integração GPT será ativada a seguir)"
    await update.message.reply_text(resposta)

def main():
    # Variáveis de ambiente
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    # Inicializar aplicação do Telegram
    app = ApplicationBuilder().token(token).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    # Iniciar o bot (em background)
    app.run_polling()

if __name__ == "__main__":
    import threading
    threading.Thread(target=main).start()
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
