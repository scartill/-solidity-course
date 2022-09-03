from brownie import accounts, config, network, Contract
from brownie import MockV3Aggregator, VRFCoordinatorV2Mock


LOCAL_BLOCKCHAIN_ENVS = ['development', 'ganache-local']
FORKED_LOCAL_ENVS = ['mainnet-fork']

DECIMALS = 8
STARTING_PRICE = 200000000000

CONTRACTS = {
    'eth_usd_price_feed': {
        'type': MockV3Aggregator
    },

    'vrf_coordinator': {
        'type': VRFCoordinatorV2Mock
    }
}


def is_localnet():
    return network.show_active() in LOCAL_BLOCKCHAIN_ENVS


def is_fork():
    return network.show_active() in FORKED_LOCAL_ENVS


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if is_localnet() or is_fork():
        return accounts[0]

    return accounts.add(config['wallets']['from_key'])


def netconfig():
    return config['networks'][network.show_active()]


def get_contract(contract_name):
    contract_type = CONTRACTS[contract_name]['type']

    if is_localnet() and len(contract_type) <= 0:
        deploy_mocks()
    else:
        contract_address = netconfig()[contract_name]['address']

        contract = Contract.from_abi(
            contract_type._name,
            contract_address,
            contract_type.abi
        )

        return contract

    contract = contract_type[-1]


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
                {'from': account}
            )

        price_feed = MockV3Aggregator[-1].address
        print(f'Moke up deployed at {price_feed}')

    return price_feed
