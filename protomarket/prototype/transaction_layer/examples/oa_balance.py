"""
example to use OA parser to track balances

OA protocol:

0x4f 0x41 OA protocol tag
0x01 0x00 version of the protocol
0x02 items
80c8afa025e0e6a5efc0eb0200

"""

from openassets import protocol
import bitcoin
import bitcoin.rpc
from bitcoin.core import b2x, lx
#import protocol.MarkerOutput as MO

#txid = '9a0466b49bc91007767caf478d9aa8e91ce04c9d0c0aae3023ed0f9bc7e567bb'
txids = [
'b25ba9cb3a02e24dc53f6672a25fdc047d243cc442dda5e25d5d1590d9a66969',
'e84107b793ff95efb9dc5a7e3a6500d47ff742f2af86aea69e92ad21d952baa1',
'6730d1972f4b286aadfb70c134ede8373ec2e2304c292d65d47f6b3bbe381316',
'25cde5b5cd28d812d441bdf230ab025b9fdcac87acd2592828cd6e400628f854']

proxy = bitcoin.rpc.Proxy()

def showTx(txid):
    txid = lx(txid)
    txes = proxy.getrawtransaction(txid)

    for transaction in txes.vout[:1]:
        mo_payload = protocol.MarkerOutput.parse_script(transaction.scriptPubKey)
        print (b2x(mo_payload))
        marker = protocol.MarkerOutput.deserialize_payload(mo_payload)
        print (marker)

    """
    output:
    4f4101000280d6a3f81be09082f7a4eb0200
    MarkerOutput(asset_quantities=[7500000000, 12482498300000], metadata=b'')
    """

if __name__=='__main__':
    for tx in txids:
        showTx(tx)
