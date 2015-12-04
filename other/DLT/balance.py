"""
"""

import bitcoin.rpc
import datetime
import binascii
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160, b2lx

def printInfo():
    bitcoinLayer = bitcoin.rpc.Proxy()
    print bitcoinLayer.getbalance()

if __name__=='__main__':
    printInfo()
