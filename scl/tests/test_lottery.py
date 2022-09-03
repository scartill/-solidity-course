from brownie import Lottery, config, network
from brownie import accounts
from web3 import Web3

# import scripts.helpers as h


targetPriceEth = 0.19
targetPriceWei = 0.19 * 10**18

print(targetPriceWei)


def test_get_entrance_fee():
    # account = h.get_account()
    account = accounts[0]

    net = network.show_active()

    lottery = Lottery.deploy(
        config['networks'][net]['eth_usd_price_feed'],
        {
            'from': account
        }
    )

    ef = lottery.getEntranceFee()
    assert ef > Web3.toWei(0.01, 'ether')
    assert ef < Web3.toWei(0.04, 'ether')
