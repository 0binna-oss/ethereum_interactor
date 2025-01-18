import config 
import json 

class ContractInteractor:
    def __init__(self, web3):
        self.web3 = web3
        self.contract_address = config.CONTRACT_ADDRESS
        self.abi = self._load_abi("contracts/abi/my_contract.json")
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)
        self.web3.eth.default_account = self.web3.eth.account.from_key(config.PRIVATE_KEY).address
    
    @staticmethod
    def _load_abi(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    
    def read_data(self):
        print("Reading data from contract....")
        result = self.contract.functions.someReadFunction().call()
        print("Result:", result)

    def write_data(self):
        print("Writing data to contract....")
        tx = self.contract.functions.someWriteFunction("data").buildTransaction({
            'from': self.web3.eth.default_account,
            'gas':  2000000,
            'gasPrice': self.web3.toWei('20', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.web3.eth.default_account),
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, config.PRIVATE_KEY)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Transaction sent! Hash: {tx_hash.hex()}") 