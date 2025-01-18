from connectors.web3_connector import Web3Connector
from contracts.contract_interactor import ContractInteractor
from events.event_listener import EventListener 

def main():
    # Connect to the Ethereum network
    web3_connector = Web3Connector()
    web3 = web3_connector.connect()

    # load and interact with the smart contract 
    contract_interactor = ContractInteractor(web3)
    contract_interactor.read_data()
    contract_interactor.write_data()

    # Listen for events
    event_listener = EventListener(web3, contract_interactor.contract)
    event_listener.listen_for_events()

if __name__ == "__main__":
    main() 