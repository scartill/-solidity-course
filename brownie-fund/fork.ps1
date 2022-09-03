$alch = "https://eth-mainnet.g.alchemy.com/v2/${Env:ALCHEMY_TOKEN}"
$addr = "http://127.0.0.1"
$cmd = "networks add development mainnet-fork-dev"
$params = "accounts=10 mnemonic=brownie port=8545"
$expr = "brownie ${cmd} cmd=ganache-cli host=${addr} fork=${alch} ${params}"
Invoke-Expression $expr
