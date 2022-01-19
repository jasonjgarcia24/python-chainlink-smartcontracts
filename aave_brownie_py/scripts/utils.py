from brownie import network, config, accounts

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-cli-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]


def _print(verbose, x):
    if verbose:
        print(x)


def get_account(index=None, id=None, verbose=False):
    _network = network.show_active()
    _print(verbose, f"Network: {_network}")

    if _network in LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIRONMENTS:
        key = "primary_public_key"
        account = config["wallets"][_network][key]
    else:
        key = "primary_private_key"
        account = accounts.add(config["wallets"][_network][key])

    _print(verbose, f"Account used: {account}")

    return account
