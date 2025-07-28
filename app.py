import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Variáveis de ambiente
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Inicializar OpenAI
openai.api_key = OPENAI_API_KEY

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Eu sou a Guardiã GPT-4 Turbo. Envia-me uma pergunta.")

# Comando /perguntar + mensagem
async def perguntar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta = " ".join(context.args)
    if not pergunta:
        await update.message.reply_text("Por favor, escreve uma pergunta depois do comando /perguntar.")
        return

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": pergunta}]
    )

    resposta = response.choices[0].message.content.strip()
    await update.message.reply_text(resposta)

# Inicializar aplicação Telegram
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("perguntar", perguntar))

    print("Bot iniciado com sucesso!")
    app.run_polling()
