
from pybitcointools.main import *
from bitcoinhw import keyUtils

#priv = sha256('yoyo')
private_key = ''.join(['%x' % random.randrange(16) for x in range(0, 64)])
print keyUtils.privateKeyToWif(private_key)

print priv

#5KEGrxgPB4zv5E6xsyzkxh1BxKCzqQpq8WoysCLMhuR2zmC2stn
#bitcoin-cli importprivkey "5KEGrxgPB4zv5E6xsyzkxh1BxKCzqQpq8WoysCLMhuR2zmC2stn" "my-new-key"

#priv '57c617d9b4e1f7af6ec97ca2ff57e94a28279a7eedd4d12a99fa11170e94f5a4'

"""
    > pub = privtopub(priv)
    > pub
    '0420f34c2786b4bae593e22596631b025f3ff46e200fc1d4b52ef49bbdc2ed00b26c584b7e32523fb01be2294a1f8a5eb0cf71a203cc034ced46ea92a8df16c6e9'
    > addr = pubtoaddr(pub)
    > addr
    '1CQLd3bhw4EzaURHbKCwM5YZbUQfA4ReY6'
    > h = history(addr)
    > h
    [{'output': u'97f7c7d8ac85e40c255f8a763b6cd9a68f3a94d2e93e8bfa08f977b92e55465e:0', 'value': 50000, 'address': u'1CQLd3bhw4EzaURHbKCwM5YZbUQfA4ReY6'}, {'output': u'4cc806bb04f730c445c60b3e0f4f44b54769a1c196ca37d8d4002135e4abd171:1', 'value': 50000, 'address': u'1CQLd3bhw4EzaURHbKCwM5YZbUQfA4ReY6'}]
    > outs = [{'value': 90000, 'address': '16iw1MQ1sy1DtRPYw3ao1bCamoyBJtRB4t'}]
    > tx = mktx(h,outs)
    > tx
    '01000000025e46552eb977f908fa8b3ee9d2943a8fa6d96c3b768a5f250ce485acd8c7f7970000000000ffffffff71d1abe4352100d4d837ca96c1a16947b5444f0f3e0bc645c430f704bb06c84c0100000000ffffffff01905f0100000000001976a9143ec6c3ed8dfc3ceabcc1cbdb0c5aef4e2d02873c88ac00000000'
    > tx2 = sign(tx,0,priv)
    > tx2
    '01000000025e46552eb977f908fa8b3ee9d2943a8fa6d96c3b768a5f250ce485acd8c7f797000000008b483045022100dd29d89a28451febb990fb1dafa21245b105140083ced315ebcdea187572b3990220713f2e554f384d29d7abfedf39f0eb92afba0ef46f374e49d43a728a0ff6046e01410420f34c2786b4bae593e22596631b025f3ff46e200fc1d4b52ef49bbdc2ed00b26c584b7e32523fb01be2294a1f8a5eb0cf71a203cc034ced46ea92a8df16c6e9ffffffff71d1abe4352100d4d837ca96c1a16947b5444f0f3e0bc645c430f704bb06c84c0100000000ffffffff01905f0100000000001976a9143ec6c3ed8dfc3ceabcc1cbdb0c5aef4e2d02873c88ac00000000'
    > tx3 = sign(tx2,1,priv)
    > tx3
    '01000000025e46552eb977f908fa8b3ee9d2943a8fa6d96c3b768a5f250ce485acd8c7f797000000008b483045022100dd29d89a28451febb990fb1dafa21245b105140083ced315ebcdea187572b3990220713f2e554f384d29d7abfedf39f0eb92afba0ef46f374e49d43a728a0ff6046e01410420f34c2786b4bae593e22596631b025f3ff46e200fc1d4b52ef49bbdc2ed00b26c584b7e32523fb01be2294a1f8a5eb0cf71a203cc034ced46ea92a8df16c6e9ffffffff71d1abe4352100d4d837ca96c1a16947b5444f0f3e0bc645c430f704bb06c84c010000008c4930460221008bbaaaf172adfefc3a1315dc7312c88645832ff76d52e0029d127e65bbeeabe1022100fdeb89658d503cf2737cedb4049e5070f689c50a9b6c85997d49e0787938f93901410420f34c2786b4bae593e22596631b025f3ff46e200fc1d4b52ef49bbdc2ed00b26c584b7e32523fb01be2294a1f8a5eb0cf71a203cc034ced46ea92a8df16c6e9ffffffff01905f0100000000001976a9143ec6c3ed8dfc3ceabcc1cbdb0c5aef4e2d02873c88ac00000000'
    > pushtx(tx3)
    'Transaction Submitted'
"""
