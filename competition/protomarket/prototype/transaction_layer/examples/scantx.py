#!/usr/bin/env python3
""" utiliies to scan blockchain for openasset tx
see https://github.com/OpenAssets/open-assets-protocol"""

import bitcoin.rpc
import datetime
import binascii

from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160, b2lx

import datetime
OP_RETURN = 106

def datestr(utime):
    dateFormat = '%Y-%m-%d'
    return datetime.datetime.fromtimestamp(int(utime)).strftime(dateFormat)

def bh(x):
    return binascii.hexlify(x)

def datestr(utime):
    dateFormat = '%Y-%m-%d'
    return datetime.datetime.fromtimestamp(int(utime)).strftime(dateFormat)

def printtx(txid):
    """ print all outputs of a transaction """
    proxy = bitcoin.rpc.Proxy()

    txid = lx(txid)
    vout = 0

    txin = CMutableTxIn(COutPoint(txid, vout))
    txes = proxy.getrawtransaction(txid)
    #print txes.vout

    print '*'*20
    print 'outputs of the transaction\n(op_code, data, sop_idx)'
    print '*'*20
    for vo in txes.vout[:]:
        for x in vo.scriptPubKey.raw_iter():
            print x


def printallTx(tx):
    for vo in tx.vout[:]:
        for y in vo.scriptPubKey.raw_iter():
            print y

def printTxOPR(tx):
    for vo in tx.vout[:]:
        for y in vo.scriptPubKey.raw_iter():
            op, data, _ = y
            print y
            #if op == 18:
            #    print y

def hasOPR(tx):
    """ check whether tx has op_return """
    for vo in tx.vout[:]:
        got_OPRETURN = False
        for y in vo.scriptPubKey.raw_iter():
            op = y[0]
            if op==OP_RETURN:
                got_OPRETURN = True
                return True


def printblock(blocknum,f=None):
    proxy = bitcoin.rpc.Proxy()

    h = proxy.getblockhash(blocknum)
    block = proxy.getblock(h)
    print '#tx : ',len(block.vtx)
    for tx in block.vtx[:]:
        #printallTx(tx)
        txid = b2lx(tx.GetHash())
        #cond = txid[:2] == 'b2'
        if True:
            print '*'*30
            print txid
            print '*'*30
            printallTx(tx)
        #if hasOPR(tx):
        #    print txid
        #    printallTx(tx)

            #printallTx(tx)

def printblockOPR(proxy, blocknum,f=None):


    h = proxy.getblockhash(blocknum)
    block = proxy.getblock(h)
    print '#tx : ',len(block.vtx)
    for tx in block.vtx[:]:
        #printallTx(tx)
        txid = b2lx(tx.GetHash())
        #cond = txid[:2] == 'b2'
        if True:
            #print txid
            for vo in tx.vout[:]:
                i = tx.vout.index(vo)
                for y in vo.scriptPubKey.raw_iter():
                    op = y[0]
                    if op==OP_RETURN:
                        print txid
                        #print tx
                        if i+1 < len(tx.vout):
                            print tx.vout[i+1]


def scanblock(proxy, blocknum,f=None):
    """ scan all tx in a block for op_return """

    h = proxy.getblockhash(blocknum)

    block = proxy.getblock(h)

    num_opr = 0
    #print '#tx : ',len(block.vtx)
    for tx in block.vtx[:]:
        txid = b2lx(tx.GetHash())
        #print txid
        if hasOPR(tx):

            #printTxOPR(tx)
            num_opr +=1

    if num_opr > 0:
        s = '%i  %s  total tx: %i  num opr %i'%(blocknum, datestr(block.nTime), len(block.vtx),num_opr)
        print s
        if f: f.write(s + '\n')
    else:
        #print blocknum
        pass
    #print 'total opr',num_opr

def scanall():
    """ scan blockain for op_return """
    start = 250000 #376682 #265459
    end = 381240
    proxy = bitcoin.rpc.Proxy()
    f = open('opr_count.csv','w')
    for bl in range(start,end):
        try:
            scanblock(proxy, bl,f)
        except:
            print 'failure scanning block'
    f.close()

if __name__=='__main__':
    block = 376682 #380550
    #printblockOPR(block)
    scanall()
