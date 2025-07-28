import os
import telebot
import openai
from flask import Flask, request

# 🔐 Variáveis de ambiente seguras
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4-turbo")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🛡️ Verificações
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN não encontrado no ambiente!")

if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY não encontrado no ambiente!")

# 🤖 Inicialização do bot
bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# 🌐 App Flask para manter o serviço vivo na Render
app = Flask(__name__)

# 🧠 Função para resposta GPT
def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao conectar ao GPT: {str(e)}"

# 📩 Reage a mensagens
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if str(message.chat.id) != str(ADMIN_ID):
        bot.reply_to(message, "Acesso restrito ao Guardião.")
        return

    resposta = ask_gpt(message.text)
    bot.send_message(message.chat.id, resposta)

# 🌐 Endpoint básico para manter a instância viva
@app.route('/', methods=["GET"])
def index():
    return "EuSou Guardiã online."

# 🔁 Atualizações long polling (funciona na Render Free)
def start_bot():
    print("Iniciando bot EuSou Guardiã...")
    bot.infinity_polling()

if __name__ == '__main__':
    start_bot()

   
