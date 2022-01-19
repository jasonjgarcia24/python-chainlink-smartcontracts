from scripts.utils import get_account
from brownie import interface, config, network


def get_weth():
    """
    Mints WETH by depositing ETH
    """
    account = get_account()
    weth = interface.IWeth(
        config["networks"][network.show_active()]["weth_token"]
    )  # ABI

    value = 0.1
    tx = weth.deposit({"from": account, "value": value * 10 ** 18})
    tx.wait(1)
    print(f"Received {value} WETH")

    return tx


def main():
    get_weth()
