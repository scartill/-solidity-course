from brownie import SimpleStorage, accounts


def test_deploy():
    account = accounts[0]
    ss = SimpleStorage.deploy({'from': account})
    sv = ss.fetch()
    assert sv == 0


def test_updating_storage():
    account = accounts[0]
    ss = SimpleStorage.deploy({'from': account})
    expected = 41
    ss.store(expected, {'from': account})

    assert expected == ss.fetch()
