from brownie import accounts, config, SimpleStorage

WALLET = "ganache_cli"


def test_deploy():
    # Arrange
    account = config["wallets"][WALLET]["primary_key"]

    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0

    # Assert
    assert starting_value == expected


def test_updating_storage():
    # Arrange
    account = config["wallets"][WALLET]["primary_key"]
    simple_storage = SimpleStorage.deploy({"from": account})

    # Act
    expected = 15
    simple_storage.store(expected, {"from": account})

    # Assert
    assert expected == simple_storage.retrieve()

