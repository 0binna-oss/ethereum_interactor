import config 
from connectors.web3_connector import Web3Connector
from contracts.contract_interactor import ContractInteractor
from events.event_listener import EventListener 

def main():
    # Validate the configuration 
    try:
        config.validate_config()

        # Connect to the Ethereum network 
        connector = Web3Connector(config.INFURA_URL)
        web3_instance = connector.connect() 

        # Confirmation message
        print("Ethereum connection established. Ready to interact")
    
    except ValueError as config_error:
        print(f"Configuration Error: {config_error}")
    except ConnectionError as connection_error:
        print(f"Connection Error: {connection_error}")

if __name__ == "__main__":
    main() 