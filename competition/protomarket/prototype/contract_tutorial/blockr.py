"""
query http://btc.blockr.io
"""

import json, re
import random
import sys
try:
    from urllib.request import build_opener
except:
    from urllib2 import build_opener

def make_request(*args):
    opener = build_opener()

    try:
        return opener.open(*args).read().strip()
    except Exception as e:
        try:
            p = e.read().strip()
        except:
            p = e
        raise Exception(p)

def get_unspent(a):
    turl = "http://btc.blockr.io/api/v1/address/unspent/" + a
    datastr = make_request(turl)
    data = json.loads(datastr)['data']
    return data['unspent']

a = "15oq1ENPGCiFEaRKBTwthyoSzBqDCKNNRr"
unspent = get_unspent(a)
for u in unspent:
    print u

"""
{u'script': u'76a91434bbb5861132c2ca4334aeae51898a42a32020fc88ac', u'amount': u'0.00010000', u'confirmations': 471, u'tx': u'25cdf13e8a14001042e9c158d0788ada3f90354c5dbb5f44be474023a5aa7c8c', u'n': 1}
{u'script': u'76a91434bbb5861132c2ca4334aeae51898a42a32020fc88ac', u'amount': u'0.00010000', u'confirmations': 772, u'tx': u'36d4c55aa85aafe57be0f2706f68aafac082571a1ebccb3891e85c58178bc377', u'n': 0}
"""
