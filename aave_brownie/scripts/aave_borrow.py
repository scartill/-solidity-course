import json
from pathlib import Path
from brownie import Contract, interface
import scripts.helpers as h
from web3 import Web3

from scripts.get_weth import get_weth


NO_REFERRAL = 0
AMOUNT = Web3.toWei(0.005, "ether")


def get_pool():
    abi = json.loads(Path('interfaces/Pool.json').read_text())
    pool_address = h.netconfig()['weth']['pool']
    pool = Contract.from_abi("Pool", pool_address, abi)
    return pool


def approve_erc20(amount, spender, erc20_address, account):
    print('Approving token')
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {'from': account})
    tx.wait(1)
    print('Approved')
    return tx


def main():
    if h.is_localnet():
        get_weth()

    pool = get_pool()
    token_address = h.netconfig()['weth']['token']

    approve_erc20(
        2*AMOUNT,
        pool.address,
        token_address,
        h.get_account()
    )

    pool.supply(token_address, AMOUNT, h.get_account(), 0, h.my())
    print('Deposited')
