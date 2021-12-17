from brownie import(
    accounts,
    config,
    network,
    MockV3Aggregator
)

from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 2000 * 10**10
LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache-cli-local"
]


def get_account():
    print("Getting account")

    _network = network.show_active()
    print(f"The active network is {_network}")

    if _network in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        account = config["wallets"][_network]["primary_public_key"]
    else:
        account = accounts.add(config["wallets"][_network]["primary_private_key"])

    print(f"The active account is {account}")
    return account


def deploy_mocks(account):  
    print("Deploying mocks...")  
    if not len(MockV3Aggregator):
        MockV3Aggregator.deploy(
            DECIMALS,
            Web3.toWei(STARTING_PRICE, "ether"),
            {"from": account}
        )

