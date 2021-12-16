from brownie import (
    accounts,
    config,
    SimpleStorage
)


def read_contract():
    # Get most recent deployment in ./deployment
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve())


def main():
    read_contract()

