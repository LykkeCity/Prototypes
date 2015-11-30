"""
payments via bitcoin

put a secret phrase in secret.txt

funds the brainwallet
"""

from cuneiform.pybitcoin import *
from cuneiform.bitcoin.core import COIN, b2lx
import cuneiform.bitcoin.wallet
import cuneiform.bitcoin.rpc
from cuneiform.bitcoin.wallet import CBitcoinAddress
import os

secret_file = "secret.key"

def get_secret():
    try:
        with open(secret_file,'r') as f:
            secret = f.read().strip()
            return secret
    except:
        return None

def get_addr(secret):

    #generate pubkey from passphrase
    priv = sha256(secret)
    pub = privtopub(priv)
    addr = pubtoaddr(pub)

    #addrstr =  #'1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T'
    return addr

def fund_brainwallet(addrstr):
    amount = 0.0001
    bitcoinLayer = cuneiform.bitcoin.rpc.Proxy()

    addr = CBitcoinAddress(addrstr)

    txid = bitcoinLayer.sendtoaddress(addr, amount * COIN)
    print(b2lx(txid))
    print ('send %s  to %s'%(addrstr, amount))

def fund(addr):
    print (addr)
    h = history(addr)
    print (h)
    #[{'output': u'97f7c7d8ac85e40c255f8a763b6cd9a68f3a94d2e93e8bfa08f977b92e55465e:0', 'value': 50000, 'address': u'1CQLd3bhw4EzaURHbKCwM5YZbUQfA4ReY6'}, {'output': u'4cc806bb04f730c445c60b3e0f4f44b54769a1c196ca37d8d4002135e4abd171:1', 'value': 50000, 'address': u'1CQLd3bhw4EzaURHbKCwM5YZbUQfA4ReY6'}]
    BTCUSD = 320.0
    amountUSD = 0.1
    amount = amountUSD/BTCUSD
    amountSat = amount * COIN
    print (amountSat)
    outs = [{'value': amountSat, 'address': addr}]
    #tx = mktx(h,outs)


if __name__=='__main__':
    #fund_brainwallet()
    secret = get_secret()
    if secret != None:
        addr = get_addr(secret)
        bal = int(history(addr)[-1]['value'])
        if bal == 0:
            print ("funding %s"%addr)
        else:
            print ("brain wallet funded with %s"%bal)
        #fund_brainwallet(addr)
    else:
        print ("put a passphrase into a file to load up a temporary brainwallet (use small amounts and not for other purposes): %s"%secret_file)
