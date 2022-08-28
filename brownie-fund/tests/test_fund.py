import pytest
from brownie import accounts
from scripts.helpers import get_account, is_localnet
from scripts.deploy import deploy_fund_me


def test_can_fund_and_withdraw():
    account = get_account()
    fm = deploy_fund_me()
    entrance_fee = fm.getEntranceFee()

    tx = fm.fund({
        'from': account,
        'value': entrance_fee
    })

    tx.wait(1)
    assert fm.getFund(account) == entrance_fee

    tx2 = fm.withdraw({'from': account})
    tx2.wait(1)
    assert fm.getFund(account) == 0


def test_only_owner_can_withdraw():
    if not is_localnet():
        pytest.skip('only for local testing')

    fund_me = deploy_fund_me()
    bad_actor = accounts.add()

    with pytest.raises(ValueError):
        fund_me.withdraw({'from': bad_actor})
