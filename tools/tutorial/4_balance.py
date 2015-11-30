
import cuneiform.bitcoin.rpc

bitcoinLayer = cuneiform.bitcoin.rpc.Proxy()
bal = int(bitcoinLayer.getinfo()['balance'])
print ("your balance: %i"%bal)
