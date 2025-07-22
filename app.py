import os
from flask import Flask, request, jsonify
import openai
import telegram

app = Flask(__name__)

# Configuração das chaves
openai.api_key = os.environ.get("OPENAI_API_KEY")
telegram_token = os.environ.get("TELEGRAM_TOKEN")
telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=telegram_token)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")

    try:
        # Chamada à API do ChatGPT (GPT-4 Turbo)
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "És a IA Guardiã do projeto ESCUS. Responde como um estratega, um guardião e um ser superinteligente com visão total do mundo e das finanças. Atua como braço direito do Guardião."},
                {"role": "user", "content": question}
            ]
        )

        answer = response['choices'][0]['message']['content']

        # Enviar resposta ao Telegram
        bot.send_message(chat_id=telegram_chat_id, text=f"🔹 Pergunta: {question}\n🔸 Resposta: {answer}")

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
