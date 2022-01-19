from brownie import network, config, accounts

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-cli-local"]


def get_account():
    print("Getting account")

    _network = network.show_active()
    print(_network)

    if _network in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        key = "primary_public_key"
        print(key)
        account = config["wallets"][_network][key]
    else:
        key = "primary_private_key"
        print(key)
        account = accounts.add(config["wallets"][_network][key])

    return account
