import os
from flask import Flask, request
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Eu sou a Guardiã GPT-4 Turbo. Envia-me uma pergunta.")

# Mensagens normais
async def reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Responde como a Guardiã da moeda ESCUS."},
            {"role": "user", "content": user_input}
        ]
    )

    answer = completion.choices[0].message.content
    await update.message.reply_text(answer)

# Configurar o bot
telegram_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
telegram_bot.add_handler(CommandHandler("start", start))
telegram_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_message))

@app.route('/')
def home():
    return "Guardiã GPT-4 Turbo ativa!"

@app.route('/webhook', methods=["POST"])
def webhook():
    telegram_bot.update_queue.put(Update.de_json(request.get_json(force=True), telegram_bot.bot))
    return "OK"

if __name__ == "__main__":
    telegram_bot.run_polling()

     
 
