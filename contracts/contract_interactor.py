import json
import requests
import asyncio
from pathlib import Path
from typing import Dict, Any
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from web3.exceptions import ContractLogicError
import config

class ContractInteractor:
    def __init__(self, web3: Web3):
        self.web3 = web3
        self.contracts = {}
        self.contract_address = config.CONTRACT_ADDRESS
        self.abi = self._load_abi("contracts/abi/my_contract.json")
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)
        self.web3.eth.default_account = self.get_account_address()

    @staticmethod
    def _load_abi(filepath: str):
        try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"ABI file not found: {filepath}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in ABI file: {filepath}")

    def read_data(self, contract_name: str, function_name: str, *args):
        """Read data from contract."""
        try:
            contract = self.get_contract(contract_name)
            function = getattr(contract.functions, function_name)
            return function(*args).call()
        except ContractLogicError as e:
            raise ValueError(f"Contract logic error: {e}")
        except Exception as e:
            raise Exception(f"Error reading contract data: {e}")

    def write_data(self, contract_name: str, function_name: str, *args):
        """Write data to a smart contract."""
        try:
            if not config.PRIVATE_KEY:
                raise ValueError("Private key is not configured. Please set the private key in the config.")

            contract = self.get_contract(contract_name)
            if not hasattr(contract.functions, function_name):
                raise ValueError(f"The function '{function_name}' does not exist in contract '{contract_name}'.")

            function = getattr(contract.functions, function_name)
            gas_estimate = function(*args).estimate_gas({'from': self.get_account_address()})
            nonce = self.web3.eth.get_transaction_count(self.get_account_address())
            gas_price = self.web3.eth.generate_gas_price() or self.web3.to_wei('20', 'gwei')

            transaction = function(*args).build_transaction({
                'from': self.get_account_address(),
                'nonce': nonce,
                'gas': int(gas_estimate * 1.2),
                'gasPrice': gas_price
            })

            signed_txn = self.web3.eth.account.sign_transaction(transaction, config.PRIVATE_KEY)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return receipt

        except ContractLogicError as e:
            raise ValueError(f"Contract logic error during '{function_name}' execution: {e}")
        except ValueError as e:
            raise ValueError(f"Validation error: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error while writing to contract '{contract_name}': {e}")

    def _load_contracts(self):
        """Load all contract ABIs and addresses."""
        try:
            contracts_dir = Path("contracts/abi")
            if not contracts_dir.exists():
                raise FileNotFoundError(f"Contracts directory not found: {contracts_dir}")

            for contract_file in contracts_dir.glob("*.json"):
                with open(contract_file, 'r') as f:
                    contract_data = json.load(f)
                    contract_name = contract_file.stem
                    self.contracts[contract_name] = {
                        'abi': contract_data.get('abi'),
                        'address': contract_data.get('address'),
                        'bytecode': contract_data.get('bytecode')
                    }
        except Exception as e:
            raise Exception(f"Error loading contracts: {e}")

    def estimate_gas(self, contract_name: str, function_name: str, *args) -> Dict[str, Any]:
        """Estimate gas cost for a contract function."""
        try:
            contract = self.get_contract(contract_name)
            function = getattr(contract.functions, function_name)
            gas_estimate = function(*args).estimate_gas({'from': self.get_account_address()})
            gas_price = self.web3.eth.generate_gas_price()
            gas_cost_wei = gas_estimate * gas_price
            gas_cost_eth = self.web3.from_wei(gas_cost_wei, 'ether')
            return {
                'gas_estimate': gas_estimate,
                'gas_price_gwei': self.web3.from_wei(gas_price, 'gwei'),
                'total_cost_eth': gas_cost_eth
            }
        except Exception as e:
            raise Exception(f"Error estimating gas: {e}")

    def deploy_contract(self, contract_name: str, *constructor_args):
        """Deploy a new contract."""
        try:
            if contract_name not in self.contracts:
                raise ValueError(f"Contract {contract_name} not found")

            contract_data = self.contracts[contract_name]
            if not contract_data.get('bytecode'):
                raise ValueError(f"Bytecode not found for contract {contract_name}")

            contract = self.web3.eth.contract(
                abi=contract_data['abi'],
                bytecode=contract_data['bytecode']
            )
            construct_txn = contract.constructor(*constructor_args).build_transaction({
                'from': self.get_account_address(),
                'nonce': self.web3.eth.get_transaction_count(self.get_account_address()),
            })
            gas_estimate = self.web3.eth.estimate_gas(construct_txn)
            construct_txn['gas'] = int(gas_estimate * 1.2)
            signed_txn = self.web3.eth.account.sign_transaction(construct_txn, config.PRIVATE_KEY)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            contract_data['address'] = tx_receipt['contractAddress']
            self._save_contract_data(contract_name, contract_data)
            return tx_receipt
        except Exception as e:
            raise Exception(f"Error deploying contract: {e}")

    def verify_contract(self, contract_name: str):
        """Verify contract on Etherscan."""
        try:
            if not config.ETHERSCAN_API_KEY:
                raise ValueError("Etherscan API key not configured")

            contract_data = self.contracts.get(contract_name)
            if not contract_data:
                raise ValueError(f"Contract {contract_name} not found")

            api_url = "https://api.etherscan.io/api"
            params = {
                "apikey": config.ETHERSCAN_API_KEY,
                "module": "contract",
                "action": "verifysourcecode",
                "contractaddress": contract_data['address'],
                "sourceCode": json.dumps(contract_data.get('sourceCode', '')),
                "contractname": contract_name,
                "compilerversion": "v0.8.19+commit.7dd6d404",
                "optimizationUsed": 1
            }
            response = requests.post(api_url, data=params)
            result = response.json()
            if result["status"] != "1":
                raise ValueError(f"Verification failed: {result['result']}")
            return result["result"]
        except Exception as e:
            raise Exception(f"Error verifying contract: {e}")

    def get_contract(self, contract_name: str):
        """Get contract instance by name."""
        try:
            if contract_name not in self.contracts:
                raise ValueError(f"Contract {contract_name} not found")

            contract_data = self.contracts[contract_name]
            if not contract_data.get('address'):
                raise ValueError(f"Contract {contract_name} not deployed")

            return self.web3.eth.contract(
                address=contract_data['address'],
                abi=contract_data['abi']
            )
        except Exception as e:
            raise Exception(f"Error getting contract: {e}")

    def get_account_address(self) -> str:
        """Get account address from private key."""
        if not config.PRIVATE_KEY:
            raise ValueError("Private key not configured")
        return Account.from_key(config.PRIVATE_KEY).address

    def _save_contract_data(self, contract_name: str, contract_data: dict):
        """Save contract data to JSON file."""
        try:
            contract_path = Path("contracts/abi") / f"{contract_name}.json"
            with open(contract_path, 'w') as f:
                json.dump(contract_data, f, indent=4)
        except Exception as e:
            raise Exception(f"Error saving contract data: {e}")

    async def watch_events(self, contract_name: str, event_name: str):
        """Watch for contract events."""
        try:
            contract = self.get_contract(contract_name)
            event = getattr(contract.events, event_name)
            event_filter = event.create_filter(fromBlock='latest')
            while True:
                for event in event_filter.get_new_entries():
                    print(f"New {event_name} event: {event}")
                await asyncio.sleep(2)
        except Exception as e:
            raise Exception(f"Error watching events: {e}")
