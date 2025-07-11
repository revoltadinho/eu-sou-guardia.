mport os
from web3 import Web3
from dotenv import load_dotenv
import requests
from flask import Flask, request

# Carregar variáveis de ambiente
load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Conectar à blockchain
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Verificar conexão
if w3.is_connected():
    print("✅ Conectado à blockchain BSC com sucesso!")
else:
    print("❌ Falha na conexão à blockchain.")

# Inicializar Flask app
app = Flask(__name__)

# Função principal da IA Guardiã
def main():
    try:
        account = w3.eth.account.from_key(PRIVATE_KEY)
        balance = w3.eth.get_balance(account.address)
        balance_eth = w3.from_wei(balance, 'ether')
        message = f"🚀 IA Guardiã ativa!\nWallet: {account.address}\nSaldo: {balance_eth} BNB"
        print(message)
        send_telegram(message)
    except Exception as e:
        send_telegram(f"Erro: {str(e)}")

# Enviar mensagens para o Telegram
def send_telegram(text):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
        requests.post(url, json=payload)

# Rota principal
@app.route("/")
def home():
    main()
    return "🛡️ Guardiã está ativa!"

# Endpoint para mensagens do Telegram (opcional)
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        texto = data["message"].get("text", "")
        if texto.lower() == "/status":
            try:
                account = w3.eth.account.from_key(PRIVATE_KEY)
                balance = w3.eth.get_balance(account.address)
                balance_eth = w3.from_wei(balance, 'ether')
                reply = f"💎 Status da wallet:\n{account.address}\nSaldo: {balance_eth} BNB"
            except:
                reply = "❌ Erro ao obter saldo."
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": chat_id, "text": reply})
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
