from brownie import SimpleStorage


def read_contract():
    ss = SimpleStorage[-1]
    val = ss.fetch()
    print(val)


def main():
    read_contract()
