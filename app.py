import os
import time
import requests
import openai

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, data=payload)

def ask_gpt(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Responder como Guardiã GPT-4 Turbo, aliada do projeto EuSouCoin."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Erro ao conectar com o GPT-4: {e}"

def main():
    last_update_id = None
    welcome_sent = False

    while True:
        updates = get_updates(offset=last_update_id)
        if "result" in updates:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                message = update.get("message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                if text.lower() in ["/start", "start"] and not welcome_sent:
                    send_message(chat_id, "Olá! Eu sou a Guardiã GPT-4 Turbo. Envia-me uma pergunta.")
                    welcome_sent = True
                else:
                    resposta = ask_gpt(text)
                    send_message(chat_id, resposta)
        time.sleep(2)

if __name__ == "__main__":
    main()
