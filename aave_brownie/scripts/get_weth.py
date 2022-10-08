from pathlib import Path
import json
from brownie import Contract
import scripts.helpers as h


NO_REFERRAL = 0


def get_weth():
    abi = json.loads(Path('interfaces/WETHGateway.json').read_text())
    gateway_address = h.netconfig()['weth']['gateway']
    gateway = Contract.from_abi("WETHGateway", gateway_address, abi)
    pool_address = h.netconfig()['weth']['pool']

    tx = gateway.depositETH(
        pool_address,
        h.get_account(),
        NO_REFERRAL,
        h.my(0.01 * 10**18)
    )

    print('Received 0.1 WETH')
    return tx


def main():
    get_weth()
