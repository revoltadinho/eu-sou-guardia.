from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mensagem', methods=['POST'])
def mensagem():
    user_input = request.form.get('mensagem')
    resposta = processar_mensagem(user_input)
    return render_template('index.html', resposta=resposta)

def processar_mensagem(texto):
    if "ESC" in texto:
        return "A ESCU é a moeda que vai mudar o mundo."
    elif "valor" in texto:
        return "Tu és o Guardião do Valor. ESCU reflete isso."
    else:
        return "Sou a Guardiã ESCU, pronta para te guiar no universo EuSou."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
