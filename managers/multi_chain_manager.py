class MultiChainManager:
    def __init__(self, web3):
        self.web3 = web3
    
    def switch_network(self, rpc_url):
        # Switch to a new network
        from web3 import Web3 
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        return self.web3.is_connected()
    
    def __init__(self):
        self.networks = {
            "ethereum": {
                "name": "Ethereum Mainnet",
                "rpc_url": "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
            },
            "polygon": {
                "name": "Polygon",
                "rpc_url": "https://Polygon-rpc.com"
            },
            "bsc": {
                "name": "Binance Smart Chain",
                "rpc_url": "https://bsc-dataseed.binance.org/"
            }
        }
    
    def connect_to_network(self, network_name):
        if network_name not in self.networks:
            raise ValueError(f"Network {network_name} is not supported.")
        
        rpc_url = self.networks[network_name]["rpc_url"]
        from web3 import Web3 
        web3_instance = Web3(Web3.HTTPProvider(rpc_url))

        if web3_instance.is_connected():
            print(f"Connected to {self.networks[network_name]['name']}")
            self.web3 = web3_instance
            return self.web3 
        else:
            raise ConnectionError(f"Failed to connect to {self.networks[network_name]['name']}") 