"""
tutorial
step 1
print some blockchain information
"""

import bitcoin.rpc
import datetime
import binascii

def dateString(utime):
    dateFormat = '%Y-%m-%d'
    return datetime.datetime.fromtimestamp(int(utime)).strftime(dateFormat)

def printBlocks():
    """ print some blocks """
    bitcoinLayer = bitcoin.rpc.Proxy()
    n = 100
    start = 1
    skip = 40000
    end = start + skip*10
    print('*** Bitcoin blocks ***')
    print('blocknum date difficulty number of tx')
    for i in range(start, end,skip):
        h = bitcoinLayer.getblockhash(i)
        block = bitcoinLayer.getblock(h)
        numTx = len(block.vtx)
        print('%i %s %s %s'%(i,dateString(block.nTime),block.difficulty, numTx))

        """
        #output
        *** Bitcoin blocks ***
        blocknum date difficulty number of tx
        1 2009-01-09 1.0 1
        40001 2010-02-13 1.81864853615 1
        80001 2010-09-16 712.884864552 3
        120001 2011-04-25 92347.5909521 12
        160001 2011-12-31 1159929.49722 20
        200001 2012-09-22 2864140.50781 32
        240001 2013-06-06 15605632.6813 211
        280001 2014-01-12 1418481395.26 53
        320001 2014-09-10 27428630902.3 166
        360001 2015-06-08 47589591153.6 542
        """

if __name__=='__main__':
    printBlocks()
