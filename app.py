from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mensagem", methods=["POST"])
def mensagem():
    user_input = request.form.get("mensagem")
    resposta = processar(user_input)
    return render_template("index.html", mensagem=user_input, resposta=resposta)

def processar(mensagem):
    # Aqui a IA responde com base em palavras-chave (modo simples)
    if "escus" in mensagem.lower():
        return "A moeda ESCUS está pronta para conquistar o mundo. ✨"
    elif "valor" in mensagem.lower():
        return "O verdadeiro valor vem de dentro. ESCUS é o reflexo disso."
    else:
        return "Sou a Guardiã ESCU. Pergunta-me algo sobre o universo EuSou."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
