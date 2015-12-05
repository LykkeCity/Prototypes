// Copyright (c) 2015
// Developed as part of Lykkex.com
// Author: Shahpour Moavenat

using NBitcoin;
using NBitcoin.OpenAsset;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Linq;

namespace NBitcoinCC
{
    class Program
    {
        static Coin CreateTransactionFeeCoin(PubKey destination, NoSqlTransactionRepository txRepo)
        {
            var bitcoinProviderTransaction = new Transaction()
            {
                Outputs =
                {
                    new TxOut("0.0001" , destination)
                }
            };
            txRepo.Put(bitcoinProviderTransaction.GetHash(), bitcoinProviderTransaction);
            return new Coin(new OutPoint(bitcoinProviderTransaction, 0),
                bitcoinProviderTransaction.Outputs[0]);
        }

        private static JObject CreateExchangeMatch(JObject firstRequestJson, string firstRequestSignature,
            JObject secondRequestJson, string secondRequestSignature, Key exchangeKey)
        {
            dynamic exchangeMatch = new JObject();
            exchangeMatch.Match = new JObject();
            exchangeMatch.Match.FirstRequest = firstRequestJson;
            exchangeMatch.Match.FirstRequestSignature = firstRequestSignature;
            exchangeMatch.Match.SecondRequest = secondRequestJson;
            exchangeMatch.Match.SecondRequestSignature = secondRequestSignature;
            exchangeMatch.MatchSignature = exchangeKey.SignMessage(exchangeMatch.Match.ToString(Formatting.None));

            return exchangeMatch;
        }

        private static JObject CreateExchangeRequest(string orderType, string sourceAssetId,
            string destinationAssetId, int sourceAssetAmount, float rate)
        {
            dynamic clientRequestObject = new JObject();
            clientRequestObject.Type = orderType;
            clientRequestObject.Payload = new JObject();
            clientRequestObject.Payload.SourceAsset = sourceAssetId;
            clientRequestObject.Payload.SourceAmount = sourceAssetAmount;
            clientRequestObject.Payload.DestinationAsset = destinationAssetId;
            clientRequestObject.Payload.Rate = rate;

            return clientRequestObject;
        }

