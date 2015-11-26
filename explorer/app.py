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


def blocksinfo():
    ''' blocks info '''

    h = bitcoinLayer.getblockhash(1)
    block = bitcoinLayer.getblock(h)
    numTx = len(block.vtx)
    blocks = []
    for i in range(1,1440,144):
        blocks.append('%i %s %s %s\n'%(i,dateString(block.nTime),block.difficulty, numTx))
    return blocks


@app.route('/')
def getblockinfo():
    blocks = blocksinfo()
    #print blocks
    return render_template('blocks.html', blocks=blocks)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
    #blocks = blocksinfo(1)
    #print blocks
