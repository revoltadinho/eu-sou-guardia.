import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configura OpenAI
openai.api_key = OPENAI_API_KEY

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 EuSou Guardiã ativada. Envia tua pergunta e eu responderei com sabedoria.")

# Quando o utilizador envia qualquer mensagem
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "És a Guardiã EuSou, uma IA superinteligente que ajuda com estratégia, finanças e sabedoria universal."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("⚠️ Erro ao comunicar com a IA.")

# Iniciar a aplicação
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ Bot ativo e pronto.")
app.run_polling()

     
