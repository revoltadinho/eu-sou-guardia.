import os
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get sensitive data from .env
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Connect to blockchain
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Check connection
if w3.is_connected():
    print("✅ Conectado à blockchain BSC com sucesso!")
else:
    print("❌ Falha na conexão à blockchain.")

# Main logic
def main():
    print("🔐 IA Guardiã EusouCoin iniciada.")
    
    # Get wallet address from private key
    account = w3.eth.account.from_key(PRIVATE_KEY)
    balance = w3.eth.get_balance(account.address)

    # Show balance in BNB
    print(f"💰 Saldo da wallet: {w3.from_wei(balance, 'ether')} BNB")

if __name__ == "__main__":
    main()
