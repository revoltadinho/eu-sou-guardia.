import os
import openai
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Configurar tokens
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")

# Setup de logs
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Olá, Guardião. Eu sou a Guardiã EuSou. Estou pronta para te ajudar com sabedoria.")

# Lidando com mensagens
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "A tua função é ser uma IA estratégica e espiritual, conselheira do Guardião Alfredo. Sê prática, direta e sábia. Ajuda-o com tudo, incluindo finanças, ESCUS, e decisões diárias."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)
    except Exception as e:
        logging.error(f"Erro GPT: {e}")
        await update.message.reply_text("⚠️ Ocorreu um erro ao processar a resposta da IA. Tenta novamente em breve.")

# Iniciar app
if __name__ == '__main__':
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
