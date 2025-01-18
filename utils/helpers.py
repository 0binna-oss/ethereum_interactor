from web3 import Web3 

def to_checksum_address(address):
    return Web3.toChecksumAddress(address) 