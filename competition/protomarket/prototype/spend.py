#!/usr/bin/env python3
"""work in progress
moving coloredcoins on low level
"""

import sys
from blockr import *
from pybtc.main import *

import hashlib

from bitcoin import SelectParams
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret

SelectParams('mainnet')

# Create the (in)famous correct brainwallet secret key.

secret_file = "secret.key"

def get_secret():
    try:
        with open(secret_file,'r') as f:
            secret = f.read().strip()
            return secret
    except:
        return None

secret = get_secret()
h = hashlib.sha256(secret.encode('UTF-8')).digest()
seckey = CBitcoinSecret.from_secret_bytes(h)
print ("=> %s"%Hash160(seckey.pub))
priv = sha256(secret)
pub = privtopub(priv)
addr = pubtoaddr(pub)
print ("addr: %s"%addr)

a = "15oq1ENPGCiFEaRKBTwthyoSzBqDCKNNRr"

"""
{u'script': u'76a91434bbb5861132c2ca4334aeae51898a42a32020fc88ac', u'amount': u'0.00010000', u'confirmations': 471, u'tx': u'25cdf13e8a14001042e9c158d0788ada3f90354c5dbb5f44be474023a5aa7c8c', u'n': 1}
{u'script': u'76a91434bbb5861132c2ca4334aeae51898a42a32020fc88ac', u'amount': u'0.00010000', u'confirmations': 772, u'tx': u'36d4c55aa85aafe57be0f2706f68aafac082571a1ebccb3891e85c58178bc377', u'n': 0}
"""


def maketx(tx):
    #txid from blockr. bitcoind does not support tx index!
    txid = lx(tx)
    vout = 0

    outp = COutPoint(txid, vout)
    print ("output: %s"%outp)
    # Create the txin structure, which includes the outpoint
    txin = CMutableTxIn(outp)
    print (txin)

    txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(seckey.pub), OP_EQUALVERIFY, OP_CHECKSIG])

    print (txin_scriptPubKey)

    amount = 0.001*COIN
    txout = CMutableTxOut(amount, CBitcoinAddress(a).to_scriptPubKey())

    print (txout)

    # Create the unsigned transaction.
    newtx = CMutableTransaction([txin], [txout])
    print (newtx)

    sighash = SignatureHash(txin_scriptPubKey, newtx, 0, SIGHASH_ALL)
    print (sighash)

    # Now sign it. We have to append the type of signature we want to the end, in
    # this case the usual SIGHASH_ALL.
    sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])
    print (sig)

    # Set the scriptSig of our transaction input appropriately.
    txin.scriptSig = CScript([sig, seckey.pub])

    try:
        VerifyScript(txin.scriptSig, txin_scriptPubKey, newtx, 0, (SCRIPT_VERIFY_P2SH,))
    except:
        pass

    print ('*'*20)
    print(b2x(newtx.serialize()))

    """
    transaction hardcoded:
    01000000018c7caaa5234047be445fbb5d4c35903fda8a78d058c1e9421000148a3ef1cd2500000000
    6b48304502210083ec30fa92994e886efe9b0c36bf41470f7629d5a2f085bdefd46e26f15fd13f0220
    294c815a8490c91bdedbfb656c44e19b8d3b5fd20d71fa762ceb97419e426b0f01210233ed500a05f9
    6b37146aa3da31d997b4cf35073ba3ff9dfb5e3437d4982a5572ffffffff01a0860100000000001976
    a91434bbb5861132c2ca4334aeae51898a42a32020fc88ac00000000
    """


unspent = get_unspent(a)
for u in unspent:
    tx = u['tx']
    print ("tx: %s"%tx)

first = unspent[1]['tx']
print (first)
maketx(first)
