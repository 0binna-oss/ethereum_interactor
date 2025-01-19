import os 
from web3 import Web3
from cryptography.fernet import Fernet

class WalletManager:
    def __init__(self, web3_instance):
        self.web3 = web3_instance
    
    def create_wallet(self):
        wallet = self.web3.eth.account.create()
        print(f"New Wallet Address: {wallet.address}")
        print(f"Private Key: {wallet.key.hex()}")
        return wallet 
    
    def import_wallet(self, private_key):
        account = self.web3.eth.account.privateKeyToAccount(private_key)
        print(f"Imported Wallet Address: {account.address}")
        return account 
    
    def get_balance(self, address):
        balance = self.web3.eth.get_balance(address)
        eth_balance = self.web3.fromWei(balance, 'ether')
        print(f"Balance of {address}: {eth_balance} ETH")
        return eth_balance 
    
    def export_wallet_to_file(self, wallet, filename="wallet.txt"):
        with open(filename, 'w') as file:
            file.write(f"Address: {wallet.address}\n")
            file.write(f"Private Key: {wallet.key.hex()}\n")
        print(f"Wallet exported to {filename}")
    
    def encrypt_private_key(self, private_key, encryption_key):
        cipher = Fernet(encryption_key)
        encrypted_key = cipher.encrypt(private_key.encode())
        print("Private key encrypted successfully")

    def decrypt_private_key(self, encrypted_key, encryption_key):
        cipher = Fernet(encryption_key)
        private_key = cipher.decrypt(encrypted_key).decode()
        print("Private Key decrypted successfully")
        return private_key 
    
    @staticmethod
    def generate_encryption_key():
        key = Fernet.generate_key()
        print("Encryption key generated")
        return key 