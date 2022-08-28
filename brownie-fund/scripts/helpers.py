from brownie import accounts, config, network
from brownie import MockV3Aggregator


LOCAL_BLOCKCHAIN_ENVS = ['development', 'ganache-local']

DECIMALS = 8
STARTING_PRICE = 200000000000


def is_localnet():
    return network.show_active() in LOCAL_BLOCKCHAIN_ENVS


def get_account():
    if is_localnet():
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


def deploy_mocks():
    account = get_account()
    net = network.show_active()

    print(f'Active network is {net}')
    if not is_localnet():
        price_feed = config['networks'][net]['eth_usd_price_feed']
    else:
        print('Deploying moke up')

        if len(MockV3Aggregator) <= 0:
            MockV3Aggregator.deploy(
                DECIMALS, STARTING_PRICE,
                {'from': account})

        price_feed = MockV3Aggregator[-1].address
        print(f'Moke up deployed at {price_feed}')

    return price_feed