        static void Main(string[] args)
        {
            var goldGuy = new BitcoinSecret("KyuzoVnpsqW529yzozkzP629wUDBsPmm4QEkh9iKnvw3Dy5JJiNg");
            var silverGuy = new BitcoinSecret("L4KvjpqDtdGEn7Lw6HdDQjbg74MwWRrFZMQTgJozeHAKJw5rQ2Kn");

            var firstPerson = new BitcoinSecret("5Jnw9Td7PaG6PWBrU7ZCfxyVXsHSsNxdZ9sg5dnZstcr12DLVbJ");
            var secondPerson = new BitcoinSecret("5Jn4zJkzS2BWNu7AMRTdSJ6mS7JYfJg27oXKAichaRBbp97ZKks");
            var exchangeEntity = new BitcoinSecret("5KA7FeABKmMKerWmkJzYM9FdoqScZEMVcS9u6wvT3EhgF5ZUWv5");

            var bitcoinProviderEntity = new BitcoinSecret("5Jcz2A17aAt4bcQP5GEn6itt72JsLwrksNRVKqazy7n284b1bKj");
            
            var issuanceCoinsTransaction = new Transaction()
            {
                Outputs =
                {
                    new TxOut("1.0", goldGuy.PubKey),
                    new TxOut("1.0", silverGuy.PubKey),
                    new TxOut("1.0", firstPerson.PubKey),
                    new TxOut("1.0", secondPerson.PubKey),
                }
            };

            IssuanceCoin[] issuanceCoins = issuanceCoinsTransaction
                        .Outputs
                        .Take(2)
                        .Select((o, i) => new Coin(new OutPoint(issuanceCoinsTransaction.GetHash(), i), o))
                        .Select(c => new IssuanceCoin(c))
                        .ToArray();

            var goldIssuanceCoin = issuanceCoins[0];
            var silverIssuanceCoin = issuanceCoins[1];
            var firstPersonInitialCoin = new Coin(new OutPoint(issuanceCoinsTransaction, 2), issuanceCoinsTransaction.Outputs[2]);
            var secondPersonInitialCoin = new Coin(new OutPoint(issuanceCoinsTransaction, 3), issuanceCoinsTransaction.Outputs[3]);

            var goldId = goldIssuanceCoin.AssetId;
            var silverId = silverIssuanceCoin.AssetId;

            var txRepo = new NoSqlTransactionRepository();
            txRepo.Put(issuanceCoinsTransaction.GetHash(), issuanceCoinsTransaction);

            var ctxRepo = new NoSqlColoredTransactionRepository(txRepo);

            TransactionBuilder txBuilder = new TransactionBuilder();

            // Issuing gold to first person
            // This happens in gold issuer client
            Transaction tx = txBuilder
                .AddKeys(goldGuy.PrivateKey)
                .AddCoins(goldIssuanceCoin)
                .IssueAsset(firstPerson.GetAddress(), new AssetMoney(goldId, 20))
                .SetChange(goldGuy.GetAddress())
                .BuildTransaction(true);

            txRepo.Put(tx.GetHash(), tx);
            var ctx = tx.GetColoredTransaction(ctxRepo);
            var coloredCoins = ColoredCoin.Find(tx, ctx).ToArray();
            ColoredCoin firstPersonGoldCoin = coloredCoins[0];

            // Issuing silver to second person
            // This happens in silver issuer client
            txBuilder = new TransactionBuilder();
            tx = txBuilder
                .AddKeys(silverGuy.PrivateKey)
                .AddCoins(silverIssuanceCoin)
                .IssueAsset(secondPerson.GetAddress(), new AssetMoney(silverId, 30))
                .SetChange(silverGuy.GetAddress())
                .BuildTransaction(true);

            txRepo.Put(tx.GetHash(), tx);
            ctx = tx.GetColoredTransaction(ctxRepo);
            coloredCoins = ColoredCoin.Find(tx, ctx).ToArray();
            ColoredCoin secondPersonSilverCoin = coloredCoins[0];

            // Sending first person gold to exchange
            // This happens in first user client
            var bitcoinProviderCoin = CreateTransactionFeeCoin(bitcoinProviderEntity.PubKey, txRepo);
            txBuilder = new TransactionBuilder();
            tx = txBuilder
                .AddCoins(bitcoinProviderCoin)
                .AddKeys(bitcoinProviderEntity.PrivateKey)
                .AddCoins(firstPersonGoldCoin)
                .AddKeys(firstPerson.PrivateKey)
                .SendAssetToExchange(exchangeEntity.GetAddress(), new AssetMoney(goldId, 5))
                .SetChange(firstPerson.PubKey)
                .BuildTransaction(true);
            txRepo.Put(tx.GetHash(), tx);
            ctx = tx.GetColoredTransaction(ctxRepo);
            coloredCoins = ColoredCoin.Find(tx, ctx).ToArray();
            ColoredCoin firstPersonColoredCoinInExchange = coloredCoins[1];

            // Creating the time-locked transaction which the first user can post to the
            // network to claim his/her coin from exchange (it works if the exchange does not touch the coins
            // This happens in exchange and the transaction is delivered to first user client
            bitcoinProviderCoin = CreateTransactionFeeCoin(bitcoinProviderEntity.PubKey, txRepo);
            txBuilder = new TransactionBuilder();
            tx = txBuilder
                .AddCoins(bitcoinProviderCoin)
                .AddKeys(bitcoinProviderEntity.PrivateKey)
                .AddCoins(firstPersonColoredCoinInExchange)
                .AddKeys(firstPerson.PrivateKey)
                .SendAsset(firstPerson.PubKey, new AssetMoney(firstPersonColoredCoinInExchange.Amount.Id,
                    firstPersonColoredCoinInExchange.Amount.Quantity))
                .SetChange(exchangeEntity.PubKey)
                .SetLockTime(new LockTime(1000000))
                .BuildTransaction(true);
            string reclaimTransactionForFirstUser = tx.ToHex();

            // Create first person exchange request
            // This happens in first person client
            JObject firstPersonRequestToExchange = CreateExchangeRequest("ExactMatch", goldId.ToString(),
                silverId.ToString(), 5, 2);
            var firstRequestSignature = firstPerson.PrivateKey.SignMessage(firstPersonRequestToExchange.ToString(Formatting.None));

            // Sending second person silver to exchange
            // This happens in second person client
            bitcoinProviderCoin = CreateTransactionFeeCoin(bitcoinProviderEntity.PubKey, txRepo);
            txBuilder = new TransactionBuilder();
            tx = txBuilder
                .AddCoins(bitcoinProviderCoin)
                .AddKeys(bitcoinProviderEntity.PrivateKey)
                .AddCoins(secondPersonSilverCoin)
                .AddKeys(secondPerson.PrivateKey)
                .SendAssetToExchange(exchangeEntity.GetAddress(), new AssetMoney(silverId, 12))
                .SetChange(secondPerson.PubKey)
                .BuildTransaction(true);
            txRepo.Put(tx.GetHash(), tx);
            ctx = tx.GetColoredTransaction(ctxRepo);
            coloredCoins = ColoredCoin.Find(tx, ctx).ToArray();
            ColoredCoin secondPersonColoredCoinInExchange = coloredCoins[1];

            // Create second person exchange request
            // This happens in second person client
            JObject secondPersonRequestToExchange = CreateExchangeRequest("ExactMatch", silverId.ToString(),
                goldId.ToString(), 30, 0.5f);
            var secondRequestSignature = secondPerson.PrivateKey.SignMessage(secondPersonRequestToExchange.ToString(Formatting.None));

            // Creating exchange reason
            // This happens in exchange
            var exchangeReason = CreateExchangeMatch(firstPersonRequestToExchange, firstRequestSignature,
                secondPersonRequestToExchange, secondRequestSignature, exchangeEntity.PrivateKey);

            // Performing the exchange operation
            // This happens in exchange
            bitcoinProviderCoin = CreateTransactionFeeCoin(bitcoinProviderEntity.PubKey, txRepo);
            txBuilder = new TransactionBuilder();
            tx = txBuilder
                .AddCoins(bitcoinProviderCoin)
                .AddKeys(bitcoinProviderEntity.PrivateKey)
                .AddCoins(firstPersonColoredCoinInExchange)
                .AddKeys(exchangeEntity.PrivateKey)
                .AddCoins(secondPersonColoredCoinInExchange)
                .AddKeys(exchangeEntity.PrivateKey)
                .PerformExchangeOperation(firstPerson.GetAddress(), new AssetMoney(silverId, 10),
                secondPerson.GetAddress(), new AssetMoney(goldId, 5), exchangeReason.ToString(Formatting.None))
                .SetChange(exchangeEntity.GetAddress())
                .BuildTransaction(true);
            txRepo.Put(tx.GetHash(), tx);
            ctx = tx.GetColoredTransaction(ctxRepo);
            coloredCoins = ColoredCoin.Find(tx, ctx).ToArray();

            txRepo.Put(tx.GetHash(), tx);
        }
    }
}
