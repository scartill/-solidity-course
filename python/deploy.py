from pathlib import Path
import json
import os
import solcx
from web3 import Web3


rinkeby_id = 4
endpoint = 'http://127.0.0.1:8545'
rinkeby_ep = 'https://rinkeby.infura.io/v3/7f5926724637445c979d794d614ccd13'
w3 = Web3(Web3.HTTPProvider(rinkeby_ep))
chain_id = rinkeby_id
my_address = '0x17086Cc0E94e21ECc21F897b1473C32fA1C40F0a'
private_key = os.getenv('ETH_PRIVATE')


def make_txn(txn_ctor, nonce):
    txn = txn_ctor.build_transaction({
        'chainId': chain_id,
        'from': my_address,
        'nonce': nonce,
        'gasPrice': w3.eth.gas_price
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print('Transaction completed', tx_hash.hex()[:8])
    print(f'Status {tx_receipt["status"]}, gas used {tx_receipt["gasUsed"]}')
    return (tx_receipt, nonce + 1)


print('Using private key', private_key[:4])
sol = Path('../sol/SimpleStorage.sol').read_text()

compiled = solcx.compile_standard(
    {
        'language': 'Solidity',
        'sources': {
            'SimpleStorage.sol': {
                'content': sol
            }
        },
        'settings': {
            'outputSelection': {
                '*': {
                    '*': [
                        'abi',
                        'metadata',
                        'evm.bytecode',
                        'evm.bytecode.sourceMap'
                    ]
                }
            }
        }
    },
    solc_version='0.8.14'
)

Path('../sol/SimpleStorage.Compiled.json').write_text(
    json.dumps(compiled, indent=4)
)

contract = compiled['contracts']['SimpleStorage.sol']['SimpleStorage']
bytecode = contract['evm']['bytecode']['object']
abi = contract['abi']
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(my_address)
(tx_receipt, nonce) = make_txn(SimpleStorage.constructor(), nonce)
simple_storage = w3.eth.contract(abi=abi, address=tx_receipt.contractAddress)
print('First fetch', simple_storage.functions.fetch().call())
(_, nonce) = make_txn(simple_storage.functions.store(42), nonce)
print('Second fetch', simple_storage.functions.fetch().call())
