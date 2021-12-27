import pytest

from brownie import accounts, config, network, exceptions, reverts

from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100

    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)

    assert fund_me.addressToAmountFunded(account) == entrance_fee

    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)

    assert fund_me.addressToAmountFunded(account) == 0


def test_only_owner_can_withdraw():
    account = get_account()
    _network = network.show_active()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100

    tx1 = fund_me.fund({"from": account, "value": entrance_fee})
    tx1.wait(1)

    if _network not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")

    bad_actor = get_account(actor="BAD")

    with reverts("You are not authorized."):
        tx2 = fund_me.withdraw({"from": bad_actor})
        tx2.wait(1)
