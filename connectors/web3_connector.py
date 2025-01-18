from web3 import Web3 
import config

class Web3Connector:
    def __init__(self, provider_url=config.INFURA_URL):
        self.provider_url = provider_url
        self.web3 = None 

    def connect(self):
        try:
            self.web3 = Web3(Web3.HTTPProvider(self.provider_url))
            if self.web3.is_connected():
                print(f"Connected to Ethereum network at {self.provider_url}")
                return self.web3
            else:
                raise Exception("Failed to connect to Ethereum network")
        except Exception as e:
            raise Exception(f"Connection error: {str(e)}")