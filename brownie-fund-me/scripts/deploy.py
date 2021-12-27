from brownie import network, config, FundMe, MockV3Aggregator

from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    FORKED_LOCAL_ENVIRONMENTS,
)


def deploy_fund_me():
    _account = get_account()
    _network = network.show_active()
    print(_network)

    # pass the price feed address to our fundme contract

    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    if (
        _network not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or _network in FORKED_LOCAL_ENVIRONMENTS
    ):
        price_feed_address = config["networks"][_network]["eth_usd_price_feed"]
    else:
        deploy_mocks(_account)
        price_feed_address = MockV3Aggregator[-1].address

    publish_source = config["networks"][_network].get("verify")

    fund_me = FundMe.deploy(
        price_feed_address, {"from": _account}, publish_source=publish_source
    )

    print(f"Contract deployed to {fund_me.address}")

    return fund_me


def main():
    deploy_fund_me()
