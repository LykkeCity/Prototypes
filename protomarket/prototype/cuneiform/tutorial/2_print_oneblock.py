"""
tutorial
step 2
print info about one block
https://en.bitcoin.it/wiki/Block

=========
a block
=========
Magic no 	value always 0xD9B4BEF9 	4 bytes
Blocksize 	number of bytes following up to end of block 	4 bytes
Blockheader 	consists of 6 items 	80 bytes
Transaction counter 	positive integer VI = VarInt 	1 - 9 bytes
transactions 	the (non empty) list of transactions 	<Transaction counter>-many transactions

functions of a block
['GetHash', '__class__', '__delattr__', '__doc__', '__eq__', '__format__', '__getattribute__',
'__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
'__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__',
'_cached_GetHash', '_cached__hash__', 'build_merkle_tree_from_txids',
'build_merkle_tree_from_txs', 'calc_difficulty', 'calc_merkle_root',
'deserialize', 'difficulty', 'get_header', 'hashMerkleRoot', 'hashPrevBlock',
'nBits', 'nNonce', 'nTime', 'nVersion', 'serialize', 'stream_deserialize', 'stream_serialize', 'vMerkleTree', 'vtx']
"""

import bitcoin.rpc
import datetime
import binascii
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160, b2lx

def printInfo(blockheight):
    #see https://blockchain.info/block-height/381410
    bitcoinLayer = bitcoin.rpc.Proxy()
    h = bitcoinLayer.getblockhash(blockheight)
    block = bitcoinLayer.getblock(h)

    print (block.nTime)
    print (block.get_header())
    print (b2lx(block.hashMerkleRoot))
    print (b2lx(block.hashPrevBlock))
    print (len(block.vMerkleTree))
    print (len(block.vtx))


if __name__=='__main__':
    blockheight = 381410
    printInfo(blockheight)
