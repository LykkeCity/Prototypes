"""
minimal python flask app
"""

from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)

import bitcoin.rpc
import datetime
import binascii

bitcoinLayer = bitcoin.rpc.Proxy()

def dateString(utime):
    dateFormat = '%Y-%m-%d'
    return datetime.datetime.fromtimestamp(int(utime)).strftime(dateFormat)

def blockinfo():
    """ info about one block """

    h = bitcoinLayer.getblockhash(i)
    block = bitcoinLayer.getblock(h)
    #numTx = len(block.vtx)
    #infostr = '%i %s %s %s\n'%(i,dateString(block.nTime),block.difficulty, numTx)
    return {'date':dateString(block.nTime),'difficulty':block.difficulty,'numtx':len(block.vtx)}

def listblocksinfo():
    ''' info about list of blocks '''

    blocks = []
    maxblock = 144*365*3
    for i in range(1,maxblock,144):
        blocks.append(blockinfo(i))
    return blocks


@app.route('/')
def getblockinfo():
    """ show some information about a list of blocks """
    blocks = listblocksinfo()
    return render_template('blocks.html', blocks=blocks)

if __name__ == '__main__':
    port = 80
    app.run(host='0.0.0.0',port=80)
    #blocks = blocksinfo(1)
    #print blocks
