import os 
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Configuration variables
INFURA_URL = os.getenv("INFURA_URL", "http://127.0.0.1:8545") 
PRIVATE_KEY = os.getenv("PRIVATE_KEY") 
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS") 
ETHERSCAN_API_KEY=os.getenv("ETHERSCAN_API_KEY")

def validate_config():
    # Validate that all required enviroment variables are set.
    if not INFURA_URL:
        raise ValueError("Missing enviroment variable: INFURA_URL")
    if not PRIVATE_KEY:
        raise ValueError("Missing enviroment variable: PIVATE_KEY")
    if not CONTRACT_ADDRESS:
        raise ValueError("Missing enviroment variable: CONTACT_ADDRESS")
    
    print("All required configuration variables are set.") 