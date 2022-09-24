from brownie import exceptions
from web3 import Web3
from scripts.deploy import deploy_lottery
import scripts.helpers as h
import pytest


def test_get_entrance_fee():
    if not h.is_localnet():
        pytest.skip()

    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    expected_entrance_fee = Web3.toWei(0.025, "ether")

    assert entrance_fee == expected_entrance_fee


def test_cant_enter_unless_started():
    if not h.is_localnet():
        pytest.skip()

    lottery = deploy_lottery()

    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter(h.my(lottery.getEntranceFee()))


def test_can_start_and_enter():
    if not h.is_localnet():
        pytest.skip()

    lottery = deploy_lottery()
    lottery.startLottery(h.my())
    lottery.enter(h.my(lottery.getEntranceFee()))

    assert lottery.getPlayer(0) == h.get_account()


def test_can_end_lottery():
    if not h.is_localnet():
        pytest.skip()

    lottery = deploy_lottery()
    lottery.startLottery(h.my())
    lottery.enter(h.my(lottery.getEntranceFee()))
    h.fund_with_link(lottery.address)
    lottery.endLottery(h.my())
    assert lottery.getLotteryState() == 2


def test_can_pick_winner():
    if not h.is_localnet():
        pytest.skip()

    account = h.get_account()
    lottery = deploy_lottery()

    lottery.startLottery(h.my())
    fee = lottery.getEntranceFee()

    lottery.enter({'from': account, 'value': fee})
    other_acc_1 = h.get_account(index=1)
    lottery.enter({'from': other_acc_1, 'value': fee})
    other_acc_2 = h.get_account(index=2)
    lottery.enter({'from': other_acc_2, 'value': fee})

    h.fund_with_link(lottery.address, amount=6 * 10 ** 18)
    lottery.topUpSubscription(5 * 10 ** 18, h.my())

    starting_winner_balance = account.balance()
    lottery_balance = lottery.balance()

    tx = lottery.endLottery(h.my())
    requestId = tx.events['RequestedRandomness']['requestId']

    coordinator = h.get_contract("vrf_coordinator")
    coordinator.fulfillRandomWordsWithOverride(
        requestId,
        lottery.address,
        [777],
        h.my()
    )

    assert lottery.recentWinner() == h.get_account()
    assert lottery.balance() == 0
    assert account.balance() == starting_winner_balance + lottery_balance
