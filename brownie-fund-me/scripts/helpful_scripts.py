from brownie import accounts, config, network, MockV3Aggregator

from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-cli-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-forked", "mainnet-forked-dev"]


def get_account(actor="GOOD"):
    print("Getting account")

    _network = network.show_active()
    print(f"The active network is {_network}")

    if (
        _network in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        key = "primary_public_key" if actor == "GOOD" else "secondary_public_key"
        print(key)
        account = config["wallets"][_network][key]
    else:
        key = "primary_private_key" if actor == "GOOD" else "secondary_private_key"
        print(key)
        account = accounts.add(config["wallets"][_network][key])

    print(f"The active account is {account}")
    return account


def deploy_mocks(account):
    print("Deploying mocks...")
    if not len(MockV3Aggregator):
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": account}
        )
