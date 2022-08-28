from brownie import accounts, config, SimpleStorage, network


def get_account():
    if network.show_active() == 'development':
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


def deploy_simple_storage():
    account = get_account()
    print('Account', account)
    ss = SimpleStorage.deploy({'from': account})
    value = ss.fetch()
    print(value)
    transaction = ss.store(42, {'from': account})
    transaction.wait(1)
    uvalue = ss.fetch()
    print(uvalue)


def main():
    deploy_simple_storage()
