import time
from brownie import Lottery

import scripts.helpers as h


def deploy_lottery():
    vrf = h.netconfig()['vrf_coordinator']
    keyhash = vrf['keyhash']
    callback_gas_limit = vrf['gas_limit']

    lottery = Lottery.deploy(
        h.get_contract('eth_usd_price_feed').address,
        h.get_contract('link_token').address,
        h.get_contract('vrf_coordinator').address,
        keyhash,
        callback_gas_limit,
        h.my(),
        publish_source=h.netconfig().get('verify', False)
    )

    print(f'Deployed lottery of {lottery}')
    return lottery


def start_lottery():
    account = h.get_account()
    lottery = Lottery[-1]
    tx = lottery.startLottery({'from': account})
    tx.wait(1)


def enter_lottery():
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 10000000
    tx = lottery.enter(h.my(value=value))
    tx.wait(1)


def end_lottery():
    lottery = Lottery[-1]

    # Fund the contract with 0.1 LINK
    h.fund_with_link(lottery.address)

    # Fund the oracle
    tx = lottery.topUpSubscription(5 * 10 ** 16, h.my())
    tx.wait(1)

    # Do end lottery
    tx = lottery.endLottery(h.my())
    tx.wait(1)

    state = lottery.getLotteryState()
    print(f'State {state}')

    winner = lottery.recentWinner()
    print(f'Winner is {winner}')

    for _ in range(12):
        print('Waiting for the oracle to respond')
        time.sleep(10)

    state = lottery.getLotteryState()
    print(f'State {state}')

    winner = lottery.recentWinner()
    print(f'Winner is {winner}')


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
