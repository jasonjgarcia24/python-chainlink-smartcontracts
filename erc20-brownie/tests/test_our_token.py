from scripts.deploy import deploy_our_token


def test_can_mint():
    our_token = deploy_our_token()

    assert our_token.name() == "OurToken"
