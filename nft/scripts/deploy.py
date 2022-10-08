from brownie import SimpleCollectible
import scripts.helpers as h


TOKEN_URI = 'https://s3.eu-north-1.amazonaws.com/public.adsight/admedia/Pug.json'
OPENSEA_URL = 'https://testnets.opensea.io/assets/{}/{}'


def deploy():
    sc = SimpleCollectible.deploy(h.my())
    tx = sc.createCollectible(TOKEN_URI, h.my())
    tx.wait(1)
    tokenId = sc.getLastTokenID()
    print('Open here', OPENSEA_URL.format(sc.address, tokenId))
    return (sc, tokenId)


def main():
    deploy()
