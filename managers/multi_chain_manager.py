from web3 import Web3

class MultiChainManager:
    def __init__(self, web3_instance):
        self.web3 = web3_instance 
    
    def switch_network(self, rpc_url):
        # Switch to a new network
        from web3 import Web3 
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        return self.web3.is_connected()
    
    def __init__(self):
        self.networks = {
            "ethereum": {
                "name": "Ethereum Mainnet",
                "rpc_url": "https://mainnet.infura.io/v3/d32168dd945e4a2590094a7c64eb431c"
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
        print(f"Attempting to connect to {network_name} at {rpc_url}") 
       
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))

        if self.web3.is_connected():
            print(f"Connected to {self.networks[network_name]['name']}")
            return self.web3 
        else:
            raise ConnectionError(f"Failed to connect to {self.networks[network_name]['name']}") 