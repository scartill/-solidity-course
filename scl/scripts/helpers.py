from brownie import accounts, config, network, Contract, interface
from brownie import MockV3Aggregator, VRFCoordinatorV2Mock, MockLinkToken


LOCAL_BLOCKCHAIN_ENVS = ['development', 'ganache-local']
FORKED_LOCAL_ENVS = ['mainnet-fork']

FEED_DECIMALS = 8
FEED_STARTING_PRICE = 200000000000

VRF_BASE_FEE = 100000
VRF_GAS_PRICE_LINK = 100000

CONTRACTS = {
    'eth_usd_price_feed': {
        'type': interface.AggregatorV2V3Interface,
        'mocktype': MockV3Aggregator
    },

    'vrf_coordinator': {
        'type': interface.VRFCoordinatorV2Interface,
        'mocktype': VRFCoordinatorV2Mock
    },

    'link_token': {
        'type': interface.LinkTokenInterface,
        'mocktype': MockLinkToken
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


def my(value=None):
    account = get_account()
    tx_data = {'from': account}

    if value:
        tx_data.update({'value': value})

    return tx_data


def netconfig():
    return config['networks'][network.show_active()]


def get_contract(contract_name):

    if not is_localnet():
        contract_type = CONTRACTS[contract_name]['type']
        contract_address = netconfig()[contract_name]['address']
        contract = contract_type(contract_address)
        return contract
    else:
        contract_type = CONTRACTS[contract_name]['mocktype']
        if len(contract_type) <= 0:
            deploy_mocks()

        return contract_type[-1]


def deploy_mocks():
    net = network.show_active()

    print(f'Active network is {net}')
    if not is_localnet():
        price_feed = config['networks'][net]['eth_usd_price_feed']
    else:
        print('Deploying moke-ups')

        if len(MockV3Aggregator) <= 0:
            MockV3Aggregator.deploy(
                FEED_DECIMALS, FEED_STARTING_PRICE,
                my()
            )

        price_feed = MockV3Aggregator[-1].address
        print(f'Price feed moke up deployed at {price_feed}')

        if len(VRFCoordinatorV2Mock) <= 0:
            VRFCoordinatorV2Mock.deploy(
                VRF_BASE_FEE,
                VRF_GAS_PRICE_LINK,
                my()
            )

        vrf = VRFCoordinatorV2Mock[-1].address
        print(f'VRF moke up deployed at {vrf}')

        if len(MockLinkToken) <= 0:
            MockLinkToken.deploy(my())

        lt = MockLinkToken[-1].address
        print(f'Link Token moke up deployed at {lt}')


def fund_with_link(
    contract_address,
    account=None,
    link_token=None,
    amount=100000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, my())
    tx.wait(1)
    print(f'Funded contract {contract_address}')
