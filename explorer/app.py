"""
minimal python flask app
"""

from flask import Flask
app = Flask(__name__)

import bitcoin.rpc
import datetime
import binascii

bitcoinLayer = bitcoin.rpc.Proxy()


def dateString(utime):
    dateFormat = '%Y-%m-%d'
    return datetime.datetime.fromtimestamp(int(utime)).strftime(dateFormat)

def blocksinfo(i):
    """ blocks info """
    i = 1
    h = bitcoinLayer.getblockhash(1)
    block = bitcoinLayer.getblock(h)
    numTx = len(block.vtx)
    s = ""
    for i in range(1,100,1):
        print (block)
        s += ('%i %s %s %s'%(i,dateString(block.nTime),block.difficulty, numTx))
    return s
    #return 'test'

@app.route('/')
def hello_world():
    info = blocksinfo(1)
    return info

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
