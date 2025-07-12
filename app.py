from flask import Flask, request
import telegram
import os
from telegram.ext import Dispatcher, CommandHandler, Updater

# Token do bot
TOKEN = os.environ.get("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

# Flask App
app = Flask(__name__)

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    bot.set_webhook(url=webhook_url)
    return f"Webhook definido para: {webhook_url}"

@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✨ Guardião conectado com a Guardiã EuSou.")

# Dispatcher
updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))

if __name__ == '__main__':
    app.run(port=5000)
