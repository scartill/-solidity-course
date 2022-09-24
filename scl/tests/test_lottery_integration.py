import scripts.helpers as h
import scripts.deploy as d
import pytest
import time


def test_can_pick_winner():
    if h.is_localnet():
        pytest.skip()

    account = h.get_account()
    lottery = d.deploy_lottery()

    lottery.startLottery(h.my())
    fee = lottery.getEntranceFee()

    lottery.enter({'from': account, 'value': fee})

    h.fund_with_link(lottery.address, amount=6 * 10 ** 18)
    lottery.topUpSubscription(5 * 10 ** 18, h.my())

    lottery.endLottery(h.my())

    for _ in range(12):
        print('Waiting for the oracle to respond')
        time.sleep(10)

    assert lottery.recentWinner() == h.get_account()
