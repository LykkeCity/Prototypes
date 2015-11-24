"""
example show script of transactions

(118, None, 0) #OP_DUP
(169, None, 1) #OP_HASH160
(20, 'c\xaf\xd7\xbaFG(4\xb3\xa9\x1a1\xec\xf1l\x8b\xcb\x19aa', 2) #20 bytes of data
(136, None, 23) #OP_EQUALVERIFY
(172, None, 24) #OP_CHECKSIG
"""

import bitcoin.rpc
import datetime
import binascii
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160, b2lx
import datetime

def printblock(blocknum):
    proxy = bitcoin.rpc.Proxy()

    h = proxy.getblockhash(blocknum)
    block = proxy.getblock(h)
    print 'number of transactions : ',len(block.vtx)
    for tx in block.vtx[:5]:
        txid = b2lx(tx.GetHash())
        print '*'*30
        print txid
        print '*'*30
        for vo in tx.vout[:]:
            for y in vo.scriptPubKey.raw_iter():
                print y


if __name__=='__main__':
    block = 376682
    printblock(block)
