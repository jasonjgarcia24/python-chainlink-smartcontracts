import json
import os

from web3 import Web3

from pathlib import Path
from dotenv import dotenv_values
from solcx import compile_standard


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ABI_DIR = lambda fn: os.path.join(BASE_DIR, f"artifacts\\{fn}")
CONTRACTS_DIR = lambda fn: os.path.join(BASE_DIR, f"contracts\\{fn}")

# Load environment variables.
config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

# Read in contract
with open(CONTRACTS_DIR("SimpleStorage.sol"), "r") as file:
    simple_storage_file = file.read()

# Compile our solidity contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# Save our generated abi file
with open(ABI_DIR("compiled_code.json"), "w") as file:
    json.dump(compiled_sol, file)


bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider(config["GANACHE_RPC_URL"]))
chain_id = int(config["GANACHE_CHAIN_ID"])
my_public_address = config["GANACHE_1_PUBLIC_KEY"]
my_private_address = config["GANACHE_1_PRIVATE_KEY"]

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_public_address)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_public_address,
        "nonce": nonce,
    }
)

signed_transaction = w3.eth.account.sign_transaction(
    transaction,
    private_key=my_private_address
)
