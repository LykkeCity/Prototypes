#!/usr/bin/env python3

import sys

import hashlib

from pybitcoin import *
from pybitcoin.bci import bci_unspent
from bitcoin import base58

def brainwallet(w):
    priv = sha256(w)
    with open('testwallet' + w + '.txt','w') as f:
        f.write('private key : %s\n'%priv)
        pub = privtopub(priv)
        addr = pubtoaddr(pub)
        f.write('public key : %s\n'%pub)
        f.write('address : %s\n'%addr)

if __name__=='__main__':
    brainwallet("Lykkex1")
    brainwallet("Lykkex2")
