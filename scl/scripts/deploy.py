from brownie import Lottery

import scripts.helpers as h


def deploy_lottery():
    account = h.get_account(id='tutoria-acc')
    vrf = h.netconfig()['vrf']
    subscription_id = vrf['subscription']
    keyhash = vrf['keyhash']
    callback_gas_limit = vrf['gas_linit']

    lottery = Lottery(
        h.get_contract('eth_usd_price_feed').address,
        h.get_contract('vrf_coordinator').address,
        subscription_id,
        keyhash,
        callback_gas_limit,
        {
            'from': account
        }
    )


def main():
    deploy_lottery()
