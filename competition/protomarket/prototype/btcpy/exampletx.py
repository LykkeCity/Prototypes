
import json
#import urllib.request
import urllib2


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

issuancetx = "b25ba9cb3a02e24dc53f6672a25fdc047d243cc442dda5e25d5d1590d9a66969"
transfertx = "e84107b793ff95efb9dc5a7e3a6500d47ff742f2af86aea69e92ad21d952baa1"

def gettx():
    burl = "https://blockchain.info/tx-index/%s?format=json"
    turl = burl%issuancetx
    resp = make_request(turl)
    print resp
    with open('example_tx.json','w') as f:
        f.write(resp)
    #data = json.loads(datastr)['data']
    #return data['unspent']


gettx()

#response = urllib2.urlopen(turl%issuancetx)
#print response.content
