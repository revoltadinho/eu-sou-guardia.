import os
from flask import Flask, request
import telegram
import openai

# Inicializar Flask
app = Flask(__name__)

# Ler variáveis de ambiente da Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Inicializar bot Telegram e OpenAI
bot = telegram.Bot(token=TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

@app.route('/')
def index():
    return "Bot EuSou está vivo!"

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    message = update.message.text

    try:
        # Enviar para GPT-4 Turbo
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Erro ao conectar com o GPT-4: {e}"

    # Responder no Telegram
    bot.send_message(chat_id=update.message.chat.id, text=reply)
    return "ok"

if __name__ == "__main__":
    app.run()
