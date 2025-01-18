import os 
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Configuration variables
INFURA_URL = os.getenv("INFURA_URL", "http://127.0.0.1:8545") 
PRIVATE_KEY = os.getenv("PRIVATE_KEY") 
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS") 
etherscan_api_key=os.getenv("api key")