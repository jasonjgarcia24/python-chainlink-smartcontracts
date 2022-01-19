from scripts.utils import get_account, FORKED_LOCAL_ENVIRONMENTS
from scripts.get_weth import get_weth
from web3 import Web3


from brownie import interface, config, network

NETWORK = network.show_active()
AMOUNT = Web3.toWei(0.1, "ether")


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][NETWORK]["lending_pool_addresses_provider"]
    )

    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)

    return lending_pool


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!!!")

    return tx


def main():
    account = get_account(verbose=True)
    erc20_address = config["networks"][NETWORK]["weth_token"]

    if NETWORK in FORKED_LOCAL_ENVIRONMENTS:
        get_weth()

    lending_pool = get_lending_pool()
    print(f"Lending pool: {lending_pool.address}")

    # Approve sending out ERC20 tokens
    approve_erc20(AMOUNT, lending_pool.address, erc20_address, account)

    print("Depositing ERC20 token...")
    tx = lending_pool.deposit(
        erc20_address, AMOUNT, account, 0, {"from": account}
    )
    tx.wait(1)

    print("Deposited!!!")
