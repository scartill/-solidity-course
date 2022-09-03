from brownie import FundMe, network, config
from scripts.helpers import get_account, deploy_mocks


def deploy_fund_me():
    net = network.show_active()
    price_feed = deploy_mocks()
    account = get_account()
    print('Account', account)
    txn = {'from': account}

    fm = FundMe.deploy(
        price_feed, txn,
        publish_source=config['networks'][net].get('verify')
    )

    print(f'Contract deployed at {fm.address}')
    return fm


def main():
    deploy_fund_me()
