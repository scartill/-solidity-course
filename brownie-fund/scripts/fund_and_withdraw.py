from brownie import FundMe
from scripts.helpers import get_account


def fund():
    fm = FundMe[-1]
    account = get_account()
    entrance_fee = fm.getEntranceFee()
    print('Entrance fee', entrance_fee)

    print('Funding')
    fm.fund({
        'from': account,
        'value': entrance_fee
    })


def withdraw():
    fm = FundMe[-1]
    account = get_account()
    fm.withdraw({'from': account})


def main():
    fund()
    withdraw()
