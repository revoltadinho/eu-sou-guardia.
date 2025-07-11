from flask import Flask
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Inicialização do Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "IA Guardiã EuSou online e funcional."

# Variáveis de ambiente
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Inicializar Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Verificar conexão com blockchain
if w3.is_connected():
    print("✅ Conectado à blockchain BSC com sucesso.")
else:
    print("❌ Falha na conexão à blockchain.")

# Função principal da IA
def main():
    print("IA Guardiã EuSouCoin iniciada.")
    account = w3.eth.account.from_key(PRIVATE_KEY)
    balance = w3.eth.get_balance(account.address)
    print(f"Saldo da wallet: {w3.from_wei(balance, 'ether')} BNB")

if __name__ == "__main__":
    app.run(debug=True)
