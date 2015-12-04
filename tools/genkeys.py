#!/usr/bin/env python3

import sys

import hashlib

from bitcoin import SelectParams

from pybitcoin import *
from pybitcoin.bci import bci_unspent
SelectParams('mainnet')

# Create a brainwallet from secret key.

def brainwallet():
    priv = sha256("secret")
    pub = privtopub(priv)
    addr = pubtoaddr(pub)
    print pub,priv,addr

if __name__=='__main__':
    brainwallet()
