"""
tutorial
step 3
print transactions and their inputs/outputs
https://en.bitcoin.it/wiki/Transaction
"""


import bitcoin.rpc
import datetime
import binascii
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160, b2lx

def printTx():
    i = 381410 # the block height we lock at
    #see https://blockchain.info/block-height/381410
    bitcoinLayer = bitcoin.rpc.Proxy()
    h = bitcoinLayer.getblockhash(i)
    block = bitcoinLayer.getblock(h)
    """
    a block has a vector of transactions (vtx)
    """
    for tx in block.vtx[:2]:
        """
        #see for the coinbase transaction : https://blockchain.info/tx/81500026f314952d74742b1fa738ae4e626adb9a2a0e3a2ea65bf0b4177db378
        #and for a normal transaction https://blockchain.info/tx/45a6e8883f5e7e1bdf27c74f18254ed4b915ddeb66d49eb8d38719cf0f24b3ca
        """

        txid = b2lx(tx.GetHash())
        print txid
        print '+'*30
        #https://en.bitcoin.it/wiki/Transaction
        for vi in tx.vin[:1]:
            print vi
            print '*'*20

            """
            input of the coinbase transaction:
            CTxIn(COutPoint(), CScript([x('e2d105'), x('55ce3456'), x('200000100006004e'), x('2f426974467572792f4249503130302f')]), 0x0)
            ********************
            regular transaction:
            CTxIn(COutPoint(lx('546cd8441af8cbd62e7ba09312a30e277670c3ca2e4641f76c18130519c097a9'), 1),
                CScript([x('3045022100ba3001eafceb074374c194c115f8c0a5240f0dfed3fdb8558634b992e011f31e0220629b9fd5c64eb5c2168d34835a3d1d200517c9ec6bd119ffbb7c47c25a09888e01'),
                x('02060dad3186ee8e64581f6866b7cc43656e992ba4f496486d35dba249cd4e3281')]), 0xfffffffe)
            """


        for vo in tx.vout[:1]:
            print vo
            
            """
            output of the coinbase transaction:
            CTxOut(25.02480707*COIN, CScript([OP_DUP, OP_HASH160, x('63afd7ba46472834b3a91a31ecf16c8bcb196161'), OP_EQUALVERIFY, OP_CHECKSIG]))
            ********************
            output regular transaction:
            CTxOut(0.01009586*COIN, CScript([OP_DUP, OP_HASH160, x('e042c579bc54e489e60ee76389ec12014adca021'), OP_EQUALVERIFY, OP_CHECKSIG]))
            CTxOut(100.0*COIN, CScript([OP_DUP, OP_HASH160, x('8119fadbc18cbdf9b83fb74953a329aaf72bfdbe'), OP_EQUALVERIFY, OP_CHECKSIG]))
            """
            #for y in vo.scriptPubKey.raw_iter():
            #    print y

if __name__=='__main__':
    printTx()
