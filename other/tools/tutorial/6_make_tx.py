#!/usr/bin/env python3

"""Low-level example of how to spend a standard pay-to-pubkey-hash (P2PKH) txout"""

import sys
if sys.version_info.major < 3:
    sys.stderr.write('Sorry, Python 3.x required by this example.\n')
    sys.exit(1)

import hashlib

from cuneiform.bitcoin import SelectParams
from cuneiform.bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from cuneiform.bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from cuneiform.bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from cuneiform.bitcoin.wallet import CBitcoinAddress, CBitcoinSecret

from cuneiform.pybitcoin import *
from cuneiform.pybitcoin.bci import bci_unspent
SelectParams('mainnet')

# Create a brainwallet secret key.

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


def maketx(secret):
    addr = get_addr(secret)
    print (addr)
    hist = history(addr)[-1]
    print (hist)
    h = hashlib.sha256(secret.encode('UTF-8')).digest()
    seckey = CBitcoinSecret.from_secret_bytes(h)
    print (seckey)
    unspent = bci_unspent(addr)
    print (bci_unspent)
    return

    # Same as the txid:vout the createrawtransaction RPC call requires
    #
    # lx() takes *little-endian* hex and converts it to bytes; in Bitcoin
    # transaction hashes are shown little-endian rather than the usual big-endian.
    # There's also a corresponding x() convenience function that takes big-endian
    # hex and converts it to bytes.
    txid = lx('7e195aa3de827814f172c362fcf838d92ba10e3f9fdd9c3ecaf79522b311b22d')
    vout = 0

    # Create the txin structure, which includes the outpoint. The scriptSig
    # defaults to being empty.
    txin = CMutableTxIn(COutPoint(txid, vout))

    print (txin)

    # We also need the scriptPubKey of the output we're spending because
    # SignatureHash() replaces the transaction scriptSig's with it.
    #
    # Here we'll create that scriptPubKey from scratch using the pubkey that
    # corresponds to the secret key we generated above.
    txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(seckey.pub), OP_EQUALVERIFY, OP_CHECKSIG])

    # Create the txout. This time we create the scriptPubKey from a Bitcoin
    # address.
    amount = 0.0001
    txout = CMutableTxOut(amount*COIN, CBitcoinAddress('1C7zdTfnkzmr13HfA2vNm5SJYRK6nEKyq8').to_scriptPubKey())

    # Create the unsigned transaction.
    tx = CMutableTransaction([txin], [txout])

    # Calculate the signature hash for that transaction.
    sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)

    # Now sign it. We have to append the type of signature we want to the end, in
    # this case the usual SIGHASH_ALL.
    sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])

    # Set the scriptSig of our transaction input appropriately.
    txin.scriptSig = CScript([sig, seckey.pub])

    # Verify the signature worked. This calls EvalScript() and actually executes
    # the opcodes in the scripts to see if everything worked out. If it doesn't an
    # exception will be raised.
    #VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))

    # Done! Print the transaction to standard output with the bytes-to-hex
    # function.
    print(b2x(tx.serialize()))

if __name__=='__main__':
    secret = get_secret()
    maketx(secret)
