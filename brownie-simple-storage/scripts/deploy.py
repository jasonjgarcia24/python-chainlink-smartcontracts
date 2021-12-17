from brownie import(
    accounts,
    config,
    network,
    SimpleStorage
)


def get_account():
    wallets = {
        "development": config["wallets"]["ganache_cli"]["primary_public_key"],
        "rinkeby":     config["wallets"]["rinkeby"]["primary_private_key"],
        "kovan":       config["wallets"]["kovan"]["primary_private_key"],
    }
    _network = network.show_active()
    print(_network)

    return accounts.add(wallets.get(_network))


def deploy_simple_storage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    
    stored_value = simple_storage.retrieve()
    print(stored_value)

    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)  
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def main():
    deploy_simple_storage()
