from brownie import OurToken
from web3 import Web3
import scripts.helpers as h

initial_supply = Web3.toWei(1000, "ether")


def main():
    our_token = OurToken.deploy(initial_supply, h.my())
    print(our_token.name())
