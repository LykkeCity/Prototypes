## Simplified market model

We develop a very simplified auction protocol so to focus on a Bitcoin <> Colored Coin swap

* we introduce a ColoredCoin for testing purposes: ProtomarketCoin (PMC)

* the market consists of two assets: Bitcoin and ProtomarketCoin, and therefore one trading pair: PMC/BTC

* clients submit requests to the server to buy or sell PMC against BTC

* the quantity of the request is fixed to 10 units

* the price has only 10 possible values: [1, ..., 10]

* if all price-slots are taken, the client receives a message to wait
