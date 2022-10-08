from brownie import accounts, config, network


LOCAL_BLOCKCHAIN_ENVS = ['development', 'ganache-local']
FORKED_LOCAL_ENVS = ['mainnet-fork']


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

