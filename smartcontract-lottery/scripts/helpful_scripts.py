from brownie import (
    accounts,
    config,
    network,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
    interface,
)
from brownie.network import account
from toolz.itertoolz import interleave

from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-cli-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-forked", "mainnet-forked-dev"]


def get_account(index=None, id=None, actor="GOOD"):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")

    print("Getting account")

    _network = network.show_active()
    print(f"The active network is {_network}")

    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if (
        _network in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or _network in FORKED_LOCAL_ENVIRONMENTS
    ):
        key = "primary_public_key" if actor == "GOOD" else "secondary_public_key"
        print(key)
        account = accounts.at(config["wallets"][_network][key])
    else:
        key = "primary_private_key" if actor == "GOOD" else "secondary_private_key"
        print(key)
        account = accounts.add(config["wallets"][_network][key])

    print(f"The active account is {account}")
    return account


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config if defined.
    Otherwise, it will deploy a mock version of that contract, and return that mock contract.

        Args:
            contract_name (string)

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed version of this
            contract.
    """
    _network = network.show_active()
    contract_type = contract_to_mock[contract_name]
    if _network in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()

        contract = contract_type[-1]
    else:
        contract_address = config["networks"][_network][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract


DECIMALS = 8
INITIAL_VALUE = 2000 * 10 ** DECIMALS


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=1 * 10 ** 17
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")

    tx = link_token.transfer(contract_address, amount, {"from": account})

    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})

    tx.wait(1)
    print("Funded contract!")
    return tx
