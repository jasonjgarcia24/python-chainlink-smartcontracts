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
config = dotenv_values(".env")

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
w3 = Web3(Web3.HTTPProvider(config["INFURA_KOVAN_URL_KEY"]))
chain_id = int(config["KOVAN_CHAIN_ID"])
my_public_address = config["PRIMARY_PUBLIC_KEY"]
my_private_address = config["PRIMARY_PRIVATE_KEY"]

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
    transaction, private_key=my_private_address
)

transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

# Working with the contract, you always need
# Cotract Address
# contract ABI
simple_storage = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change
print(simple_storage.functions.retrieve().call())

# Initial value of favoriteNumber
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_public_address,
        "nonce": nonce + 1,
    }
)

signed_store_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=my_private_address
)

send_transaction_hash = w3.eth.send_raw_transaction(
    signed_store_transaction.rawTransaction
)

send_transaction_receipt = w3.eth.wait_for_transaction_receipt(send_transaction_hash)
print(simple_storage.functions.retrieve().call())
