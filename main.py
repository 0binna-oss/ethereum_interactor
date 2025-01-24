import sys 
import config 
from web3 import Web3
from connectors.web3_connector import Web3Connector
from contracts.contract_interactor import ContractInteractor
from events.event_listener import EventListener 
from wallet.wallet_manager import WalletManager 
from defi.defi_manager import DefiManager 
from managers.multi_chain_manager import MultiChainManager 

def main():
    default_network_name = input("Enter the default network (ethereum/polygon/bsc): ").lower()

    networks = {
        "ethereum": "https://mainnet.infura.io/v3/d32168dd945e4a2590094a7c64eb431c",
        "polygon": "https://polygon-rpc.com", 
        "bsc": "https://bsc-dataseed.binance.org/"
    }

    if default_network_name not in networks:
        print(f"Network {default_network_name} is not supported.")
        return 
    
    rpc_url = networks[default_network_name] 
    Web3_instance = Web3(Web3.HTTPProvider(rpc_url))

    if not Web3_instance.is_connected():
        print("Failed to connect to the Ethereum Mainnet. Please check your RPC URL.")
        return 

    print("Successfully connected to Ethereum Mainnet.")

    multi_chain_manager = MultiChainManager() 

    network_name = input("Enter the network name (ethereum/polygon/bsc): ").lower()
    try:
        Web3_instance = multi_chain_manager.connect_to_network(network_name)
        print(f"Connected to {network_name}.")
    except (ValueError, ConnectionError) as e:
        print(f"Error: {e}")

def main():
    multi_chain_manager = MultiChainManager()
    print("Available networks: ethereum, polygon, bsc")
    network_name = input("Enter the network you want to connect to: ")
    web3_instance = multi_chain_manager.connect_to_network(network_name)

    # Initialize managers
    wallet_manager = WalletManager(web3_instance)
    defi_manager = DefiManager(web3_instance)
    multi_chain_manager = MultiChainManager()

    # User menu
    while True:
        print("\nOptions:")
        print("1. Create Wallet")
        print("2. Import wallet")
        print("3. Display Balance")
        print("4. Get Token Balance (Defi)")
        print("5. Swap tokens (Defi)")
        print("6. Exit") 

        choice = input("Enter your choice: ")
        if choice == "1":
            wallet_manager.create_wallet()
        elif choice == "2":
            private_key = input("Enter your private key: ")
            wallet_manager.import_wallet(private_key)
        elif choice == "3":
            address = input("Enter wallet address: ")
            wallet_manager.get_balance(address)
        elif choice == "4":
            address = input("Enter wallet address: ")
            token_address = input("Enter token contract address: ")
            balance = defi_manager.get_token_balance(address, token_address)
            print(f"Token Balance: {balance}")
        elif choice == "5":
            # Dummy inputs for token swap
            router = input("Enter router address: ")
            token_in = input("Enter token in address: ")
            token_out = input("Enter token out address: ")
            amount = int(input("Enter amount to swap: "))
            wallet_address = input("Enter wallet address: ")
            wallet_private_key = input("Enter wallet private key: ")
            wallet = wallet_manager.import_wallet(wallet_private_key)
            defi_manager.swap_tokens(router, token_in, token_out, amount, wallet)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("invalid option. Please try again.") 



if __name__ == "__main__":
    main() 