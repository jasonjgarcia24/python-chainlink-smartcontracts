from brownie import OurToken

from scripts.utils import get_account

from web3 import Web3


def deploy_our_token():
    account = get_account()
    initial_supply = Web3.toWei(100, "ether")

    our_token = OurToken.deploy(initial_supply, {"from": account})

    print(f"Contract deployed to {our_token.address}")

    return our_token


def main():
    deploy_our_token()
