from flask import Flask
from flask import render_template
from flask import request
from SimpleCoinComplete import blockChain
from SimpleCoinComplete import Transaction
from SimpleCoinComplete import Wallet
import json
app = Flask(__name__)

creatorKey = open("Apublic.key" , "r").read()
creatorPrivKey = open("Aprivate.key" , "r").read()

creator = Wallet("Creator A", creatorKey, creatorPrivKey)
simpleCoin = blockChain(creator)

# All unspecified paths will return an error page
@app.route('/<path:path>')
def catchPath(path):
    return render_template('error.html'), 404

# This path shows the post with the given id, the id is an integer
# If the id is not an integer or a block is not found, an error page is returned
@app.route('/transactions/<id>')
def transaction(id):
    try:
        blockId = int(id)
        temp = simpleCoin.getHead()
        while temp!=None:
            if(temp.index == blockId):
                return render_template('singleBlock.html', blockId = blockId, block=temp,)
            else:
                temp = temp.nextBlock
    except:
        return render_template('error.html'), 404

    return render_template('error.html'), 404

# This path acts as both a path for Posting new transactions or getting all blocks and transactions starting at a given id
# For each transaction, verify the transaction and check no overspending then add the transaction to a verifiedTransactions list then mine the block
# For get, if start is not given return all blocks
@app.route('/transactions', methods=['GET', 'POST'])
def template():
    if request.method == 'POST':
        data = json.loads(request.get_data().decode('UTF-8'))
        transactionsArray = []

        for i in range(len(data['transactions'])):
            senderWallet = Wallet("DNE", data['transactions'][i]["senderPub"], "")
            receiverWallet = Wallet("IDK", data['transactions'][i]["receiverPub"], "")
            timeStamp = data['transactions'][i]["timeStamp"]
            operation = data['transactions'][i]["op"]
            _hash = data['transactions'][i]["hash"]

            newTransaction = Transaction(receiverWallet, operation, senderWallet, timeStamp, _hash)
            transactionsArray.append(newTransaction)

        verifiedTransactions = []

        for indexY, y in enumerate(transactionsArray):
            if simpleCoin.verifyTransaction(y) and simpleCoin.noOverspending(y.senderPub, verifiedTransactions, y):
                verifiedTransactions.append(y)
        if len(verifiedTransactions) !=0:
            simpleCoin.mineBlock(verifiedTransactions)
            latestBlock = simpleCoin.getLatestBlock()
            return ("Block Mined with " + str(len(verifiedTransactions)) + " transactions\nStatus Okay \n")
        return "Block Unable to be Mined"
    else:
        start = request.args.get('start')
        try:
            if(start != None):
                start = int(start)

                if(start<0):
                    return render_template('error.html'), 404

                temp = simpleCoin.getHead()
                blocks = []
                while temp!=None:
                    if(temp.index >= start):
                        blocks.append(temp)
                    temp = temp.nextBlock  
                if(len(blocks)==0):
                    return render_template('error.html'), 404
                return render_template('startBlock.html', start = start, blocks=blocks,)
            else:
                temp = simpleCoin.getHead()
                blocks = []
                while temp!=None:
                    blocks.append(temp)
                    temp = temp.nextBlock
                return render_template('startBlock.html', start = 0, blocks=blocks,)
        except:
            return render_template('error.html'), 404

app.run(port=8001)