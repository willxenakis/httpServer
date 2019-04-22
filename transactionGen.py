import sys, os
import json
import SimpleCoinComplete as blockchain
import rsa as RSA

testDir = '.'

# Initialize the System Wallet and main BlockChain
system_public = RSA.load('Apublic.key')
system_private = RSA.load('Aprivate.key')

systemWallet = blockchain.Wallet('Creator', system_public, system_private)
testChain = blockchain.blockChain(systemWallet)


test_public = RSA.load(os.path.join(testDir,'Bpublic.key'))
test_private = RSA.load(os.path.join(testDir,'Bprivate.key'))
testWallet = blockchain.Wallet('Tester', test_public, test_private)

testTransaction = blockchain.Transaction(testWallet, 10, systemWallet)
testTransaction2 = blockchain.Transaction(testWallet, 30, systemWallet)
testTransactionArray = [
    testTransaction,
    testTransaction2
]

output = {
    "transactions" : testTransactionArray
}

print( json.dumps(output, indent=2, cls=blockchain.ChainEncoder) )