from bitcoin import *

priv = sha256('lykke')
print priv

pub = privtopub(priv)
print pub

addr = pubtoaddr(pub)
print addr

h = history(addr)
print h

"""
output
fb9f64c5b8f947bf32c288e38fe830dd8c04637b9657515d2ec328f3b0d49f0e
045c1a11dfc4b3698e133c5c1007e0f79f36e73bd29b5de48643af12b85210fee31a22973b5eaacca9133b5f5483a0ba04eff627d4688893a909e9c1655c1f8e61
16WTB9d9S17cohtcqKqU2R22F4a3PXao6H
[]
"""
