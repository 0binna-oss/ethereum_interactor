from web3 import Web3 
import config

class Web3Connector:
    def __init__(self, provider_url=config.INFURA_URL):
        self.provider_url = provider_url
        self.web3 = None 

    def connect(self):
        web3 = web3(Web3.HTTPProvider(self.provider_url))
        if web3.isConnected():
            print(f"Connected to Ethereum network at {self.provider_url}")
            return web3
        else:
            raise Exception("Fialed to connect to Ethereum network") 