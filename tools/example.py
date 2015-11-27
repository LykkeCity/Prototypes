from bitcoin import *

priv = sha256('lykke')
print priv

pub = privtopub(priv)
print pub

addr = pubtoaddr(pub)
print addr

h = history(addr)
print h
