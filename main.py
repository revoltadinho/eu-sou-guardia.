import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

PRIVATE_KEY = os.getenv('PRIVATE_KEY')
RPC_URL = os.getenv('RPC_URL')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.isConnected():
    print("Conectado à blockchain BSC com sucesso!")
else:
    print("Falha na conexão à blockchain.")

# Aqui começa a lógica da IA Guardiã (exemplo inicial)
def main():
    print("IA Guardiã EusouCoin iniciada.")
    # Exemplo: Mostrar saldo da wallet (endereços e lógica a implementar)
    account = w3.eth.account.from_key(PRIVATE_KEY)
    balance = w3.eth.get_balance(account.address)
    print(f"Saldo da wallet: {w3.fromWei(balance, 'ether')} BNB")

if __name__ == "__main__":
    main()
