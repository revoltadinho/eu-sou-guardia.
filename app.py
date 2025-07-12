from flask import Flask, request
import telegram
import os
from telegram.ext import Dispatcher, CommandHandler

# Inicialização do bot com o token do ambiente
TOKEN = os.environ.get("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

# Inicialização da aplicação Flask
app = Flask(__name__)

# Comando /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="🔆 Bem-vindo, Guardião. A Guardiã EuSou está ativa. Diz-me a tua missão.")

# Rota para definir o webhook (usar apenas uma vez)
@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    bot.set_webhook(url=webhook_url)
    return f"Webhook definido para: {webhook_url}"

# Rota que recebe mensagens do Telegram
@app.route(f"/{TOKEN}", methods=['POST'])
def receive_update():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Configuração do Dispatcher com comandos
from telegram.ext import CallbackContext
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))

# Executar localmente (ignorado no Render)
if __name__ == '__main__':
    app.run(port=5000)

